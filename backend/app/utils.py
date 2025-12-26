import os
import json
import pandas as pd
from typing import Dict, Any, List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class DataUtils:
    """Utility functions for data processing and validation"""
    
    @staticmethod
    def load_data_from_file(file_path: str) -> pd.DataFrame:
        """Load data from various file formats"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.csv':
            return pd.read_csv(file_path)
        elif file_extension == '.json':
            return pd.read_json(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        elif file_extension == '.parquet':
            return pd.read_parquet(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    @staticmethod
    def save_validation_report(results: Dict[str, Any], output_path: str):
        """Save validation results to a JSON report"""
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
    
    @staticmethod
    def generate_data_profile(df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive data profile"""
        profile = {
            'shape': {
                'rows': len(df),
                'columns': len(df.columns)
            },
            'columns': {},
            'memory_usage': df.memory_usage(deep=True).sum(),
            'missing_data': {
                'total_missing': df.isnull().sum().sum(),
                'missing_percentage': (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            }
        }
        
        for column in df.columns:
            col_data = df[column]
            col_profile = {
                'dtype': str(col_data.dtype),
                'non_null_count': col_data.count(),
                'null_count': col_data.isnull().sum(),
                'null_percentage': (col_data.isnull().sum() / len(col_data)) * 100,
                'unique_count': col_data.nunique(),
                'unique_percentage': (col_data.nunique() / len(col_data)) * 100
            }
            
            # Add type-specific statistics
            if pd.api.types.is_numeric_dtype(col_data):
                col_profile.update({
                    'min': col_data.min(),
                    'max': col_data.max(),
                    'mean': col_data.mean(),
                    'median': col_data.median(),
                    'std': col_data.std()
                })
            elif pd.api.types.is_string_dtype(col_data):
                col_profile.update({
                    'min_length': col_data.str.len().min() if not col_data.empty else 0,
                    'max_length': col_data.str.len().max() if not col_data.empty else 0,
                    'avg_length': col_data.str.len().mean() if not col_data.empty else 0
                })
            
            # Sample values
            col_profile['sample_values'] = col_data.dropna().head(5).tolist()
            
            profile['columns'][column] = col_profile
        
        return profile

class NotificationUtils:
    """Utility functions for sending notifications"""
    
    @staticmethod
    def send_email(
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
        to_email: str,
        subject: str,
        message: str
    ):
        """Send email notification"""
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
        server.quit()
    
    @staticmethod
    def format_validation_alert(validation_results: Dict[str, Any]) -> str:
        """Format validation results for alert notifications"""
        source = validation_results.get('source', 'Unknown')
        quality_score = validation_results.get('quality_score', 0)
        timestamp = validation_results.get('timestamp', 'Unknown')
        
        message = f"""
🚨 Data Quality Alert - DQ-Guard

Source: {source}
Quality Score: {quality_score}%
Timestamp: {timestamp}

Quality Assessment: {
    'Excellent' if quality_score >= 90 else
    'Good' if quality_score >= 70 else
    'Fair' if quality_score >= 50 else
    'Poor'
}

The data quality has been assessed. Please review the detailed results in the DQ-Guard dashboard.

Dashboard: http://localhost:3000
        """
        
        return message.strip()

class ConfigUtils:
    """Utility functions for configuration management"""
    
    @staticmethod
    def load_config(config_path: str = "config.json") -> Dict[str, Any]:
        """Load configuration from JSON file"""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {}
    
    @staticmethod
    def save_config(config: Dict[str, Any], config_path: str = "config.json"):
        """Save configuration to JSON file"""
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "database": {
                "path": "dq_guard.db"
            },
            "scheduler": {
                "enabled": True,
                "check_interval": 60
            },
            "alerts": {
                "email": {
                    "smtp_server": "localhost",
                    "smtp_port": 587,
                    "username": "",
                    "password": ""
                },
                "slack": {
                    "webhook_url": ""
                }
            },
            "validation": {
                "default_quality_threshold": 80,
                "max_file_size_mb": 100
            }
        }

class ValidationRuleTemplates:
    """Pre-built validation rule templates"""
    
    @staticmethod
    def get_email_validation_rule(column_name: str) -> Dict[str, Any]:
        """Email validation rule template"""
        return {
            "name": f"Email validation for {column_name}",
            "type": "regex_check",
            "column": column_name,
            "params": {
                "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            }
        }
    
    @staticmethod
    def get_phone_validation_rule(column_name: str) -> Dict[str, Any]:
        """Phone number validation rule template"""
        return {
            "name": f"Phone validation for {column_name}",
            "type": "regex_check",
            "column": column_name,
            "params": {
                "pattern": r"^\+?1?-?\.?\s?\(?(\d{3})\)?[\s\-\.]?(\d{3})[\s\-\.]?(\d{4})$"
            }
        }
    
    @staticmethod
    def get_date_range_rule(column_name: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Date range validation rule template"""
        return {
            "name": f"Date range validation for {column_name}",
            "type": "range_check",
            "column": column_name,
            "params": {
                "min": start_date,
                "max": end_date
            }
        }
    
    @staticmethod
    def get_completeness_rule(column_name: str, min_completeness: float = 0.95) -> Dict[str, Any]:
        """Data completeness rule template"""
        return {
            "name": f"Completeness check for {column_name}",
            "type": "null_check",
            "column": column_name,
            "params": {
                "max_null_percentage": (1 - min_completeness) * 100
            }
        }
    
    @staticmethod
    def get_all_templates() -> List[Dict[str, Any]]:
        """Get all available rule templates"""
        return [
            {
                "name": "Email Validation",
                "description": "Validates email addresses using regex pattern",
                "type": "regex_check",
                "template": "email"
            },
            {
                "name": "Phone Number Validation",
                "description": "Validates phone numbers in various formats",
                "type": "regex_check",
                "template": "phone"
            },
            {
                "name": "Date Range Validation",
                "description": "Ensures dates fall within specified range",
                "type": "range_check",
                "template": "date_range"
            },
            {
                "name": "Data Completeness",
                "description": "Checks for minimum data completeness percentage",
                "type": "null_check",
                "template": "completeness"
            },
            {
                "name": "Numeric Range",
                "description": "Validates numeric values within specified range",
                "type": "range_check",
                "template": "numeric_range"
            },
            {
                "name": "Uniqueness Check",
                "description": "Ensures all values in column are unique",
                "type": "unique_check",
                "template": "uniqueness"
            }
        ]