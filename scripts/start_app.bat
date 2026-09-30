@echo off
title Universal Reel & Shorts AI Extractor
cd /d "D:\Personal Projects\recipe-extractor"
echo Starting Universal Reel & Shorts AI Extractor...
echo.
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
pause
