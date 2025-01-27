import threading
import re
import requests
import random
import time
from datetime import datetime

# Hàm tạo session email ngẫu nhiên
def create_email_session(token):
    url = f"https://dropmail.me/api/graphql/{token}"
    query = """mutation {
        introduceSession {
            id,
            addresses {
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

# Hàm gửi SMS
def send_sms(email):
    url = "https://api.vmoscloud.com/vcpcloud/api/sms/smsSend"
    headers = {"Content-Type": "application/json"}
    data = {
        "smsType": 2,
        "mobilePhone": email,
        "captchaVerifyParam": "{\"sceneId\":\"5jvar3wp\",\"certifyId\":\"2kUIqW7\"}"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print(f"ERROR: Failed to send SMS to {email}")

# Hàm kiểm tra email để lấy mã xác minh và xuất tất cả email hiện có
def check_received_emails(token, session_id):
    url = f"https://dropmail.me/api/graphql/{token}"
    query = f"""query {{
        session(id: "{session_id}") {{
            mails {{
                text
            }}
        }}
    }}"""
    response = requests.post(
        url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"query": query},
    )
    mails = response.json().get("data", {}).get("session", {}).get("mails", [])
    
    if mails:
        # print(f"Đã nhận {len(mails)} email(s):")
        # # for index, mail in enumerate(mails):
        # #     print(f"\nEmail {index + 1}:")
        # #     print(mail['text'])  # In nội dung email

        # Bạn có thể muốn trả về danh sách các mã xác minh nếu cần
        verification_codes = []
        for mail in mails:
            six_digit_code = re.search(r'\b\d{6}\b', mail['text'])
            if six_digit_code:
                verification_codes.append(six_digit_code.group())
        
        return verification_codes  # Trả về danh sách các mã xác minh tìm được

    print("Không có email nào.")
    return None


# Hàm thực thi cho mỗi tài khoản
def process_account(dropmail_token,typeSms):
    try:
        # Bước 1: Tạo email session
        email_session = create_email_session(dropmail_token)
        email = email_session["addresses"][0]["address"]
        session_id = email_session["id"]
        print(f"Tạo email: {email}")

        # Bước 2: Gửi SMS để nhận mã xác minh
        send_sms(email)

        # Bước 3: Kiểm tra email để lấy mã xác minh
        time.sleep(20)  # Delay 5 giây trước khi thông báo
        print(f"Đang chờ mã xác minh cho {email}...")

        verification_codes = []  # Danh sách các mã xác minh

        while not verification_codes:
            verification_codes = check_received_emails(dropmail_token, session_id)
            if not verification_codes:
                time.sleep(1)  # Delay 1 giây nếu chưa có mã

        # Lấy mã xác minh mới nhất (index cuối cùng của danh sách)
        latest_verification_code = verification_codes[-1] if verification_codes else None

        if latest_verification_code:
            print(f"Mã xác minh mới nhất cho {email}: {latest_verification_code}")
        else:
            print(f"Không tìm thấy mã xác minh cho {email}")
    except Exception as e:
        print(f"ERROR: {str(e)}")

# Hàm chính
def main():
    dropmail_token = "web-test-20250122pRGyt"

    # Nhập số lượng tài khoản cần tạo
    count = int(input("Nhập số lượng tài khoản: "))

    # Danh sách các luồng
    threads = []

    for _ in range(count):
        thread = threading.Thread(target=process_account, args=(dropmail_token,))
        threads.append(thread)
        thread.start()
        time.sleep(random.uniform(0.5, 1.5))  # Tạo delay ngẫu nhiên giữa các luồng

    # Chờ tất cả các luồng hoàn thành
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()