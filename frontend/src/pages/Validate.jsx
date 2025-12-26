import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, CheckCircle, XCircle, AlertTriangle, Zap, Settings, Plus } from 'lucide-react';
import axios from 'axios';

const Validate = () => {
  const [validationResult, setValidationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [customRules, setCustomRules] = useState([]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'text/csv': ['.csv'],
      'application/json': ['.json']
    },
    onDrop: handleFileDrop
  });

  async function handleFileDrop(acceptedFiles) {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post('/validate/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setValidationResult(response.data);
    } catch (error) {
      console.error('Validation error:', error);
      alert('Error validating file: ' + error.message);
    } finally {
      setLoading(false);
    }
  }

  const addCustomRule = () => {
    setCustomRules([...customRules, {
      name: '',
      type: 'null_check',
      column: '',
      params: {}
    }]);
  };

  const updateCustomRule = (index, field, value) => {
    const updated = [...customRules];
    if (field === 'params') {
      updated[index].params = { ...updated[index].params, ...value };
    } else {
      updated[index][field] = value;
    }
    setCustomRules(updated);
  };

  const removeCustomRule = (index) => {
    setCustomRules(customRules.filter((_, i) => i !== index));
  };

  const validateWithCustomRules = async () => {
    if (!validationResult || customRules.length === 0) return;

    setLoading(true);
    try {
      const response = await axios.post('/validate/rules', {
        data: [],
        rules: customRules
      });
      
      setValidationResult(response.data);
    } catch (error) {
      console.error('Custom validation error:', error);
      alert('Error with custom validation: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const getValidationIcon = (passed) => {
    if (passed) return <CheckCircle className="h-5 w-5 text-green-600" />;
    return <XCircle className="h-5 w-5 text-red-600" />;
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Data Validation</h1>
        <p className="text-lg text-gray-600">Upload your data files to validate quality and integrity</p>
      </div>

      {/* File Upload */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-6">
          <div className="p-2 bg-gray-900 rounded-lg">
            <Upload className="h-5 w-5 text-white" />
          </div>
          <h2 className="text-xl font-bold text-gray-900">Upload Data File</h2>
        </div>
        
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-300 ${
            isDragActive 
              ? 'border-gray-900 bg-gray-50 scale-105' 
              : 'border-gray-300 hover:border-gray-900 hover:bg-gray-50'
          }`}
        >
          <input {...getInputProps()} />
          <Upload className="mx-auto h-16 w-16 text-gray-400 mb-4" />
          {isDragActive ? (
            <div>
              <p className="text-xl font-semibold text-gray-900 mb-2">Drop the file here...</p>
              <p className="text-gray-600">Release to upload</p>
            </div>
          ) : (
            <div>
              <p className="text-xl font-semibold text-gray-900 mb-2">Drag & drop a file here, or click to select</p>
              <p className="text-gray-600 mb-4">Supports CSV and JSON files up to 100MB</p>
              <button className="btn-dark">
                Choose File
              </button>
            </div>
          )}
        </div>

        {loading && (
          <div className="mt-6 flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
            <span className="ml-3 text-gray-700 font-medium">Validating data...</span>
          </div>
        )}
      </div>

      {/* Custom Rules */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gray-900 rounded-lg">
              <Settings className="h-5 w-5 text-white" />
            </div>
            <h2 className="text-xl font-bold text-gray-900">Custom Validation Rules</h2>
          </div>
          <button onClick={addCustomRule} className="btn-dark flex items-center space-x-2">
            <Plus className="h-4 w-4" />
            <span>Add Rule</span>
          </button>
        </div>

        {customRules.map((rule, index) => (
          <div key={index} className="border-2 border-gray-200 rounded-xl p-6 mb-4 hover:border-gray-300 transition-colors">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">Rule Name</label>
                <input
                  type="text"
                  value={rule.name}
                  onChange={(e) => updateCustomRule(index, 'name', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
                  placeholder="Enter rule name"
                />
              </div>
              
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">Rule Type</label>
                <select
                  value={rule.type}
                  onChange={(e) => updateCustomRule(index, 'type', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
                >
                  <option value="null_check">Null Check</option>
                  <option value="type_check">Type Check</option>
                  <option value="unique_check">Unique Check</option>
                  <option value="range_check">Range Check</option>
                  <option value="regex_check">Regex Check</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">Column</label>
                <input
                  type="text"
                  value={rule.column}
                  onChange={(e) => updateCustomRule(index, 'column', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
                  placeholder="Column name"
                />
              </div>
              
              <div className="flex items-end">
                <button
                  onClick={() => removeCustomRule(index)}
                  className="w-full bg-red-600 hover:bg-red-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors duration-200"
                >
                  Remove
                </button>
              </div>
            </div>

            {/* Rule-specific parameters */}
            {rule.type === 'range_check' && (
              <div className="grid grid-cols-2 gap-4 mt-4">
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">Min Value</label>
                  <input
                    type="number"
                    value={rule.params.min || ''}
                    onChange={(e) => updateCustomRule(index, 'params', { min: parseFloat(e.target.value) })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">Max Value</label>
                  <input
                    type="number"
                    value={rule.params.max || ''}
                    onChange={(e) => updateCustomRule(index, 'params', { max: parseFloat(e.target.value) })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
                  />
                </div>
              </div>
            )}

            {rule.type === 'regex_check' && (
              <div className="mt-4">
                <label className="block text-sm font-bold text-gray-700 mb-2">Regex Pattern</label>
                <input
                  type="text"
                  value={rule.params.pattern || ''}
                  onChange={(e) => updateCustomRule(index, 'params', { pattern: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
                  placeholder="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
                />
              </div>
            )}
          </div>
        ))}

        {customRules.length > 0 && (
          <button onClick={validateWithCustomRules} className="btn-primary flex items-center space-x-2">
            <Zap className="h-4 w-4" />
            <span>Run Custom Validation</span>
          </button>
        )}
      </div>

      {/* Validation Results */}
      {validationResult && (
        <div className="card">
          <div className="flex items-center space-x-3 mb-6">
            <div className="p-2 bg-gray-900 rounded-lg">
              <FileText className="h-5 w-5 text-white" />
            </div>
            <h2 className="text-xl font-bold text-gray-900">Validation Results</h2>
          </div>
          
          {/* Summary */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-6">
              <div className="flex items-center">
                <FileText className="h-6 w-6 text-gray-700 mr-3" />
                <span className="text-sm font-bold text-gray-700 uppercase tracking-wide">Data Shape</span>
              </div>
              <p className="text-2xl font-bold text-gray-900 mt-2">
                {validationResult.total_rows} × {validationResult.total_columns}
              </p>
            </div>
            
            <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-6">
              <div className="flex items-center">
                <CheckCircle className="h-6 w-6 text-green-700 mr-3" />
                <span className="text-sm font-bold text-green-700 uppercase tracking-wide">Quality Score</span>
              </div>
              <p className="text-2xl font-bold text-green-900 mt-2">
                {validationResult.quality_score}%
              </p>
            </div>
            
            <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-xl p-6">
              <div className="flex items-center">
                <AlertTriangle className="h-6 w-6 text-yellow-700 mr-3" />
                <span className="text-sm font-bold text-yellow-700 uppercase tracking-wide">Issues Found</span>
              </div>
              <p className="text-2xl font-bold text-yellow-900 mt-2">
                {validationResult.issues_found?.length || 0}
              </p>
            </div>
          </div>

          {/* Detailed Results */}
          <div className="space-y-4">
            {Object.entries(validationResult.validation_results || {}).map(([checkType, result]) => (
              <div key={checkType} className="border-2 border-gray-200 rounded-xl p-6 hover:border-gray-300 transition-colors">
                <h3 className="text-lg font-bold text-gray-900 mb-4 capitalize flex items-center">
                  <div className="w-3 h-3 bg-gray-900 rounded-full mr-3"></div>
                  {checkType.replace('_', ' ')}
                </h3>
                
                {result.columns ? (
                  <div className="space-y-3">
                    {Object.entries(result.columns).map(([column, columnResult]) => (
                      <div key={column} className="flex items-center justify-between py-3 px-4 bg-gray-50 rounded-lg">
                        <span className="font-semibold text-gray-800">{column}</span>
                        <div className="flex items-center space-x-3">
                          {typeof columnResult === 'object' && columnResult.null_count !== undefined && (
                            <span className="text-sm text-gray-600 bg-white px-3 py-1 rounded-full">
                              {columnResult.null_count} nulls ({columnResult.null_percentage}%)
                            </span>
                          )}
                          {typeof columnResult === 'object' && columnResult.passed !== undefined && 
                            getValidationIcon(columnResult.passed)
                          }
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="flex items-center justify-between bg-gray-50 rounded-lg p-4">
                    <span className="text-gray-700 font-medium">
                      {result.duplicate_rows !== undefined && `${result.duplicate_rows} duplicate rows found`}
                      {result.total_nulls !== undefined && `${result.total_nulls} null values found`}
                    </span>
                    {result.passed !== undefined && getValidationIcon(result.passed)}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Validate;