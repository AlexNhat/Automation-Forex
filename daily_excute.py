
from trading.login import login_mt5
from trading.order import close_order, get_current_order, place_order
from get_all_signal import get_all_signal
import MetaTrader5 as mt5
import pandas as pd
import gc

def check_current_order(current_orders, values):
    # Neu vua sideway vua k cos lenh thif tr ve 1
    if isinstance(current_orders, dict) and int(values)==1:
        return 1
        
    elif isinstance(current_orders, dict):
        return 2

    else:
        return 3
    
def check_exists_symbol(symbols_trade):
    """Hàm này dùng để check xem sự tồn tại của 1 list hoặc set symbol của tài khoản
    Đầu vào: là list hay set symbol
    Trả về: LÀ list hay set symbol đã được kiểm định"""
    symbol = pd.read_excel("year_symbol/check_year.xlsx")
    symbol_list = symbol["symbol"].values

    symbols_copy = list(symbols_trade)
    symbols_all = symbols_copy.copy()
    
    # print(symbols_copy)
    # print(symbol_list)
    for sym in symbols_all:

        if sym in symbol_list:
  
            pass
        else:
            symbols_copy.remove(sym)
    print(symbols_copy)
    return symbols_copy

def daily_execute(symbols = None):
    """Hàm Daily_excute dùng để thực hiện các tác vụ giao dịch trong tài khoản thông qua signal
    Đầu vào: Là list symbols hoặc không để gì
    Nếu có symbols đưa vào thì nó sẽ trade symbol đó trên toàn bộ tài khoản có được
    Nếu không có symbols được đưa vào nó sẽ truy cập tài khoản và lấy symbols của tài khoản đang giao dịch để dự đoán

    Các tác vụ thực hiện gồm giao dịch, đóng giao dịch, mở giao dịch mới

    Return: Về True hay False nếu giao dịch thành cồng"""
    # login_mt5(151652,"Forex_123")
    # Neu symbol khong None thi thuc thi predict
    if (symbols is not None) and (symbols != []):
        symbols_trade = symbols
        # Lay signal cua tung symbol
        signal = get_all_signal(symbols_trade) 

    accounts = pd.read_csv("account.csv")

    # Lay thong tin account
    for n in range(len(accounts)):
        # Đăng nhập vào tài khoản giao dịch 
        acc = int(accounts["account"][n])
        passw = accounts["password"][n]
        # Thực hiện đăng nhập
        mt5.initialize(login= acc, password= passw, server='ThinkMarkets-Demo' )
        print(mt5.initialize())
        account = mt5.account_info()
        
        # Kiem tra account cos cho phep trade hay khong
        # Neu khong thi tra ve
        if not account.trade_allowed:
            return True

        # Nếu không nhập gì thì lấy theo symbols của account
        if symbols is None: 
            symbol_trade = set()
            positions = mt5.positions_get()
            for pos in positions:
                symbol_trade.add(pos.symbol)
            
            
            symbols_trade = check_exists_symbol(symbol_trade)
            signal = get_all_signal(symbols_trade) #Lay signal de trade

        
        volume = 0.01  # Đặt volume cố định
            # Lấy tín hiệu giao dịch cho mỗi symbol
        
        for sym, values in signal.items():
            print(sym)
            # Neu chua ton tai thi ngat
            current_orders = get_current_order(sym)
            check_current = check_current_order(current_orders, values)
            print(current_orders)

            if check_current == 1:
                continue
            if check_current == 2:
                po  = place_order(sym, volume, int(values))
                # print("Thuc thi ham nay")
                print(po)
                continue

            """ 0 la sell, 1 la sideway, 2 la buy"""
            # Lấy danh sách các lệnh hiện có cho symbol
            for order in current_orders:
                if order.type == 0 and int(values) == 0: # truong hop nguowjc huong mua va ban
                    #order.type = 0  la buy 
                    
                    # Đóng lệnh hiện tại nếu loại lệnh không phù hợp với tín hiệu mới
                    co = close_order(sym, ticket=order.ticket)
                    print(co)
                    if co == 'xxx':
                        return False  # Dừng nếu không thể đóng lệnh
                    # Đặt lệnh mới nếu lệnh hiện tại được đóng thành công
                    po  = place_order(sym, volume, int(values)-1)
                    if po == 'xxx':
                        return False  # Dừng nếu không thể đặt lệnh mới
                
                if order.type == 1 and int(values) == 2: # truong hop nguowjc huong ban va mua
                    #order.type = 1 la sell
                    
                    # Đóng lệnh hiện tại nếu loại lệnh không phù hợp với tín hiệu mới
                    co = close_order(sym, ticket=order.ticket)
                    print(co)
                    if co == 'xxx':
                        return False  # Dừng nếu không thể đóng lệnh
                    # Đặt lệnh mới nếu lệnh hiện tại được đóng thành công
                    po  = place_order(sym, volume, int(values) -1)
                    if po == 'xxx':
                        return False  # Dừng nếu không thể đặt lệnh mới
                    
                if int(values) == 1: # Neu sideway thi xoa het
                    print("Da xoa")
                    co = close_order(sym, ticket=order.ticket)
      
        mt5.shutdown()
    gc.collect()
    return True
        
                    
    #return True  # Trả về True nếu tất cả các lệnh được xử lý thành công

# symbols = [
#         "EURCHF", "EURNZD","USDJPY", "USDCHF"
 
#     ]

# a = daily_execute(symbols)

#print(a) # Trả về True nếu tất cả các lệnh được xử lý thành công

