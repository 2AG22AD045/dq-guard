# 🛡️ DQ-Guard: Data Quality Monitoring & Validation Framework

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.3+-38B2AC.svg)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive, production-ready data quality monitoring and validation framework designed to ensure your data is accurate, complete, consistent, and reliable. Built with modern technologies and featuring a professional, enterprise-grade UI.

![DQ-Guard Dashboard](https://via.placeholder.com/800x400/1f2937/ffffff?text=DQ-Guard+Dashboard)

## ✨ Features

### 🔍 **Data Validation Engine**
- **6 Built-in Validation Rules**: Null checks, type validation, uniqueness, range validation, regex patterns, duplicate detection
- **Custom Rules Builder**: Create user-defined validation rules with parameters
- **Rule Templates**: Pre-built templates for emails, phone numbers, dates, and more
- **Quality Scoring**: 0-100% quality assessment with intelligent categorization

### 📊 **Real-time Dashboard**
- **Quality Metrics**: Total validations, average scores, data sources overview
- **Interactive Charts**: Historical quality trends with Recharts visualization
- **Distribution Analysis**: Quality score distribution with pie charts
- **Recent Activity**: Latest validation results with detailed status

### 🤖 **Automated Monitoring**
- **Flexible Scheduling**: Daily, hourly, weekly, or custom intervals
- **Multi-source Support**: Files (CSV/JSON), APIs, databases
- **Smart Alerts**: Email, Slack, webhook notifications with configurable thresholds
- **Job Management**: Start, stop, delete scheduled validations with ease

### 🎨 **Professional UI/UX**
- **Modern Design**: Clean, responsive interface with dark-themed buttons
- **Interactive Components**: Drag & drop uploads, modal dialogs, hover effects
- **Status Indicators**: Color-coded quality scores and progress bars
- **Export Functionality**: CSV export for validation history and reports

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/2AG22AD045/dq-guard.git
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
   - **Frontend Dashboard**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
dq-guard/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application entry point
│   │   ├── validators.py   # Data validation engine
│   │   ├── scheduler.py    # Background job scheduler
│   │   ├── db.py          # Database manager
│   │   └── utils.py       # Utility functions
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend container config
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Main application pages
│   │   ├── App.jsx        # Main React component
│   │   └── index.css      # TailwindCSS styles
│   ├── package.json       # Node.js dependencies
│   └── Dockerfile         # Frontend container config
├── tests/                  # Test suite
├── docs/                   # Documentation
├── docker-compose.yml      # Multi-container setup
└── README.md              # This file
```

## 🔧 Usage

### Data Validation

1. **Upload Files**: Drag & drop CSV or JSON files for instant validation
2. **Custom Rules**: Create specific validation rules for your data requirements
3. **View Results**: Get detailed quality scores and issue breakdowns

### Dashboard Monitoring

- **Quality Overview**: Monitor overall data quality trends
- **Source Analysis**: Track quality across different data sources
- **Historical Trends**: View quality improvements over time

### Automated Scheduling

1. **Create Jobs**: Set up recurring validation jobs
2. **Configure Alerts**: Get notified when quality drops below thresholds
3. **Manage Schedules**: Start, pause, or delete automated jobs

## 📊 Sample Data

The project includes sample datasets for testing:

- `sample_data.csv` - Clean data (100% quality score)
- `problematic_data.csv` - Data with various quality issues
- `customer_data_issues.csv` - Customer data with validation problems
- `sales_data_messy.csv` - Sales data with missing values
- `financial_data_errors.csv` - Financial data with validation errors

## 🛠️ API Endpoints

### Validation
- `POST /validate/upload` - Upload file for validation
- `POST /validate/rules` - Validate with custom rules

### Dashboard
- `GET /dashboard/summary` - Get dashboard metrics
- `GET /dashboard/trends` - Get quality trends

### History
- `GET /validation/history` - Get validation history

### Scheduling
- `POST /schedule/validation` - Create scheduled job

## 🧪 Testing

Run the test suite:

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
```

## 🐳 Docker Deployment

The application includes full Docker support:

```bash
# Build and run all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL` - Database connection string
- `CORS_ORIGINS` - Allowed CORS origins
- `SMTP_SERVER` - Email server configuration

### Custom Configuration
Create `config.json` in the backend directory for custom settings.

## 📈 Quality Score Interpretation

- **90-100%**: Excellent - Data meets all quality standards
- **70-89%**: Good - Minor issues that may need attention
- **50-69%**: Fair - Several issues requiring review
- **0-49%**: Poor - Significant quality problems

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) for the backend
- [React](https://reactjs.org/) and [TailwindCSS](https://tailwindcss.com/) for the frontend
- [Recharts](https://recharts.org/) for data visualization
- [Lucide React](https://lucide.dev/) for icons

## 📞 Support

For support and questions:
- Create an issue in this repository
- Check the [User Guide](docs/USER_GUIDE.md) for detailed documentation

---

**DQ-Guard** - Ensuring data quality, one validation at a time. 🛡️