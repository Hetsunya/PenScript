@echo off

rem Запуск сервера Go
cd ..\backend
start go run main.go

rem Запуск скрипта предсказания
start python .\NN\predict.py

rem Запуск фронтенда с Vite
cd ..\frontend
npm run dev
