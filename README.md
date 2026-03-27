# 🍽️ Chuks Kitchen

A full-stack food ordering web app with a FastAPI backend, plain HTML/CSS/JS frontend, MySQL database, and Nginx reverse proxy — all containerised with Docker.

## Features

- User registration with OTP verification
- JWT-based authentication
- Browse menu by category with search
- Add to cart, adjust quantities, place orders
- Admin panel — manage food items, orders, and users
- Cloudinary image uploads for food items

## Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | FastAPI, SQLAlchemy, Alembic      |
| Frontend  | HTML, CSS, Vanilla JS, Nginx      |
| Database  | MySQL 8                           |
| Auth      | JWT (python-jose), bcrypt         |
| Storage   | Cloudinary                        |
| Container | Docker, Docker Compose            |

## Project Structure

```
Chuks-Kitchen/
├── backend/
│   ├── app/
│   │   ├── models/        # SQLAlchemy models
│   │   ├── routers/       # API route handlers
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Auth, OTP logic
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   └── main.py
│   ├── alembic/           # DB migrations
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── css/
│   ├── js/
│   ├── pages/             # menu, orders, login, register, admin
│   └── index.html
├── nginx/
│   └── default.conf
└── docker-compose.yml
```

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose

### Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/chuks-kitchen.git
   cd chuks-kitchen
   ```

2. Create the backend env file:
   ```bash
   cp backend/.env.example backend/.env
   ```
   Fill in your values in `backend/.env`:
   ```
   DB_URL=mysql+pymysql://chuks:secret@db:3306/chuks_kitchen
   SECRET_KEY=your_secret_key
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   ```

3. Start the containers:
   ```bash
   docker compose up -d --build
   ```

4. App is live at **http://localhost**
   API docs at **http://localhost:8000/docs**

### Create an Admin User

```bash
docker compose exec api python -c "
from app.database import SessionLocal
from app.models.user import User
from app.services.auth_service import hash_password
db = SessionLocal()
db.add(User(name='Admin', email='admin@example.com', hashed_password=hash_password('yourpassword'), is_verified=True, is_admin=True))
db.commit()
db.close()
"
```

Then log in at **http://localhost/pages/login.html** and visit **http://localhost/pages/admin.html**.

## API Overview

| Method | Endpoint                        | Description              |
|--------|---------------------------------|--------------------------|
| POST   | /auth/register                  | Register user            |
| POST   | /auth/verify-otp                | Verify OTP               |
| POST   | /auth/login                     | Login, get JWT           |
| GET    | /food/                          | List all food items      |
| POST   | /cart/                          | Add / update cart item   |
| DELETE | /cart/{id}                      | Remove cart item         |
| POST   | /orders/                        | Place order              |
| GET    | /admin/orders                   | All orders (admin)       |
| PATCH  | /admin/orders/{id}/status       | Update order status      |
| GET    | /admin/users                    | All users (admin)        |

## License

MIT — see [LICENSE](LICENSE)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
