import sys
sys.path.append(r"C:\Users\Forex_lstm")
import joblib
sym_target = "AUDNZD"
year = 2021
scaler = joblib.load("scaler_data/" + "scaler_" + sym_target + "_" + str(year) + ".pkl")