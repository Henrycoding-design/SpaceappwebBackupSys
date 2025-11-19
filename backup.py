import os
import subprocess
from datetime import datetime

db_url = os.environ["DATABASE_URL"]

filename = f"backup-{datetime.now().strftime('%Y-%m-%d')}.sql"

subprocess.run(
    ["pg_dump", 
     "--no-owner",
     "--no-privileges",
     "--clean",
     db_url, 
     "-f", filename
     ], check=True
)

print("Backup generated:", filename)

# ====== Push to github ======
import base64, requests

token = os.environ["GITHUB_TOKEN"]
repo = "yourusername/backup-repo"

# encode file
with open(filename, "rb") as f:
    content = base64.b64encode(f.read()).decode()

url = f"https://api.github.com/repos/{repo}/contents/{filename}"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

payload = {
    "message": f"Backup {datetime.now().strftime("%Y-%m-%d")}",
    "content": content
}

# upload
res = requests.put(url, json=payload, headers=headers)
print(res.json())

