from data_collection import get_data_with_vps
from metrics import preprocess
import pandas as pd
from tensorflow.keras.models import  load_model
import numpy as np

def get_predict(symbol):
    # Lay nam du lieu cu the
    
    df_check_year = pd.read_excel("year_symbol/check_year.xlsx")
    year_symbol = int(df_check_year[df_check_year["symbol"] == symbol]["year"].iloc[0])
    start_year = str(year_symbol)+ "-01-01T00:00:00"
    # lay nam bat dau sau do lay du lieu
    data  = get_data_with_vps(symbol, year= start_year)
    
    
    # Neu hom nay khong lay dc du lieu ma nay thi khong choi
    if data is None:
        return -1
    
    data_current= preprocess.setup_data(data, symbol, year = year_symbol)
    data_test = data_current[-50:]
    
    best_model = load_model("model_lstm/"+"model_"+ symbol+ "_" + str(year_symbol)+ ".h5")
    
    # Lay du doan bang cach predict
    X_new_eval = []
    # lay 10 ngay du lieu
    timesteps = 10
    for i in range(len(data_test) - timesteps + 1):
        X_new_eval.append(data_test[i:i + timesteps])
    # sau do dua ra du doan
    X_new = np.array(X_new_eval)
    y_pred_best = best_model.predict(X_new)
    y_pred_best_classes = np.argmax(y_pred_best, axis=1)
    y_pred = y_pred_best_classes[-1].astype(int)
    
    del best_model
    del data
    del data_current
    del X_new
    del X_new_eval
    del data_test
    
    return y_pred

# pred = get_predict("EURCHF")
# print(pred)