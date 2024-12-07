from datetime import datetime
import pytz
import MetaTrader5 as mt5
import pandas as pd

def get_history(symbol: str,  # Tên của cặp tiền tệ hoặc mã chứng khoán bạn muốn lấy lịch sử giao dịch.
                timeframe = mt5.TIMEFRAME_D1,  # Khung thời gian cho lịch sử giao dịch, mặc định là D1 (ngày).
                start_time: str = "2018-01-01T00:00:00",  # Thời điểm bắt đầu của khoảng thời gian lịch sử, mặc định là "2012-01-01".
                end_time: str = datetime.now().date().isoformat()): 
    
    # Thời điểm kết thúc của khoảng thời gian lịch sử, mặc định là ngày hiện tại.
    # str = datetime.now().date().isoformat()
    """
    Hàm này truy vấn và trả về dữ liệu lịch sử giao dịch cho một cặp tiền tệ hoặc mã chứng khoán được chỉ định từ MetaTrader 5.

    Parameters:
    - symbol (str): Tên của cặp tiền tệ hoặc mã chứng khoán bạn muốn lấy lịch sử giao dịch.
    - timeframe: Khung thời gian cho lịch sử giao dịch, mặc định là D1 (ngày).
    - start_time (str): Thời điểm bắt đầu của khoảng thời gian lịch sử, mặc định là "2012-01-01".
    - end_time (str): Thời điểm kết thúc của khoảng thời gian lịch sử, mặc định là ngày hiện tại.

    Returns:
    - pandas.DataFrame: DataFrame chứa dữ liệu lịch sử giao dịch, với cột 'time' làm chỉ mục và các cột 'open', 'high', 'low', 'close', 'volume' chứa giá trị tương ứng.
    """
    # Khởi tạo MetaTrader 5
    if not mt5.initialize():
        return {"error": "initialize() failed", "error_code": mt5.last_error()}
    if not mt5.symbol_select(symbol, True):
        return {"error": "Symbol selection failed", "symbol": symbol}
    # Đặt múi giờ thành UTC
    timezone = pytz.timezone("Etc/UTC")
    # Tính độ dài của khoảng thời gian từ start_time đến hiện tại
    start_time = datetime.fromisoformat(start_time).replace(tzinfo=timezone)
    end_time = datetime.fromisoformat(end_time).replace(tzinfo=timezone)
    len_of_bar = end_time - start_time
    # Truy vấn dữ liệu giá lịch sử
    history = mt5.copy_rates_from(symbol, timeframe, end_time, len_of_bar.days)
    if not mt5.symbol_select(symbol, True):
        return {"error": "Symbol selection failed", "symbol": symbol}
    rates_frame = pd.DataFrame(history)
    rates_frame.index = pd.to_datetime(rates_frame['time'], unit='s')
    rates_frame = rates_frame.loc[start_time.date():end_time.date()]
    rates_frame = rates_frame.rename(columns={'tick_volume': 'volume'})
    rates_frame = rates_frame.drop(['time', 'spread', 'real_volume'], axis=1)
    
    del history
    del timezone
    rates_frame = rates_frame[0:-1]
    return rates_frame

"""Đoạn code này có thể chỉnh sửa lấy loại tiền tệ theo yêu cầu"""
def get_data_with_vps(symbol, year):
    """
    Hàm này truy vấn và trả về dữ liệu lịch sử giao dịch cho một danh sách các cặp tiền tệ hoặc mã chứng khoán được chỉ định từ MetaTrader 5.

    Parameters:
    - symbols (list): Danh sách các cặp tiền tệ hoặc mã chứng khoán bạn muốn lấy dữ liệu lịch sử.

    Returns:
    - dict: Một từ điển chứa dữ liệu lịch sử giao dịch cho mỗi cặp tiền tệ hoặc mã chứng khoán. Khóa của từ điển là tên cặp tiền tệ hoặc mã chứng khoán, và giá trị tương ứng là một pandas.DataFrame chứa dữ liệu lịch sử giao dịch của cặp tiền tệ hoặc mã chứng khoán đó.
    """
    n = 0    
    while n<3:
             # Khởi tạo một từ điển để lưu trữ dữ liệu lịch sử giao dịch cho mỗi cặp tiền tệ hoặc mã chứng khoán.
  # Duyệt qua mỗi cặp tiền tệ hoặc mã chứng khoán trong danh sách được chỉ định.
        data = get_history(symbol, start_time= year) 
            # Kiem tra xem trung ngay voi hien tai hay khong
    # Kiem tra 3 lan
        
        last_index= data.index[-1]
        current_day = datetime.now().date().isoformat()
        comparison_date = pd.to_datetime(current_day)
        last_day = comparison_date - pd.Timedelta(days=1)
        if last_index == last_day:
            data = data.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"})
            
            del last_index
            del current_day
            del comparison_date
            del last_day
            # Tra ve du lieu
            return data
        else:
            n+=1
    print("Ngay nghi khong giao dich")
  
    return None# Trả về từ điển chứa dữ liệu lịch sử giao dịch cho tất cả các cặp tiền tệ hoặc mã chứng khoán được chỉ định.

# symbols = [
#         "EURCHF", "EURNZD", "CHFJPY", "EURGBP", "EURCAD", "GBPUSD", 
#         "GBPAUD", "AUDUSD", "USDCAD", "CADCHF", "USDCHF", "GBPJPY", 
#         "USDJPY", "AUDNZD", "CADJPY"
#     ]

# symbols = ["EURUSD", "EURAUD", "NZDCHF", "GBPCAD", "NZDCAD"]
# for sym in symbols:
#     data = get_data_with_vps(sym)
#     print(data)
    