import requests
from colorama import init
init(autoreset=True)

# ANSI escape codes for text formatting
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN_COLOR = "\033[32m"  # Green
RED_COLOR = "\033[31m"    # Red
YELLOW_COLOR = "\033[33m"    # Yellow
WHITE_COLOR = "\033[37m"     # White
def add_time(token, equipment_id, user_id):
    url = "https://api.vmoscloud.com/vcpcloud/api/agentRewardDurationExchange/durationExchange"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en",
        "appversion": "1004000",
        "clienttype": "web",
        "connection": "keep-alive",
        "content-type": "application/json",
        "dnt": "1",
        "host": "api.vmoscloud.com",
        "origin": "https://cloud.vmoscloud.com",
        "referer": "https://cloud.vmoscloud.com/",
        "requestsource": "wechat-miniapp",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "suppliertype": "0",
        "token": token,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "userid": str(user_id)
    }

    payload = {
        "duration": 540,
        "equipmentId": equipment_id
    }

    # Sử dụng POST thay vì GET
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            response_data = response.json()
            print(f"{BOLD}{GREEN_COLOR}✅ Success Device +9H{RESET}")
            return response_data
        except ValueError:
            print(f"ERROR: Response is not in JSON format. Response: {response.text}")
            return None
    else:
        print(f"ERROR: Failed to add time. Status code: {response.status_code}, Response: {response.text}")
        return None


def main():
    token = "0WlRmrkVdDEftNuYiADz3gQrDzdDKQcf"
    equipment_id = 249467
    user_id = 239076

    result = add_time(token, equipment_id, user_id)
    if result:
        print("Response from API:", result)

if __name__ == "__main__":
    main()