from datetime import date as today_date, datetime
import re
from flask import Flask, render_template, request

from app.pipeline.complaint_pipeline import run_complaint_pipeline

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static",
)


def is_hindi_text(text: str) -> bool:
  """Detect if the input string contains Devanagari (Hindi) characters."""
  return bool(re.search(r"[\u0900-\u097F]", text))


@app.route("/")
def home():
  return render_template("index.html", today=today_date.today().isoformat())


@app.route("/submit", methods=["POST"])
def submit_complaint():
  complaint = request.form.get("complaint", "").strip()
  selected_language = request.form.get("language", "").strip()
  date = request.form.get("date", "").strip()
  time = request.form.get("time", "").strip()
  location = request.form.get("location", "").strip()

  # 1. Date validation
  if date:
    try:
      selected_date = datetime.strptime(date, "%Y-%m-%d").date()
      if selected_date > today_date.today():
        return render_template(
            "index.html",
            error="Please select today or an earlier date.",
            today=today_date.today().isoformat(),
        )
    except ValueError:
      return render_template(
          "index.html",
          error="Please enter a valid date.",
          today=today_date.today().isoformat(),
      )

  # 2. Complaint empty check
  if not complaint:
    return render_template(
        "index.html",
        error="Please enter a complaint before submitting.",
        today=today_date.today().isoformat(),
    )

  # 3. Language resolution:
  # If Devanagari text is detected in the input, force language mode to "Hindi".
  # Otherwise, fall back to the dropdown choice (defaulting to "English").
  if is_hindi_text(complaint):
    active_language = "Hindi"
  elif selected_language in ["English", "Hindi"]:
    active_language = selected_language
  else:
    active_language = "English"

  try:
    result = run_complaint_pipeline(
        complaint=complaint,
        language=active_language,
        date=date,
        time=time,
        location=location,
    )

    return render_template(
        "index.html", result=result, today=today_date.today().isoformat()
    )

  except Exception as e:
    print("Pipeline Error:", e)
    return render_template(
        "index.html",
        error="Something went wrong while processing the complaint.",
        today=today_date.today().isoformat(),
    )


if __name__ == "__main__":
  app.run(debug=True)