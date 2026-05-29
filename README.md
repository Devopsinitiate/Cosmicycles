# Cosmic Cycles (Cycles of Life Mastery)

A Django web application that helps users understand the different cycles of their lives, based on the book *"Self Mastery and Fate with the Cycles of Life"* by H. Spencer Lewis. Calculates and visualizes daily, yearly, human life, soul, business, health, and reincarnation cycles with personalized insights for each period.

## Features

- **User Authentication** — signup with email verification, login/logout, profile management
- **Email Verification** — verification link sent on signup; email configurable via env vars
- **Personalized Cycles** — calculated from user's date of birth and business start dates
- **Dashboard** — authenticated dashboard showing all active cycles at a glance
- **Daily Cycle (Public)** — anonymous users see the current daily cycle on the landing page
- **Business Cycles** — users can register businesses and track their cycles
- **Cycle Education Hub** — detailed descriptions, glossary, and quiz questions per cycle period
- **Lesson Progress** — tracks completed lessons and quiz scores per period
- **Journal** — daily journal entries tied to current cycle period, with mood tracking and pagination
- **Alerts / Upcoming Transitions** — notifications for upcoming period changes across all cycles
- **Visualizations** — visual overview of all cycles with progress indicators
- **PDF Report** — downloadable PDF report of all cycle data (via ReportLab)
- **REST API** — cycle data available in JSON via DRF endpoints
- **htmx-driven Tabs** — cycle tabs on home page are swapped via htmx for instant navigation
- **Skeleton Loading** — skeleton card placeholders during htmx tab swaps
- **Responsive UI** — Tailwind CSS + mobile-friendly navigation
- **Accessibility** — skip-to-content link, ARIA landmarks, roles, and labels on nav/mobile menu

## Tech Stack

- **Backend:** Python 3, Django 4.2, Django REST Framework
- **Frontend:** HTML5, Tailwind CSS (django-tailwind), JavaScript, htmx
- **Database:** SQLite (dev), PostgreSQL (production)
- **Additional:** ReportLab (PDF), google-generativeai (AI integrations), whitenoise (static serving), python-dotenv

## Recent Changes (Sprint Summary)

### Sprint 1 — Security
- Deleted `set_admin_password.py` (hardcoded password); added to `.gitignore`
- Replaced `mark_safe()` with `format_html()` + `escape()` in `render_helpers.py`
- Fixed `seed_soul_cycle_details.py` — replaced `"..."` placeholders with real educational content
- Removed bare `except Exception: pass` blocks in journal/business views
- Merged duplicate `reverse` imports

### Sprint 2 — Architecture
- Extracted business logic to `cycles/services.py` (`get_all_current_periods`, `get_experience_based_recommendations`)
- Refactored dashboard and visualizations views (~90→30 lines each)

### Sprint 3 — Testing
- Edge case tests: midnight crossover, leap year, soul year boundary, very old user
- View tests: education quiz GET/POST, journal CRUD, auth-gated views
- Templatetag tests: `color_hex`, `div`/`mul`/`sub` filters (zero-division safe), `render_recommendations`
- 29 → 61 tests

### Sprint 4 — Performance
- Added `crossorigin="anonymous"` to CDN resource links

### Sprint 5 — Accessibility
- Skip-to-content link, `<main id="main-content">` landmark
- `aria-label`, `aria-expanded`, `role` attributes on nav/mobile menu

### Sprint 6 — Polish
- Journal pagination (20 per page via Django `Paginator`)
- Skeleton loading cards for htmx tab swaps
- CSS deconfliction — removed generic `body` selector and conflicting dark-themed `.cycle-card` styles from `styles.css`
- SECRET_KEY fail-fast — removed hardcoded fallback; raises `RuntimeError` if not in env

### Email Verification (Latest)
- Custom `SignUpForm` with required email field
- `UserProfile` gains `email_verified`, `verification_token`, `verification_sent_at`
- `cycles/email_service.py` sends HTML email with `secrets.token_urlsafe(48)` verification link
- `verify_email` view validates token, marks verified, redirects to login
- Email backend configurable via environment variables (console default in dev)

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js and npm

