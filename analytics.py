"""
Analytics Module for Startup Success Predictor
Provides advanced analytics and benchmark data
"""

import numpy as np
from datetime import datetime, timedelta

# Constants for financial calculations
COST_PER_EMPLOYEE = 5000  # Estimated monthly cost per employee
OPERATIONAL_OVERHEAD = 1.2  # Operational overhead multiplier (20%)


def get_benchmark_data(prediction_label):
    """
    Get industry benchmark data based on prediction category
    
    Args:
        prediction_label: The predicted success level
    
    Returns:
        dict: Normalized benchmark values (0-100 scale)
    """
    benchmarks = {
        "High Potential": {
            'funding': 80,
            'team_size': 75,
            'market_size': 85,
            'revenue': 70,
            'growth_rate': 80
        },
        "Moderate Potential": {
            'funding': 50,
            'team_size': 45,
            'market_size': 55,
            'revenue': 50,
            'growth_rate': 50
        },
        "Low Potential": {
            'funding': 25,
            'team_size': 20,
            'market_size': 30,
            'revenue': 25,
            'growth_rate': 20
        }
    }
    
    return benchmarks.get(prediction_label, benchmarks["Moderate Potential"])


def calculate_feature_importance(model):
    """
    Calculate feature importance from the trained model
    
    Args:
        model: Trained RandomForest model
    
    Returns:
        dict: Feature names with importance percentages
    """
    feature_names = ['Funding', 'Team Size', 'Market Size', 'Monthly Revenue', 'Growth Rate']
    
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        # Convert to percentages
        total = sum(importances)
        importance_percentages = [(imp / total) * 100 for imp in importances]
        
        return dict(zip(feature_names, importance_percentages))
    else:
        # Default equal importance if model doesn't support it
        return {name: 20.0 for name in feature_names}


def generate_insights(features, prediction_label, success_score):
    """
    Generate detailed insights based on the analysis
    
    Args:
        features: dict with startup features
        prediction_label: The predicted success level
        success_score: float between 0-100
    
    Returns:
        dict: Various insights and metrics
    """
    insights = {
        'funding_adequacy': analyze_funding_adequacy(features),
        'team_efficiency': analyze_team_efficiency(features),
        'market_opportunity': analyze_market_opportunity(features),
        'revenue_health': analyze_revenue_health(features),
        'growth_momentum': analyze_growth_momentum(features),
        'risk_factors': identify_risk_factors(features, prediction_label),
        'strengths': identify_strengths(features, success_score)
    }
    
    return insights


def analyze_funding_adequacy(features):
    """Analyze if funding is adequate for current scale"""
    funding_per_employee = features['funding'] / max(features['team_size'], 1)
    
    if funding_per_employee > 100000:
        return {
            'status': 'Strong',
            'message': 'Funding level is healthy relative to team size',
            'score': 85
        }
    elif funding_per_employee > 50000:
        return {
            'status': 'Adequate',
            'message': 'Funding is reasonable but could be improved',
            'score': 60
        }
    else:
        return {
            'status': 'Concern',
            'message': 'Funding may be stretched thin for team size',
            'score': 35
        }


def analyze_team_efficiency(features):
    """Analyze team efficiency metrics"""
    revenue_per_employee = features['revenue'] / max(features['team_size'], 1)
    
    if revenue_per_employee > 10000:
        return {
            'status': 'Excellent',
            'message': 'High revenue per employee indicates strong efficiency',
            'score': 90
        }
    elif revenue_per_employee > 5000:
        return {
            'status': 'Good',
            'message': 'Team efficiency is solid',
            'score': 70
        }
    else:
        return {
            'status': 'Needs Improvement',
            'message': 'Focus on improving revenue per team member',
            'score': 40
        }


def analyze_market_opportunity(features):
    """Analyze market size opportunity"""
    revenue_market_ratio = (features['revenue'] * 12) / max(features['market_size'], 1)
    
    if revenue_market_ratio < 0.001:
        return {
            'status': 'Huge Opportunity',
            'message': 'Large untapped market potential',
            'score': 95
        }
    elif revenue_market_ratio < 0.01:
        return {
            'status': 'Good Opportunity',
            'message': 'Significant room for market expansion',
            'score': 75
        }
    else:
        return {
            'status': 'Limited',
            'message': 'Consider expanding to new markets',
            'score': 45
        }


def analyze_revenue_health(features):
    """Analyze revenue health indicators"""
    if features['revenue'] > 100000:
        return {
            'status': 'Strong',
            'message': 'Revenue demonstrates strong product-market fit',
            'score': 85
        }
    elif features['revenue'] > 10000:
        return {
            'status': 'Growing',
            'message': 'Revenue shows promising early traction',
            'score': 65
        }
    else:
        return {
            'status': 'Early Stage',
            'message': 'Focus on achieving product-market fit',
            'score': 35
        }


