"""
AI Startup Success Predictor - Streamlit Application
A modern web app for predicting startup success using machine learning
"""

import streamlit as st
import time
from datetime import datetime
from model import predict_startup_success, get_model
from utils import (
    validate_inputs, 
    get_strategy_suggestions, 
    format_currency,
    get_success_color,
    get_score_color
)
from visualizations import (
    create_probability_chart,
    create_success_gauge,
    create_feature_comparison_chart,
    create_feature_impact_chart,
    create_success_trajectory_chart
)
from analytics import (
    get_benchmark_data,
    calculate_feature_importance,
    generate_insights,
    calculate_runway_months,
    generate_comparison_metrics
)
from data_export import (
    prepare_export_data,
    create_csv_export,
    create_json_export,
    create_detailed_report_text,
    format_csv_download
)

# Constants for visualization tabs
VIZ_TAB_LABELS = [
    "📊 Probability Chart", 
    "🎯 Success Gauge", 
    "📉 Trajectory",
    "🔍 Comparison"
]

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
        
        # Visualizations
        st.markdown("---")
        st.subheader("📈 Interactive Visualizations")
        
        # Create tabs for different visualizations
        viz_tab1, viz_tab2, viz_tab3, viz_tab4 = st.tabs(VIZ_TAB_LABELS)
        
        with viz_tab1:
            st.plotly_chart(
                create_probability_chart(result['probabilities']),
                use_container_width=True
            )
        
        with viz_tab2:
            st.plotly_chart(
                create_success_gauge(result['success_score']),
                use_container_width=True
            )
        
        with viz_tab3:
            st.plotly_chart(
                create_success_trajectory_chart(result['success_score']),
                use_container_width=True
            )
            st.caption("📝 This projection shows potential growth scenarios based on your current success score")
        
        with viz_tab4:
            benchmark_data = get_benchmark_data(result['prediction_label'])
            st.plotly_chart(
                create_feature_comparison_chart(features, benchmark_data),
                use_container_width=True
            )
            st.caption("📝 Compare your metrics against industry benchmarks for your prediction category")
        
        st.markdown("---")
        
        # Advanced Analytics
        st.subheader("🔬 Advanced Analytics")
        
        # Generate insights
        insights = generate_insights(features, result['prediction_label'], result['success_score'])
        
        # Display insights in columns
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            st.markdown("**💪 Key Strengths**")
            if insights['strengths']:
                for strength in insights['strengths'][:3]:
                    st.success(f"**{strength['factor']}**: {strength['description']}")
            else:
                st.info("Focus on building fundamental strengths")
            
            st.markdown("**💰 Financial Health**")
            runway = calculate_runway_months(features)
            if isinstance(runway['runway_months'], str):
                st.success(f"✅ {runway['runway_months']}")
            else:
                color_map = {
                    'Excellent': 'success',
                    'Healthy': 'success',
                    'Adequate': 'info',
                    'Concerning': 'warning',
                    'Critical': 'error'
                }
                st_method = getattr(st, color_map.get(runway['status'], 'info'))
                st_method(f"**Estimated Runway:** {runway['runway_months']} months ({runway['status']})")
        
        with insight_col2:
            st.markdown("**⚠️ Risk Factors**")
            if insights['risk_factors']:
                for risk in insights['risk_factors'][:3]:
                    severity_emoji = {
                        'Critical': '🔴',
                        'High': '🟠',
                        'Medium': '🟡',
                        'Low': '🟢'
                    }
                    emoji = severity_emoji.get(risk['severity'], '⚪')
                    st.warning(f"{emoji} **{risk['factor']}**: {risk['description']}")
            else:
                st.success("No major risk factors identified!")
            
            st.markdown("**📊 Efficiency Metrics**")
            st.info(f"**Funding Adequacy:** {insights['funding_adequacy']['status']} ({insights['funding_adequacy']['score']}/100)")
            st.info(f"**Team Efficiency:** {insights['team_efficiency']['status']} ({insights['team_efficiency']['score']}/100)")
        
        # Feature Importance
        st.markdown("---")
        st.subheader("🎯 Feature Impact Analysis")
        
        model = get_model()
        feature_importance = calculate_feature_importance(model.model)
        
        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.plotly_chart(
                create_feature_impact_chart(feature_importance),
                use_container_width=True
            )
        with col_b:
            st.markdown("**What This Shows:**")
            st.write("This chart displays which features have the most impact on the prediction model's decisions.")
            st.write("Higher percentages indicate features that more strongly influence your success score.")
        
        # Comparison with typical startups
        st.markdown("---")
        st.subheader("📊 Comparative Analysis")
        
        comparisons = generate_comparison_metrics(features)
        comp_cols = st.columns(5)
        
        metrics_display = [
            ('funding', 'Funding', '💰'),
            ('team_size', 'Team', '👥'),
            ('market_size', 'Market', '🎯'),
            ('revenue', 'Revenue', '💵'),
            ('growth_rate', 'Growth', '📈')
        ]
        
        for idx, (key, label, emoji) in enumerate(metrics_display):
            with comp_cols[idx]:
                comp = comparisons[key]
                st.metric(
                    label=f"{emoji} {label}",
                    value=f"{comp['ratio']}x",
                    delta=comp['status'],
                    help=f"Your value vs typical startup"
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
        
        # Export functionality
        st.markdown("---")
        st.subheader("📥 Export Analysis")
        
        export_col1, export_col2, export_col3 = st.columns(3)
        
        with export_col1:
            # CSV Export
            csv_data = create_csv_export(features, result)
            csv_string = format_csv_download(csv_data)
            st.download_button(
                label="📊 Download CSV",
                data=csv_string,
                file_name=f"startup_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                help="Download results as CSV file"
            )
        
        with export_col2:
            # JSON Export
            export_data = prepare_export_data(features, result, insights)
            json_string = create_json_export(export_data)
            st.download_button(
                label="📋 Download JSON",
                data=json_string,
                file_name=f"startup_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                help="Download results as JSON file"
            )
        
        with export_col3:
            # Text Report Export
            report_text = create_detailed_report_text(features, result, insights)
            st.download_button(
                label="📄 Download Report",
                data=report_text,
                file_name=f"startup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                help="Download detailed text report"
            )
        
        st.markdown("---")
        
        # Success message
        if result['success_score'] >= 70:
            st.success("🎉 Excellent! Your startup shows strong potential for success!")
        elif result['success_score'] >= 40:
            st.info("💪 Good foundation! Focus on the recommendations to improve further.")
        else:
            st.warning("🔄 Consider pivoting or adjusting your strategy based on the recommendations.")


if __name__ == "__main__":
    main()
