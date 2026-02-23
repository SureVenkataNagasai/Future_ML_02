
import re

# A comprehensive list of skills for demonstration. 
# In a real-world scenario, this would be more extensive or fetched from a skills database.
TECH_SKILLS = {
    'python', 'java', 'c++', 'javascript', 'html', 'css', 'sql', 'nosql', 'mongodb', 
    'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'springboot',
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github', 
    'machine learning', 'deep learning', 'nlp', 'data analysis', 'pandas', 'numpy', 
    'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'statistics', 'mathematics',
    'excel', 'power bi', 'tableau', 'spark', 'hadoop', 'flutter', 'swift', 'kotlin',
    'android', 'ios', 'linux', 'bash', 'shell scripting'
}

SOFT_SKILLS = {
    'communication', 'teamwork', 'leadership', 'problem solving', 'critical thinking',
    'time management', 'adaptability', 'creativity', 'attention to detail', 'project management',
    'agile', 'scrum', 'collaboration', 'presentation', 'negotiation'
}

ALL_SKILLS = TECH_SKILLS.union(SOFT_SKILLS)

class SkillExtractor:
    def __init__(self, skills_list=None):
        self.skills = skills_list if skills_list else ALL_SKILLS

    def extract_skills(self, text):
        """
        Extracts skills found in the given text based on pre-defined skill list.
        """
        if not text:
            return []
        
        found_skills = set()
        text_lower = text.lower()
        
        # Simple extraction based on word boundaries
        # This handles multi-word skills incorrectly if not careful, 
        # but for simplicity we match exact phrases or words.
        for skill in self.skills:
            # Create regex pattern for whole word match
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)
                
        return list(found_skills)

    def extract_skills_from_job_description(self, jd_text):
        """
        Same as extract_skills, meant for JD.
        """
        return self.extract_skills(jd_text)