def analyze_growth_momentum(features):
    """Analyze growth rate and momentum"""
    growth_rate = features['growth_rate']
    
    if growth_rate > 20:
        return {
            'status': 'Exceptional',
            'message': 'Outstanding growth momentum',
            'score': 95
        }
    elif growth_rate > 10:
        return {
            'status': 'Strong',
            'message': 'Solid growth trajectory',
            'score': 75
        }
    elif growth_rate > 5:
        return {
            'status': 'Moderate',
            'message': 'Steady growth, room for acceleration',
            'score': 55
        }
    else:
        return {
            'status': 'Slow',
            'message': 'Growth needs significant improvement',
            'score': 30
        }


def identify_risk_factors(features, prediction_label):
    """Identify key risk factors"""
    risks = []
    
    if features['funding'] < 50000:
        risks.append({
            'factor': 'Underfunded',
            'severity': 'High',
            'description': 'Insufficient funding may limit growth'
        })
    
    if features['team_size'] < 3:
        risks.append({
            'factor': 'Small Team',
            'severity': 'Medium',
            'description': 'Limited team may slow execution'
        })
    
    if features['revenue'] < 5000:
        risks.append({
            'factor': 'Low Revenue',
            'severity': 'High',
            'description': 'Need to establish revenue stream'
        })
    
    if features['growth_rate'] < 0:
        risks.append({
            'factor': 'Negative Growth',
            'severity': 'Critical',
            'description': 'Declining metrics require immediate action'
        })
    
    if features['market_size'] < 5000000:
        risks.append({
            'factor': 'Small Market',
            'severity': 'Medium',
            'description': 'Limited market size may cap growth potential'
        })
    
    return risks


def identify_strengths(features, success_score):
    """Identify key strengths"""
    strengths = []
    
    if features['funding'] > 1000000:
        strengths.append({
            'factor': 'Well-Funded',
            'description': 'Strong financial backing for growth'
        })
    
    if features['team_size'] > 20:
        strengths.append({
            'factor': 'Strong Team',
            'description': 'Substantial team to execute on vision'
        })
    
    if features['revenue'] > 50000:
        strengths.append({
            'factor': 'Revenue Traction',
            'description': 'Demonstrated ability to generate revenue'
        })
    
    if features['growth_rate'] > 15:
        strengths.append({
            'factor': 'High Growth',
            'description': 'Strong momentum and market validation'
        })
    
    if features['market_size'] > 100000000:
        strengths.append({
            'factor': 'Large Market',
            'description': 'Significant opportunity for expansion'
        })
    
    if success_score > 70:
        strengths.append({
            'factor': 'Strong Overall Score',
            'description': 'Well-balanced metrics across all dimensions'
        })
    
    return strengths


def calculate_runway_months(features):
    """
    Calculate estimated runway in months
    
    Args:
        features: dict with startup features
    
    Returns:
        dict: Runway analysis
    """
    # Estimate monthly burn rate (simplified)
    monthly_burn = (features['team_size'] * COST_PER_EMPLOYEE) * OPERATIONAL_OVERHEAD
    monthly_net = features['revenue'] - monthly_burn
    
    if monthly_net >= 0:
        return {
            'runway_months': 'Indefinite (Cash Flow Positive)',
            'status': 'Excellent',
            'monthly_burn': monthly_burn,
            'monthly_net': monthly_net
        }
    else:
        runway = features['funding'] / abs(monthly_net) if monthly_net < 0 else float('inf')
        
        if runway > 18:
            status = 'Healthy'
        elif runway > 12:
            status = 'Adequate'
        elif runway > 6:
            status = 'Concerning'
        else:
            status = 'Critical'
        
        return {
            'runway_months': round(runway, 1),
            'status': status,
            'monthly_burn': monthly_burn,
            'monthly_net': monthly_net
        }


def generate_comparison_metrics(features):
    """
    Generate comparison metrics against typical startups
    
    Args:
        features: dict with startup features
    
    Returns:
        dict: Comparison metrics
    """
    # Typical startup benchmarks (median values)
    typical = {
        'funding': 250000,
        'team_size': 8,
        'market_size': 25000000,
        'revenue': 15000,
        'growth_rate': 10
    }
    
    comparisons = {}
    for key, value in features.items():
        typical_value = typical.get(key, 1)
        ratio = value / max(typical_value, 1)
        
        if ratio > 2:
            status = 'Well Above Average'
        elif ratio > 1.2:
            status = 'Above Average'
        elif ratio > 0.8:
            status = 'Average'
        elif ratio > 0.5:
            status = 'Below Average'
        else:
            status = 'Well Below Average'
        
        comparisons[key] = {
            'ratio': round(ratio, 2),
            'status': status,
            'typical_value': typical_value
        }
    
    return comparisons
