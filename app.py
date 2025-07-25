import streamlit as st
from main_app import MainApplication
import sys
import os

# Add the directory containing your modules to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# If 'pages' is a subdirectory, also add it to the path
pages_dir = os.path.join(current_dir, 'pages')
if pages_dir not in sys.path:
    sys.path.insert(0, pages_dir)

if __name__ == "__main__":
    app = MainApplication()
    app.run()