# Contributing to Chuks Kitchen

Thanks for taking the time to contribute! Here's how to get started.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/chuks-kitchen.git
   cd chuks-kitchen
   ```
3. Create a new branch for your change:
   ```bash
   git checkout -b feat/your-feature-name
   ```

## Development Setup

Follow the [README](README.md) setup steps to get the app running locally with Docker.

## Making Changes

- **Backend** — FastAPI routes live in `backend/app/routers/`. Add new models in `models/`, schemas in `schemas/`.
- **Frontend** — Plain HTML/CSS/JS in `frontend/`. Shared utilities are in `frontend/js/api.js`.
- **Database** — After changing models, generate a migration:
  ```bash
  docker compose exec api alembic revision --autogenerate -m "describe your change"
  docker compose exec api alembic upgrade head
  ```

## Submitting a Pull Request

1. Make sure the app runs without errors after your changes
2. Keep commits focused — one logical change per commit
3. Write a clear PR description explaining what and why
4. Open a pull request against the `main` branch

## Code Style

- Python: follow [PEP 8](https://peps.python.org/pep-0008/)
- JavaScript: use `const`/`let`, async/await, and keep functions small
- No secrets or credentials in code

## Reporting Issues

Open a GitHub issue with:
- A clear title
- Steps to reproduce
- Expected vs actual behaviour
- Any relevant logs or screenshots
