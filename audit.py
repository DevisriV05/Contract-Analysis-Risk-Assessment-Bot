import json
import uuid
from datetime import datetime
import os

os.makedirs("audits", exist_ok=True)


def save_audit(data):
    audit_id = str(uuid.uuid4())
    path = f"audits/{audit_id}.json"

    data["timestamp"] = datetime.now().isoformat()

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    return audit_id