### Installation

```bash
git clone https://github.com/your-username/cosmic-cycles.git
cd cosmic-cycles

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS/Linux

# Install dependencies
pip install -r requirements.txt
npm install

# Set up .env (copy template below)
# DJANGO_SECRET_KEY, DJANGO_DEBUG, EMAIL_* as needed

# Run migrations
python manage.py migrate

# Build Tailwind CSS
python manage.py tailwind install
python manage.py tailwind build

# Run dev server
python manage.py runserver
```

### Minimal .env

```env
DJANGO_SECRET_KEY="your-generated-secret-key"
DJANGO_DEBUG="True"
# Email (defaults to console backend for dev):
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_HOST_USER=your@email.com
# EMAIL_HOST_PASSWORD=your-app-password
```

## Project Structure

```
cosmic-cycles/
├── .env                          # Environment variables (gitignored)
├── .gitignore
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── cycle_project/                # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── cycles/                       # Core application
│   ├── admin.py                  # Admin registrations
│   ├── ai_integrations.py         # Google Gemini integrations
│   ├── apps.py                   # App config with signal loading
│   ├── email_service.py           # Email verification sending
│   ├── forms.py                  # ModelForms (UserProfile, Business, Journal, SignUp)
│   ├── models.py                 # UserProfile, CycleTemplate, CyclePeriodDetail, etc.
│   ├── serializers.py            # DRF serializers
│   ├── services.py               # Business logic (get_all_current_periods, etc.)
│   ├── signals.py                # post_save auto-create UserProfile
│   ├── urls.py                   # App URL configuration
│   ├── utils.py                  # Cycle calculation utilities
│   ├── views.py                  # All views (function-based + class-based)
│   ├── templatetags/             # Custom template tags/filters
│   │   └── custom_filters.py
│   ├── templates/cycles/         # App templates
│   ├── management/               # Custom management commands
│   ├── migrations/               # Database migrations
│   ├── tests.py                  # Core utilities tests
│   ├── tests_views.py            # View tests
│   ├── tests_integration.py      # Integration tests
│   ├── tests_api_extra.py        # API extra tests
│   └── tests_templatetags.py     # Template tag tests
├── theme/                        # Tailwind CSS theme app (django-tailwind)
│   ├── static_src/
│   └── templates/
│       ├── base.html
│       ├── registration/         # signup.html, login.html, email_verification.html
│       └── includes/             # Navbar, footer, etc.
├── static/                       # Collected static files
├── logs/                         # Application logs
└── scripts/                      # Utility scripts
```

## API Endpoints

- `GET /api/cycles/daily/` — Current daily cycle (anonymous allowed)
- `GET /api/cycles/<str:cycle_type>/` — Cycle data by type (auth required; types: `yearly`, `human`, `business`, `health`, `soul`, `reincarnation`)

All endpoints return JSON via DRF serializers (`CycleTemplate` + `CyclePeriodDetail`).

## Testing

```bash
python manage.py test cycles --verbosity=2
```

Tests are organized across four files:

| File | Scope |
|------|-------|
| `tests.py` | Utility functions (cycle period calculations, edge cases, parse recommendations) and model tests |
| `tests_views.py` | View behavior (signup, login, journal CRUD, education/quiz, email verification) |
| `tests_integration.py` | Full request-response cycle (auth guards, API endpoints) |
| `tests_templatetags.py` | Custom filters (`color_hex`, `div`/`mul`/`sub`, `render_recommendations`) |

## Production Preparation

1. **`DJANGO_SECRET_KEY`** — must be set in environment; fails fast if missing
2. **`DJANGO_DEBUG`** — set to `False`
3. **`ALLOWED_HOSTS`** — add your domain(s)
4. **Database** — switch to PostgreSQL; set `DATABASE_URL` (configure in settings)
5. **Email** — configure real SMTP in `.env`
6. **Static Files** — run `python manage.py collectstatic`
7. **Web Server** — use Gunicorn + nginx or similar
8. **HTTPS** — enable in production (settings auto-configure `SECURE_SSL_REDIRECT`, HSTS, etc. when `DEBUG=False`)
