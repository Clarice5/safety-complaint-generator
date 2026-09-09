from flask import Flask, render_template, request
from datetime import date as today_date, datetime

from app.pipeline.complaint_pipeline import run_complaint_pipeline


app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)


@app.route("/")
def home():
    return render_template(
        "index.html",
        today=today_date.today().isoformat()
    )


@app.route("/submit", methods=["POST"])
def submit_complaint():

    complaint = request.form.get("complaint", "").strip()
    language = request.form.get("language", "").strip()
    date = request.form.get("date", "").strip()
    time = request.form.get("time", "").strip()
    location = request.form.get("location", "").strip()

    # Check whether the selected date is valid and not in the future
    if date:
        try:
            selected_date = datetime.strptime(date, "%Y-%m-%d").date()

            if selected_date > today_date.today():
                return render_template(
                    "index.html",
                    error="Please select today or an earlier date.",
                    today=today_date.today().isoformat()
                )

        except ValueError:
            return render_template(
                "index.html",
                error="Please enter a valid date.",
                today=today_date.today().isoformat()
            )

    # Check whether complaint was entered
    if not complaint:

        return render_template(
            "index.html",
            error="Please enter a complaint before submitting.",
            today=today_date.today().isoformat()
        )

    # Check language
    if language not in ["English", "Hindi"]:

        return render_template(
            "index.html",
            error="Please select a valid language.",
            today=today_date.today().isoformat()
        )

    try:

        result = run_complaint_pipeline(
            complaint=complaint,
            language=language,
            date=date,
            time=time,
            location=location
        )

        return render_template(
            "index.html",
            result=result,
            today=today_date.today().isoformat()
        )

    except Exception as e:

        print("Pipeline Error:", e)

        return render_template(
            "index.html",
            error="Something went wrong while processing the complaint.",
            today=today_date.today().isoformat()
        )


if __name__ == "__main__":
    app.run(debug=True)