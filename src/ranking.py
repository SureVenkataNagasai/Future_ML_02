
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

class ResumeRanker:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        
    def score_resumes(self, resumes, job_description):
        """
        Calculates similarity scores using TF-IDF and Cosine Similarity.
        
        Args:
        - resumes: List of preprocessed resume strings.
        - job_description: Preprocessed job description string.
        """
        if isinstance(resumes, pd.Series):
            resumes = resumes.tolist()
        elif not isinstance(resumes, list):
             # Ensure it's a list if it's some other iterable
            resumes = list(resumes)

        if not resumes:
            return []
            
        # If JD is empty after cleaning, return 0 scores for all
        if not job_description:
            return [0.0] * len(resumes)
            
        # Combine JD and resumes into one list for vectorization
        corpus = [job_description] + resumes
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
        except ValueError:
            # Handle cases where vocabulary is empty (e.g. only stopwords)
            return [0.0] * len(resumes)
        
        # JD vector is the first item
        jd_vector = tfidf_matrix[0]
        
        # Resume vectors are the rest
        resume_vectors = tfidf_matrix[1:]
        
        # Compute cosine similarity
        similarities = cosine_similarity(jd_vector, resume_vectors)
        
        # Flatten to 1D array
        sim_scores = similarities.flatten()
        
        return sim_scores
