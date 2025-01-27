import requests
# ANSI escape codes for text formatting
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN_COLOR = "\033[32m"  # Green
RED_COLOR = "\033[31m"    # Red
YELLOW_COLOR = "\033[33m"    # Yellow
WHITE_COLOR = "\033[37m"     # White

def send_sms(token, user_id, mobile_phone):
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
        "userId": str(user_id)  # Chuyển user_id thành chuỗi
    }
    data = {
        "smsType": 7,
        "mobilePhone": mobile_phone
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return 1
    else:
        print(f"{BOLD}{RED_COLOR}⛔️ ERROR: Failed to send SMS, Trying to resend{RESET}")
        return 0

def main():
    token = "JdYY5NewBqJmZGwBfEnt86kXwGtel1YO"
    user_id = 275578
    mobile_phone = "zf9pawr3@mailpwr.com"
    
    result = send_sms(token, user_id, mobile_phone)
    if result:
        print("Response from API:", result)
    
if __name__ == "__main__":
    main()
