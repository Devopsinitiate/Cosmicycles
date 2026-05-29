# Contributing to Cosmic Cycles

Thanks for your interest in contributing! This document covers the workflow, conventions, and standards for this project.

## Project Overview

Cosmic Cycles is a Django 4.2 application using Tailwind CSS (django-tailwind), Django REST Framework, and htmx. See the README for a full feature list.

## Getting Started

1. Fork and clone the repo
2. Create a virtual environment: `python -m venv .venv && .venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt && npm install`
4. Copy `.env` template from README, set `DJANGO_SECRET_KEY`
5. Run migrations: `python manage.py migrate`
6. Build Tailwind: `python manage.py tailwind install && python manage.py tailwind build`
7. Run the dev server: `python manage.py runserver`

## Code Standards

### Python

- Follow PEP 8
- Use descriptive names (not abbreviations)
- Import order: stdlib → Django → third-party → local; one import group per section
- Function-based views for simple pages, class-based (`CreateView`) for forms
- Keep views thin — extract business logic into `services.py` or utility functions
- No bare `except Exception: pass` — catch specific exceptions or log them

### Templates (Django + Tailwind CSS)

- Extend `base.html` for all pages
- Use Tailwind utility classes — avoid custom CSS unless necessary
- Follow existing patterns for form styling (gray-800 cards, purple accent, etc.)
- Use `{% load static %}` and `{% static '...' %}` for assets
- New templates go in `theme/templates/` (for base/frontend) or `cycles/templates/cycles/`

### JavaScript

- Keep JS in `base.html` or include inline for htmx partials
- Use `DOMContentLoaded` to attach event listeners
- Follow the existing pattern of minimal, vanilla JS

### Database / Models

- Model field changes require a migration: `python manage.py makemigrations`
- Use `python manage.py migrate` before running tests
- New models or fields should have `help_text` where the meaning isn't obvious
- Add a `Meta` class with `ordering` and `verbose_name` where applicable
- `__str__` should return something human-readable

## Testing

Run all tests before submitting:

```bash
python manage.py test cycles --verbosity=2
```

### Test Organization

| File | What to put here |
|------|-----------------|
| `cycles/tests.py` | Utility/helper function tests, model unit tests |
| `cycles/tests_views.py` | View tests — GET/POST, auth guards, form validation |
| `cycles/tests_integration.py` | Full request-response cycle, API endpoint tests |
| `cycles/tests_templatetags.py` | Custom template tag and filter tests |
| `cycles/tests_api_extra.py` | DRF serializer and API extra tests |

### Test Guidelines

- Every new view needs at least: a success case, a failure/404 case, and an auth guard
- Every new model needs a `__str__` test and any custom method tests
- Use Django's `TestCase` (not `SimpleTestCase`) when the database is needed
- Use `setUp` to create shared fixtures, not module-level data
- Test edge cases: empty inputs, zero division, boundary values, missing relations
- New features should come with tests before merging

## Branching & Commits

- Create a feature branch from `main`: `git checkout -b feat/your-feature`
- Use conventional commit messages:
  - `feat: add email verification on signup`
  - `fix: resolve 404 on quiz page for daily cycle`
  - `refactor: extract period calculation into services.py`
  - `test: add edge case tests for midnight crossover`
- Keep commits atomic — one logical change per commit
- Rebase onto `main` before opening a PR

## Pull Request Process

1. Ensure all tests pass
2. Add tests for any new functionality
3. Update the README if the change affects setup, API, or project structure
4. Keep PRs focused — one feature or fix per PR
5. PR title should match the commit style (e.g., "feat: add email verification")
6. Respond to review feedback promptly

## Environment Variables

Sensitive configuration lives in `.env` (gitignored). Document any new env vars in the README.

Key variables:

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `DJANGO_SECRET_KEY` | Yes | — | Django secret key (fails fast if missing) |
| `DJANGO_DEBUG` | No | `True` | Debug mode |
| `EMAIL_BACKEND` | No | Console backend | Email sending backend |
| `EMAIL_HOST` | No | — | SMTP host |
| `EMAIL_PORT` | No | `587` | SMTP port |
| `EMAIL_HOST_USER` | No | — | SMTP username |
| `EMAIL_HOST_PASSWORD` | No | — | SMTP password |
| `DEFAULT_FROM_EMAIL` | No | noreply@cyclesofmastery.com | From address |

## Questions?

Open a discussion or issue on GitHub.
