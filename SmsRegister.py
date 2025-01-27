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
def send_sms(email):
    url = "https://api.vmoscloud.com/vcpcloud/api/sms/smsSend"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "smsType": 2,
        "mobilePhone": email,
        "captchaVerifyParam": "{\"sceneId\":\"5jvar3wp\",\"certifyId\":\"2kUIqW7\"}"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print(f"{BOLD}{ERROR_COLOR}ERROR: Failed to send SMS to {email}{RESET}")