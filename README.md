# Lakshya — AI Money Mentor for Indian Investors

> **"Your money, finally clear."**  
> Upload your CAMS statement, get a portfolio X-Ray, check your financial health, and find out exactly when you can retire — all powered by AI.

## Demo

> 🔗 **[https://lakshya-jade.vercel.app/](https://lakshya-jade.vercel.app/)**

<!-- Replace YOUR_DEMO_LINK_HERE with your Render / Vercel / Railway URL -->

---

## What Lakshya Does

| Feature | Description |
|---|---|
| **Portfolio X-Ray** | Upload your CAMS PDF — detect fund overlap, fee leaks, and get rebalancing suggestions |
| **Money Health Score** | Get a 0–100 score across savings rate, emergency fund, debt, and investment behaviour |
| **FIRE Planner** | Monte Carlo simulation across 10,000 scenarios — find your exact retirement probability |
| **AI Money Mentor** | Chat with Lakshya in plain English — powered by Google Gemini 2.0 Flash |

---

## Architecture
```
┌─────────────────────────────────┐
│     Frontend  (HTML / JS)       │
│  Portfolio · Health · FIRE      │
│  AI Chat · Dashboard            │
└──────────────┬──────────────────┘
               │ REST / JSON
               ▼
┌─────────────────────────────────┐
│     FastAPI Backend (Python)    │
│                                 │
│  ┌──────────┐  ┌─────────────┐  │
│  │ Portfolio│  │   Health    │  │
│  │  X-Ray   │  │   Score     │  │
│  └──────────┘  └─────────────┘  │
│  ┌──────────┐  ┌─────────────┐  │
│  │  FIRE    │  │  AI Chat    │  │
│  │ Planner  │  │  (Gemini)   │  │
│  └──────────┘  └─────────────┘  │
└─────────────────────────────────┘
```

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI, Python 3.11 |
| **AI Engine** | Google Gemini 2.0 Flash |
| **PDF Parsing** | LlamaCloud / LlamaParse |
| **Financial Math** | NumPy, SciPy, Pandas, pyxirr |
| **Frontend** | Vanilla JS, HTML5 Canvas |
| **Infrastructure** | Docker, Render |

---

## Quick Start

### Prerequisites

- Python 3.9+
- API keys: `GEMINI_API_KEY`, `OPENAI_API_KEY`, `LLAMA_CLOUD_API_KEY`

### 1. Clone the repo
```bash
git clone https://github.com/sanvviratthore/lakshya.git
cd lakshya
```

### 2. Set up environment variables

Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
LLAMA_CLOUD_API_KEY=your_llama_cloud_api_key_here
```

> ⚠️ Never commit your `.env` file. It is already in `.gitignore`.

### 3. Run the backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

Backend runs at `http://localhost:8000`  
API docs at `http://localhost:8000/docs`

### 4. Open the frontend

Just open `frontend/index.html` in your browser — no build step needed.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/chat` | AI money mentor chat (Gemini) |
| `POST` | `/api/v1/analyze-portfolio` | Upload CAMS PDF, get fund analysis |
| `POST` | `/api/v1/fire-analysis` | Run Monte Carlo FIRE simulation |
| `POST` | `/api/v1/comprehensive-health` | Submit financials, get health score |
| `POST` | `/api/v1/auth/login` | User authentication |
| `GET`  | `/` | Health check |

---

## AI Agents

### PortfolioXRay
Parses CAMS statements via LlamaParse, calculates XIRR, detects fund overlap across holdings, flags regular plans vs direct plans, and estimates annual fee savings.

### HealthScore
Scores financial health across 6 dimensions: savings rate, emergency fund coverage, debt-to-income ratio, tax efficiency, insurance adequacy, and retirement readiness.

### FIREPlanner
Runs 10,000 Monte Carlo scenarios using historical Indian market volatility. Outputs probability of reaching your corpus by target date, with median / optimistic / conservative trajectories.

### Lakshya Mentor
Context-aware conversational AI built on Gemini 2.0 Flash with a system prompt tuned for Indian personal finance — SIPs, 80C, NPS, ELSS, term insurance, and more.

---

## Project Structure
```
lakshya/
├── backend/
│   ├── main.py                  # FastAPI app + CORS + keep-alive
│   ├── api/
│   │   └── routes.py            # All API endpoints
│   ├── agents/
│   │   ├── portfolio_xray.py    # Overlap + fee leak detection
│   │   ├── health_score.py      # Financial health scoring
│   │   └── fire_planner.py      # Monte Carlo simulation
│   ├── core/
│   │   ├── parser.py            # CAMS PDF parser (LlamaParse)
│   │   ├── math_utils.py        # XIRR, compounding helpers
│   │   ├── ai_engine.py         # Gemini integration
│   │   └── config.py            # Env var loader + validation
│   └── requirements.txt
├── frontend/
│   └── index.html               # Single-file frontend
├── .env                         # Local secrets (never commit)
├── .gitignore
└── README.md
```

---

## Roadmap

- [ ] PostgreSQL for persistent user portfolios
- [ ] JWT-based multi-user authentication
- [ ] Direct MF API integration (MFU / BSE StarMF)
- [ ] Tax optimisation recommendations (LTCG / STCG / 80C)
- [ ] Mobile app (React Native)
- [ ] WhatsApp bot integration

---

## Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

---

## 📄 License

MIT © [Sanvi Ratthore](https://github.com/sanvviratthore)

---

<div align="center">
  Built for Indian investors 🇮🇳 · Powered by Gemini AI 🤖 · Made for financial independence 🔥
</div>
