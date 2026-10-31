"""শুধু day28–30 শিডিউল (FB ২৮ দিনের লিমিট পার হলে, ৫ নভেম্বরের পরে চালান)."""
import subprocess,sys,os
ROOT=os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable,os.path.join(ROOT,"schedule.py"),"--start","2026-11-03","--only","28,29,30"])
