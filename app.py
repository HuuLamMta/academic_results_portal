from flask import Flask, render_template, request
import sqlite3, os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "grades.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def letter_color(letter):
    if letter in ("A+", "A"):  return "pass"
    if letter in ("B+", "B"):  return "good"
    if letter in ("C+", "C"):  return "warn"
    return "fail"


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error  = None
    query  = ""

    if request.method == "POST":
        query           = request.form.get("student_id", "").strip()
        semester_filter = request.form.get("semester", "").strip()

        conn    = get_db()
        student = conn.execute(
            "SELECT * FROM students WHERE id = ? COLLATE NOCASE", (query,)
        ).fetchone()

        if not student:
            error = f'Không tìm thấy sinh viên với mã "{query}".'
        else:
            sql    = "SELECT * FROM grades WHERE student_id = ?"
            params = [student["id"]]
            if semester_filter:
                sql    += " AND semester = ?"
                params.append(semester_filter)
            sql += " ORDER BY semester, subject_name"

            rows = conn.execute(sql, params).fetchall()

            semesters_all = conn.execute(
                "SELECT DISTINCT semester FROM grades WHERE student_id = ? ORDER BY semester",
                (student["id"],)
            ).fetchall()

            # Weighted GPA (hệ 10)
            total_pts  = sum(r["score_10"] * r["credits"] for r in rows
                             if r["score_10"] is not None and r["credits"])
            total_cred = sum(r["credits"] for r in rows
                             if r["score_10"] is not None and r["credits"])
            avg_10 = round(total_pts / total_cred, 2) if total_cred else None

            # Weighted GPA (hệ 4)
            pts4  = sum(r["score_4"] * r["credits"] for r in rows
                        if r["score_4"] is not None and r["credits"])
            avg_4 = round(pts4 / total_cred, 2) if total_cred else None

            grades = [
                dict(r) | {"color": letter_color(r["letter"] or "")}
                for r in rows
            ]

            result = {
                "student":         dict(student),
                "grades":          grades,
                "avg_10":          avg_10,
                "avg_4":           avg_4,
                "total_credits":   total_cred,
                "semesters_all":   [r["semester"] for r in semesters_all],
                "semester_filter": semester_filter,
            }
        conn.close()

    return render_template("index.html", result=result, error=error, query=query)


if __name__ == "__main__":
    app.run(debug=True)
