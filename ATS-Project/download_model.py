import os
from sentence_transformers import SentenceTransformer

def download_model():
    print(" Downloading SBERT model 'all-MiniLM-L6-v2' to cache...")
    # This will download the model to the default torch cache directory
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print(" Model downloaded successfully.")

if __name__ == "__main__":
    download_model()
