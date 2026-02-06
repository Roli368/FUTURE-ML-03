import os
import json
import pdfplumber
import spacy
import numpy as np
from sentence_transformers import SentenceTransformer, util

# -------------------------------------------------
# CONFIG & GLOBALS

ARTIFACTS_DIR = "artifacts"
SKILL_FILE = os.path.join(ARTIFACTS_DIR, "skill_vocab.json")

# Load NLP for preprocessing 
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser", "tagger"])

# Load SBERT Model (Lazy loading recommended, but here we load globally)
print("⏳ Loading SBERT Model...")
MODEL = SentenceTransformer('all-MiniLM-L6-v2')

# Load Skill Cache
SKILL_VOCAB = []
if os.path.exists(SKILL_FILE):
    with open(SKILL_FILE, "r") as f:
        SKILL_VOCAB = set(json.load(f))
else:
    print("⚠ WARNING: Skill vocabulary not found. Run trainer.py first.")

# -------------------------------------------------
# HELPERS

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:2]: 
                t = page.extract_text()
                if t: text += t + " "
    except:
        return ""
    return text.strip()

def preprocess_text(text):
    """Normalize text for consistent matching."""
    doc = nlp(text.lower())
    tokens = [t.lemma_ for t in doc if t.is_alpha and not t.is_stop]
    return " ".join(tokens)

def extract_skills(text, vocab):
    """Finds overlap between text and skill vocabulary."""
  
    text_tokens = set(text.split())
    
   
    
    matched = {skill for skill in vocab if skill in text_tokens}
    return list(matched)

# -------------------------------------------------
# CORE ENGINE

def rank_uploaded_resumes(uploaded_files, jd_text):
    """
    Ranks resumes using SBERT (Semantic) + Keyword Matching (Skills).
    """
    results = []
    
    # 1. Preprocess JD
    jd_clean = preprocess_text(jd_text)
    jd_emb = MODEL.encode(jd_clean, convert_to_tensor=True)
    
    # Extract expected skills from JD (using the same vocab)
    jd_skills = set(extract_skills(jd_clean, SKILL_VOCAB))
    
    # 2. Process Resume
    for pdf_path in uploaded_files:
        filename = os.path.basename(pdf_path)
        
        #  Extract Text
        content = extract_text_from_pdf(pdf_path)
        if len(content) < 50:
            continue 
            
        content_clean = preprocess_text(content)
        
        #  Semantic Similarity 
        resume_emb = MODEL.encode(content_clean, convert_to_tensor=True)
        semantic_score = util.cos_sim(jd_emb, resume_emb).item()
        
        #  Skill Match
        resume_skills = set(extract_skills(content_clean, SKILL_VOCAB))
        
        matched_skills = resume_skills & jd_skills
        missing_skills = jd_skills - resume_skills
        
        # Skill Score: % of JD skills found in resume
        if len(jd_skills) > 0:
            skill_score = len(matched_skills) / len(jd_skills)
        else:
            skill_score = 0.5 
            
       
        final_score = (0.6 * semantic_score) + (0.4 * skill_score)
        final_score = round(final_score * 100, 2)
        
        results.append({
            "resume": filename,
            "score": final_score,
            "matched": list(matched_skills),
            "missing": list(missing_skills),
            "debug_semantic": round(semantic_score, 2),
            "debug_skill": round(skill_score, 2)
        })

   
    return sorted(results, key=lambda x: x["score"], reverse=True)
