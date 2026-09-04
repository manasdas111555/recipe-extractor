@echo off
title Instagram Reel Recipe Extractor & Mobile Server
cd /d "D:\Personal Projects\recipe-extractor"
echo Starting Recipe Extractor App...
echo.
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
pause
