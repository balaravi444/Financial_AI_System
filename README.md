# FinanceAI

FinanceAI is a full-stack Indian personal finance assistant that combines a FastAPI backend, an AI-driven advisory engine, and a client-side web dashboard. It is built to help users manage savings, investments, insurance, tax planning, financial health, stock analysis, and fraud detection through conversational guidance.

## Project Summary

FinanceAI includes two primary execution modes:

- **Web application**: `app/main.py` exposes a FastAPI server with static UI assets in `static/` and API endpoints for profile, chat, stock analysis, savings, tax, insurance, goals, portfolio, health score, and fraud protection.
- **CLI mode**: `main.py` launches a terminal-based chat agent powered by the Groq LLM API.

The project stores user state in a local SQLite database at `financeai.db` and persists profiles, conversations, snapshots, goals, and portfolio items.

## Key Features

- Personalized financial advice using a live profile context
- Fraud scan integration for suspicious investment requests
- Stock analysis and quick market price lookup via `yfinance`
- Savings plan generation and insurance need assessment
- Tax optimization support and investment roadmap creation
- Financial health score with actionable breakdowns
- Goals tracking, portfolio management, daily tips, and education modules
- Clean static web dashboard without a separate frontend build step

## Architecture

- `app/main.py` - FastAPI server entrypoint
- `app/agent.py` - AI prompt builder and Groq chat integration
- `app/models.py` - request/response models through Pydantic
- `app/db_manager.py` - SQLite schema and persistence operations
- `app/database.py` - lightweight DB access wrapper
- `app/stock_routes.py` - API routes for analysis and utility actions
- `static/` - browser UI including `index.html`, `app.js`, and `styles.css`
- `requirements.txt` - required Python packages

## Required Environment

- Python 3.11+ recommended
- `GROQ_API_KEY` environment variable for Groq API access
- Optional `.env` file support via `python-dotenv`

Example `.env`:

```
GROQ_API_KEY=your_groq_api_key_here
```

## Setup and Local Run

From the project root:

```powershell
python -m pip install -r requirements.txt
```

### Run the web application

```powershell
python -m uvicorn app.main:app --reload
```

Then open the browser at:

```
http://127.0.0.1:8000/
```

### Run the CLI agent

```powershell
python main.py
```

This command starts a simple terminal chat interface powered by the same Groq-backed AI model.

## API Endpoints

The FastAPI backend provides the following endpoints:

- `GET /` - Serve the UI at `static/index.html`
- `POST /profile` - Save or update user profile data
- `GET /profile/{session_id}` - Get saved profile by session
- `POST /chat` - AI chat interaction with profile-aware context
- `POST /analyze-stock` - Perform stock analysis + AI commentary
- `GET /quick-price/{symbol}` - Fetch live price for market symbols
- `POST /savings-analysis` - Savings plan report and AI summary
- `POST /tax-analysis` - Tax savings guidance
- `POST /investment-roadmap` - Personalized roadmap generation
- `POST /insurance-analysis` - Insurance need assessment
- `POST /spending-leaks` - Detect spending leaks and alerts
- `POST /learn` - Education content based on topic
- `POST /daily-tips` - Daily finance tip + AI commentary
- `POST /health-score` - Financial health score with snapshot

## Database

The app automatically initializes a SQLite database named `financeai.db` when the server starts. The schema includes tables for:

- `profiles`
- `conversations`
- `financial_snapshots`
- `goals`
- `portfolio`

The database is created by `app/db_manager.py` using `init_db()`.

## Deployment Guidance

This project can be hosted on any Python-capable platform that supports FastAPI, such as:

- Railway
- Render
- Fly.io
- Azure App Service
- AWS Elastic Beanstalk

Recommended deployment steps:

1. Ensure the environment variable `GROQ_API_KEY` is configured in the hosting platform.
2. Install dependencies from `requirements.txt`.
3. Start the app with `uvicorn app.main:app --host 0.0.0.0 --port 8000`.
4. Expose port `8000` or the platform-specific runtime port.

For a live demo experience, make sure the static UI is available and the API can be reached from the browser.

## Pushing to GitHub

After verifying your changes locally, push to your repository:

```powershell
git add .
git commit -m "Add README and document FinanceAI"
git push origin main
```

If your branch is different, replace `main` with the active branch name.

## Troubleshooting

- If the app fails to start, confirm `GROQ_API_KEY` is set and valid.
- If the web UI does not load, verify `uvicorn` is running and open `http://127.0.0.1:8000/`.
- If the database cannot connect, confirm the process has write permission in the project folder.

## Notes for Improvements

The current implementation is ready for production polishing, including:

- stronger input validation on the frontend and backend
- rate limiting or API key protection for public hosting
- migrating SQLite to a managed database for scale
- adding formal unit tests and CI checks
- securing `/static` and production logging

## Contribution

1. Fork the repository.
2. Create a feature branch.
3. Add or update code and tests.
4. Commit with clear messages.
5. Open a pull request for review.

---

FinanceAI is designed to be a fast, practical smart finance assistant for Indian users with a modern API-driven frontend and AI-backed advisory capabilities.