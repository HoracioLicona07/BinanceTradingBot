#!/bin/bash
echo "Starting BinanceTradingBot API..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
