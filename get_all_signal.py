from model_h5 import get_predict
import os
import csv
from datetime import datetime
import gc

def create_history_file():
    """
    Hàm này tạo file lịch sử giao dịch nếu không tồn tại.
    """
    history_file = r"C:\Users\Forex\CheckTradeSymbol\history_trade.csv"
    if not os.path.exists("CheckTradeSymbol"):
        os.makedirs("CheckTradeSymbol")
    if not os.path.exists(history_file):
        with open(history_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Symbol", "Prediction"])


def get_all_signal(all_symbols):
    """
    Hàm này nhận danh sách các biểu tượng và trả về một từ điển 
    chứa dự đoán cho mỗi biểu tượng.

    Parameters:
        all_symbols (list): Danh sách các biểu tượng cần dự đoán.

    Returns:
        dict: Từ điển chứa dự đoán cho mỗi biểu tượng.
    """
    current_date = datetime.now()
    current_date_str = current_date.strftime("%Y-%m-%d")

    # Tạo từ điển để lưu trữ dự đoán cho mỗi biểu tượng
    signal_all = {}
    n_symbol= len(all_symbols)

    # Đường dẫn tới file lịch sử giao dịch
    history_file = "CheckTradeSymbol/history_trade.csv"

    # Kiểm tra xem thư mục và file lịch sử có tồn tại không
    create_history_file()

    # Kiểm tra xem file lịch sử có tồn tại không
    if os.path.exists(history_file):
        # Nếu file tồn tại, đọc nội dung và kiểm tra dự đoán
        with open(history_file, mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Bỏ qua dòng tiêu đề
            for date, symbol, prediction in reader:
                # Nếu tồn tại thì lấy mã đó ra
                if (prediction is not None) and (symbol in all_symbols) and (date == current_date_str):
                # Ngược lại, sử dụng dự đoán từ file
                  signal_all[symbol] = int(prediction)
                  all_symbols.remove(symbol)
  

    # Kiểm tra xem tất cả các biểu tượng có dự đoán không
    if len(signal_all) == n_symbol and all(signal_all.values()):
        return signal_all

    # Nếu có biểu tượng nào chưa có dự đoán, thực hiện dự đoán cho nó
    for symbol in all_symbols:
        if symbol not in signal_all:
            pred = get_predict(symbol)
            signal_all[symbol] = pred

    # Ghi dự đoán vào file lịch sử
    with open(history_file, mode="a+", newline="") as file:
        writer = csv.writer(file)
        file.seek(0, os.SEEK_END)
        if file.tell() == 0:
            writer.writerow(["Date", "Symbol", "Prediction"])
        file.seek(0, os.SEEK_END)
        for symbol, prediction in signal_all.items():
            # Ghi dự đoán và ngày hiện tại vào file
            if (prediction is not None) and (symbol in all_symbols):
                writer.writerow([datetime.now().strftime("%Y-%m-%d"), symbol,prediction ])
    gc.collect()

    # Trả về từ điển chứa dự đoán cho mỗi biểu tượng
    return signal_all

    