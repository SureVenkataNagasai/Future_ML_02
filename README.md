# Resume Screening System

This is an end-to-end Resume Screening and Candidate Ranking System built using Python and NLP. It processes resumes, extracts skills, and ranks candidates based on their similarity to a given Job Description (JD).

## Features

- **Data Loading**: Loads and processes resume data from CSV.
- **Preprocessing**: Cleans resume text (lowercasing, tokenization, lemmatization, stopword removal).
- **Skill Extraction**: Identifies key technical and soft skills from resumes.
- **Ranking**: Uses TF-IDF and Cosine Similarity to score resumes against a Job Description.
- **Gap Analysis**: Identifies missing skills for each candidate.

## Project Structure

```
.
├── src/
│   ├── preprocessing.py  # Text cleaning and preprocessing
│   ├── skills.py         # Skill extraction logic
│   ├── ranking.py        # TF-IDF and Consine Similarity ranking
│   └── __init__.py
├── main.py               # Main execution script
├── create_notebook.py    # Script to generate the Jupyter Notebook
├── Resume_Screening_System.ipynb # The generated Jupyter Notebook
├── requirements.txt      # Project dependencies
├── inspect_data.py       # Data exploration script
└── README.md             # Project documentation
```

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Download NLTK Data** (First run will handle this automatically):
    - `punkt`
    - `stopwords`
    - `wordnet`

## Usage

### Option 1: Run the converted Jupyter Notebook
Open `Resume_Screening_System.ipynb` in Jupyter Notebook or JupyterLab to interactively run the analysis.

### Option 2: Run the Python Script
Execute the main script:
```bash
python main.py
```
- The script will load the resumes.
- It will prompt you to enter a Job Description (or press Enter to use a default one).
- It will display the top 10 ranked candidates.
- The full ranked list will be saved to `ranked_candidates.csv`.

## Dependencies
- pandas
- numpy
- nltk
- scikit-learn
