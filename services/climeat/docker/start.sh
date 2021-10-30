alembic upgrade head
uvicorn --log-level info --host=0.0.0.0 --port=8009 app.main:app 