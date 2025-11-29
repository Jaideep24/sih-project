# PostgreSQL Setup Guide

## Quick Setup Steps

### 1. Create Neon.tech Account & Database

1. Go to https://neon.tech and sign up (free tier available)
2. Create a new project
3. Copy your connection string (DATABASE_URL)
   - Format: `postgresql://user:password@host/database?sslmode=require`

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
SECRET_KEY=django-insecure-9s6fa3z#71al1p%rv7yn0yopn-3xj*4xpxz+sb3o6em%7dhw!d
STREAM_API_KEY=ygzv4mky4dz3
STREAM_API_SECRET=h4yq4uqqmahp48zvxs6b4dxbq4x3q9ute79uqkdsauwy2ky5z4durtv73g8v5ssq
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Load Environment Variables

```powershell
pip install python-dotenv
```

Then add this to `manage.py` and `wsgi.py` at the top (after imports):

```python
from dotenv import load_dotenv
load_dotenv()
```

### 5. Run Migrations

```powershell
python manage.py migrate
```

This creates all tables in your PostgreSQL database.

### 6. Create Superuser

```powershell
python manage.py createsuperuser
```

### 7. Run Server

```powershell
python manage.py runserver
```

## Troubleshooting

### Error: "DATABASE_URL not set"
- Make sure `.env` file exists in project root
- Verify `python-dotenv` is installed
- Check that `load_dotenv()` is called in `manage.py`

### Error: "SSL connection error"
- Ensure your DATABASE_URL includes `?sslmode=require` at the end

### Error: "Connection refused"
- Check that your Neon.tech database is active
- Verify the connection string is correct

## Next Steps

After successful setup:
1. You can delete `db.sqlite3` file (no longer needed)
2. Delete `migrate_to_postgres.sh` (not needed for fresh setup)
3. Your app now uses PostgreSQL exclusively
4. Ready for deployment on any modern hosting platform!
