import MetaTrader5 as mt5
import pytz
from datetime import datetime
import pandas as pd
import time



def _RawOrder(order_type, symbol, volume, price, comment=None, ticket=None):
    # Định nghĩa lệnh giao dịch
    order = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": price,
        "deviation": 10,
    }

    # Thêm comment nếu có
    if comment is not None:
        order["comment"] = comment

    # Thêm ticket nếu có
    if ticket is not None:
        order["position"] = ticket

    # Gửi lệnh
    result = mt5.order_send(order)
    print(result)

    # Kiểm tra và xử lý kết quả gửi lệnh
    if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
        # Lệnh giao dịch thành công
        return True, f"Order executed successfully. Ticket: {result.order}", result
    elif result is not None:
        # Lệnh giao dịch thất bại, có mã lỗi
        error_message = mt5.last_error()
        return False, f"Order failed. Retcode: {result.retcode}. Error: {error_message}",result
    else:
        # Trường hợp không xác định (result is None)
        return False, "Order failed. No additional information available."
    
    
def Trade(action, symbol, volume, price=None, *, comment=None, ticket=None):
    """
    Thực hiện mua hoặc bán một lượng cố định của một loại tài sản (symbol) trên MetaTrader 5 (MT5).

    Parameters:
    - action: mt5.ORDER_TYPE_BUY hoặc mt5.ORDER_TYPE_SELL để chỉ định hành động là mua hoặc bán.
    - symbol: Tên của tài sản muốn giao dịch.
    - volume: Lượng tài sản muốn giao dịch.
    - price: Giá giao dịch mong muốn. Nếu None, sẽ giao dịch với giá thị trường hiện tại.
    - comment: Bình luận cho lệnh giao dịch (optional).
    - ticket: Ticket của lệnh giao dịch nếu có (optional).

    Returns:
    Tuple[bool, str] indicating success/failure and additional information or error message.
    """
    if price is not None:
        return _RawOrder(action, symbol, volume, price, comment, ticket)

    # Kiểm tra thông tin symbol trước khi giao dịch
    info = mt5.symbol_info_tick(symbol)
    if info is None:
        return False, "Symbol information not available"

    # Thực hiện giao dịch với giá thị trường
    for tries in range(10): # Thực hiện giao dịch 10 lần
        current_price = info.ask if action == mt5.ORDER_TYPE_BUY else info.bid
        result = _RawOrder(action, symbol, volume, current_price, comment, ticket)
        if result[0]:  # Kiểm tra nếu lệnh giao dịch thành công
            return result
        elif result[2].retcode not in [mt5.TRADE_RETCODE_REQUOTE, mt5.TRADE_RETCODE_PRICE_OFF]:
            break  # Ngừng thử nếu lỗi không phải do giá

    return result  # Trả về kết quả cuối cùng


def place_order(symbol, volume, order_type):
    if not mt5.initialize():
        return False, f"Error initializing MT5. Code: {mt5.last_error()}"

    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        return False, f"Symbol not found. Code: {mt5.last_error()}"

    account_info = mt5.account_info()
    if account_info is None:
        return False, "Unable to retrieve account information."

    # Tính toán margin yêu cầu
    margin_required = (volume * symbol_info.margin_initial)/30
    if account_info.margin_free < margin_required:
        return False, "Not enough money to place the order."

    # Đặt lệnh mua hoặc bán
    if order_type == 2:
        r = Trade(mt5.ORDER_TYPE_BUY,symbol, volume)
    elif order_type == 0:
        r = Trade(mt5.ORDER_TYPE_SELL,symbol, volume)
    else:
        return False, "Invalid order type."

    if r[0]:  # Nếu giao dịch thành công
        return True, f"Order placed. Details: {r[1]}"
    else:
        return False, f"Failed to place order. Details: {r[1]}"

def close_order(symbol, *, comment=None, ticket=None):
    """
    Close a trading order using the MetaTrader 5 (MT5) platform.

    Parameters:
    - symbol (str): The financial instrument symbol for the order to be closed (e.g., currency pair).
    - comment (str, optional): A user-defined comment or label for the closing order. Default is None.
    - ticket (int, optional): The ticket number of the order to be closed. Default is None.

    Returns:
    - tuple: A tuple containing a boolean indicating the success of the closing operation and a comment.

    Note:
    - If initialization of the MetaTrader 5 platform fails, the function prints an error message and quits.
    - The symbol_info function is used to check if the provided symbol is valid.
    - The positions_get function is used to retrieve information about open positions.
    - The _RawOrder function is a placeholder; you may need to replace it with the actual function for placing orders.

    Example Usage:
    success, close_comment = close_order('EURUSD', comment='Closing Order', ticket=12345)
    """
    if not mt5.initialize():
        return False, f"MT5 initialization failed. Error code: {mt5.last_error()}"

    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        return False, "Symbol not found. Please check the symbol name."


    positions = mt5.positions_get(ticket=ticket) if ticket else mt5.positions_get(symbol=symbol)
    if positions is None or len(positions) == 0:
        return False, "No open positions found for the given criteria."


    done = 0  # Counter for successfully closed positions
    for pos in positions:
        if pos.type in [mt5.ORDER_TYPE_BUY, mt5.ORDER_TYPE_SELL]:
            # Determine the closing order type
            close_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(symbol).ask if close_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid

            # Attempt to close the position
            result, order_mess, news = _RawOrder(close_type, symbol, pos.volume, price, comment, pos.ticket)
            print(result)
            if result:
                done += 1
                time.sleep(1)  # Throttle the closing attempts to avoid hitting rate limits
            else:
                # Handle other errors immediately without retrying
                return False, "Failed to close position. Error: " + str(order_mess)

    if done == len(positions):
        return True, "All positions closed successfully."
    else:
        return False, f"Closed {done} out of {len(positions)} positions. Some positions could not be closed."
    
    
def get_current_order(symbol,ticket=None):
    if not mt5.initialize():
        return {"error": "initialize() failed", "error_code": mt5.last_error()}
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        return {"error": "Invalid symbol"}
    if ticket is not None:
        positions = mt5.positions_get(ticket=ticket)
    else:
        positions = mt5.positions_get(symbol=symbol)
    if positions == ():
        return {"error": "No positions found for symbol"}
    return positions