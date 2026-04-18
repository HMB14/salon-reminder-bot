from __future__ import annotations
import json
import os
from datetime import datetime
from pathlib import Path

from salon.models import Appointment

_DATE_FMT = "%Y-%m-%d %H:%M"


def _log_path() -> Path:
    if env := os.environ.get("SALON_LOG"):
        return Path(env)
    base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return base / "salon-bot" / "appointments.jsonl"


def _serialize(appt: Appointment) -> str:
    return json.dumps({
        "name": appt.name,
        "service": appt.service,
        "time": appt.time.strftime(_DATE_FMT),
        "phone": appt.phone,
        "stylist": appt.stylist,
        "branch": appt.branch,
        "notes": appt.notes,
        "logged_at": appt.logged_at.strftime(_DATE_FMT),
    }, ensure_ascii=False)


def _deserialize(line: str) -> Appointment:
    d = json.loads(line)
    return Appointment(
        name=d["name"],
        service=d["service"],
        time=datetime.strptime(d["time"], _DATE_FMT),
        phone=d["phone"],
        stylist=d.get("stylist"),
        branch=d.get("branch"),
        notes=d.get("notes"),
        logged_at=datetime.strptime(d["logged_at"], _DATE_FMT),
    )


def append_appointment(appt: Appointment) -> None:
    path = _log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(_serialize(appt) + "\n")


def load_appointments() -> list[Appointment]:
    path = _log_path()
    if not path.exists():
        return []
    appointments = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                appointments.append(_deserialize(line))
    return appointments
