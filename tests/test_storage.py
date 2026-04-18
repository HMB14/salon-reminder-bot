import pytest
from datetime import datetime
from salon.models import Appointment
from salon.storage import append_appointment, load_appointments


@pytest.fixture(autouse=True)
def salon_log(tmp_path, monkeypatch):
    monkeypatch.setenv("SALON_LOG", str(tmp_path / "appointments.jsonl"))


def _make_appt(**kwargs):
    defaults = dict(
        name="Fatima",
        service="Haircut",
        time=datetime(2026, 4, 20, 14, 0),
        phone="+966501234567",
    )
    defaults.update(kwargs)
    return Appointment(**defaults)


def test_roundtrip_minimal():
    appt = _make_appt()
    append_appointment(appt)
    loaded = load_appointments()
    assert len(loaded) == 1
    a = loaded[0]
    assert a.name == "Fatima"
    assert a.service == "Haircut"
    assert a.time == datetime(2026, 4, 20, 14, 0)
    assert a.phone == "+966501234567"
    assert a.stylist is None
    assert a.branch is None
    assert a.notes is None


def test_roundtrip_full():
    appt = _make_appt(stylist="Noura", branch="Riyadh Main", notes="No heat styling")
    append_appointment(appt)
    a = load_appointments()[0]
    assert a.stylist == "Noura"
    assert a.branch == "Riyadh Main"
    assert a.notes == "No heat styling"


def test_arabic_name_preserved():
    appt = _make_appt(name="فاطمة", service="قص شعر")
    append_appointment(appt)
    a = load_appointments()[0]
    assert a.name == "فاطمة"
    assert a.service == "قص شعر"


def test_multiple_appointments_order():
    append_appointment(_make_appt(name="A"))
    append_appointment(_make_appt(name="B"))
    append_appointment(_make_appt(name="C"))
    loaded = load_appointments()
    assert [a.name for a in loaded] == ["A", "B", "C"]


def test_empty_log_returns_empty_list():
    assert load_appointments() == []
