from __future__ import annotations
from salon.models import Appointment

_TIME_FMT = "%I:%M %p"
_DATE_FMT = "%A, %B %d %Y"


def generate_messages(appt: Appointment) -> tuple[str, str]:
    date_en = appt.time.strftime(_DATE_FMT)
    time_en = appt.time.strftime(_TIME_FMT)

    en_lines = [f"Hi {appt.name}! 👋", f"This is a reminder for your *{appt.service}* appointment"]
    if appt.branch:
        en_lines.append(f"📍 {appt.branch}")
    en_lines.append(f"🗓️ {date_en} at {time_en}")
    if appt.stylist:
        en_lines.append(f"💇 Stylist: {appt.stylist}")
    if appt.notes:
        en_lines.append(f"📝 {appt.notes}")
    en_lines.append("")
    en_lines.append("We look forward to seeing you! ✨")

    ar_lines = [f"مرحباً {appt.name}! 👋", f"هذا تذكير بموعدك لـ *{appt.service}*"]
    if appt.branch:
        ar_lines.append(f"📍 {appt.branch}")
    ar_lines.append(f"🗓️ {date_en} الساعة {time_en}")
    if appt.stylist:
        ar_lines.append(f"💇 مع: {appt.stylist}")
    if appt.notes:
        ar_lines.append(f"📝 {appt.notes}")
    ar_lines.append("")
    ar_lines.append("نتطلع لرؤيتكِ! ✨")

    return "\n".join(en_lines), "\n".join(ar_lines)
