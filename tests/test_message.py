from datetime import datetime
from salon.models import Appointment
from salon.message import generate_messages


def _appt(**kwargs):
    defaults = dict(
        name="Fatima",
        service="Haircut",
        time=datetime(2026, 4, 20, 14, 0),
        phone="+966501234567",
    )
    defaults.update(kwargs)
    return Appointment(**defaults)


def test_english_contains_name_and_service():
    en, _ = generate_messages(_appt())
    assert "Fatima" in en
    assert "Haircut" in en


def test_arabic_contains_name_and_service():
    _, ar = generate_messages(_appt())
    assert "Fatima" in ar
    assert "Haircut" in ar


def test_optional_fields_omitted_when_absent():
    en, ar = generate_messages(_appt())
    assert "Stylist" not in en
    assert "مع:" not in ar
    assert "📍" not in en
    assert "📍" not in ar


def test_optional_fields_included_when_present():
    en, ar = generate_messages(_appt(stylist="Noura", branch="Riyadh Main", notes="No heat"))
    assert "Noura" in en
    assert "Riyadh Main" in en
    assert "No heat" in en
    assert "Noura" in ar
    assert "Riyadh Main" in ar


def test_arabic_greeting_present():
    _, ar = generate_messages(_appt())
    assert "مرحباً" in ar


def test_english_closing_present():
    en, _ = generate_messages(_appt())
    assert "look forward" in en


def test_arabic_closing_present():
    _, ar = generate_messages(_appt())
    assert "نتطلع" in ar
