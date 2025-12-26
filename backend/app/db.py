import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os

class DatabaseManager:
    """Database manager for storing validation results and metrics"""
    
    def __init__(self, db_path: str = "dq_guard.db"):
        self.db_path = db_path
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Validation results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS validation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_name TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                total_rows INTEGER,
                total_columns INTEGER,
                quality_score REAL,
                validation_data TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Data quality metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quality_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_name TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                metric_value REAL,
                timestamp TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Scheduled jobs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT UNIQUE NOT NULL,
                job_name TEXT NOT NULL,
                schedule_expression TEXT NOT NULL,
                job_config TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_validation_result(self, result: Dict[str, Any]):
        """Store validation result in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO validation_results 
            (source_name, timestamp, total_rows, total_columns, quality_score, validation_data)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            result.get('source', 'unknown'),
            result.get('timestamp'),
            result.get('total_rows', 0),
            result.get('total_columns', 0),
            result.get('quality_score', 0),
            json.dumps(result)
        ))
        
        # Store individual metrics
        source_name = result.get('source', 'unknown')
        timestamp = result.get('timestamp')
        
        # Store quality score as metric
        cursor.execute('''
            INSERT INTO quality_metrics (source_name, metric_name, metric_value, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (source_name, 'quality_score', result.get('quality_score', 0), timestamp))
        
        # Store null percentage if available
        validation_results = result.get('validation_results', {})
        if 'null_check' in validation_results:
            null_data = validation_results['null_check']
            if 'total_nulls' in null_data:
                total_cells = result.get('total_rows', 1) * result.get('total_columns', 1)
                null_percentage = (null_data['total_nulls'] / total_cells) * 100 if total_cells > 0 else 0
                
                cursor.execute('''
                    INSERT INTO quality_metrics (source_name, metric_name, metric_value, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (source_name, 'null_percentage', null_percentage, timestamp))
        
        conn.commit()
        conn.close()
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get dashboard summary data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get total validations
        cursor.execute('SELECT COUNT(*) FROM validation_results')
        total_validations = cursor.fetchone()[0]
        
        # Get average quality score
        cursor.execute('SELECT AVG(quality_score) FROM validation_results WHERE quality_score IS NOT NULL')
        avg_quality = cursor.fetchone()[0] or 0
        
        # Get recent validations
        cursor.execute('''
            SELECT source_name, quality_score, timestamp 
            FROM validation_results 
            ORDER BY created_at DESC 
            LIMIT 10
        ''')
        recent_validations = [
            {
                'source': row[0],
                'quality_score': row[1],
                'timestamp': row[2]
            }
            for row in cursor.fetchall()
        ]
        
        # Get unique data sources
        cursor.execute('SELECT COUNT(DISTINCT source_name) FROM validation_results')
        unique_sources = cursor.fetchone()[0]
        
        # Get quality distribution
        cursor.execute('''
            SELECT 
                CASE 
                    WHEN quality_score >= 90 THEN 'Excellent'
                    WHEN quality_score >= 70 THEN 'Good'
                    WHEN quality_score >= 50 THEN 'Fair'
                    ELSE 'Poor'
                END as quality_category,
                COUNT(*) as count
            FROM validation_results 
            WHERE quality_score IS NOT NULL
            GROUP BY quality_category
        ''')
        quality_distribution = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            'total_validations': total_validations,
            'average_quality_score': round(avg_quality, 2),
            'unique_sources': unique_sources,
            'recent_validations': recent_validations,
            'quality_distribution': quality_distribution
        }
    
    def get_quality_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get quality trends over time"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get quality trends by day
        cursor.execute('''
            SELECT 
                DATE(timestamp) as date,
                AVG(quality_score) as avg_score,
                COUNT(*) as validation_count
            FROM validation_results 
            WHERE timestamp >= datetime('now', '-{} days')
            AND quality_score IS NOT NULL
            GROUP BY DATE(timestamp)
            ORDER BY date
        '''.format(days))
        
        trends = [
            {
                'date': row[0],
                'average_score': round(row[1], 2),
                'validation_count': row[2]
            }
            for row in cursor.fetchall()
        ]
        
        # Get trends by source
        cursor.execute('''
            SELECT 
                source_name,
                AVG(quality_score) as avg_score,
                COUNT(*) as validation_count
            FROM validation_results 
            WHERE timestamp >= datetime('now', '-{} days')
            AND quality_score IS NOT NULL
            GROUP BY source_name
            ORDER BY avg_score DESC
        '''.format(days))
        
        source_trends = [
            {
                'source': row[0],
                'average_score': round(row[1], 2),
                'validation_count': row[2]
            }
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return {
            'daily_trends': trends,
            'source_trends': source_trends
        }
    
    def get_validation_history(self, limit: int = 50) -> List[Dict]:
        """Get validation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT source_name, timestamp, total_rows, total_columns, quality_score, created_at
            FROM validation_results 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        history = [
            {
                'source': row[0],
                'timestamp': row[1],
                'total_rows': row[2],
                'total_columns': row[3],
                'quality_score': row[4],
                'created_at': row[5]
            }
            for row in cursor.fetchall()
        ]
        
        conn.close()
        return history
    
    def store_scheduled_job(self, job_id: str, job_name: str, schedule_expression: str, job_config: Dict):
        """Store scheduled job configuration"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO scheduled_jobs 
            (job_id, job_name, schedule_expression, job_config)
            VALUES (?, ?, ?, ?)
        ''', (job_id, job_name, schedule_expression, json.dumps(job_config)))
        
        conn.commit()
        conn.close()
    
    def get_scheduled_jobs(self) -> List[Dict]:
        """Get all scheduled jobs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT job_id, job_name, schedule_expression, job_config, is_active, created_at
            FROM scheduled_jobs 
            WHERE is_active = 1
        ''')
        
        jobs = [
            {
                'job_id': row[0],
                'job_name': row[1],
                'schedule_expression': row[2],
                'job_config': json.loads(row[3]),
                'is_active': bool(row[4]),
                'created_at': row[5]
            }
            for row in cursor.fetchall()
        ]
        
        conn.close()
        return jobs