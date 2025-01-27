import requests
from colorama import init
init(autoreset=True)

# ANSI escape codes for text formatting
RESET = "\033[0m"
BOLD = "\033[1m"
SUCCESS_COLOR = "\033[32m"  # Green
ERROR_COLOR = "\033[31m"    # Red
EMAIL_COLOR = "\033[33m"    # Yellow
TEXT_COLOR = "\033[37m"     # White

# Hàm gửi SMS để yêu cầu mã xác minh
def send_sms_verify(token, user_id, email):
    url = "https://api.vmoscloud.com/vcpcloud/api/sms/smsSend"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "DNT": "1",
        "Host": "api.vmoscloud.com",
        "Origin": "https://cloud.vmoscloud.com",
        "Referer": "https://cloud.vmoscloud.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Token": token,  
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "appVersion": "1004000",
        "clientType": "web",
        "requestsource": "wechat-miniapp",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "userId": str(user_id), 
    }
    data = {
        "smsType": 13,
        "mobilePhone": email, 
    }
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code != 200:
        print(f"{BOLD}{ERROR_COLOR}ERROR: Failed to send SMS to {email} {RESET}")
        return 0
    else:
        return 1

# Hàm gửi SMS để yêu cầu mã xác minh
def Agent_verify(token, user_id, email, verifyCode):
    url = "https://api.vmoscloud.com/vcpcloud/api/agentUser/saveAgentUserInvite"
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en",
        "Connection": "keep-alive",
        "Content-Length": "23",
        "Content-Type": "application/json",
        "DNT": "1",
        "Host": "api.vmoscloud.com",
        "Origin": "https://cloud.vmoscloud.com",
        "Referer": "https://cloud.vmoscloud.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "SupplierType": "0",  # Bạn có thể thay đổi giá trị này nếu cần
        "Token": token,  # Thêm Token vào header
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "appVersion": "1004000",
        "clientType": "web",
        "requestsource": "wechat-miniapp",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "userId": str(user_id)  # userId là thông tin người dùng, có thể là số
    }
    
    # Dữ liệu (payload) cần gửi
    data = {
        "verifyCode": verifyCode  # Mã xác minh
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        # Kiểm tra mã trạng thái HTTP trả về
        if response.status_code != 200:
            print(f"ERROR: Failed to verify user {email}, status code: {response.status_code}")
            return None
        else:
            return response.json()  # Trả về kết quả từ API nếu thành công
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Request failed due to {e}")
        return None
