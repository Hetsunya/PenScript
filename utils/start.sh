#!/bin/bash

cd ../backend || exit
go run main.go > backend.log 2>&1 &

python ./NN/predict.py

cd ../frontend || exit
npm run dev
