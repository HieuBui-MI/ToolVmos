import sys
import threading
import requests
import hashlib
import random
import time
import UserInfo
import ChanelCode
import CheckMail
import SmsTranfer
import DetecUserEquipments
import DeviceTransfer
import re
import AddTime
from colorama import init
init(autoreset=True)

# ANSI escape codes for text formatting
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN_COLOR = "\033[32m"  # Green
RED_COLOR = "\033[31m"    # Red
YELLOW_COLOR = "\033[33m"    # Yellow
WHITE_COLOR = "\033[37m"     # White

# Mã hóa md5
def md5_encode(input_string):
    # Tạo một đối tượng MD5
    md5_hash = hashlib.md5()
    # Mã hóa chuỗi đầu vào
    md5_hash.update(input_string.encode('utf-8'))
    # Trả về chuỗi mã hóa dạng hex
    return md5_hash.hexdigest()

# Hàm tạo session mới với một địa chỉ email ngẫu nhiên
def create_email_session(token):
    url = f"https://dropmail.me/api/graphql/{token}"
    query = """mutation {
        introduceSession {
            id,
            expiresAt,
            addresses {
                id,
                address
            }
        }
    }"""
    response = requests.post(
        url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"query": query},
    )
    data = response.json()
    return data["data"]["introduceSession"]

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
        print(f"{BOLD}{RED_COLOR}⛔️ ERROR: Failed to send SMS to {email}, Trying to resend{RESET}")
        return 0
    else:
        return 1

