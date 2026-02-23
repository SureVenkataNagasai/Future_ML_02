
import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# End-to-End Resume Screening and Candidate Ranking System\n",
    "\n",
    "## Project Overview\n",
    "This project implements an automated resume screening system using NLP techniques. It ranks candidates based on the relevance of their resumes to a given Job Description (JD).\n",
    "\n",
    "### Pipeline Steps:\n",
    "1. **Data Loading**: Load the resume dataset.\n",
    "2. **Preprocessing**: Clean text (lowercase, remove stopwords, lemmatization).\n",
    "3. **Feature Engineering**: Convert text to numerical vectors using TF-IDF.\n",
    "4. **Similarity Calculation**: Compute Cosine Similarity between resumes and JD.\n",
    "5. **Ranking**: Sort candidates by relevance score."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "from src.preprocessing import Preprocessor\n",
    "from src.skills import SkillExtractor\n",
    "from src.ranking import ResumeRanker\n",
    "\n",
    "%matplotlib inline\n",
    "%load_ext autoreload\n",
    "%autoreload 2"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Load Data\n",
    "Load the resume dataset from 'Resume/Resume.csv'."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "data_path = 'Resume/Resume.csv'\n",
    "df = pd.read_csv(data_path)\n",
    "print(f\"Dataset Shape: {df.shape}\")\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Preprocessing\n",
    "Clean the resume text to remove noise and standardize it for analysis."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "preprocessor = Preprocessor()\n",
    "df['Cleaned_Resume'] = df['Resume_str'].apply(preprocessor.clean_text)\n",
    "df[['Resume_str', 'Cleaned_Resume']].head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Skill Extraction\n",
    "Extract key skills from the resumes to aid in analysis."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "extractor = SkillExtractor()\n",
    "df['Skills'] = df['Cleaned_Resume'].apply(extractor.extract_skills)\n",
    "df[['Cleaned_Resume', 'Skills']].head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Define Job Description\n",
    "Enter the job description for the role you are hiring for."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "job_description = \"\"\"\n",
    "We are looking for a Data Scientist with strong Python and Machine Learning skills.\n",
    "Experience with Deep Learning frameworks like TensorFlow or PyTorch is required.\n",
    "Knowledge of SQL and Big Data tools like Spark is a plus.\n",
    "\"\"\"\n",
    "\n",
    "# Clean the JD\n",
    "cleaned_jd = preprocessor.clean_text(job_description)\n",
    "jd_skills = extractor.extract_skills_from_job_description(cleaned_jd)\n",
    "print(f\"Extracted Skills from JD: {jd_skills}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Ranking Candidates\n",
    "Compute similarity scores using TF-IDF and Cosine Similarity."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "ranker = ResumeRanker()\n",
    "scores = ranker.score_resumes(df['Cleaned_Resume'], cleaned_jd)\n",
    "df['Similarity_Score'] = scores"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. Results and Analysis\n",
    "Display top ranked candidates and analyze missing skills."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Identify missing skills\n",
    "def get_missing_skills(candidate_skills, required_skills):\n",
    "    return list(set(required_skills) - set(candidate_skills))\n",
    "\n",
    "df['Missing_Skills'] = df['Skills'].apply(lambda x: get_missing_skills(x, jd_skills))\n",
    "\n",
    "ranked_df = df.sort_values(by='Similarity_Score', ascending=False)\n",
    "print(\"Top 10 Candidates:\")\n",
    "ranked_df[['ID', 'Category', 'Similarity_Score', 'Skills', 'Missing_Skills']].head(10)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

with open('Resume_Screening_System.ipynb', 'w') as f:
    json.dump(notebook_content, f, indent=4)
