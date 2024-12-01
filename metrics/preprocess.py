
import ta
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib


# Tính toán chỉ số kỹ thuật
# Thêm tất cả chỉ số kỹ thuật có sẵn
def add_technical_indicator(data_forex):
    """
    Thêm tất cả các chỉ số kỹ thuật có sẵn vào dữ liệu Forex.

    Parameters:
    - data_forex (DataFrame): DataFrame chứa dữ liệu Forex.

    Returns:
    - DataFrame: DataFrame chứa dữ liệu Forex đã được bổ sung các chỉ số kỹ thuật.
    """
    data_forex.index.name = 'Date'
    data_ori  = data_forex.rename(columns = {"Date":"DATE", "Open": "OPEN", "High": "HIGH", "Low": "LOW","Close": "CLOSE", "Volume": "VOLUME"  })
    data_add_ti = ta.add_all_ta_features(
        df=data_ori,

        open="OPEN",
        high="HIGH",
        low="LOW",
        close="CLOSE",
        volume="VOLUME",
        fillna=True
    )
    return data_add_ti


def setup_data(data_forex,sym_target, year):
    """
    Chỉnh sửa dữ liệu Forex và chuẩn bị các tập dữ liệu train và validation.

    Parameters:
    - data_forex (DataFrame): DataFrame chứa dữ liệu Forex.
    - diff_or_pct (int): Loại biến đổi, 1 nếu là diff(), 2 nếu là pct_change().
    - upper_rate (int): Phần trăm ngưỡng trên.
    - lower_rate (int): Phần trăm ngưỡng dưới.

    Returns:
    - list: Danh sách chứa các tập dữ liệu train và validation.
    """
    # Thêm data có indicators
    data_add_ti = add_technical_indicator(data_forex)
    
    # sau do load scaler
    data = data_add_ti.copy()
    
    scaler = joblib.load("scaler_data/" + "scaler_" + sym_target + "_" + str(year) + ".pkl")
    
    # transform cho scaler
    data_scaled = pd.DataFrame(scaler.transform(data))

    if 'DATE' in data_scaled.columns:
        data_scaled =data_scaled.drop(['DATE'], axis=1)
    
    del data_add_ti
    del data
    del scaler

    return data_scaled
