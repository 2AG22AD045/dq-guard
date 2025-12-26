import pytest
import pandas as pd
import numpy as np
from backend.app.validators import DataValidator

class TestDataValidator:
    
    def setup_method(self):
        """Set up test fixtures"""
        self.validator = DataValidator()
        
        # Create test dataframe
        self.test_df = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', None, 'David', 'Eve'],
            'email': ['alice@test.com', 'bob@test.com', 'invalid-email', 'david@test.com', None],
            'age': [25, 30, 35, None, 28],
            'score': [85.5, 92.0, 78.5, 88.0, 95.5]
        })
    
    def test_null_check_single_column(self):
        """Test null check for a single column"""
        result = self.validator._check_nulls(self.test_df, 'name')
        
        assert result['column'] == 'name'
        assert result['null_count'] == 1
        assert result['total_count'] == 5
        assert result['null_percentage'] == 20.0
        assert result['passed'] == False
    
    def test_null_check_all_columns(self):
        """Test null check for all columns"""
        result = self.validator._check_nulls(self.test_df)
        
        assert result['type'] == 'null_check'
        assert 'columns' in result
        assert result['columns']['name']['null_count'] == 1
        assert result['columns']['age']['null_count'] == 1
        assert result['total_nulls'] == 3
    
    def test_type_check_single_column(self):
        """Test type check for a single column"""
        result = self.validator._check_types(
            self.test_df, 
            'age', 
            {'expected_type': 'int64'}
        )
        
        assert result['column'] == 'age'
        assert result['expected_type'] == 'int64'
        assert 'actual_type' in result
    
    def test_uniqueness_check(self):
        """Test uniqueness check"""
        result = self.validator._check_uniqueness(self.test_df, 'id')
        
        assert result['column'] == 'id'
        assert result['total_count'] == 5
        assert result['unique_count'] == 5
        assert result['duplicate_count'] == 0
        assert result['passed'] == True
    
    def test_range_check_numeric(self):
        """Test range check for numeric column"""
        result = self.validator._check_range(
            self.test_df, 
            'age', 
            {'min': 20, 'max': 40}
        )
        
        assert result['column'] == 'age'
        assert result['min_allowed'] == 20
        assert result['max_allowed'] == 40
        assert result['out_of_range_count'] == 0
        assert result['passed'] == True
    
    def test_regex_check_email(self):
        """Test regex check for email validation"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        result = self.validator._check_regex(
            self.test_df, 
            'email', 
            {'pattern': email_pattern}
        )
        
        assert result['column'] == 'email'
        assert result['pattern'] == email_pattern
        assert result['non_matches'] > 0  # Should catch invalid email and None
        assert result['passed'] == False
    
    def test_duplicate_check(self):
        """Test duplicate check"""
        # Create dataframe with duplicates
        df_with_duplicates = pd.DataFrame({
            'a': [1, 2, 2, 3],
            'b': ['x', 'y', 'y', 'z']
        })
        
        result = self.validator._check_duplicates(df_with_duplicates)
        
        assert result['type'] == 'duplicate_check'
        assert result['duplicate_rows'] == 1
        assert result['total_rows'] == 4
        assert result['passed'] == False
    
    def test_validate_dataframe(self):
        """Test complete dataframe validation"""
        result = self.validator.validate_dataframe(self.test_df, 'test_data.csv')
        
        assert result['source'] == 'test_data.csv'
        assert result['total_rows'] == 5
        assert result['total_columns'] == 5
        assert 'validation_results' in result
        assert 'quality_score' in result
        assert 'summary' in result
        
        # Check that all basic validations are present
        assert 'null_check' in result['validation_results']
        assert 'type_check' in result['validation_results']
        assert 'duplicate_check' in result['validation_results']
    
    def test_validate_with_custom_rules(self):
        """Test validation with custom rules"""
        custom_rules = [
            {
                'name': 'age_range',
                'type': 'range_check',
                'column': 'age',
                'params': {'min': 18, 'max': 65}
            },
            {
                'name': 'email_format',
                'type': 'regex_check',
                'column': 'email',
                'params': {'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'}
            }
        ]
        
        result = self.validator.validate_with_rules(self.test_df, custom_rules)
        
        assert 'custom_rules_results' in result
        assert 'age_range' in result['custom_rules_results']
        assert 'email_format' in result['custom_rules_results']
        assert 'quality_score' in result
    
    def test_calculate_quality_score(self):
        """Test quality score calculation"""
        # Mock validation results
        validation_results = {
            'test1': {'passed': True},
            'test2': {'passed': False},
            'test3': {'passed': True},
            'test4': {'passed': True}
        }
        
        score = self.validator._calculate_quality_score(validation_results)
        assert score == 75.0  # 3 out of 4 passed
    
    def test_generate_summary(self):
        """Test summary generation"""
        validation_results = {
            'null_check': {'total_nulls': 3},
            'type_check': {'columns': {}},
            'duplicate_check': {'duplicate_rows': 0}
        }
        
        summary = self.validator._generate_summary(self.test_df, validation_results)
        
        assert 'data_shape' in summary
        assert 'memory_usage' in summary
        assert 'numeric_columns' in summary
        assert 'text_columns' in summary
        assert summary['data_shape'] == "5 rows × 5 columns"

class TestValidationRuleEdgeCases:
    
    def setup_method(self):
        self.validator = DataValidator()
    
    def test_empty_dataframe(self):
        """Test validation with empty dataframe"""
        empty_df = pd.DataFrame()
        result = self.validator.validate_dataframe(empty_df, 'empty.csv')
        
        assert result['total_rows'] == 0
        assert result['total_columns'] == 0
        assert result['quality_score'] == 100.0  # No data, no issues
    
    def test_single_row_dataframe(self):
        """Test validation with single row"""
        single_row_df = pd.DataFrame({'col1': [1], 'col2': ['test']})
        result = self.validator.validate_dataframe(single_row_df, 'single.csv')
        
        assert result['total_rows'] == 1
        assert result['total_columns'] == 2
    
    def test_all_null_column(self):
        """Test validation with column containing all nulls"""
        all_null_df = pd.DataFrame({
            'good_col': [1, 2, 3],
            'null_col': [None, None, None]
        })
        
        result = self.validator._check_nulls(all_null_df, 'null_col')
        assert result['null_percentage'] == 100.0
        assert result['passed'] == False
    
    def test_invalid_regex_pattern(self):
        """Test regex check with invalid pattern"""
        df = pd.DataFrame({'text': ['test', 'data']})
        result = self.validator._check_regex(df, 'text', {'pattern': '['})  # Invalid regex
        
        assert 'error' in result
        assert result['passed'] == False
    
    def test_range_check_non_numeric(self):
        """Test range check on non-numeric column"""
        df = pd.DataFrame({'text': ['a', 'b', 'c']})
        result = self.validator._check_range(df, 'text', {'min': 1, 'max': 10})
        
        assert 'error' in result
        assert result['passed'] == False

if __name__ == '__main__':
    pytest.main([__file__])