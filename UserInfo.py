import requests
import hashlib

# Mã hóa md5
def md5_encode(input_string):
    # Tạo một đối tượng MD5
    md5_hash = hashlib.md5()
    # Mã hóa chuỗi đầu vào
    md5_hash.update(input_string.encode('utf-8'))
    # Trả về chuỗi mã hóa dạng hex
    return md5_hash.hexdigest()

def login_to_vmoscloud(mobile_phone, password):
    url = "https://api.vmoscloud.com/vcpcloud/api/user/login"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en",
        "Connection": "keep-alive",
        "Content-Length": "114",
        "Content-Type": "application/json",
        "DNT": "1",
        "Host": "api.vmoscloud.com",
        "Origin": "https://cloud.vmoscloud.com",
        "Referer": "https://cloud.vmoscloud.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "SupplierType": "0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "appVersion": "1004000",
        "channel": "web",
        "clientType": "web",
        "requestsource": "wechat-miniapp",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }
    data = {
        "mobilePhone": mobile_phone,
        "password": md5_encode(password),
        "loginType": 1,
        "channel": "web"
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("code") == 200 and "data" in response_data and "token" in response_data["data"]:
            token = response_data["data"]["token"]
            user_id = response_data["data"].get("userId", "")  # Extract userId from the response data
            return token, user_id
        else:
            print(f"ERROR: Unexpected response structure. Response: {response_data}")
            return None, None
    else:
        print(f"ERROR: Failed to login. Status code: {response.status_code}, Response: {response.text}")
        return None