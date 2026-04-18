import pytest
from click.testing import CliRunner
from salon.cli import cli
from salon.storage import load_appointments


@pytest.fixture(autouse=True)
def salon_log(tmp_path, monkeypatch):
    monkeypatch.setenv("SALON_LOG", str(tmp_path / "appointments.jsonl"))


def test_add_logs_appointment():
    runner = CliRunner()
    result = runner.invoke(cli, [
        "add",
        "--name", "Fatima",
        "--service", "Haircut",
        "--time", "2026-04-20 14:00",
        "--phone", "+966501234567",
    ])
    assert result.exit_code == 0
    appointments = load_appointments()
    assert len(appointments) == 1
    assert appointments[0].name == "Fatima"


def test_add_prints_both_languages():
    runner = CliRunner()
    result = runner.invoke(cli, [
        "add", "--name", "Sara", "--service", "Manicure",
        "--time", "2026-04-21 10:00", "--phone", "+966509999999",
    ])
    assert "Sara" in result.output
    assert "مرحباً" in result.output


def test_add_invalid_time_format():
    runner = CliRunner()
    result = runner.invoke(cli, [
        "add", "--name", "Sara", "--service", "Manicure",
        "--time", "not-a-date", "--phone", "+966509999999",
    ])
    assert result.exit_code != 0


def test_add_with_all_options():
    runner = CliRunner()
    result = runner.invoke(cli, [
        "add", "--name", "Noura", "--service", "Balayage",
        "--time", "2026-04-22 16:30", "--phone", "+966501111111",
        "--stylist", "Lina", "--branch", "Jeddah Branch", "--notes", "Sensitive scalp",
    ])
    assert result.exit_code == 0
    appt = load_appointments()[0]
    assert appt.stylist == "Lina"
    assert appt.branch == "Jeddah Branch"
    assert appt.notes == "Sensitive scalp"


def test_list_empty():
    runner = CliRunner()
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "No appointments" in result.output


def test_list_shows_logged_appointments():
    runner = CliRunner()
    runner.invoke(cli, [
        "add", "--name", "Huda", "--service", "Blowout",
        "--time", "2026-04-23 11:00", "--phone", "+966502222222",
    ])
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "Huda" in result.output
