@echo off
title Pangea Help Desk IA - Servidor
cd /d %~dp0
uvicorn app:app --reload --port 8000
pause
