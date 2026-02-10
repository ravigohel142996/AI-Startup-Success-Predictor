"""
AI Startup Success Predictor - Streamlit Application
A modern web app for predicting startup success using machine learning
"""

import streamlit as st
import time
from model import predict_startup_success
from utils import (
    validate_inputs, 
    get_strategy_suggestions, 
    format_currency,
    get_success_color,
    get_score_color
)

# Page configuration
st.set_page_config(
    page_title="AI Startup Success Predictor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.75rem;
        font-size: 1.1rem;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .success-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        padding-bottom: 1rem;
    }
    h2 {
        color: #34495e;
        padding-top: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #7f8c8d;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    """Main application function"""
    
    # Header
    st.title("🚀 AI Startup Success Predictor")
    st.markdown(
        '<p class="subtitle">Predict your startup\'s success potential using AI-powered analytics</p>',
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # Sidebar with information
    with st.sidebar:
        st.header("📊 About This App")
        st.write("""
        This application uses a machine learning model to predict startup success based on key metrics:
        
        - **Funding Amount**: Total funding raised
        - **Team Size**: Number of team members
        - **Market Size**: Total addressable market
        - **Monthly Revenue**: Current monthly revenue
        - **Growth Rate**: Month-over-month growth
        
        The model classifies startups into three categories:
        - 🟢 High Potential
        - 🟡 Moderate Potential
        - 🔴 Low Potential
        """)
        
        st.markdown("---")
        st.info("💡 **Tip**: Realistic inputs lead to better predictions!")
    
    # Main input form
    st.header("📝 Enter Your Startup Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        funding = st.number_input(
            "💰 Funding Amount ($)",
            min_value=0,
            max_value=10000000000,
            value=500000,
            step=10000,
            help="Total funding raised by your startup"
        )
        
        team_size = st.number_input(
            "👥 Team Size",
            min_value=1,
            max_value=10000,
            value=10,
            step=1,
            help="Number of full-time team members"
        )
        
        market_size = st.number_input(
            "🎯 Market Size ($)",
            min_value=0,
            max_value=1000000000000,
            value=50000000,
            step=1000000,
            help="Total addressable market size"
        )
    
    with col2:
        revenue = st.number_input(
            "💵 Monthly Revenue ($)",
            min_value=0,
            max_value=1000000000,
            value=25000,
            step=1000,
            help="Current monthly recurring revenue"
        )
        
        growth_rate = st.number_input(
            "📈 Growth Rate (%)",
            min_value=-100.0,
            max_value=1000.0,
            value=15.0,
            step=0.5,
            help="Month-over-month growth percentage"
        )
    
    st.markdown("---")
    
    # Predict button
    if st.button("🔮 Predict Success Potential", type="primary"):
        # Validate inputs
        is_valid, error_message = validate_inputs(
            funding, team_size, market_size, revenue, growth_rate
        )
        
        if not is_valid:
            st.error(f"❌ {error_message}")
            return
        
        # Show progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🔍 Analyzing your startup data...")
        progress_bar.progress(25)
        time.sleep(0.3)
        
        status_text.text("🤖 Running AI prediction model...")
        progress_bar.progress(50)
        time.sleep(0.3)
        
        status_text.text("📊 Calculating success metrics...")
        progress_bar.progress(75)
        
        # Prepare features
        features = {
            'funding': funding,
            'team_size': team_size,
            'market_size': market_size,
            'revenue': revenue,
            'growth_rate': growth_rate
        }
        
        # Get prediction
        result = predict_startup_success(features)
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")
        time.sleep(0.5)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        # Display results
        st.markdown("---")
        st.header("🎯 Prediction Results")
        
        # Main metrics in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Success Score",
                value=f"{result['success_score']}/100",
                delta=None
            )
        
        with col2:
            prediction_color = get_success_color(result['prediction_label'])
            st.markdown(
                f"<div style='text-align: center;'>"
                f"<p style='color: #666; font-size: 0.9rem; margin: 0;'>Prediction</p>"
                f"<p style='color: {prediction_color}; font-size: 1.8rem; font-weight: bold; margin: 0;'>"
                f"{result['prediction_label']}</p></div>",
                unsafe_allow_html=True
            )
        
        with col3:
            st.metric(
                label="Confidence",
                value=f"{result['confidence']}%",
                delta=None
            )
        
        st.markdown("---")
        
        # Detailed probability breakdown
        st.subheader("📊 Probability Breakdown")
        
        prob_col1, prob_col2, prob_col3 = st.columns(3)
        
        with prob_col1:
            st.metric(
                label="🔴 Low Potential",
                value=f"{result['probabilities']['low']}%"
            )
        
        with prob_col2:
            st.metric(
                label="🟡 Moderate Potential",
                value=f"{result['probabilities']['moderate']}%"
            )
        
        with prob_col3:
            st.metric(
                label="🟢 High Potential",
                value=f"{result['probabilities']['high']}%"
            )
        
        st.markdown("---")
        
        # Strategy suggestions
        st.subheader("💡 Strategic Recommendations")
        suggestions = get_strategy_suggestions(result['prediction_label'], features)
        
        for i, suggestion in enumerate(suggestions, 1):
            st.markdown(f"**{i}.** {suggestion}")
        
        st.markdown("---")
        
        # Input summary
        with st.expander("📋 View Input Summary"):
            summary_col1, summary_col2 = st.columns(2)
            
            with summary_col1:
                st.write(f"**Funding:** {format_currency(funding)}")
                st.write(f"**Team Size:** {team_size} members")
                st.write(f"**Market Size:** {format_currency(market_size)}")
            
            with summary_col2:
                st.write(f"**Monthly Revenue:** {format_currency(revenue)}")
                st.write(f"**Growth Rate:** {growth_rate}%")
        
        # Success message
        if result['success_score'] >= 70:
            st.success("🎉 Excellent! Your startup shows strong potential for success!")
        elif result['success_score'] >= 40:
            st.info("💪 Good foundation! Focus on the recommendations to improve further.")
        else:
            st.warning("🔄 Consider pivoting or adjusting your strategy based on the recommendations.")


if __name__ == "__main__":
    main()
