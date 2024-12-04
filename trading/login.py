import MetaTrader5 as mt5

def login_mt5(user_id, passwords, servers='ThinkMarkets-Demo'):
    """
    Đăng nhập vào MetaTrader 5 sử dụng thông tin tài khoản được cung cấp.

    Tham số:
    - user_id (str): Tên đăng nhập hoặc số tài khoản của người dùng.
    - passwords (str): Mật khẩu tương ứng với tài khoản.
    - servers (str): Tên máy chủ MetaTrader 5, mặc định là 'ThinkMarkets-Demo'.

    Returns:
    - Tuple[bool, str]: Một tuple chứa giá trị boolean chỉ định thành công của quá trình đăng nhập
                       và một chuỗi cung cấp thông tin bổ sung hoặc thông báo lỗi.

    Ghi chú:
    - Hàm này khởi tạo kết nối với nền tảng MetaTrader 5 và thực hiện đăng nhập sử dụng thông tin tài khoản.
    - Nếu quá trình khởi tạo không thành công, hàm trả về False cùng với thông báo lỗi.
    - Nếu đăng nhập thất bại, hàm trả về False cùng với mã lỗi.
    - Sau khi đăng nhập thành công, hàm thử truy cập thông tin tài khoản và trả về False nếu không thể.
    - Hàm trả về True nếu quá trình đăng nhập và truy cập thông tin tài khoản thành công.

    Ví dụ:
    ```
    success, result = login_mt5("your_user_id", "your_password")
    if success:
        print(f"Đăng nhập thành công: {result}")
    else:
        print(f"Đăng nhập thất bại. Lỗi: {result}")
    ```
    """

    try:
        if not mt5.initialize():
            raise RuntimeError(f"Error initializing MetaTrader 5. Error code: {mt5.last_error()}")

        login_result = mt5.login(user_id, password=passwords, server=servers)
        if not login_result:
            error_code = mt5.last_error()
            raise ValueError(f"Login failed. Error code: {error_code}")

        account_info = mt5.account_info()
        if account_info is None:
            raise ValueError("Unable to retrieve account information after successful login.")

        return True, "Login successful"

    except RuntimeError as e:
        # Xử lý lỗi khởi tạo MT5
        return False, str(e)

    except ValueError as e:
        # Xử lý lỗi đăng nhập hoặc lỗi truy cập thông tin tài khoản
        return False, str(e)

    except Exception as e:
        # Xử lý bất kỳ lỗi ngoại lệ nào khác không được dự đoán
        return False, f"An unexpected error occurred: {str(e)}"