"""
Data Export Module for Startup Success Predictor
Provides functionality to export results and analysis
"""

import pandas as pd
from datetime import datetime
import json


def prepare_export_data(features, result, insights=None):
    """
    Prepare data for export in various formats
    
    Args:
        features: dict with startup features
        result: dict with prediction results
        insights: optional dict with analytics insights
    
    Returns:
        dict: Formatted data ready for export
    """
    export_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'input_metrics': {
            'funding': features['funding'],
            'team_size': features['team_size'],
            'market_size': features['market_size'],
            'monthly_revenue': features['revenue'],
            'growth_rate': features['growth_rate']
        },
        'prediction': {
            'success_score': result['success_score'],
            'prediction_label': result['prediction_label'],
            'confidence': result['confidence'],
            'probabilities': result['probabilities']
        }
    }
    
    if insights:
        export_data['insights'] = insights
    
    return export_data


def create_csv_export(features, result):
    """
    Create CSV export data
    
    Args:
        features: dict with startup features
        result: dict with prediction results
    
    Returns:
        pandas DataFrame
    """
    data = {
        'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        'Funding ($)': [features['funding']],
        'Team Size': [features['team_size']],
        'Market Size ($)': [features['market_size']],
        'Monthly Revenue ($)': [features['revenue']],
        'Growth Rate (%)': [features['growth_rate']],
        'Success Score': [result['success_score']],
        'Prediction': [result['prediction_label']],
        'Confidence (%)': [result['confidence']],
        'Low Potential (%)': [result['probabilities']['low']],
        'Moderate Potential (%)': [result['probabilities']['moderate']],
        'High Potential (%)': [result['probabilities']['high']]
    }
    
    return pd.DataFrame(data)


def create_json_export(export_data):
    """
    Create JSON export string
    
    Args:
        export_data: dict with all export data
    
    Returns:
        str: JSON formatted string
    """
    return json.dumps(export_data, indent=2)


def create_detailed_report_text(features, result, insights=None):
    """
    Create a detailed text report
    
    Args:
        features: dict with startup features
        result: dict with prediction results
        insights: optional dict with analytics insights
    
    Returns:
        str: Formatted text report
    """
    report = []
    report.append("=" * 60)
    report.append("AI STARTUP SUCCESS PREDICTOR - ANALYSIS REPORT")
    report.append("=" * 60)
    report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    report.append("\n" + "-" * 60)
    report.append("INPUT METRICS")
    report.append("-" * 60)
    report.append(f"Funding Amount:        ${features['funding']:,.2f}")
    report.append(f"Team Size:             {features['team_size']} members")
    report.append(f"Market Size:           ${features['market_size']:,.2f}")
    report.append(f"Monthly Revenue:       ${features['revenue']:,.2f}")
    report.append(f"Growth Rate:           {features['growth_rate']}%")
    
    report.append("\n" + "-" * 60)
    report.append("PREDICTION RESULTS")
    report.append("-" * 60)
    report.append(f"Success Score:         {result['success_score']}/100")
    report.append(f"Prediction:            {result['prediction_label']}")
    report.append(f"Confidence:            {result['confidence']}%")
    
    report.append("\n" + "-" * 60)
    report.append("PROBABILITY BREAKDOWN")
    report.append("-" * 60)
    report.append(f"Low Potential:         {result['probabilities']['low']}%")
    report.append(f"Moderate Potential:    {result['probabilities']['moderate']}%")
    report.append(f"High Potential:        {result['probabilities']['high']}%")
    
    if insights:
        report.append("\n" + "-" * 60)
        report.append("DETAILED INSIGHTS")
        report.append("-" * 60)
        
        if 'strengths' in insights and insights['strengths']:
            report.append("\nSTRENGTHS:")
            for strength in insights['strengths']:
                report.append(f"  • {strength['factor']}: {strength['description']}")
        
        if 'risk_factors' in insights and insights['risk_factors']:
            report.append("\nRISK FACTORS:")
            for risk in insights['risk_factors']:
                report.append(f"  • {risk['factor']} ({risk['severity']}): {risk['description']}")
        
        if 'funding_adequacy' in insights:
            report.append(f"\nFunding Adequacy:      {insights['funding_adequacy']['status']}")
            report.append(f"  {insights['funding_adequacy']['message']}")
        
        if 'team_efficiency' in insights:
            report.append(f"\nTeam Efficiency:       {insights['team_efficiency']['status']}")
            report.append(f"  {insights['team_efficiency']['message']}")
        
        if 'growth_momentum' in insights:
            report.append(f"\nGrowth Momentum:       {insights['growth_momentum']['status']}")
            report.append(f"  {insights['growth_momentum']['message']}")
    
    report.append("\n" + "=" * 60)
    report.append("END OF REPORT")
    report.append("=" * 60)
    
    return "\n".join(report)


def format_csv_download(df):
    """
    Format DataFrame for CSV download
    
    Args:
        df: pandas DataFrame
    
    Returns:
        str: CSV formatted string
    """
    return df.to_csv(index=False)
