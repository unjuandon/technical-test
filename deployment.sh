#!/bin/bash
echo "Starting deployment and configurations"
ls
cd leasy-backend/
ls
python3 -m venv venv
echo "Activating virtual environment"
source venv/bin/activate
pip3 install -r requirements.txt
echo "packages completed"
ls
echo "Starting application"
ls
cd Api/
echo "Deployment succesfully"
python3 app.py