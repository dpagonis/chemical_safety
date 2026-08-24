from pathlib import Path
import os
from datetime import datetime

LOGS_DIR = Path.joinpath(Path(__file__).parent,"logs")
os.makedirs(LOGS_DIR,exist_ok=True)

PUG_VIEW_LOG_PATH = Path.joinpath(LOGS_DIR,"PUG_VIEW_LOG.txt")
PUG_VIEW_LOG_PATH.touch(exist_ok=True)

PUG_REST_LOG_PATH = Path.joinpath(LOGS_DIR,"PUG_REST_LOG.txt")
PUG_REST_LOG_PATH.touch(exist_ok=True)

def log_pugview(response):
    logstring = _make_logstring(response)
    _log(PUG_VIEW_LOG_PATH,logstring)
    return

def log_pugrest(response):
    logstring = _make_logstring(response)
    _log(PUG_REST_LOG_PATH,logstring)
    return

def _make_logstring(response):
    if response.status_code == 200:
        throttling = response.headers.get('X-Throttling-Control', 'Throttle Info N/A')
        return f"{response.status_code}: {throttling}"
    
    # Non-200 status handling
    reason = getattr(response, 'reason', '') or 'Unknown Error'
    
    # Try to extract a clean JSON error message, fall back to truncated raw text
    try:
        error_body = response.json()
    except Exception:
        # Strip whitespace and limit length to prevent huge HTML dumps in logs
        error_body = response.text.strip()[:200] if response.text else "No response body"
        
    return f"{response.status_code} {reason}: {error_body}"

def _log(path,logstring):
    try:
        with open(path, "a", encoding='utf-8') as f:
            line = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {logstring}\n'
            f.write(line)
    except:
        pass

    return
