import pandas as pd
import numpy as np
import re
from typing import Dict, List, Any, Optional
from datetime import datetime

class DataValidator:
    """Core data validation engine"""
    
    def __init__(self):
        self.validation_rules = {
            'null_check': self._check_nulls,
            'type_check': self._check_types,
            'unique_check': self._check_uniqueness,
            'range_check': self._check_range,
            'regex_check': self._check_regex,
            'duplicate_check': self._check_duplicates
        }
    
    def validate_dataframe(self, df: pd.DataFrame, source_name: str) -> Dict[str, Any]:
        """Run comprehensive validation on a dataframe"""
        results = {
            'source': source_name,
            'timestamp': datetime.now().isoformat(),
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'validation_results': {},
            'quality_score': 0,
            'issues_found': [],
            'summary': {}
        }
        
        # Run basic validations
        null_results = self._check_nulls(df)
        type_results = self._check_types(df)
        duplicate_results = self._check_duplicates(df)
        
        results['validation_results'] = {
            'null_check': null_results,
            'type_check': type_results,
            'duplicate_check': duplicate_results
        }
        
        # Calculate quality score
        results['quality_score'] = self._calculate_quality_score(results['validation_results'])
        
        # Generate summary
        results['summary'] = self._generate_summary(df, results['validation_results'])
        
        return results
    
    def validate_with_rules(self, df: pd.DataFrame, rules: List[Dict]) -> Dict[str, Any]:
        """Validate dataframe with custom rules"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'custom_rules_results': {},
            'quality_score': 0,
            'issues_found': []
        }
        
        for rule in rules:
            rule_name = rule.get('name', 'unnamed_rule')
            rule_type = rule.get('type')
            column = rule.get('column')
            
            if rule_type in self.validation_rules:
                rule_result = self.validation_rules[rule_type](df, column, rule.get('params', {}))
                results['custom_rules_results'][rule_name] = rule_result
        
        results['quality_score'] = self._calculate_quality_score(results['custom_rules_results'])
        
        return results
    
    def _check_nulls(self, df: pd.DataFrame, column: str = None, params: Dict = None) -> Dict:
        """Check for null/missing values"""
        if column:
            null_count = df[column].isnull().sum()
            total_count = len(df[column])
            null_percentage = (null_count / total_count) * 100
            
            return {
                'column': column,
                'null_count': int(null_count),
                'total_count': int(total_count),
                'null_percentage': round(null_percentage, 2),
                'passed': null_count == 0
            }
        else:
            # Check all columns
            null_summary = {}
            for col in df.columns:
                null_count = df[col].isnull().sum()
                null_summary[col] = {
                    'null_count': int(null_count),
                    'null_percentage': round((null_count / len(df)) * 100, 2)
                }
            
            return {
                'type': 'null_check',
                'columns': null_summary,
                'total_nulls': int(df.isnull().sum().sum())
            }
    
    def _check_types(self, df: pd.DataFrame, column: str = None, params: Dict = None) -> Dict:
        """Check data types"""
        if column and params:
            expected_type = params.get('expected_type')
            actual_type = str(df[column].dtype)
            
            return {
                'column': column,
                'expected_type': expected_type,
                'actual_type': actual_type,
                'passed': expected_type.lower() in actual_type.lower()
            }
        else:
            # Get type summary for all columns
            type_summary = {}
            for col in df.columns:
                type_summary[col] = {
                    'dtype': str(df[col].dtype),
                    'unique_values': int(df[col].nunique()),
                    'sample_values': df[col].dropna().head(3).tolist()
                }
            
            return {
                'type': 'type_check',
                'columns': type_summary
            }
    
    def _check_uniqueness(self, df: pd.DataFrame, column: str, params: Dict = None) -> Dict:
        """Check for unique values in a column"""
        total_count = len(df[column])
        unique_count = df[column].nunique()
        duplicate_count = total_count - unique_count
        
        return {
            'column': column,
            'total_count': int(total_count),
            'unique_count': int(unique_count),
            'duplicate_count': int(duplicate_count),
            'uniqueness_percentage': round((unique_count / total_count) * 100, 2),
            'passed': duplicate_count == 0
        }
    
    def _check_range(self, df: pd.DataFrame, column: str, params: Dict) -> Dict:
        """Check if values are within specified range"""
        min_val = params.get('min')
        max_val = params.get('max')
        
        if pd.api.types.is_numeric_dtype(df[column]):
            out_of_range = df[(df[column] < min_val) | (df[column] > max_val)]
            
            return {
                'column': column,
                'min_allowed': min_val,
                'max_allowed': max_val,
                'out_of_range_count': len(out_of_range),
                'out_of_range_percentage': round((len(out_of_range) / len(df)) * 100, 2),
                'passed': len(out_of_range) == 0
            }
        else:
            return {
                'column': column,
                'error': 'Column is not numeric',
                'passed': False
            }
    
    def _check_regex(self, df: pd.DataFrame, column: str, params: Dict) -> Dict:
        """Check if values match regex pattern"""
        pattern = params.get('pattern')
        
        if not pattern:
            return {'error': 'No regex pattern provided', 'passed': False}
        
        try:
            matches = df[column].astype(str).str.match(pattern, na=False)
            non_matches = (~matches).sum()
            
            return {
                'column': column,
                'pattern': pattern,
                'matches': int(matches.sum()),
                'non_matches': int(non_matches),
                'match_percentage': round((matches.sum() / len(df)) * 100, 2),
                'passed': non_matches == 0
            }
        except Exception as e:
            return {
                'column': column,
                'error': f'Regex error: {str(e)}',
                'passed': False
            }
    
    def _check_duplicates(self, df: pd.DataFrame, column: str = None, params: Dict = None) -> Dict:
        """Check for duplicate rows"""
        if column:
            duplicates = df[df[column].duplicated()]
        else:
            duplicates = df[df.duplicated()]
        
        return {
            'type': 'duplicate_check',
            'duplicate_rows': len(duplicates),
            'total_rows': len(df),
            'duplicate_percentage': round((len(duplicates) / len(df)) * 100, 2),
            'passed': len(duplicates) == 0
        }
    
    def _calculate_quality_score(self, validation_results: Dict) -> float:
        """Calculate overall data quality score (0-100)"""
        total_checks = 0
        passed_checks = 0
        
        for check_name, result in validation_results.items():
            if isinstance(result, dict):
                if 'passed' in result:
                    total_checks += 1
                    if result['passed']:
                        passed_checks += 1
                elif 'columns' in result:
                    # Handle multi-column results
                    for col_result in result['columns'].values():
                        if isinstance(col_result, dict) and 'passed' in col_result:
                            total_checks += 1
                            if col_result['passed']:
                                passed_checks += 1
        
        if total_checks == 0:
            return 100.0
        
        return round((passed_checks / total_checks) * 100, 2)
    
    def _generate_summary(self, df: pd.DataFrame, validation_results: Dict) -> Dict:
        """Generate validation summary"""
        return {
            'data_shape': f"{len(df)} rows × {len(df.columns)} columns",
            'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB",
            'numeric_columns': len(df.select_dtypes(include=[np.number]).columns),
            'text_columns': len(df.select_dtypes(include=['object']).columns),
            'datetime_columns': len(df.select_dtypes(include=['datetime']).columns)
        }