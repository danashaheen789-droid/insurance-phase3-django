# Deployment Guide

## Local run
```bash
cd insurance_webapp
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Open: http://127.0.0.1:8000/

## Render deployment
1. Upload this folder to GitHub.
2. Create a new Web Service on Render.
3. Use the included render.yaml or set build/start commands manually.
4. Add SECRET_KEY, DEBUG=False, and ALLOWED_HOSTS.
5. After deployment, copy the live URL into the final PDF report.
