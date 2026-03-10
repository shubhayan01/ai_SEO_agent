"""
Flask bridge server for AI Overview Content Gap Agent UI
"""

import os, sys, json, subprocess, threading, uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder=".")
CORS(app)

# Track running jobs
jobs = {}


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/run", methods=["POST"])
def run_analysis():
    data       = request.json or {}
    keyword    = data.get("keyword",    "").strip()
    client_url = data.get("clientUrl",  "").strip()
    output     = data.get("outputName", "gap_report").strip() or "gap_report"
    mock_dir   = data.get("mockHtmlDir","").strip()

    if not keyword:
        return jsonify({"error": "keyword is required"}), 400

    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {"status": "running", "log": [], "result": None, "error": None}

    def worker():
        cmd = [sys.executable, "agent.py", "--keyword", keyword]

        if client_url:
            cmd += ["--client-url", client_url]

        cmd += ["--output", f"{output}.docx"]

        if mock_dir:
            cmd += ["--mock-html-dir", mock_dir]

        jobs[job_id]["log"].append(f"[SERVER] Running: {' '.join(cmd)}")
        print(f"[SERVER] Running: {' '.join(cmd)}")

        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            for line in proc.stdout:
                line = line.rstrip()
                jobs[job_id]["log"].append(line)
                print(line)

            proc.wait()

            if proc.returncode != 0:
                jobs[job_id]["status"] = "error"
                jobs[job_id]["error"] = (
                    f"agent.py exited with code {proc.returncode}. "
                    "Check the log above for details."
                )
                return

            json_path = f"{output}.json"
            if os.path.exists(json_path):
                with open(json_path) as f:
                    jobs[job_id]["result"] = json.load(f)
                jobs[job_id]["status"] = "done"
            else:
                jobs[job_id]["status"] = "error"
                jobs[job_id]["error"] = f"Output file '{json_path}' not found after run."

        except Exception as e:
            jobs[job_id]["status"] = "error"
            jobs[job_id]["error"] = str(e)

    threading.Thread(target=worker, daemon=True).start()
    return jsonify({"job_id": job_id})


@app.route("/status/<job_id>")
def job_status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "unknown job"}), 404
    return jsonify(job)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Server running on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
