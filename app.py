#!/usr/bin/env python3
"""
Provenance Guard — the web service.

    python app.py

Then, in another terminal:

    curl -X POST http://127.0.0.1:5000/ping \
      -H "Content-Type: application/json" \
      -d '{"message": "hello"}'

That's the example route. It works right now, before you've written anything.
**Leave it alone** — it's your control. When something breaks later, check that
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself.

Routes:

    POST /ping        the worked example. Already works. Don't edit it
    POST /submit      ← YOU BUILD THIS (Milestone 3, 4, 5)
    POST /appeal      ← YOU BUILD THIS (Milestone 5)
    GET  /log         the audit log. Already works
    GET  /health      is the service up, and is the model loaded
"""

import uuid

from flask import Flask, jsonify, request

import audit
import config
import detector
import scoring
import stylometry

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 100_000


@app.errorhandler(413)
def request_too_large(exc):
    if request.endpoint == "submit":
        return reject_submission(None, "request_too_large", "The request body is too large.", 413)
    return jsonify(error="request_too_large", message="The request body is too large."), 413


# ── Rate limiting — UNIT 8 ────────────────────────────────────────────────────
# A process-local limiter for the course prototype. Restarting clears its counters.

class _LimiterOff:
    """
    Stands in for the real limiter while rate limiting is off.

    It makes @limiter.limit(...) a decorator that returns the route
    untouched, so uncommenting the line before you flip the setting is
    harmless instead of a crash on startup.
    """

    def reset(self):
        pass

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()
if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        payload = request.get_json(silent=True)
        creator = payload.get("creator_id") if isinstance(payload, dict) else None
        if isinstance(creator, str) and 0 < len(creator) <= 200 and creator.strip():
            return f"creator:{creator.strip()}"
        return f"address:{get_remote_address()}"

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """
        A rejected request still leaves a trace.

        ⚠️ An attack that shows up only as an absence is one you'll never find.
        """
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}
        audit.log_rejection(
            creator_id=audit_creator(payload.get("creator_id")),
            reason="rate_limited",
            http_status=429,
            limit=str(exc.description),
        )
        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429


# ── The worked example. Already works. Don't edit. ────────────────────────────

@app.post("/ping")
def ping():
    """
    Everything a route needs, in six lines.

    JSON arrives as a dict. You pull things out of it. You return a dict and
    the framework turns it into a response. That's the whole idea.
    """
    payload = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


@app.get("/health")
def health():
    """Is the service up, and has the model been downloaded yet?"""
    import detector

    loaded = detector._model is not None
    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })


# Submission and appeal routes

def audit_creator(creator_id):
    if isinstance(creator_id, str) and len(creator_id) <= 200:
        return creator_id.strip() or "unknown"
    return "unknown"


def reject_submission(creator_id, error, message, status=400, *, reason=None):
    audit.log_rejection(
        creator_id=audit_creator(creator_id),
        reason=reason or error,
        http_status=status,
        message=message,
    )
    return jsonify(error=error, message=message), status


@app.post("/submit")
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    """Validate a submission, run both signals, log the decision, and return its label."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return reject_submission(None, "invalid_input", "Send a JSON object.")
    text = payload.get("text")
    creator_id = payload.get("creator_id")
    if not isinstance(text, str) or not text.strip():
        return reject_submission(creator_id, "invalid_input", "text must be a nonempty string.")
    if not isinstance(creator_id, str) or not creator_id.strip():
        return reject_submission(creator_id, "invalid_input", "creator_id must be a nonempty string.")
    if len(text) > config.MAX_TEXT_CHARACTERS:
        return reject_submission(creator_id, "text_too_large", "text must be at most 10000 characters.", 413)
    if len(creator_id) > 200:
        return reject_submission(creator_id, "invalid_input", "creator_id must be at most 200 characters.")
    try:
        model_score = detector.model_signal(text)
    except detector.DetectorUnavailable:
        app.logger.exception("The local detector could not load")
        return reject_submission(
            creator_id, "detector_unavailable",
            "The local detector is unavailable. Install the dependencies and run python detector.py.", 503,
        )
    except ValueError:
        return reject_submission(
            creator_id, "invalid_input", "Text is too short to score. Send a few sentences.",
            reason="text_too_short",
        )
    style_score = stylometry.style_signal(text)
    combined_score = scoring.combine_signals(model_score, style_score)
    guess, label = scoring.score_to_label(combined_score)
    content_id = str(uuid.uuid4())
    entry = audit.log_decision(
        content_id=content_id, creator_id=creator_id.strip(),
        guess=guess, model_score=model_score, style_score=style_score,
        combined_score=combined_score,
        label=label,
    )
    return jsonify(content_id=content_id, guess=entry["guess"],
                   confidence=combined_score, label=entry["label"],
                   model_score=model_score, style_score=style_score, status=entry["status"])


@app.post("/appeal")
def appeal():
    """Record a writer's reasoning and move an existing submission under review."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="invalid_input", message="Send a JSON object."), 400
    content_id = payload.get("content_id")
    reasoning = payload.get("reasoning")
    if not isinstance(content_id, str) or not content_id.strip() or len(content_id) > 200:
        return jsonify(error="invalid_input", message="content_id must be a nonempty string of at most 200 characters."), 400
    if not isinstance(reasoning, str) or not reasoning.strip() or len(reasoning) > 5000:
        return jsonify(error="invalid_input", message="reasoning must be a nonempty string of at most 5000 characters."), 400
    content_id = content_id.strip()
    decisions = [entry for entry in audit.entries_for(content_id)
                 if entry.get("status") == "decided"]
    if not decisions:
        return jsonify(error="not_found", message="No submission has that content_id."), 404
    audit.log_appeal(content_id=content_id,
                     creator_id=decisions[0]["creator_id"], reasoning=reasoning)
    return jsonify(content_id=content_id, status="under_review",
                   message="Your appeal has been recorded and the submission is under review.")


# ── Already works ─────────────────────────────────────────────────────────────

@app.get("/log")
def get_log():
    """
    The audit log, most recent last.

        curl "http://127.0.0.1:5000/log?limit=10"

    You need this in unit 8 to paste entries into your README, and you need it
    now to see whether your logging is actually working.
    """
    limit = request.args.get("limit", type=int)
    entries = audit.read_entries(limit=limit)
    return jsonify({"count": len(entries), "entries": entries})


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print()
    print("Check it's alive:")
    print(f'  curl -X POST http://{config.HOST}:{config.PORT}/ping \\')
    print('    -H "Content-Type: application/json" \\')
    print("    -d '{\"message\": \"hello\"}'")
    print()
    # debug=True hands out an interactive debugger, so it's local-only — see config.py
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
