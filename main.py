
import subprocess
import os
import sys

def main():
    print("Launching Candidate Shortlisting System Web App...")
    
    # Run the streamlit app
    # Using sys.executable to ensure we use the same python interpreter
    cmd = ["streamlit", "run", "app.py"]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nStopping application...")
    except Exception as e:
        print(f"Error launching app: {e}")

if __name__ == "__main__":
    main()
