# DQ-Guard User Guide

## Overview

DQ-Guard is a comprehensive data quality monitoring and validation framework designed to ensure your data is accurate, complete, consistent, and reliable.

## Getting Started

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd dq-guard
   ```

2. **Using Docker (Recommended):**
   ```bash
   docker-compose up -d
   ```

3. **Manual Installation:**
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   python app/main.py

   # Frontend (new terminal)
   cd frontend
   npm install
   npm start
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## Features

### 1. Data Validation

Upload CSV or JSON files to validate data quality:

- **Null Checks**: Identify missing values
- **Type Validation**: Verify data types
- **Duplicate Detection**: Find duplicate records
- **Custom Rules**: Create specific validation rules

### 2. Dashboard

Monitor data quality metrics:

- **Quality Scores**: Overall data quality assessment
- **Trends**: Historical quality trends
- **Distribution**: Quality score distribution
- **Recent Validations**: Latest validation results

### 3. Validation History

Track all validation activities:

- **Complete History**: All past validations
- **Filtering**: Filter by status (passed/failed)
- **Export**: Download history as CSV
- **Details**: View detailed validation results

### 4. Scheduled Validations

Automate data quality monitoring:

- **Recurring Jobs**: Daily, hourly, or custom schedules
- **Multiple Sources**: Files, APIs, databases
- **Alerts**: Email, Slack, or webhook notifications
- **Thresholds**: Set quality score thresholds

## Using the Dashboard

### Quality Score Interpretation

- **90-100%**: Excellent - Data meets all quality standards
- **70-89%**: Good - Minor issues that may need attention
- **50-69%**: Fair - Several issues requiring review
- **0-49%**: Poor - Significant quality problems

### Key Metrics

- **Total Validations**: Number of validation runs
- **Average Quality Score**: Overall data quality trend
- **Data Sources**: Number of unique data sources
- **Issues Found**: Count of quality issues

## Validation Rules

### Built-in Rules

1. **Null Check**: Identifies missing values
2. **Type Check**: Validates data types
3. **Unique Check**: Ensures uniqueness
4. **Range Check**: Validates numeric ranges
5. **Regex Check**: Pattern matching validation
6. **Duplicate Check**: Finds duplicate rows

### Custom Rules

Create custom validation rules:

```json
{
  "name": "Email Validation",
  "type": "regex_check",
  "column": "email",
  "params": {
    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
  }
}
```

### Rule Templates

Pre-built templates for common validations:

- Email addresses
- Phone numbers
- Date ranges
- Data completeness
- Numeric ranges

## Scheduling Validations

### Creating Scheduled Jobs

1. Navigate to the Schedule page
2. Click "Schedule New Job"
3. Configure:
   - Job name and schedule frequency
   - Data source (file, API, database)
   - Alert settings and thresholds

### Schedule Options

- **Daily**: Runs once per day at 9:00 AM
- **Hourly**: Runs every hour
- **Weekly**: Runs once per week
- **Custom**: Every N minutes/hours

### Alert Configuration

Set up notifications when quality drops below thresholds:

- **Email**: SMTP-based email alerts
- **Slack**: Webhook-based Slack notifications
- **Webhook**: Custom webhook endpoints

## API Usage

### Upload File for Validation

```bash
curl -X POST "http://localhost:8000/validate/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data.csv"
```

### Custom Rule Validation

```bash
curl -X POST "http://localhost:8000/validate/rules" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [...],
    "rules": [...]
  }'
```

### Get Dashboard Summary

```bash
curl "http://localhost:8000/dashboard/summary"
```

## Configuration

### Environment Variables

- `DATABASE_URL`: Database connection string
- `CORS_ORIGINS`: Allowed CORS origins
- `SMTP_SERVER`: Email server configuration
- `SLACK_WEBHOOK`: Slack webhook URL

### Configuration File

Create `config.json` in the backend directory:

```json
{
  "database": {
    "path": "dq_guard.db"
  },
  "alerts": {
    "email": {
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      "username": "your-email@gmail.com",
      "password": "your-password"
    }
  },
  "validation": {
    "default_quality_threshold": 80,
    "max_file_size_mb": 100
  }
}
```

## Troubleshooting

### Common Issues

1. **File Upload Fails**
   - Check file format (CSV/JSON only)
   - Verify file size limits
   - Ensure proper encoding

2. **Scheduled Jobs Not Running**
   - Check scheduler service status
   - Verify data source accessibility
   - Review job configuration

3. **Alerts Not Sending**
   - Verify SMTP/webhook configuration
   - Check network connectivity
   - Review alert thresholds

### Logs

Check application logs:

```bash
# Docker
docker-compose logs backend
docker-compose logs frontend

# Manual installation
# Backend logs in terminal
# Frontend logs in browser console
```

## Best Practices

### Data Quality Standards

1. **Set Realistic Thresholds**: Start with 70-80% quality scores
2. **Regular Monitoring**: Schedule daily or hourly checks
3. **Incremental Improvement**: Focus on one quality dimension at a time
4. **Documentation**: Document validation rules and thresholds

### Performance Optimization

1. **File Size**: Keep files under 100MB for optimal performance
2. **Batch Processing**: Process large datasets in chunks
3. **Indexing**: Use appropriate database indexes
4. **Caching**: Enable caching for frequently accessed data

### Security

1. **Access Control**: Implement proper authentication
2. **Data Privacy**: Ensure sensitive data is protected
3. **Network Security**: Use HTTPS in production
4. **Regular Updates**: Keep dependencies updated

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review application logs
3. Create an issue in the repository
4. Contact the development team

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.