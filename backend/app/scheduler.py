import schedule
import time
import threading
from typing import Dict, Any
import uuid
from datetime import datetime
import pandas as pd
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from validators import DataValidator
from db import DatabaseManager

class ValidationScheduler:
    """Scheduler for recurring data validation jobs"""
    
    def __init__(self):
        self.validator = DataValidator()
        self.db_manager = DatabaseManager()
        self.running = False
        self.scheduler_thread = None
    
    def start(self):
        """Start the scheduler in a background thread"""
        if not self.running:
            self.running = True
            self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.scheduler_thread.start()
            print("Validation scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        print("Validation scheduler stopped")
    
    def _run_scheduler(self):
        """Run the scheduler loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def schedule_validation(self, schedule_data: Dict[str, Any]) -> str:
        """Schedule a recurring validation job"""
        job_id = str(uuid.uuid4())
        job_name = schedule_data.get('name', f'Validation Job {job_id[:8]}')
        schedule_expression = schedule_data.get('schedule', 'daily')
        
        # Store job configuration
        self.db_manager.store_scheduled_job(job_id, job_name, schedule_expression, schedule_data)
        
        # Create the scheduled job
        job_func = lambda: self._execute_scheduled_validation(schedule_data)
        
        if schedule_expression == 'daily':
            schedule.every().day.at("09:00").do(job_func).tag(job_id)
        elif schedule_expression == 'hourly':
            schedule.every().hour.do(job_func).tag(job_id)
        elif schedule_expression == 'weekly':
            schedule.every().week.do(job_func).tag(job_id)
        elif schedule_expression.startswith('every_'):
            # Custom intervals like 'every_30_minutes'
            parts = schedule_expression.split('_')
            if len(parts) == 3:
                interval = int(parts[1])
                unit = parts[2]
                if unit == 'minutes':
                    schedule.every(interval).minutes.do(job_func).tag(job_id)
                elif unit == 'hours':
                    schedule.every(interval).hours.do(job_func).tag(job_id)
        
        return job_id
    
    def _execute_scheduled_validation(self, job_config: Dict[str, Any]):
        """Execute a scheduled validation job"""
        try:
            print(f"Executing scheduled validation: {job_config.get('name', 'Unknown')}")
            
            data_source = job_config.get('data_source', {})
            source_type = data_source.get('type')
            
            if source_type == 'file':
                # Validate file
                file_path = data_source.get('path')
                if file_path and file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                    results = self.validator.validate_dataframe(df, file_path)
                    self.db_manager.store_validation_result(results)
                    
                    # Check if alerts should be sent
                    self._check_and_send_alerts(results, job_config)
            
            elif source_type == 'api':
                # Validate API data
                api_url = data_source.get('url')
                response = requests.get(api_url)
                if response.status_code == 200:
                    data = response.json()
                    df = pd.DataFrame(data)
                    results = self.validator.validate_dataframe(df, api_url)
                    self.db_manager.store_validation_result(results)
                    
                    self._check_and_send_alerts(results, job_config)
            
            elif source_type == 'database':
                # Validate database table
                # This would require database connection setup
                pass
        
        except Exception as e:
            print(f"Error executing scheduled validation: {str(e)}")
    
    def _check_and_send_alerts(self, validation_results: Dict[str, Any], job_config: Dict[str, Any]):
        """Check validation results and send alerts if needed"""
        quality_score = validation_results.get('quality_score', 100)
        alert_config = job_config.get('alerts', {})
        
        if not alert_config.get('enabled', False):
            return
        
        threshold = alert_config.get('quality_threshold', 80)
        
        if quality_score < threshold:
            self._send_alert(validation_results, job_config, alert_config)
    
    def _send_alert(self, validation_results: Dict[str, Any], job_config: Dict[str, Any], alert_config: Dict[str, Any]):
        """Send alert notification"""
        try:
            alert_type = alert_config.get('type', 'email')
            
            message = self._create_alert_message(validation_results, job_config)
            
            if alert_type == 'email':
                self._send_email_alert(message, alert_config)
            elif alert_type == 'slack':
                self._send_slack_alert(message, alert_config)
            elif alert_type == 'webhook':
                self._send_webhook_alert(validation_results, alert_config)
        
        except Exception as e:
            print(f"Error sending alert: {str(e)}")
    
    def _create_alert_message(self, validation_results: Dict[str, Any], job_config: Dict[str, Any]) -> str:
        """Create alert message"""
        source = validation_results.get('source', 'Unknown')
        quality_score = validation_results.get('quality_score', 0)
        timestamp = validation_results.get('timestamp', datetime.now().isoformat())
        
        message = f"""
        🚨 Data Quality Alert - DQ-Guard
        
        Source: {source}
        Quality Score: {quality_score}%
        Timestamp: {timestamp}
        
        The data quality has fallen below the configured threshold.
        Please review the validation results in the DQ-Guard dashboard.
        """
        
        return message.strip()
    
    def _send_email_alert(self, message: str, alert_config: Dict[str, Any]):
        """Send email alert"""
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        smtp_server = alert_config.get('smtp_server', 'localhost')
        smtp_port = alert_config.get('smtp_port', 587)
        username = alert_config.get('username')
        password = alert_config.get('password')
        to_email = alert_config.get('to_email')
        
        if not all([username, password, to_email]):
            print("Email configuration incomplete")
            return
        
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = to_email
        msg['Subject'] = "DQ-Guard Data Quality Alert"
        
        msg.attach(MIMEText(message, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
        server.quit()
        
        print(f"Email alert sent to {to_email}")
    
    def _send_slack_alert(self, message: str, alert_config: Dict[str, Any]):
        """Send Slack alert"""
        webhook_url = alert_config.get('webhook_url')
        
        if not webhook_url:
            print("Slack webhook URL not configured")
            return
        
        payload = {
            'text': message,
            'username': 'DQ-Guard',
            'icon_emoji': ':warning:'
        }
        
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            print("Slack alert sent successfully")
        else:
            print(f"Failed to send Slack alert: {response.status_code}")
    
    def _send_webhook_alert(self, validation_results: Dict[str, Any], alert_config: Dict[str, Any]):
        """Send webhook alert"""
        webhook_url = alert_config.get('webhook_url')
        
        if not webhook_url:
            print("Webhook URL not configured")
            return
        
        payload = {
            'alert_type': 'data_quality',
            'source': 'dq-guard',
            'validation_results': validation_results,
            'timestamp': datetime.now().isoformat()
        }
        
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            print("Webhook alert sent successfully")
        else:
            print(f"Failed to send webhook alert: {response.status_code}")
    
    def cancel_job(self, job_id: str):
        """Cancel a scheduled job"""
        schedule.clear(job_id)
        print(f"Cancelled scheduled job: {job_id}")
    
    def get_scheduled_jobs(self) -> list:
        """Get list of scheduled jobs"""
        return self.db_manager.get_scheduled_jobs()