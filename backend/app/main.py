from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import json
from typing import List, Dict, Any
from datetime import datetime
import sqlite3
import os

from validators import DataValidator
from scheduler import ValidationScheduler
from db import DatabaseManager

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db_manager.init_db()
    scheduler.start()
    yield
    # Shutdown
    scheduler.stop()

app = FastAPI(title="DQ-Guard API", version="1.0.0", lifespan=lifespan)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
db_manager = DatabaseManager()
validator = DataValidator()
scheduler = ValidationScheduler()

@app.get("/")
async def root():
    return {"message": "DQ-Guard API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/validate/upload")
async def validate_uploaded_file(file: UploadFile = File(...)):
    """Validate uploaded CSV/JSON file"""
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file.file)
        elif file.filename.endswith('.json'):
            df = pd.read_json(file.file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        # Run validation
        results = validator.validate_dataframe(df, file.filename)
        
        # Store results
        db_manager.store_validation_result(results)
        
        return JSONResponse(content=results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate/rules")
async def validate_with_custom_rules(data: Dict[str, Any]):
    """Validate data with custom rules"""
    try:
        df = pd.DataFrame(data.get('data', []))
        rules = data.get('rules', [])
        
        results = validator.validate_with_rules(df, rules)
        db_manager.store_validation_result(results)
        
        return JSONResponse(content=results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard/summary")
async def get_dashboard_summary():
    """Get dashboard summary data"""
    try:
        summary = db_manager.get_dashboard_summary()
        return JSONResponse(content=summary)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard/trends")
async def get_quality_trends():
    """Get data quality trends over time"""
    try:
        trends = db_manager.get_quality_trends()
        return JSONResponse(content=trends)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/validation/history")
async def get_validation_history():
    """Get validation history"""
    try:
        history = db_manager.get_validation_history()
        return JSONResponse(content=history)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/schedule/validation")
async def schedule_validation(schedule_data: Dict[str, Any]):
    """Schedule recurring validation"""
    try:
        job_id = scheduler.schedule_validation(schedule_data)
        return {"job_id": job_id, "status": "scheduled"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)