# 🚀 AI Startup Success Predictor

A modern web application that uses machine learning to predict startup success potential based on key business metrics.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🌟 Features

- **AI-Powered Predictions**: Uses RandomForest classifier to predict startup success
- **Interactive UI**: Clean and modern interface built with Streamlit
- **Real-time Analysis**: Instant predictions with probability breakdowns
- **Strategic Recommendations**: Personalized suggestions based on your startup metrics
- **Visual Insights**: Color-coded results and detailed metrics display

## 📊 What It Predicts

The model analyzes five key metrics:
- 💰 **Funding Amount**: Total funding raised
- 👥 **Team Size**: Number of team members
- 🎯 **Market Size**: Total addressable market
- 💵 **Monthly Revenue**: Current monthly recurring revenue
- 📈 **Growth Rate**: Month-over-month growth percentage

Based on these inputs, it classifies startups into three categories:
- 🟢 **High Potential**: Strong fundamentals and growth trajectory
- 🟡 **Moderate Potential**: Solid foundation with room for improvement
- 🔴 **Low Potential**: Significant challenges requiring strategic changes

## 🏗️ Project Structure

```
AI-Startup-Success-Predictor/
│
├── app.py                 # Main Streamlit application
├── model.py               # ML model training and prediction logic
├── utils.py               # Helper functions and validation
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── assets/               # Directory for assets (images, etc.)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ravigohel142996/AI-Startup-Success-Predictor.git
   cd AI-Startup-Success-Predictor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   
   The app will automatically open at `http://localhost:8501`

## 🌐 Deploy on Streamlit Cloud

### Step-by-Step Deployment

1. **Push code to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

3. **Deploy the app**
   - Click "New app"
   - Select your repository: `ravigohel142996/AI-Startup-Success-Predictor`
   - Set main file path: `app.py`
   - Click "Deploy"

4. **Your app is live!**
   - Streamlit will provide a public URL
   - Share it with anyone!

### Deployment Configuration

No additional configuration needed! The app uses:
- Python 3.8+
- Dependencies from `requirements.txt`
- Default Streamlit settings

## 💻 Usage

1. **Enter Your Startup Metrics**
   - Fill in the funding amount, team size, market size, revenue, and growth rate
   - All fields have helpful tooltips

2. **Click "Predict Success Potential"**
   - Watch the AI analyze your data
   - Progress bar shows analysis stages

3. **Review Results**
   - See your success score (0-100)
   - Check the prediction category
   - Review probability breakdown

4. **Get Strategic Recommendations**
   - Personalized suggestions based on your metrics
   - Actionable insights to improve success potential

## 🧪 How It Works

### Machine Learning Model

The app uses a **RandomForest Classifier** trained on synthetic data:

- **Training Data**: 1,000 synthetic startup samples
- **Features**: 5 key business metrics
- **Classes**: 3 success categories (Low, Moderate, High)
- **Accuracy**: Optimized for realistic startup scenarios

### Prediction Process

1. **Input Validation**: Checks for realistic and valid inputs
2. **Feature Scaling**: Standardizes inputs using StandardScaler
3. **Model Prediction**: RandomForest classifier generates predictions
4. **Probability Calculation**: Computes confidence scores
5. **Strategy Generation**: Creates personalized recommendations

## 📁 File Descriptions

### `app.py`
Main Streamlit application with:
- UI components and layout
- Input forms and validation
- Results display and visualization
- Custom CSS styling

### `model.py`
Machine learning logic including:
- RandomForest classifier implementation
- Synthetic training data generation
- Prediction function
- Model training and persistence

### `utils.py`
Utility functions for:
- Input validation
- Strategy suggestion generation
- Currency formatting
- Color coding for results

### `requirements.txt`
Python dependencies:
- `streamlit`: Web application framework
- `numpy`: Numerical computations
- `scikit-learn`: Machine learning library

## 🎨 Customization

### Modify Training Data

Edit `model.py` to adjust the training data ranges:
```python
def create_training_data(self):
    # Adjust these ranges based on your needs
    high_funding = np.random.uniform(1000000, 10000000, n_samples // 3)
    # ... more customization
```

### Change UI Styling

Edit the CSS in `app.py`:
```python
st.markdown("""
    <style>
    /* Add your custom CSS here */
    </style>
    """, unsafe_allow_html=True)
```

### Add New Features

1. Update `model.py` to include new features in training
2. Add input fields in `app.py`
3. Update validation in `utils.py`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Machine learning powered by [scikit-learn](https://scikit-learn.org/)
- Inspired by startup analytics and predictive modeling

## 📧 Contact

**Ravi Gohel** - [@ravigohel142996](https://github.com/ravigohel142996)

Project Link: [https://github.com/ravigohel142996/AI-Startup-Success-Predictor](https://github.com/ravigohel142996/AI-Startup-Success-Predictor)

---

⭐ If you find this project useful, please consider giving it a star!
