#!/usr/bin/env python3
"""Run the five acceptance criteria against a running Provenance Guard service."""

import argparse
import datetime as dt
import json
import statistics
import uuid

import requests

import config
import scenarios
import scoring

TARGETS = {
    "1. False accusations": "At most 1 of 20",
    "2. AI-human mean gap": "At least +0.20 on matched sets of 10",
    "3. Label coverage": "3 of 3 live labels and a complete, exclusive score grid",
    "4. Appeal logging": "10 of 10 valid appeals and one unknown-ID 404",
    "5. Invalid submissions": "All expected JSON errors, no detector calls or decisions",
}


class Evaluation:
    def __init__(self, url, timeout):
        self.url = url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.prefix = f"eval_{uuid.uuid4().hex[:10]}"

    def request(self, method, route, **kwargs):
        response = self.session.request(method, f"{self.url}/{route}", timeout=self.timeout, **kwargs)
        return {
            "http_status": response.status_code,
            "json": response.json() if "application/json" in response.headers.get("Content-Type", "") else None,
        }

    def submit(self, texts, name):
        return [
            self.request("POST", "submit", json={"text": text, "creator_id": f"{self.prefix}_{name}_{i}"})
            for i, text in enumerate(texts, 1)
        ]

    def log(self):
        return self.request("GET", "log")["json"]["entries"]

    def false_accusations(self, human, trial):
        responses = self.submit(human, f"{trial}_human")
        scored = [r for r in responses if r["http_status"] == 200]
        flagged = sum(r["json"]["guess"] == "ai" for r in scored)
        passed = flagged <= 1 if len(scored) == 20 else None
        return result(f"{flagged}/{len(scored)} scored", passed, responses)

    def score_gap(self, human, ai, trial):
        human_responses = self.submit(human[:10], f"{trial}_gap_human")
        ai_responses = self.submit(ai, f"{trial}_gap_ai")
        means = {}
        for name, responses in (("human", human_responses), ("ai", ai_responses)):
            scores = [r["json"]["confidence"] for r in responses if r["http_status"] == 200]
            means[name] = statistics.mean(scores) if scores else None
        complete = len(human_responses) == len(ai_responses) == 10 and all(
            r["http_status"] == 200 for r in human_responses + ai_responses
        )
        gap = means["ai"] - means["human"] if None not in means.values() else None
        observed = f"{gap:+.4f}" if gap is not None else "No mean gap"
        return result(
            observed, gap >= 0.20 if complete else None,
            {"human": human_responses, "ai": ai_responses, "means": means, "gap": gap},
        )

    def labels(self, trial):
        responses = self.submit([row["text"] for row in scenarios.CALIBRATION], f"{trial}_labels")
        labels = sorted({r["json"]["guess"] for r in responses if r["http_status"] == 200})
        human, ai = config.HUMAN_THRESHOLD, config.AI_THRESHOLD
        grid = sorted({*(i / 1000 for i in range(1001)), human, ai})
        matches = 0
        for score in grid:
            expected = [
                guess for guess, matches_band in (
                    ("human", score <= human),
                    ("unsure", human < score < ai),
                    ("ai", score >= ai),
                ) if matches_band
            ]
            guess, label = scoring.score_to_label(score)
            matches += expected == [guess] and bool(label)
        complete = all(r["http_status"] == 200 for r in responses)
        return result(
            f"{len(labels)}/3 labels, {matches}/{len(grid)} grid",
            len(labels) == 3 and matches == len(grid) if complete else None,
            {"responses": responses, "grid_points": len(grid), "grid_matched": matches,
             "boundaries": {str(score): scoring.score_to_label(score) for score in (human, ai)}},
        )

    def appeals(self, trial):
        texts = [row["text"] for row in scenarios.CALIBRATION]
        submissions = self.submit((texts * 3)[:10], f"{trial}_appeals")
        original = {e.get("content_id"): e for e in self.log() if e["status"] == "decided"}
        cases = []
        for i, response in enumerate(submissions, 1):
            if response["http_status"] != 200:
                cases.append({"submission": response})
                continue
            content_id = response["json"]["content_id"]
            reasoning = f"  I wrote this and can show my earlier draft {i}.  "
            reply = self.request("POST", "appeal", json={"content_id": content_id, "reasoning": reasoning})
            cases.append({"content_id": content_id, "reasoning": reasoning, "response": reply})

        unknown = self.request("POST", "appeal", json={"content_id": self.prefix, "reasoning": "Please review."})
        entries = self.log()
        count = 0
        for case in cases:
            if "content_id" not in case:
                continue
            content_id = case["content_id"]
            case["audit"] = [e for e in entries if e.get("content_id") == content_id]
            reply = case["response"]
            decisions = [e for e in case["audit"] if e["status"] == "decided"]
            appeals = [e for e in case["audit"] if e["status"] == "under_review"]
            count += (
                reply["http_status"] == 200 and reply["json"]["status"] == "under_review"
                and len(decisions) == 1 and decisions[0] == original.get(content_id)
                and len(appeals) == 1 and appeals[0]["reasoning"] == case["reasoning"]
            )
        complete = all("content_id" in case for case in cases)
        return result(f"{count}/10, unknown {unknown['http_status']}",
                      count == 10 and unknown["http_status"] == 404 if complete else None,
                      {"cases": cases, "unknown": unknown})

    def invalid(self, trial):
        old_length = len(self.log())
        cases = [
            {"case": name, "expected": expected, **self.request("POST", "submit", **kwargs)}
            for name, kwargs, expected in scenarios.bad_inputs(f"{self.prefix}_{trial}_invalid")
        ]
        audit = self.log()[old_length:]
        count = sum(
            c["http_status"] == c["expected"] and isinstance(c["json"], dict) and bool(c["json"].get("error"))
            for c in cases
        )
        decisions = sum(e["status"] == "decided" for e in audit)
        return result(f"{count}/{len(cases)}, {decisions} decisions",
                      count == len(cases) and decisions == 0,
                      {"responses": cases, "audit": audit})


