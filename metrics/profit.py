def calculate_total_profit(y_pred, prices):
    """
    Tính tổng lợi nhuận dựa trên dự đoán của meta-model.
    :param y_true: Nhãn thực tế (không nhất thiết sử dụng trong hàm này nhưng để cho mục đích so sánh).
    :param y_pred: Dự đoán từ meta-model.
    :param prices: Mảng giá tại mỗi điểm thời gian (ví dụ, giá đóng cửa của cổ phiếu).
    :return: Tổng lợi nhuận từ chiến lược.
    """
    profit = 0
    for i in range(1, len(prices)):
        if y_pred[i-1] == 1:  # Dự đoán là tăng
            profit += prices[i] - prices[i-1]  # Lợi nhuận từ việc mua và sau đó bán
        elif y_pred[i-1] == -1:  # Dự đoán là giảm
            profit += prices[i-1] - prices[i]  # Lợi nhuận từ việc bán và sau đó mua lại
    return profit

def caculate_profit(sym, total_profit):
  """Khởi tạo các biến để tính tiền cho forex"""
  usd_rate = {
    "EURCHF": 1.11, 
    "EURGBP": 1.22, 
    "GBPAUD": 0.64, 
    "EURJPY": 0.0066, 
    "USDCHF": 1.11, 
    "EURNZD": 0.59,  
    "AUDJPY": 0.0066, 
    "EURCAD": 0.72, 
    "NZDUSD": 1,
    "AUDCAD": 0.72, 
    "NZDJPY": 0.0066, 
    "GBPJPY": 0.0066, 
    "USDJPY": 0.0066, 
    "AUDNZD": 0.59,
    "USDCAD": 0.72 
  }
  volume = 0.01
  contract_size = 100000
  """Sau đó tính tiền"""
  profit = total_profit * volume * contract_size * usd_rate[sym]
  return profit
