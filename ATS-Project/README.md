# 📄 AI-Powered Resume Screening System

A powerful, intelligent Applicant Tracking System (ATS) that utilizes Natural Language Processing (NLP) to rank resumes against job descriptions. This system goes beyond simple keyword matching by understanding semantic meaning and filtering out generic "noise" to find the best candidates.

## ✨ Features

*   **🧠 AI-Powered Ranking**: Uses `Sentence-BERT` for semantic understanding and `TF-IDF` for keyword precision.
*   **📊 Smart Skill Extraction**: Automatically identifies technical skills while ignoring generic filler words (e.g., "team player", "hardworking") using a custom-trained blacklist.
*   **⚡ Instant Feedback**: visual badges for "Matched" and "Missing" skills to help recruiters make quick decisions.

*   **🔄 Auto-Fill JD**: Select a job role (e.g., "Python Developer") and the system pre-fills a professional Job Description for you.
*   **📂 PDF Analysis**: Securely parses and analyzes PDF resumes.

## 🛠️ Technology Stack

*   **Backend**: Python, Flask
*   **ML/NLP**: 
    *   `spaCy` (Text Processing)
    *   `sentence-transformers` (Semantic Search)
    *   `scikit-learn` (Vectorization)
*   **Frontend**: HTML5, CSS3 (Vanilla), JavaScript

## 🚀 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd ATS-Project
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Download NLP Models**
    ```bash
    python -m spacy download en_core_web_sm
    ```

4.  **Train the Skill Extractor (First Run Only)**
    This step scans your `data/` folder (resume dataset) to build a "Knowledge Base" of valid skills and ignore common noise.
    ```bash
    python trainer.py
    ```
    *Output: Generates `artifacts/skill_vocab.json` and `artifacts/tfidf_model.pkl`.*

5.  **Run the Application**
    ```bash
    python app.py
    ```

6.  **Access the Dashboard**
    Open your browser and navigate to: `http://127.0.0.1:5000/`

## � Running in VS Code
##  Running in VS Code

1.  Open the project folder (`ATS-Project`) in VS Code.
2.  Open a **New Terminal** (`Ctrl + ~`).
3.  Ensure you are in the project root directory.
4.  Run the application:
    ```powershell
    python app.py
    ```
5.  `Ctrl + Click` the link `http://127.0.0.1:5000/` in the terminal to open.

## 🌍 Deployment

You can deploy this application using Docker or any cloud platform that supports Python/Docker (e.g., Render, Heroku).

### 🐳 Docker

1.  **Build the Image**:
    ```bash
    docker build -t ats-app .
    ```

2.  **Run the Container**:
    ```bash
    docker run -p 5000:5000 ats-app
    ```
    Access the app at `http://localhost:5000`.

### ☁️ Cloud Deployment

The project includes a `Dockerfile` and `Procfile` ready for deployment.

1.  Push your code to a GitHub repository.
2.  Connect your repository to **Render**, **Heroku**, or **Railway**.
3.  The platform will automatically detect the configuration and deploy.

## 📖 Usage Guide

1.  **Select a Job Role**: Choose from the dropdown (e.g., ENGINEERING, SALES). The Job Description will auto-fill.
2.  **Upload Resumes**: Click "Upload Resumes" or drag & drop PDF files.
3.  **Analyze**: Click the **🚀 Analyze & Rank** button.
4.  **View Results**:
    *   See candidates ranked by score (0-100%).
    *   Green tags = Matched Skills.
    *   Red tags = Missing Skills.
    *   Click "View PDF" to inspect the original document.

## 📂 Project Structure


```bash
ATS-Project/
├── app.py              # Main Flask Application
├── ats_engine.py       # Core Logic (Ranking, Parsing, Matching)
├── trainer.py          # Offline Training Script (Noise Reduction)
├── requirements.txt    # Project Dependencies
├── artifacts/          # Generated ML Models & Vocab
│   ├── skill_vocab.json
│   └── tfidf_model.pkl
├── static/
│   ├── style.css       # Premium Styling
│   └── jd_templates.js # Pre-defined Job Descriptions
└── templates/
    └── index.html      # Main Dashboard
```

*Built for the Future ML Internship.*
