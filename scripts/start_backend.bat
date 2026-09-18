@echo off
title Universal Pro AI - Backend Gateway
echo ========================================================
echo Starting Universal Pro AI FastAPI Backend Gateway...
echo Swagger Docs: http://localhost:8000/docs
echo Health Check: http://localhost:8000/health
echo ========================================================
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
pause