def result(observed, passed, evidence):
    return {"observed": observed, "passed": passed, "evidence": evidence}


def verdict(trials):
    if any(trial["passed"] is False for trial in trials):
        return "MISSED"
    if any(trial["passed"] is None for trial in trials):
        return "INCOMPLETE"
    return "MET"


def write_report(rows, label):
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    suffix = f"_{label}" if label else ""
    path = config.RESULTS_DIR / f"run_{stamp}{suffix}.md"
    config.RESULTS_DIR.mkdir(exist_ok=True)
    lines = [
        f"# Run log{f' — {label}' if label else ''}", "",
        "Produced by `run_eval.py::Evaluation`. The score grid calls `scoring.py::score_to_label`.",
        "`verify.py` separately asserts that invalid inputs never call the detector.", "",
        "| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |",
        "|---|---|---|---|---|---|",
    ]
    for (name, target), trials in zip(TARGETS.items(), rows):
        observed = " | ".join(trial["observed"] for trial in trials)
        lines.append(f"| {name} | {target} | {observed} | {verdict(trials)} |")
    for name, trials in zip(TARGETS, rows):
        lines += ["", f"## {name}"]
        for i, trial in enumerate(trials, 1):
            lines += ["", f"### Trial {i}", "", "```json",
                      json.dumps(trial["evidence"], indent=2), "```"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", default="", choices=("", "before", "after"))
    parser.add_argument("--url", default=f"http://{config.HOST}:{config.PORT}")
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()
    human, ai = scenarios.writing_inputs()
    evaluation = Evaluation(args.url, args.timeout)
    health = evaluation.request("GET", "health")
    if health["http_status"] != 200 or not health["json"]["rate_limiting"]:
        parser.error("start app.py with rate limiting enabled")
    rows = [[] for _ in TARGETS]
    for trial in range(1, 4):
        results = [
            evaluation.false_accusations(human, trial),
            evaluation.score_gap(human, ai, trial),
            evaluation.labels(trial),
            evaluation.appeals(trial),
            evaluation.invalid(trial),
        ]
        for row, measured in zip(rows, results):
            row.append(measured)
        print(f"Trial {trial}: " + " | ".join(r["observed"] for r in results))
    write_report(rows, args.label)


if __name__ == "__main__":
    main()
