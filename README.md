# Dataset
GMDCSA-24 Fall Datase: https://github.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos
https://figshare.com/articles/dataset/UMA_ADL_FALL_Dataset_zip/4214283/8

# Structure
FallGuard/
├── backend/                # Server-side logic & AI processing
│   ├── core/               # Central coordination logic
│   │   └── vision_pipeline.py  # Orchestrates AI, privacy, and data flow
│   ├── services/           # External integrations & Heavy logic
│   │   ├── pose_estimator.py   # MediaPipe/AI Pose Estimation logic
│   │   └── database_service.py # Supabase connection & CRUD operations
│   ├── utils/              # Helper functions & secondary tools
│   │   └── anonymizer.py       # Face blurring & Privacy compliance
│   ├── models/             # Data structures & Type definitions
│   └── main.py             # FastAPI entry point & API routes
│
├── frontend/               # User Interface (React/Next.js)
│   ├── src/
│   │   ├── components/     # Reusable UI elements (VideoFeed, Alerts)
│   │   ├── hooks/          # API fetching & WebSocket listeners
│   │   ├── pages/          # Main views (Dashboard, History)
│   │   └── assets/         # Static files (Icons, Global CSS)
│   └── public/             # Browser resources
│
├── data/                   # Local datasets & Test resources
│            
├── .env                    # Environment variables (Supabase Keys)
├── .gitignore              # Files ignored by Git (venv, .env)