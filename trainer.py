# -------------------------------------------------
# FIX FOR WINDOWS + SKLEARN/NUMPY CRASH

import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import re
import json
import pickle
import spacy
import pdfplumber
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer


# CONFIG
# ------------------------------------------------
DATA_DIR = "data"
ARTIFACTS_DIR = "artifacts"
NLP_MODEL = "en_core_web_sm"
MAX_SKILLS = 2000

# SETUP
# -------------------------------------------------
if not os.path.exists(ARTIFACTS_DIR):
    os.makedirs(ARTIFACTS_DIR)

print(f"⏳ Loading spaCy model '{NLP_MODEL}'...")
try:
    nlp = spacy.load(NLP_MODEL, disable=["ner", "parser"])
except OSError:
    print(f" Model '{NLP_MODEL}' not found. Please run: python -m spacy download {NLP_MODEL}")
    exit(1)

# HELPER FUNCTIONS
# -------------------------------------------------
def extract_text_from_pdf(pdf_path):
    """Extracts text from the first 2 pages of a PDF."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:2]:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
    except Exception as e:
        pass # Ignore bad PDFs
    return text


# IGNORE LIST (Blacklist common generic terms)
# -------------------------------------------------
IGNORE_TERMS = {
    "experience", "knowledge", "skill", "ability", "year", "month", "role",
    "responsibility", "duty", "work", "team", "company", "candidate", "job",
    "description", "requirement", "application", "detail", "overview",
    "management", "manage", "manager", "assist", "general", "balance",
    "flow", "maintenance", "level", "system", "service", "support",
    "project", "process", "business", "client", "customer", "ensure",
    "provide", "maintain", "perform", "prepare", "participate", "create",
    "develop", "analyze", "coordinate", "good", "strong", "excellent",
    "proficient", "basic", "advanced", "various", "daily", "monthly",
    "report", "document", "record", "compliance", "policy", "procedure",
    "issue", "problem", "solution", "activity", "task", "goal", "target",
    "objective", "result", "outcome", "status", "change", "review",
    "standard", "quality", "practice", "need", "time", "date", "day",
    "number", "total", "amount", "budget", "cost", "price", "rate",
    "value", "cash", "bank", "account", "fund", "payment", "invoice",
    "filing", "audit", "tax", "finance", "financial", "legal", "law",
    "case", "court", "file", "record", "datum", "information", "communication",
    "writing", "reading", "speaking", "listening", "language", "english",
    "hindi", "degree", "diploma", "certificate", "qualification",
    "education", "university", "college", "school", "grade", "score",
    "mark", "result", "pass", "fail", "subject", "course", "class",
    "training", "workshop", "seminar", "conference", "meeting", "presentation",
    "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december",
    "summary", "profile", "career", "objective", "declaration", "reference",
    "name", "address", "phone", "email", "mobile", "contact",
    "page", "curriculum", "vitae", "resume",
    "street", "road", "city", "state", "country", "india", "delhi", "mumbai",
    "sector", "industry", "field", "domain", "area", "type", "category",
    "start", "end", "period", "duration", "current", "previous", "next",
    "first", "second", "third", "main", "major", "minor", "part", "full",
    "assistant", "executive", "senior", "junior", "lead", "head", "chief",
    "officer", "director", "associate", "analyst", "consultant", "intern",
    "trainee", "apprentice", "fresher", "staff", "member", "group", "employee",
    "handling", "monitoring", "controlling", "reporting", "coordinating",
    "planning", "executing", "implementing", "developing", "managing",
    "assisting", "supporting", "providing", "maintaining", "preparing",
    "participating", "creating", "analyzing", "ensuring", "performing",
}

def preprocess_text(text):
    """Cleans text and extracts potential skill tokens (NOUN/PROPN)."""
    text = re.sub(r"\s+", " ", text)
    doc = nlp(text.lower())
    
    tokens = []
    for token in doc:
        # 1. Must be a Noun or Proper Noun
        if token.pos_ not in ["NOUN", "PROPN"]:
            continue
            
        # 2. Skip Stop Words and Short Words
        if token.is_stop or len(token.text) < 3:
            continue
            
        # 3. Skip Blacklisted Terms
        lemma = token.lemma_.lower()
        if lemma in IGNORE_TERMS:
            continue
            
        tokens.append(lemma)

    return tokens


# MAIN TRAINING LOOP
# -------------------------------------------------
def train():
    print(" Starting Offline Training...")
    
    all_tokens = []
    category_counts = {}
    
    # 1. Iterate through Data Directory
    # -------------------------------------------------
    if not os.path.exists(DATA_DIR):
        print(f" Data directory '{DATA_DIR}' not found!")
        exit(1)

    categories = [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]
    print(f" Found {len(categories)} job categories.")

    for category in categories:
        cat_path = os.path.join(DATA_DIR, category)
        files = [f for f in os.listdir(cat_path) if f.endswith(".pdf")]
        
        # Limit to 5 files per category for speed (balance between speed and accuracy)
        files = files[:5]
        category_counts[category] = len(files)
        
        print(f"   - Processing {category}: {len(files)} files...")
        
        for file in files:
            pdf_path = os.path.join(cat_path, file)
            text = extract_text_from_pdf(pdf_path)
            if text:
                tokens = preprocess_text(text)
                all_tokens.extend(tokens)

    # 2. Build Skill Vocabulary
    # -------------------------------------------------
    print(" Building Skill Vocabulary...")
    common_terms = Counter(all_tokens).most_common(MAX_SKILLS)
    skill_vocab = [term for term, _ in common_terms]
    
    # Save to JSON
    vocab_path = os.path.join(ARTIFACTS_DIR, "skill_vocab.json")
    with open(vocab_path, "w") as f:
        json.dump(skill_vocab, f)
    
    print(f" Saved {len(skill_vocab)} skills to '{vocab_path}'")

    # 3. Save TF-IDF Vectorizer (Optional, for hybrid fallback)
    # -------------------------------------------------
    print("Training TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(vocabulary=skill_vocab)
    # We fit it on dummy data just to initialize it with the vocab
    vectorizer.fit(skill_vocab) 
    
    tfidf_path = os.path.join(ARTIFACTS_DIR, "tfidf_model.pkl")
    with open(tfidf_path, "wb") as f:
        pickle.dump(vectorizer, f)
        
    print(f" Saved TF-IDF model to '{tfidf_path}'")
    print("\n Training Complete! You can now run the ATS Engine.")

if __name__ == "__main__":
    train()
