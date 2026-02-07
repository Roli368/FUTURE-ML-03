# AI-Powered Resume Screening System (ATS)

An intelligent **Applicant Tracking System (ATS)** that leverages **Natural Language Processing (NLP)** to rank resumes against job descriptions.  
Unlike traditional keyword-based ATS, this system understands **semantic meaning** and filters out generic “noise” to identify the **most relevant candidates**.

---

## 🎥 Demo (GIF)

![ATS Demo](static/demo.gif)

---

## 🚀 Features

* **AI-Powered Ranking**  
  Combines **Sentence-BERT** for semantic similarity and **TF-IDF** for keyword precision to generate accurate resume–JD match scores.

* **Smart Skill Extraction**  
  Automatically extracts technical skills while ignoring generic filler terms (e.g., *“team player”*, *“hardworking”*) using a custom-trained noise blacklist.

* **Instant Feedback for Recruiters**  
  Visual badges highlight **Matched Skills** and **Missing Skills**, enabling faster and clearer decision-making.

* **Auto-Fill Job Descriptions**  
  Select a predefined job role (e.g., *Python Developer*) and the system auto-fills a professional Job Description.

* **Secure PDF Resume Analysis**  
  Parses and analyzes uploaded PDF resumes safely and efficiently.

---

## 🧠 Technology Stack

* **Backend**: Python, Flask (REST-based architecture)
* **ML / NLP**:
  * `spaCy` – Text processing & linguistic analysis  
  * `sentence-transformers` – Semantic similarity (SBERT)  
  * `scikit-learn` – TF-IDF vectorization & scoring
* **Frontend**: HTML5, CSS3 (Vanilla), JavaScript
* **Deployment**: Docker, Render

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone <repository-url>
cd <repo-name>


