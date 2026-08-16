import json
from pathlib import Path
from datetime import datetime


REQUESTS_FILE = Path("data/requests.json")


def load_requests():
    """Load existing requests."""

    if not REQUESTS_FILE.exists():
        return []

    with open(
        REQUESTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def save_requests(requests):
    """Save requests to disk."""

    REQUESTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        REQUESTS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            requests,
            file,
            indent=4
        )


def create_laptop_request(
    employee_name,
    department,
    reason,
    specifications
):
    """Create a new laptop request."""

    requests = load_requests()

    request_id = (
        f"IT-{len(requests) + 1:04d}"
    )

    request = {
        "request_id": request_id,
        "request_type": "Laptop Request",
        "employee_name": employee_name,
        "department": department,
        "reason": reason,
        "specifications": specifications,
        "status": "Pending Manager Approval",
        "created_at": datetime.now().isoformat(
            timespec="seconds"
        )
    }

    requests.append(request)

    save_requests(requests)

    return request


def get_requests():
    """Return all requests."""

    return load_requests()
def update_request_status(request_id, new_status):
    """Update the status of an existing request."""

    requests = load_requests()

    for request in requests:

        if request["request_id"] == request_id:

            request["status"] = new_status

            save_requests(requests)

            return request

    return None


def get_pending_requests():
    """Return requests waiting for manager approval."""

    requests = load_requests()

    return [
        request
        for request in requests
        if request["status"] == "Pending Manager Approval"
    ]