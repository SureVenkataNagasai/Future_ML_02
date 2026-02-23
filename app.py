
import streamlit as st
import pandas as pd
from src.preprocessing import Preprocessor
from src.skills import SkillExtractor
from src.ranking import ResumeRanker

# Page Configuration
st.set_page_config(
    page_title="Candidate Shortlisting System",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        font-weight: bold;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Classes (Cached)
@st.cache_resource
def load_resources():
    preprocessor = Preprocessor()
    extractor = SkillExtractor()
    ranker = ResumeRanker()
    return preprocessor, extractor, ranker

preprocessor, extractor, ranker = load_resources()

# Load Dataset (Cached)
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Resume/Resume.csv')
        # Pre-process resumes once
        if 'Cleaned_Resume' not in df.columns:
            df['Cleaned_Resume'] = df['Resume_str'].apply(preprocessor.clean_text)
            df['Extracted_Skills'] = df['Resume_str'].apply(extractor.extract_skills)
        return df
    except FileNotFoundError:
        return None

def process_single_role(role_title, job_description, df, top_n, selected_category):
    # Filter by category if selected
    filtered_df = df.copy()
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]
    
    if filtered_df.empty:
        st.warning(f"No candidates found in category: {selected_category}")
        return

    # Process JD
    cleaned_jd = preprocessor.clean_text(job_description)
    jd_skills = set(extractor.extract_skills(job_description))

    # Display JD Analysis
    st.info(f"**Required Skills extracted for '{role_title}':** {', '.join(jd_skills) if jd_skills else 'No specific skills detected'}")
    
    # Rank Candidates
    scores = ranker.score_resumes(filtered_df['Cleaned_Resume'].tolist(), cleaned_jd)
    filtered_df['Similarity_Score'] = scores
    
    # Sort
    ranked_df = filtered_df.sort_values(by='Similarity_Score', ascending=False).head(top_n)

    # Identify Missing Skills
    def get_missing(candidate_skills):
        return list(jd_skills - set(candidate_skills))

    ranked_df['Missing_Skills'] = ranked_df['Extracted_Skills'].apply(get_missing)
    
    st.markdown(f"### 🏆 Top {top_n} Candidates for {role_title}")
    
    # Display Results
    for i, (index, row) in enumerate(ranked_df.iterrows()):
        score = row['Similarity_Score']
        skills = row['Extracted_Skills']
        missing = row['Missing_Skills']
        
        with st.expander(f"#{i+1} | ID: {row['ID']} | Match: {score*100:.1f}%"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Category:** {row['Category']}")
                st.markdown(f"**✅ Matched Skills:**")
                st.write(", ".join(skills))
                
            with c2:
                    st.markdown(f"**⚠️ Missing Skills:**")
                    if missing:
                        st.error(", ".join(missing))
                    else:
                        st.success("All required skills found!")
            
            # Show resume preview (snippet)
            st.divider()
            st.caption("Resume Snippet:")
            st.text(row['Resume_str'][:500] + "...")

def main():
    st.title("📄 Candidate Shortlisting System")
    st.markdown("### 🚀 Shortlist candidates for **multiple roles** simultaneously.")

    # Initialize session state for multiple roles
    if 'roles' not in st.session_state:
        st.session_state.roles = [{'title': 'Role 1', 'description': ''}]

    def add_role():
        st.session_state.roles.append({'title': f'Role {len(st.session_state.roles) + 1}', 'description': ''})

    def remove_role(index):
        if len(st.session_state.roles) > 1:
            st.session_state.roles.pop(index)

    df = load_data()
    if df is None:
        st.error("Dataset not found! Please ensure 'Resume/Resume.csv' exists.")
        return

    # Sidebar Options
    st.sidebar.header("Global Settings")
    categories = ['All'] + sorted(df['Category'].unique().tolist())
    selected_category = st.sidebar.selectbox("Filter by Category (Applied to all)", categories)
    top_n = st.sidebar.slider("Candidates per Role", 5, 50, 10)

    # Role Input Section
    st.subheader("1. Define Roles")
    
    for i, role in enumerate(st.session_state.roles):
        # Using a container for each role input
        with st.container():
            col1, col2, col3 = st.columns([2, 4, 0.5])
            with col1:
                role['title'] = st.text_input(f"Role Title", value=role['title'], key=f"title_{i}", placeholder="e.g. Data Scientist")
            with col2:
                role['description'] = st.text_area(f"Job Description", value=role['description'], height=100, key=f"desc_{i}", placeholder="Paste job description here...")
            with col3:
                # Spacer to align button
                st.write("")
                st.write("")
                if len(st.session_state.roles) > 1:
                    if st.button("🗑️", key=f"remove_{i}", help="Remove this role"):
                        remove_role(i)
                        st.rerun()
            st.divider()

    st.button("➕ Add Another Role", on_click=add_role)

    # Analysis Section
    st.subheader("2. Analysis")
    analyze_btn = st.button("🔍 Shortlist Candidates for ALL Roles", type="primary")

    if analyze_btn:
        # Filter out empty roles
        valid_roles = [r for r in st.session_state.roles if r['description'].strip()]
        
        if not valid_roles:
            st.warning("⚠️ Please enter at least one job description.")
            return

        with st.spinner('Analyzing resumes for all roles...'):
            # Use tabs to display results for each role
            role_titles = [r['title'] for r in valid_roles]
            tabs = st.tabs(role_titles)
            
            for tab, role in zip(tabs, valid_roles):
                with tab:
                    process_single_role(role['title'], role['description'], df, top_n, selected_category)

if __name__ == "__main__":
    main()
