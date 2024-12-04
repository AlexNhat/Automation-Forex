import datetime
import pytz
import time
from daily_excute import daily_execute
import gc
# import schedule

def get_current_time_VN():
    # Đặt múi giờ cho Việt Nam
    vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')

    # Lấy ngày giờ hiện tại theo múi giờ Việt Nam
    current_time_VN = datetime.datetime.now(vn_timezone)

    return current_time_VN

def config_frequency():
    """
    Configures and runs a scheduled task at a specified frequency, executing the 'daily_execute' function.

    This function performs the following tasks:
    1. Invokes the 'daily_execute' function to execute daily trading operations immediately and stores the result.
    2. Sets up a recurring schedule using the 'schedule' module to run the 'daily_execute' function at specified intervals.
    3. Enters a loop where the schedule is checked and the 'daily_execute' function is executed periodically.
    4. Prints 'True' in each iteration.
    5. If the result of the initial 'daily_execute' is True, continues running the scheduled task and the loop.
       - If the result is False, the loop breaks, and the function returns False.
    Note:
    - The 'daily_execute' function should be correctly implemented and available in the 'daily_execute' module.
    - Adjust the 'daily_execute' function and its return values as needed for your specific use case.
    Example Usage:
    success = config_frequency(1)  # Schedule to run every 1 hour
    if success:
        print("Configuration completed successfully.")
    else:
        print("Error occurred during configuration.")

    :param schedule_time: The frequency at which the 'daily_execute' function should be scheduled (in hours).
    :return: True if the initial execution and scheduling are successful, False if any operation fails.
    """
    # Lấy thời gian hiện tại của Việt Nam
  

    # Lặp vô hạn cho đến khi kết quả của 'daily_execute' là False
    while True:
        current_time_VN = get_current_time_VN()
    
    # # Tính toán thời gian 4 giờ sáng ngày mai
    #     tomorrow_4am = current_time_VN.replace(hour=4, minute=15, second=0, microsecond=0) + datetime.timedelta(days=1)
        if current_time_VN.weekday() in (5, 6):
            print("Hôm nay là thứ 7 hoặc chủ nhật, nghỉ ngơi.")
            time.sleep(1800)  # Chờ 1 phút và kiểm tra lại
            continue
        
        # Thực hiện các công việc lên lịch
        if (current_time_VN.hour >=4 and current_time_VN.minute >= 15) or current_time_VN <=5:
            

            print("Thuc hien du doan va giao dich ngay: ", current_time_VN)
            result = daily_execute(symbol =  ["EURCHF", "EURNZD", "AUDNZD"
                                              ,"USDJPY", "USDCHF", "USDCAD"
                                              ,"EURCAD", "EURGBP", "GBPUSD", 
                                              "GBPAUD", "EURAUD", "GBPCAD"]) 
            if result is None:
                print("Ngay nghi le khong giao dich duoc")
            # In ra 'True' trong mỗi lần lặp
            else:
                print("Thuc hien giao dich thanh cong")
        
        time.sleep(60)
        del current_time_VN
        
        gc.collect()
    
    return False

# a = config_frequency()
