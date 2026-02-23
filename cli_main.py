
import pandas as pd
import numpy as np
from src.preprocessing import Preprocessor
from src.skills import SkillExtractor
from src.ranking import ResumeRanker

def main():
    try:
        # Load Dataset
        print("Loading dataset...")
        data_path = r'c:\Users\Admin\OneDrive\Desktop\Task3\Resume\Resume.csv'
        df = pd.read_csv(data_path)
        
        # Limit dataset for faster execution during development/demo (optional)
        # df = df.head(100) 
        
        if 'Resume_str' not in df.columns:
            print("Error: 'Resume_str' column not found in dataset")
            return

        print(f"Loaded {len(df)} resumes.")
        
        # Preprocess Resumes
        print("Preprocessing resumes...")
        preprocessor = Preprocessor()
        df['Cleaned_Resume'] = df['Resume_str'].apply(preprocessor.clean_text)
        
        # Skill Extraction
        print("Extracting skills from resumes...")
        extractor = SkillExtractor()
        df['Extracted_Skills'] = df['Resume_str'].apply(extractor.extract_skills)

        # Prompt for Job Description
        print("\n--- Enter Job Description ---")
        # For non-interactive environments, use a default JD
        default_jd = """
        We are looking for a skilled Data Scientist with experience in Python, Machine Learning, and SQL. 
        Knowledge of AWS and Deep Learning frameworks like TensorFlow or PyTorch is a plus.
        The candidate should have strong communication skills and be a team player.
        """
        
        try:
            print("Enter Job Description (Press Enter to use default JD):")
            user_input = input()
            job_description = user_input if user_input.strip() else default_jd
        except EOFError:
             job_description = default_jd

        print(f"\nUsing Job Description:\n{job_description}\n")
        
        # Process Job Description
        cleaned_jd = preprocessor.clean_text(job_description)
        jd_skills = set(extractor.extract_skills(job_description))
        
        print(f"Extracted Skills from JD: {jd_skills}")
        
        # Ranking
        print("Ranking candidates...")
        ranker = ResumeRanker()
        similarity_scores = ranker.score_resumes(df['Cleaned_Resume'].tolist(), cleaned_jd)
        
        df['Similarity_Score'] = similarity_scores
        
        # Sort by similarity score
        ranked_df = df.sort_values(by='Similarity_Score', ascending=False)
        
        # Gap Analysis
        def identify_missing_skills(candidate_skills, required_skills):
            candidate_skills_set = set(candidate_skills)
            missing = required_skills - candidate_skills_set
            return list(missing)

        ranked_df['Missing_Skills'] = ranked_df['Extracted_Skills'].apply(lambda x: identify_missing_skills(x, jd_skills))
        
        # Display Top 10 Candidates
        top_candidates = ranked_df[['ID', 'Category', 'Similarity_Score', 'Extracted_Skills', 'Missing_Skills']].head(10)
        
        print("\n--- Top 10 Ranked Candidates ---")
        print(top_candidates.to_string(index=False))
        
        # Save results
        ranked_df.to_csv('ranked_candidates.csv', index=False)
        print("\nRanked list saved to 'ranked_candidates.csv'.")
        
    except FileNotFoundError:
        print(f"Error: Dataset not found at {data_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
