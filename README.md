# DQ-Guard: Data Quality Monitoring & Validation Framework

A comprehensive data quality monitoring and validation framework that ensures data flowing into your systems is accurate, complete, consistent, and reliable.

## Features

- **Data Validation**: Check for missing values, data types, constraints, and regex patterns
- **Data Consistency**: Cross-table consistency and referential integrity checks
- **Data Profiling**: Generate summary statistics and track distributions over time
- **Monitoring & Alerts**: Real-time monitoring with email/Slack notifications
- **Dashboard**: Visual data quality scores and historical trends
- **Automated Remediation**: Auto-correct common data issues

## Quick Start

1. Install dependencies:
   ```bash
   # Backend
   cd backend && pip install -r requirements.txt
   
   # Frontend
   cd frontend && npm install
   ```

2. Start the application:
   ```bash
   # Start backend API
   cd backend && python app/main.py
   
   # Start frontend (new terminal)
   cd frontend && npm start
   ```

3. Open http://localhost:3000 to access the dashboard

## Architecture

- **Backend**: Python FastAPI with pandas for data processing
- **Frontend**: React with TailwindCSS for responsive UI
- **Database**: SQLite for development, PostgreSQL for production
- **Validation Engine**: Custom rules engine with pre-built templates

## Documentation

See `docs/` folder for detailed user guide and API documentation.