from __future__ import annotations
from datetime import datetime
from flask import Flask, render_template, request
from salon.models import Appointment
from salon.message import generate_messages

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    en_msg = ar_msg = error = None

    if request.method == "POST":
        try:
            raw_time = request.form["appointment_time"]
            appt_time = datetime.fromisoformat(raw_time)
            appt = Appointment(
                name=request.form["name"].strip(),
                service=request.form["service"].strip(),
                time=appt_time,
                phone=request.form["phone"].strip(),
                stylist=request.form["stylist"].strip() or None,
                branch=request.form["branch"].strip() or None,
            )
            en_msg, ar_msg = generate_messages(appt)
        except (ValueError, KeyError) as exc:
            error = str(exc)

    return render_template("index.html", en_msg=en_msg, ar_msg=ar_msg, error=error)


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
