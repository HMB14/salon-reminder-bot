from __future__ import annotations
from salon.models import Appointment

_TIME_FMT = "%I:%M %p"
_DATE_FMT = "%A, %B %d %Y"

_DAYS_AR = {
    "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء",
    "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت", "Sunday": "الأحد",
}
_MONTHS_AR = {
    "January": "يناير", "February": "فبراير", "March": "مارس", "April": "أبريل",
    "May": "مايو", "June": "يونيو", "July": "يوليو", "August": "أغسطس",
    "September": "سبتمبر", "October": "أكتوبر", "November": "نوفمبر", "December": "ديسمبر",
}


def _arabic_datetime(dt) -> tuple[str, str]:
    day_ar = _DAYS_AR[dt.strftime("%A")]
    month_ar = _MONTHS_AR[dt.strftime("%B")]
    date_ar = f"{day_ar}، {dt.day} {month_ar} {dt.year}"
    hour = dt.strftime("%I").lstrip("0") or "12"
    minute = dt.strftime("%M")
    period = "مساءً" if dt.strftime("%p") == "PM" else "صباحاً"
    time_ar = f"{hour}:{minute} {period}"
    return date_ar, time_ar


def generate_messages(appt: Appointment) -> tuple[str, str]:
    date_en = appt.time.strftime(_DATE_FMT)
    time_en = appt.time.strftime(_TIME_FMT)
    date_ar, time_ar = _arabic_datetime(appt.time)

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
    ar_lines.append(f"🗓️ {date_ar} الساعة {time_ar}")
    if appt.stylist:
        ar_lines.append(f"💇 المصففة: {appt.stylist}")
    if appt.notes:
        ar_lines.append(f"📝 {appt.notes}")
    ar_lines.append("")
    ar_lines.append("نتطلع لرؤيتكِ! ✨")

    return "\n".join(en_lines), "\n".join(ar_lines)
