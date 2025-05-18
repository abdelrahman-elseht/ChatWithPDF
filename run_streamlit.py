import streamlit.web.cli as stcli
import os
import sys

if __name__ == '__main__':
    # Add the current directory (project root) to sys.path
    # to ensure the 'app' package can be found.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Define the path to your main Streamlit app script
    # This assumes your main.py is at app/main.py
    app_script_path = os.path.join("src", "main.py")
    
    # Construct the arguments for Streamlit CLI
    # This is equivalent to `streamlit run app/main.py`
    sys.argv = [
        "streamlit",  # The program name, as Python scripts often expect
        "run",
        app_script_path,
        # Add any other default streamlit args you want, e.g.
        # "--server.port", "8501"
    ]
    # Use Streamlit's internal CLI runner
    stcli.main()