#!/bin/bash

uvicorn api.main:app --host 0.0.0.0 --port 8000 &

streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0