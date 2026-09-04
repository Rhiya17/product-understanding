import os
import sys
import time
import json
import requests
import subprocess
from pathlib import Path

# Load env
os.environ["FAL_KEY"] = "c06d5a26-a1b8-4bee-a9b3-dec02f2828aa:891ad6242172679e5cb31d9017e6b90d"
if "SHOWME_VIDEO_RENDERER" in os.environ:
    del os.environ["SHOWME_VIDEO_RENDERER"]

# Start server
server = subprocess.Popen(["python3", "-m", "app.server"])

t0 = time.time()
for _ in range(10):
    time.sleep(2)
    try:
        res = requests.post("http://localhost:8000/api/chat", json={
            "messages": [{"role": "user", "content": "Show me a video of how to connect Bose QuietComfort Ultra headphones to a MacBook Air using the audio cable."}]
        })
        print(f"Server answered with {res.status_code}")
        break
    except requests.exceptions.ConnectionError:
        pass
else:
    print("Server failed to start")
    server.terminate()
    sys.exit(1)

try:
    # We should have a job enqueued.
    # Wait up to 5 minutes
    for i in range(120):
        time.sleep(5)
        # check if connect-aux-cable-walkthrough.mp4 exists
        if Path("generated-assets/bose-qc-ultra-headphones/connect-aux-cable-walkthrough.mp4").exists():
            print("Video generated!")
            break
        # check if verification file exists
        if Path("generated-assets/bose-qc-ultra-headphones/connect-aux-cable-walkthrough-verification.json").exists():
            print("Verification file exists!")
            break
            
        kf_dir = Path("generated-assets/bose-qc-ultra-headphones/keyframes")
        if kf_dir.exists():
            print(f"Checking keyframes at {time.time() - t0:.1f}s...")
            for p in kf_dir.glob("*.provenance.json"):
                with open(p) as f:
                    d = json.load(f)
                    if d.get("verdict", {}).get("verdict") == "fail":
                        print(f"Keyframe {p.name} failed verification!")
                        # Do NOT break outer loop, we just log it. If it fails twice, it will raise exception in the background thread.
    
    t1 = time.time()
    print(f"Finished in {t1 - t0:.1f}s")
    
finally:
    server.terminate()
    server.wait()

