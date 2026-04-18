from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Appointment:
    name: str
    service: str
    time: datetime
    phone: str
    stylist: str | None = None
    branch: str | None = None
    notes: str | None = None
    logged_at: datetime = field(default_factory=datetime.now)
