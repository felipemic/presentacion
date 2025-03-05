# CV Analyzer

An automated system for analyzing candidate resumes/CVs and evaluating them against job requirements.

## Features

- Upload CV documents in PDF format
- Specify job requirements through a text interface
- Generate detailed analysis of how the candidate matches the requirements
- Provide translation capabilities for non-Spanish documents
- Deliver a final evaluation of candidate suitability

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/cv-analyzer.git
cd cv-analyzer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy the `.env` file and add your API keys and configuration
   - Make sure to set your OpenAI API key

## Usage

1. Start the application:
```bash
cd src
streamlit run main.py
```

2. Open your browser at `http://localhost:8501`

3. Upload a CV, specify job requirements, and click "Analyze" to get results

## Project Structure

```
cv_analyzer/
├── .env                  # Environment variables
├── README.md             # Project documentation
├── requirements.txt      # Dependencies list
├── assets/
│   └── cyborg.png        # Logo image
├── src/
│   ├── __init__.py
│   ├── main.py           # Main application entry point
│   ├── config.py         # Configuration and constants
│   ├── agents.py         # CrewAI agents definition
│   ├── tasks.py          # CrewAI tasks definition
│   ├── ui.py             # Streamlit UI components
│   └── utils.py          # Helper functions
└── tests/                # Test files
    └── __init__.py
```

## Development

- The application uses [Streamlit](https://streamlit.io/) for the user interface
- It leverages [CrewAI](https://github.com/joaomdmoura/crewAI) for agent orchestration
- OpenAI models are used through LangChain for AI processing

## License

[Specify your license here]

## Contributors

[Your name/organization]
