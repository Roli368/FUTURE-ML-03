
import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"


import threading
import uuid
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename


from ats_engine import rank_uploaded_resumes

app = Flask(__name__)

# ---------------- CONFIG ---------------
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------- ROUTES ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    error = None

    if request.method == "POST":
        jd = request.form.get("jd")
        files = request.files.getlist("resumes")

        if not jd:
            error = "Job Description is required."
            return render_template("index.html", results=None, error=error)

        if not files or files[0].filename == "":
            error = "Please upload at least one PDF resume."
            return render_template("index.html", results=None, error=error)

        uploaded_paths = []

        for file in files:
            if file and allowed_file(file.filename):
                unique_name = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
                file.save(save_path)
                uploaded_paths.append(save_path)

        if not uploaded_paths:
            error = "Only PDF files are allowed."
            return render_template("index.html", results=None, error=error)

        # -------- RUN ATS ENGINE --------
        results = rank_uploaded_resumes(
            uploaded_files=uploaded_paths,
            jd_text=jd
        )

    return render_template("index.html", results=results, error=error)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