# Hàm đăng nhập bằng mã xác minh
def login_account(email, verify_code, channel):
    url = "https://api.vmoscloud.com/vcpcloud/api/user/login"
    raw_password = verify_code
    hashed_password = hashlib.md5(raw_password.encode()).hexdigest()
    data = {
        "mobilePhone": email,
        "loginType": 0,
        "verifyCode": raw_password,
        "password": hashed_password,
        "channel": "",
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en",
        "Content-Type": "application/json",
        "Origin": "https://cloud.vmoscloud.com",
        "Referer": "https://cloud.vmoscloud.com/",
        "SupplierType": "0",
        "Token": "jZIM7ryozuAJUvPqQQfVCi7YyatOZjvD",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "appVersion": "1004000",
        "channel": channel,
        "clientType": "web",
        "requestsource": "wechat-miniapp",
        "userId": "",
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("code") == 200 and "data" in response_data and "token" in response_data["data"]:
            token = response_data["data"]["token"]
            user_id = response_data["data"].get("userId", "")  # Extract userId from the response data
            return token, user_id
        else:
            print(f"{BOLD}{RED_COLOR}⛔️ ERROR: Unexpected response structure. Response: {response_data}")
            return None, None
    else:
        print(f"{BOLD}{RED_COLOR}⛔️ ERROR: Failed to login. Status code: {response.status_code}, Response: {response.text}")
        return None, None

# Hàm thực thi công việc cho từng tài khoản email
def process_account(dropmail_token, seen_mails, accounts, channel):
    try:
        # Bước 1: Tạo email ảo
        email_session = create_email_session(dropmail_token)
        email = email_session["addresses"][0]["address"]
        session_id = email_session["id"]

        # Bước 2: Gửi SMS để nhận mã xác minh
        check_send_sms = 0
        while check_send_sms == 0:
            check_send_sms = send_sms(email)
            time.sleep(1)
        
        # Bước 3: Kiểm tra email để nhận mã xác minh
        verify_code_register = None
        while not verify_code_register:
            verify_code_register = CheckMail.check_received_emails(dropmail_token, session_id, seen_mails)
            time.sleep(1)

        # Bước 4: Đăng nhập bằng mã xác minh
        token, user_id = login_account(email, verify_code_register, channel)

        # Bước 5: Lưu tài khoản, mật khẩu mã hóa và userId vào danh sách
        raw_password = verify_code_register
        if token and user_id:  # Ensure both token and user_id are valid
            accounts.append((email, raw_password, token, user_id, session_id))  # Lưu tài khoản, mật khẩu đã mã hóa và userId vào danh sách            
    except Exception as e:
        print(f"{BOLD}{RED_COLOR}⛔️ Exception occurred: {str(e)}{RESET}")

# Hàm trả về thời gian ngẫu nhiên từ 0.5 giây đến 2 giây
def get_random_delay():
    return random.uniform(0.5, 1.5)

# Main function
def main():
    ########Email Input########
    mobile_phone = input(f"✒️ Enter email address: ")
    email_pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
    if re.match(email_pattern, mobile_phone):
        print(f"{BOLD}{GREEN_COLOR}✅ Valid email: {mobile_phone}{RESET}")
    else:
        print(f"{BOLD}{RED_COLOR}⛔️ Invalid email. Please enter a valid Gmail address.{RESET}")
    
    ########Password Input########
    password = input(f"✒️ Emter password: ")

    ########Take user infomation########
    login_token_main, user_id_main = UserInfo.login_to_vmoscloud(mobile_phone, password)
    if login_token_main:
        print(f"{BOLD}{GREEN_COLOR}Token: {YELLOW_COLOR}{login_token_main} | {GREEN_COLOR}User ID: {YELLOW_COLOR}{user_id_main}{RESET}")
    DetecUserEquipments.get_equipment_info(login_token_main)
    
    ########Set up variables########
    dropmail_token = "web-test-20250122pRGyt"
    seen_mails = set()
    accounts1 = []  # Danh sách lưu tài khoản 1
    accounts2 = []  # Danh sách lưu tài khoản 2

    ########Create host accounts########
    while True:
        try:
            count = int(input(f"{BOLD}✒️ Enter the number of host accounts. The number must be between 1 and 26 (1 = 36 hours buff):{RESET} "))
            if count < 1 or count >= 26:
                print(f"{BOLD}{RED_COLOR}⛔️ Invalid input. Defaulting to 10.{RESET}")
                count = 20
                break
            else:
                break
        except ValueError:
            print(f"{BOLD}{RED_COLOR}⛔️ Invalid input. Defaulting to 10.{RESET}")
            count = 10
            break
    
    print(f"{BOLD}{GREEN_COLOR}\n✅ Generating email{RESET}")
    
    ########Create threads and process accounts########
    threads = []
    for i in range(count):
        time.sleep(0.3)
        thread = threading.Thread(target=process_account, args=(dropmail_token, seen_mails, accounts1, ""))
        threads.append(thread)
        thread.start()

    # Chờ cho đến khi tất cả các luồng hoàn thành
    for thread in threads:
        thread.join()

    # Sau khi tất cả luồng hoàn thành, in ra danh sách tài khoản đã tạo
    print("\nHost accounts list")
    for email, password, token, user_id, session_id in accounts1:
        print(f"{BOLD}{GREEN_COLOR}Account added: {YELLOW_COLOR}{email} | {password} | {token} | {user_id} | {session_id}{RESET}")
        
    # Nhap thong tin thiet bi
    equipment_id = input(f"{BOLD}✒️ Enter device id (device u want to buff):{RESET} ")  # Nhập mã thiết bị từ người dùng
    
    # Acc chinh qua host 1
    check_transfer_send_sms = 0
    while check_transfer_send_sms == 0:
        check_transfer_send_sms = SmsTranfer.send_sms(login_token_main, user_id_main, mobile_phone)
        time.sleep(1)
    print(f"{BOLD}{GREEN_COLOR}\n✅ Sms sent!{RESET}")
        
    google_verify_code = input(f"{BOLD}📩 Enter google verify code (go to your account's mail box):{RESET} ")  # Nhập mã thiết bị từ người dùng
    equipment_ids = [int(equipment_id)]
    
    print(f"{BOLD}{GREEN_COLOR}\n⌛ Transfer Device to host account 1/{count}...{RESET}")
    if DeviceTransfer.transfer_device(login_token_main, accounts1[0][0], google_verify_code, equipment_ids) == 1:    ####
        print(f"{BOLD}{GREEN_COLOR}\nTransfer Complete!{RESET}")
    else:
        print(f"{BOLD}{RED_COLOR}\nTransfer Failed!{RESET}")
        sys.exit()
        
    sumTime = 0
    temp_count = 0
    for email, password, token, user_id, session_id in accounts1:
        channel_code = ChanelCode.getChanelCode(token, user_id, email, dropmail_token, seen_mails, session_id)
        
        # Tạo tài khoản cho accounts2 (12 tài khoản tiếp theo)
        thread2s = []  # Danh sách chứa các luồng mới
        for i in range(12):  # Tạo 12 tài khoản mới
            # Tạo một luồng mới cho mỗi tài khoản email
            thread = threading.Thread(target=process_account, args=(dropmail_token, seen_mails, accounts2, channel_code))
            thread2s.append(thread)
            thread.start()

        # Chờ cho đến khi tất cả các luồng hoàn thành
        for thread in thread2s:
            thread.join()
            
        temp_count += 1
        index = temp_count+1
        
        for i in range(4):
            AddTime.add_time(token, equipment_id, user_id)  
            sumTime += 9               
        
        time.sleep(1)
        
        # Gửi tin nhắn
        check_transfer_send_sms = 0
        while check_transfer_send_sms == 0:
            check_transfer_send_sms = SmsTranfer.send_sms(token, user_id, email)
            time.sleep(1)
            
        verify_code = None
        while  not verify_code:
            verify_code = CheckMail.check_received_emails("web-test-20250122pRGyt", session_id, seen_mails)
        
        if temp_count == count:
            print(f"{BOLD}{GREEN_COLOR}\nTOTAL TIME BUFF {sumTime}{RESET}")
            print(f"{BOLD}{GREEN_COLOR}\n⌛ Transfer Device to original account ...{RESET}")
            DeviceTransfer.transfer_device(token, mobile_phone, verify_code, equipment_ids)
            print(f"{BOLD}{GREEN_COLOR}\n✅ Complete!{RESET}")
            print(f"{BOLD}{GREEN_COLOR}\nEnd!{RESET}")
        else:
            print(f"{BOLD}{GREEN_COLOR}\n⌛ Transfer Device to host account {index}/{count}...{RESET}")
            if DeviceTransfer.transfer_device(token, accounts1[temp_count][0], verify_code, equipment_ids) == 1:    ####
                print(f"{BOLD}{GREEN_COLOR}\n✅ Transfer Complete!{RESET}")   

            else:
                print(f"{BOLD}{RED_COLOR}\n⛔️ Transfer Failed!{RESET}")
                sys.exit()
            
if __name__ == "__main__":
    main()
