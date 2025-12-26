import React from 'react';
import { CheckCircle, AlertTriangle, XCircle, Info } from 'lucide-react';

const QualityScoreCard = ({ score, title, subtitle }) => {
  const getScoreColor = (score) => {
    if (score >= 90) return 'quality-score-excellent';
    if (score >= 70) return 'quality-score-good';
    if (score >= 50) return 'quality-score-fair';
    return 'quality-score-poor';
  };
  
  const getScoreIcon = (score) => {
    if (score >= 90) return <CheckCircle className="h-5 w-5" />;
    if (score >= 70) return <Info className="h-5 w-5" />;
    if (score >= 50) return <AlertTriangle className="h-5 w-5" />;
    return <XCircle className="h-5 w-5" />;
  };
  
  const getScoreLabel = (score) => {
    if (score >= 90) return 'Excellent';
    if (score >= 70) return 'Good';
    if (score >= 50) return 'Fair';
    return 'Poor';
  };
  
  return (
    <div className="metric-card">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          {subtitle && <p className="text-sm text-gray-600">{subtitle}</p>}
        </div>
        <div className={`flex items-center space-x-2 px-3 py-1 rounded-full ${getScoreColor(score)}`}>
          {getScoreIcon(score)}
          <span className="font-medium">{getScoreLabel(score)}</span>
        </div>
      </div>
      
      <div className="mt-4">
        <div className="flex items-baseline">
          <span className="text-3xl font-bold text-gray-900">{score}%</span>
          <span className="ml-2 text-sm text-gray-600">Quality Score</span>
        </div>
        
        <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all duration-300 ${
              score >= 90 ? 'bg-success-500' :
              score >= 70 ? 'bg-primary-500' :
              score >= 50 ? 'bg-warning-500' : 'bg-danger-500'
            }`}
            style={{ width: `${score}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default QualityScoreCard;