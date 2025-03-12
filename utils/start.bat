@echo off

rem Запуск сервера Go
cd ..\backend
start go run main.go

rem Запуск фронтенда с Vite
cd ..\frontend
npm run dev
