## Setup

1. Create a Neon project, find the "Connect" button, turn connection pooling off and copy the connection string.

2. Backend (in one terminal):

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Open `.env`, paste the Neon string after `DATABASE_URL=`, and put any random string after `SECRET_KEY=`. You can generate one with the following:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Then, to connect to the database and run the server:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Until we have a shared production database, your choice of username and password doesn't matter. It just creates an account with full permissions in Django's admin site, where you can view and edit every table in the database.

3. Frontend (in a second terminal):

```bash
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

4. Open http://localhost:3000. If it says "Backend status: ok", you're set.
