# Good First Issue

A simple tool to help developers find beginner-friendly GitHub repositories to contribute to.

## What it does

- Checks if a repo has essential files (`README.md`, `CONTRIBUTING.md`)
- Shows count of "Good First Issues" within configurable time filters
- Checks if the repo is actively maintained
- Shows basic repo info (stars, forks, language)

## How to use it

### Run locally
```bash
git clone https://github.com/yourusername/github-api-etl
cd github-api-etl
pip install -r requirements.txt
streamlit run app.py
```

### GitHub Token (optional)
The app uses GitHub's public API with standard rate limits (60 requests/hour). For higher limits, add your GitHub token:

1. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and add your GitHub token:
   ```
   GITHUB_TOKEN=your_token_here
   ```

## Tech Stack

- Python
- Streamlit
- GitHub REST API
- pandas for data display

---
