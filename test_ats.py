import os
import json
from ats_engine import rank_uploaded_resumes


DATA_FILE = "data/ACCOUNTANT/10554236.pdf" 
if not os.path.exists(DATA_FILE):
    # Search for any pdf
    for root, dirs, files in os.walk("data"):
        for file in files:
            if file.endswith(".pdf"):
                DATA_FILE = os.path.join(root, file)
                break
        if DATA_FILE != "data/ACCOUNTANT/10554236.pdf": break

print(f" Testing ATS Engine with file: {DATA_FILE}")

JD_TEXT = """
Looking for a Senior Accountant with experience in Financial Analysis, 
Auditing, and Tax filing. Must know Excel and SAP.
"""

try:
    results = rank_uploaded_resumes([DATA_FILE], JD_TEXT)
    
    print("\n RANKING SUCCESSFUL!")
    print(f"   Score: {results[0]['score']}%")
    print(f"   Matched Skills: {results[0]['matched']}")
    print(f"   Missing Skills: {results[0]['missing']}")
    
    if results[0]['score'] > 0:
        print("\n Verification Passed: Engine produced a non-zero score.")
    else:
        print("\n Warning: Score is 0. Check if skills match.")
        
except Exception as e:
    print(f"\n Verification Failed: {e}")
