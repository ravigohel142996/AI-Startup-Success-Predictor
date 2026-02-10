"""
Machine Learning Model for Startup Success Prediction
This module trains a RandomForest classifier and provides prediction functionality.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


class StartupSuccessModel:
    """RandomForest model for predicting startup success"""
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def create_training_data(self):
        """
        Create synthetic training data for startup success prediction
        Features: [Funding, Team Size, Market Size, Monthly Revenue, Growth Rate]
        Labels: 0 (Low), 1 (Moderate), 2 (High)
        """
        np.random.seed(42)
        
        # Generate 1000 synthetic training samples
        n_samples = 1000
        
        # High Success Startups (label 2)
        high_funding = np.random.uniform(1000000, 10000000, n_samples // 3)
        high_team = np.random.uniform(20, 100, n_samples // 3)
        high_market = np.random.uniform(50000000, 500000000, n_samples // 3)
        high_revenue = np.random.uniform(100000, 1000000, n_samples // 3)
        high_growth = np.random.uniform(15, 50, n_samples // 3)
        high_samples = np.column_stack([high_funding, high_team, high_market, high_revenue, high_growth])
        high_labels = np.full(n_samples // 3, 2)
        
        # Moderate Success Startups (label 1)
        mod_funding = np.random.uniform(100000, 1000000, n_samples // 3)
        mod_team = np.random.uniform(5, 20, n_samples // 3)
        mod_market = np.random.uniform(10000000, 50000000, n_samples // 3)
        mod_revenue = np.random.uniform(10000, 100000, n_samples // 3)
        mod_growth = np.random.uniform(5, 15, n_samples // 3)
        mod_samples = np.column_stack([mod_funding, mod_team, mod_market, mod_revenue, mod_growth])
        mod_labels = np.full(n_samples // 3, 1)
        
        # Low Success Startups (label 0)
        low_funding = np.random.uniform(10000, 100000, n_samples // 3)
        low_team = np.random.uniform(1, 5, n_samples // 3)
        low_market = np.random.uniform(1000000, 10000000, n_samples // 3)
        low_revenue = np.random.uniform(0, 10000, n_samples // 3)
        low_growth = np.random.uniform(-5, 5, n_samples // 3)
        low_samples = np.column_stack([low_funding, low_team, low_market, low_revenue, low_growth])
        low_labels = np.full(n_samples // 3, 0)
        
        # Combine all samples
        X = np.vstack([high_samples, mod_samples, low_samples])
        y = np.concatenate([high_labels, mod_labels, low_labels])
        
        # Shuffle the data
        indices = np.random.permutation(len(X))
        X = X[indices]
        y = y[indices]
        
        return X, y
    
    def train(self):
        """Train the model on synthetic data"""
        X, y = self.create_training_data()
        
        # Standardize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train the model
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        return self
    
    def predict(self, features):
        """
        Predict startup success
        
        Args:
            features: dict with keys ['funding', 'team_size', 'market_size', 'revenue', 'growth_rate']
        
        Returns:
            tuple: (success_score, prediction_label, confidence)
        """
        if not self.is_trained:
            self.train()
        
        # Convert features dict to array
        X = np.array([[
            features['funding'],
            features['team_size'],
            features['market_size'],
            features['revenue'],
            features['growth_rate']
        ]])
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Get prediction and probabilities
        prediction = self.model.predict(X_scaled)[0]
        probabilities = self.model.predict_proba(X_scaled)[0]
        
        # Convert prediction to label
        labels = {0: "Low Potential", 1: "Moderate Potential", 2: "High Potential"}
        prediction_label = labels[prediction]
        
        # Calculate success score (0-100)
        # Weighted average of probabilities
        success_score = (probabilities[0] * 0 + probabilities[1] * 50 + probabilities[2] * 100)
        
        # Confidence is the max probability
        confidence = max(probabilities) * 100
        
        return success_score, prediction_label, confidence, probabilities


# Global model instance
_model_instance = None

def get_model():
    """Get or create the global model instance"""
    global _model_instance
    if _model_instance is None:
        _model_instance = StartupSuccessModel()
        _model_instance.train()
    return _model_instance


def predict_startup_success(data):
    """
    Main prediction function
    
    Args:
        data: dict with startup features
    
    Returns:
        dict with prediction results
    """
    model = get_model()
    success_score, prediction_label, confidence, probabilities = model.predict(data)
    
    return {
        'success_score': round(success_score, 2),
        'prediction_label': prediction_label,
        'confidence': round(confidence, 2),
        'probabilities': {
            'low': round(probabilities[0] * 100, 2),
            'moderate': round(probabilities[1] * 100, 2),
            'high': round(probabilities[2] * 100, 2)
        }
    }
