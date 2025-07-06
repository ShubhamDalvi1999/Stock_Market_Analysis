# OI Pattern Classifier - Usage Guide

## Overview
This notebook implements a machine learning classifier to predict Open Interest (OI) patterns in futures and options trading data.

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r ../../requirements.txt
   ```

2. **Data Requirements**:
   - The notebook expects processed analysis data in `../../data/visualization/Processed_YYYYMMDD_Analysis.csv`
   - Data should contain columns: `INSTRUMENT`, `SYMBOL`, `PRICE_CHANGE`, `PRICE_CHANGE_PCT`, `CHG_IN_OI`, `OI_CHANGE_PCT`, `OI_PATTERN`

3. **Run the Notebook**:
   ```bash
   jupyter notebook OI_Pattern_Classifier.ipynb
   ```

## What the Notebook Does

### 1. Data Analysis
- Loads and explores the processed stock market data
- Analyzes the distribution of OI patterns
- Visualizes feature relationships

### 2. Model Training
- Trains a Random Forest classifier to predict OI patterns
- Uses features: Price Change, Price Change %, OI Change, OI Change %
- Evaluates model performance with confusion matrix and classification report

### 3. Model Comparison
- Uses LazyPredict to compare 30+ different ML algorithms
- Identifies the best performing models for the dataset

### 4. Pattern Prediction
- Provides a function to predict OI patterns for new data
- Shows feature importance and model interpretability

### 5. Model Persistence
- Saves trained model, scaler, and encoder for future use
- Creates summary statistics and performance metrics

## OI Pattern Types

- **Long Build-up**: Price ↑ & OI ↑ (Bulls adding positions)
- **Short Build-up**: Price ↓ & OI ↑ (Bears adding positions)
- **Long Unwinding**: Price ↓ & OI ↓ (Bulls exiting positions)
- **Short Covering**: Price ↑ & OI ↓ (Bears exiting positions)

## Output Files

The notebook generates:
- `../../models/oi_pattern_classifier_rf.pkl` - Trained Random Forest model
- `../../models/oi_pattern_scaler.pkl` - Feature scaler
- `../../models/oi_pattern_encoder.pkl` - Label encoder

## Business Applications

1. **Trading Strategy**: Predict market sentiment for better entry/exit decisions
2. **Risk Management**: Identify high-risk patterns early
3. **Portfolio Optimization**: Balance positions based on predicted patterns
4. **Market Analysis**: Understand price-volume relationships

## Next Steps

1. **Integration**: Use the saved models in production trading systems
2. **Enhancement**: Add more technical indicators and time-series features
3. **Automation**: Schedule regular model retraining with new data
4. **Visualization**: Create real-time dashboards showing pattern predictions 