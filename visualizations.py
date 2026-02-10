"""
Visualization Module for Startup Success Predictor
Provides various charts and graphs for data visualization
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots


def create_probability_chart(probabilities):
    """
    Create a bar chart showing probability distribution across categories
    
    Args:
        probabilities: dict with keys 'low', 'moderate', 'high'
    
    Returns:
        plotly figure object
    """
    categories = ['Low Potential', 'Moderate Potential', 'High Potential']
    values = [probabilities['low'], probabilities['moderate'], probabilities['high']]
    colors = ['#dc3545', '#ffc107', '#28a745']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=[f'{v:.1f}%' for v in values],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title='Success Probability Distribution',
        xaxis_title='Success Category',
        yaxis_title='Probability (%)',
        yaxis_range=[0, 100],
        height=400,
        showlegend=False,
        template='plotly_white'
    )
    
    return fig


def create_success_gauge(success_score):
    """
    Create a gauge chart showing the success score
    
    Args:
        success_score: float between 0-100
    
    Returns:
        plotly figure object
    """
    # Determine color based on score
    if success_score >= 70:
        color = '#28a745'
    elif success_score >= 40:
        color = '#ffc107'
    else:
        color = '#dc3545'
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=success_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Success Score", 'font': {'size': 24}},
        delta={'reference': 50, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#ffebee'},
                {'range': [40, 70], 'color': '#fff8e1'},
                {'range': [70, 100], 'color': '#e8f5e9'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


def create_feature_comparison_chart(features, benchmark_data):
    """
    Create a radar chart comparing user's metrics with benchmarks
    
    Args:
        features: dict with startup features
        benchmark_data: dict with benchmark values for each category
    
    Returns:
        plotly figure object
    """
    categories = ['Funding', 'Team Size', 'Market Size', 'Revenue', 'Growth Rate']
    
    # Normalize features to 0-100 scale for comparison
    user_values = [
        min(features['funding'] / 10000000 * 100, 100),  # Cap at 10M
        min(features['team_size'] / 100 * 100, 100),  # Cap at 100
        min(features['market_size'] / 500000000 * 100, 100),  # Cap at 500M
        min(features['revenue'] / 1000000 * 100, 100),  # Cap at 1M
        min(features['growth_rate'] / 50 * 100, 100)  # Cap at 50%
    ]
    
    # Get benchmark values
    benchmark_values = [
        benchmark_data['funding'],
        benchmark_data['team_size'],
        benchmark_data['market_size'],
        benchmark_data['revenue'],
        benchmark_data['growth_rate']
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=user_values,
        theta=categories,
        fill='toself',
        name='Your Startup',
        line_color='#4CAF50'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=benchmark_values,
        theta=categories,
        fill='toself',
        name='Industry Benchmark',
        line_color='#2196F3'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title='Metrics Comparison vs. Industry Benchmark',
        height=500
    )
    
    return fig


def create_feature_impact_chart(feature_importance):
    """
    Create a horizontal bar chart showing feature importance
    
    Args:
        feature_importance: dict with feature names and importance scores
    
    Returns:
        plotly figure object
    """
    features = list(feature_importance.keys())
    importance = list(feature_importance.values())
    
    fig = go.Figure(go.Bar(
        x=importance,
        y=features,
        orientation='h',
        marker_color='#4CAF50',
        text=[f'{v:.1f}%' for v in importance],
        textposition='auto',
    ))
    
    fig.update_layout(
        title='Feature Importance in Prediction',
        xaxis_title='Importance (%)',
        yaxis_title='Features',
        height=400,
        showlegend=False,
        template='plotly_white'
    )
    
    return fig


def create_metrics_overview(features):
    """
    Create a multi-chart overview of all metrics
    
    Args:
        features: dict with startup features
    
    Returns:
        plotly figure object with subplots
    """
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=('Funding', 'Team Size', 'Market Size', 
                       'Monthly Revenue', 'Growth Rate', 'Summary'),
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}],
               [{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'table'}]]
    )
    
    # Format currency for display
    def format_currency(amount):
        if amount >= 1e9:
            return f"${amount/1e9:.2f}B"
        elif amount >= 1e6:
            return f"${amount/1e6:.2f}M"
        elif amount >= 1e3:
            return f"${amount/1e3:.2f}K"
        else:
            return f"${amount:.2f}"
    
    # Add indicators
    fig.add_trace(go.Indicator(
        mode="number",
        value=features['funding'],
        title={'text': "Funding"},
        number={'prefix': "$", 'valueformat': ",.0f"},
    ), row=1, col=1)
    
    fig.add_trace(go.Indicator(
        mode="number",
        value=features['team_size'],
        title={'text': "Team Size"},
    ), row=1, col=2)
    
    fig.add_trace(go.Indicator(
        mode="number",
        value=features['market_size'],
        title={'text': "Market Size"},
        number={'prefix': "$", 'valueformat': ",.0f"},
    ), row=1, col=3)
    
    fig.add_trace(go.Indicator(
        mode="number",
        value=features['revenue'],
        title={'text': "Monthly Revenue"},
        number={'prefix': "$", 'valueformat': ",.0f"},
    ), row=2, col=1)
    
    fig.add_trace(go.Indicator(
        mode="number",
        value=features['growth_rate'],
        title={'text': "Growth Rate"},
        number={'suffix': "%"},
    ), row=2, col=2)
    
    # Add summary table
    fig.add_trace(go.Table(
        header=dict(values=['Metric', 'Value'],
                   fill_color='paleturquoise',
                   align='left'),
        cells=dict(values=[
            ['Funding', 'Team', 'Market', 'Revenue', 'Growth'],
            [format_currency(features['funding']),
             f"{features['team_size']} members",
             format_currency(features['market_size']),
             format_currency(features['revenue']),
             f"{features['growth_rate']}%"]
        ],
        fill_color='lavender',
        align='left')
    ), row=2, col=3)
    
    fig.update_layout(height=600, showlegend=False)
    
    return fig


def create_success_trajectory_chart(success_score):
    """
    Create a visualization showing potential growth trajectory
    
    Args:
        success_score: float between 0-100
    
    Returns:
        plotly figure object
    """
    months = list(range(0, 13))
    
    # Generate trajectories based on success score
    if success_score >= 70:
        growth_rate = 0.15  # 15% monthly growth for high potential
    elif success_score >= 40:
        growth_rate = 0.08  # 8% monthly growth for moderate
    else:
        growth_rate = 0.03  # 3% monthly growth for low potential
    
    base_value = 100
    trajectory = [base_value * ((1 + growth_rate) ** month) for month in months]
    
    # Also show alternative scenarios
    optimistic = [base_value * ((1 + growth_rate * 1.5) ** month) for month in months]
    conservative = [base_value * ((1 + growth_rate * 0.5) ** month) for month in months]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months, y=trajectory,
        mode='lines+markers',
        name='Expected Growth',
        line=dict(color='#4CAF50', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=optimistic,
        mode='lines',
        name='Optimistic Scenario',
        line=dict(color='#81C784', width=2, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=conservative,
        mode='lines',
        name='Conservative Scenario',
        line=dict(color='#FFB74D', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title='Projected Growth Trajectory (12 Months)',
        xaxis_title='Months',
        yaxis_title='Relative Growth Index',
        height=400,
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig
