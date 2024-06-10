# EIA Report AI Oil Analyst

## Overview
The EIA Oil Report AI Oil Analyser is a Streamlit application that analyses 
the weekly EIA (Energy Information Administration) from investing api report 
[investing.com](https://www.investing.com/earnings-calendar/) 
using OpenAI's language model. 
The app gets the EIA report, performs AI-based analysis to rate the report, 
and displays the results in an interactive and visually appealing manner 
also plots [tradingview(https://www.tradingview.com/) widget for USOIL price. 

- This project happened with the scope to gain hands-on experience after a quick training in langchain_openai.
Don't take that as trade ideals, as it has not been evaluated or optimised further, may try more complex and more expensive models architectures.

## Features
- **EIA Report:** Gets the weekly EIA report data from investing.com.
- **AI Analysis:** Uses OpenAI's language model to analyze the report and provide a rating.
- **Interactive Visualization:** Displays the report data, AI analysis, and a rating bar in a user-friendly interface.


## Screenshot
![EIA Report AI Analyzer](html/screenshot.png)

## Project Structure
    
    LLM-eia-weekly-report/
    ├── config/
    │ └── config.yaml
    ├── html/
    │ ├── rating_bar.html
    │ ├── screenshot.png
    │ └── tradeview.html
    ├── src/
    │ ├── init.py
    │ ├── config_loader.py
    │ ├── economic_calendar.py
    │ ├── openai_analysis.py
    │ ├── setup.py
    │ ├── utils.py
    │ └── run_analysis.py
    ├── tests/
    │ ├── init.py
    │ ├── test_run_analysis.py
    ├── .env
    ├── .gitignore
    ├── README.md
    ├── requirements.txt
    └── streamlit_app.py

## Setup

### Prerequisites
- Python 3.9 or higher
- Virtual environment tool (venv, conda, etc.)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/LLM-eia-weekly-report.git
   cd LLM-eia-weekly-report
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
   ```
4. **Set up environment variables:**
    
    - Create a .env file in the root directory.
    - Add your OpenAI API key:
    - OPENAI_API_KEY=your_openai_api_key

### Usage
Run the Streamlit app:
   ```bash
  streamlit run streamlit_app.py
   ```

## License
Under the MIT License. See the LICENSE file for details.