import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Shield, BarChart3, Upload, History, Clock, Sparkles } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/', label: 'Dashboard', icon: BarChart3, description: 'Monitor Quality' },
    { path: '/validate', label: 'Validate', icon: Upload, description: 'Check Data' },
    { path: '/history', label: 'History', icon: History, description: 'View Reports' },
    { path: '/schedule', label: 'Schedule', icon: Clock, description: 'Automate Jobs' },
  ];
  
  return (
    <nav className="bg-white shadow-lg border-b border-gray-200">
      <div className="container mx-auto px-6">
        <div className="flex items-center justify-between h-20">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <Shield className="h-10 w-10 text-gray-900" />
              <Sparkles className="h-4 w-4 text-yellow-500 absolute -top-1 -right-1" />
            </div>
            <div>
              <span className="text-2xl font-bold text-gray-900">DQ-Guard</span>
              <p className="text-sm text-gray-600 font-medium">Data Quality Framework</p>
            </div>
          </div>
          
          <div className="flex space-x-2">
            {navItems.map(({ path, label, icon: Icon, description }) => (
              <Link
                key={path}
                to={path}
                className={`nav-link ${
                  location.pathname === path
                    ? 'nav-link-active'
                    : 'nav-link-inactive'
                }`}
              >
                <Icon className="h-5 w-5" />
                <div className="text-left">
                  <div className="font-semibold">{label}</div>
                  <div className="text-xs opacity-75">{description}</div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;