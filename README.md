# CoShikshya

## Overview

Co-shikshya is an innovative platform designed to empower educators with a comprehensive suite of AI-powered tools. This platform streamlines various teaching tasks, from lesson planning and assessment generation to creating engaging learning materials.


## Installation

### Prerequisites

- `venv` for managing virtual environments
- `pip` for package management

### Setup Instructions

1. **Clone the repository**:  
   `git clone https://github.com/symbiosissolutions/coshikshya.git`  
   `cd coshikshya`

2. **Create and activate a virtual environment**:  
   `python -m venv .venv`

   On Windows command prompt:  
   `.venv\Scripts\activate.bat`

   On Windows PowerShell:  
   `.venv\Scripts\Activate.ps1`

   On macOS and Linux:  
   `source .venv/bin/activate`


3. **Install dependencies**:  
   `pip install -r requirements.txt`

4. **Set up environment variables**:  
   Create a file called secrets.toml in a folder called .streamlit at the root of your app repo 
   and add the necessary secrets.

   `ANTHROPIC_API_KEY='your-api-key'`

5. **Run the app**:  
   `streamlit run app.py`