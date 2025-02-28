# Automation-Forex: AI-Powered Trading Revolution 🚀

> *Exploring Forex Data with Ensemble Learning Models*
*Unleashing the future of forex, gold, and stock trading with cutting-edge AI! This project harnesses Python, Deep Learning, and advanced ML techniques to automate trading across 50+ currency pairs, delivering over 100,000 data points from MetaTrader5.*

![My Image](images/abc.jpg)

## Table of Contents
- [Project Overview](#automation-forex-ai-powered-trading-revolution-)
- [Features](#features)
- [Data & Methodology](#data--methodology)
- [Models & Workflow](#models--workflow)
- [Results](#results)
- [Getting Started](#getting-started)
- [Installation](#installation)

## Features
- Real-time automated trading for forex, gold, and stocks.
- Advanced predictive modeling with a suite of ML and DL algorithms.
- Dynamic data visualization to track market trends.
- Scalable deployment on VPS for MT5 integration.
- Daily performance reports and strategy optimization.

## Data & Methodology
This project aggregates data from over 50 currency pairs, gold, and various stocks, totaling nearly 100,000 data points collected via MetaTrader5. The methodology includes:
- **Data Collection**: Gathering high-quality market data.
- **Preprocessing & Exploration**: Analyzing trends and correlations across currency pairs.
- **Correlation Fusion**: Combining data from highly correlated assets for enhanced predictions.
- **Deployment**: Running the system on a VPS to execute trades on MT5.

## Models & Workflow
A robust pipeline powers this project, featuring:
1. **Data Ingestion**: Collecting and cleaning raw data.
2. **Exploratory Analysis**: Identifying common trends across currency pairs.
3. **Data Integration**: Merging correlated assets for robust modeling.
4. **Model Implementation**: Deploying a diverse set of algorithms:
   - Traditional ML: Random Forest, XGBoost, AdaBoost, CatBoost.
   - Deep Learning: LSTM, Bi-LSTM, Transformer, CNN-LSTM, GRU, Temporal Fusion Transformer (TFT).
5. **Model Filtering**: Eliminating low-accuracy models and those predicting significant losses.
6. **Ensemble Prediction**: Combining outputs from multiple models for optimal results.
7. **Post-Processing**: Adjusting bet ratios based on accuracy thresholds.
8. **Automation**: Deploying a self-running trading system with daily reports.

## Results
The models shine on test datasets, achieving:
- **Binary Classification**: Over 80% accuracy across 50+ currency pairs.
- **Ternary Classification**: 84% accuracy (up, down, sideways) on multi-label data.
These results highlight the project's potential for profitable, automated trading strategies.

## Getting Started
To set up and run the Automation-Forex project on your local machine, follow these steps:

### Clone the Repository
Download the project files to your system.
```bash
git clone https://github.com/AlexNhat/Automation-Forex.git
```

### Navigate to the Project Directory
Move into the cloned folder.
```bash
cd Automation-Forex
```

### Install Dependencies
Ensure you have Python installed (preferably 3.8+), then install the required libraries from the `requirements.txt` file.
```bash
pip install -r requirements.txt
```
> **Note:** The `requirements.txt` file contains all necessary packages, including libraries for machine learning (e.g., TensorFlow, Scikit-learn), data handling (e.g., Pandas, NumPy), and MetaTrader5 integration.

### Configure MetaTrader5
Set up your MT5 account and ensure the MT5 Python API is properly linked (details in the `docs/` folder if provided).

### Run the System
Execute the main script to start the automation process.
```bash
python main.py
```
