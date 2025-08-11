# FastAPI Backend Structure 

backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # Database connection & session
│   ├── config.py            # Settings/environment config
│   │
│   ├── models/              # SQLAlchemy models (database tables)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── song.py
│   │   ├── album.py
│   │   ├── artist.py
│   │   └── review.py
│   │
│   ├── schemas/             # Pydantic models (API input/output)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── song.py
│   │   └── review.py
│   │
│   ├── routers/             # API endpoints/routes
│   │   ├── __init__.py
│   │   ├── auth.py          # Login, tokens
│   │   ├── songs.py         # Song search, details
│   │   ├── albums.py        # Album endpoints
│   │   ├── artists.py       # Artist endpoints
│   │   └── reviews.py       # Review submission
│   │
│   └── utils/               # Helper functions
│       ├── __init__.py
│       └── auth.py          # Password hashing, JWT
│
├── alembic/                 # Database migrations (auto-generated)
├── alembic.ini              # Alembic config
├── .env                     # Environment variables
├── requirements.txt         # Dependencies
└── venv/                    # Virtual environment (gitignored)