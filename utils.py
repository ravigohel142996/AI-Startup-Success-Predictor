"""
Utility functions for the Startup Success Predictor
Includes input validation and helper functions
"""


def validate_inputs(funding, team_size, market_size, revenue, growth_rate):
    """
    Validate user inputs
    
    Args:
        funding: Funding amount in dollars
        team_size: Number of team members
        market_size: Total addressable market in dollars
        revenue: Monthly revenue in dollars
        growth_rate: Monthly growth rate percentage
    
    Returns:
        tuple: (is_valid, error_message)
    """
    errors = []
    
    # Validate funding
    if funding < 0:
        errors.append("Funding cannot be negative")
    if funding > 1e10:  # 10 billion
        errors.append("Funding amount seems unrealistic (max: $10B)")
    
    # Validate team size
    if team_size < 1:
        errors.append("Team size must be at least 1")
    if team_size > 10000:
        errors.append("Team size seems unrealistic (max: 10,000)")
    
    # Validate market size
    if market_size < 0:
        errors.append("Market size cannot be negative")
    if market_size > 1e12:  # 1 trillion
        errors.append("Market size seems unrealistic (max: $1T)")
    
    # Validate revenue
    if revenue < 0:
        errors.append("Revenue cannot be negative")
    if revenue > 1e9:  # 1 billion per month
        errors.append("Monthly revenue seems unrealistic (max: $1B/month)")
    
    # Validate growth rate
    if growth_rate < -100:
        errors.append("Growth rate cannot be less than -100%")
    if growth_rate > 1000:
        errors.append("Growth rate seems unrealistic (max: 1000%)")
    
    if errors:
        return False, "; ".join(errors)
    
    return True, ""


def get_strategy_suggestions(prediction_label, features):
    """
    Generate strategic suggestions based on prediction and input features
    
    Args:
        prediction_label: The predicted success level
        features: Dict of startup features
    
    Returns:
        list: Strategic suggestions
    """
    suggestions = []
    
    # Check funding level
    if features['funding'] < 100000:
        suggestions.append("💰 Consider seeking additional funding to scale operations")
    
    # Check team size
    if features['team_size'] < 5:
        suggestions.append("👥 Growing your team could help accelerate development")
    elif features['team_size'] > 50 and features['revenue'] < 50000:
        suggestions.append("⚖️ Team size seems large relative to revenue - optimize costs")
    
    # Check market size
    if features['market_size'] < 10000000:
        suggestions.append("🎯 Consider expanding to larger markets for better growth potential")
    
    # Check revenue
    if features['revenue'] < 10000:
        suggestions.append("💵 Focus on revenue generation and finding product-market fit")
    
    # Check growth rate
    if features['growth_rate'] < 5:
        suggestions.append("📈 Implement aggressive growth strategies to improve momentum")
    elif features['growth_rate'] > 30:
        suggestions.append("🚀 Excellent growth! Ensure infrastructure scales with demand")
    
    # Prediction-specific suggestions
    if prediction_label == "High Potential":
        suggestions.append("✨ Strong fundamentals! Focus on execution and scaling")
        suggestions.append("🎯 Consider strategic partnerships to accelerate market dominance")
    elif prediction_label == "Moderate Potential":
        suggestions.append("📊 Solid foundation - identify key metrics to push to next level")
        suggestions.append("🔍 Analyze competitors and find differentiation opportunities")
    else:  # Low Potential
        suggestions.append("🔄 Pivot consideration: Reassess product-market fit")
        suggestions.append("💡 Focus on lean operations and validated learning")
        suggestions.append("🤝 Seek mentorship and advisory support")
    
    # If no suggestions, add generic positive message
    if not suggestions:
        suggestions.append("Keep iterating and focusing on customer needs!")
    
    return suggestions[:5]  # Return max 5 suggestions


def format_currency(amount):
    """Format a number as currency"""
    if amount >= 1e9:
        return f"${amount/1e9:.2f}B"
    elif amount >= 1e6:
        return f"${amount/1e6:.2f}M"
    elif amount >= 1e3:
        return f"${amount/1e3:.2f}K"
    else:
        return f"${amount:.2f}"


def get_success_color(prediction_label):
    """Get color code based on prediction label"""
    colors = {
        "High Potential": "#28a745",  # Green
        "Moderate Potential": "#ffc107",  # Yellow
        "Low Potential": "#dc3545"  # Red
    }
    return colors.get(prediction_label, "#6c757d")


def get_score_color(score):
    """Get color based on success score"""
    if score >= 70:
        return "#28a745"  # Green
    elif score >= 40:
        return "#ffc107"  # Yellow
    else:
        return "#dc3545"  # Red
