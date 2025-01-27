import requests
import re
import time

def check_received_emails(token, session_id, seen_mails):
    url = f"https://dropmail.me/api/graphql/{token}"
    query = f"""query {{
        session(id: "{session_id}") {{
            mails {{
                id,
                fromAddr,
                toAddr,
                headerSubject,
                text
            }}
        }}
    }}"""
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"query": query},
        )
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        data = response.json()

        mails = data.get("data", {}).get("session", {}).get("mails", [])
        for mail in mails:
            if mail["id"] not in seen_mails:
                seen_mails.add(mail["id"])
                
                # Tìm mã xác minh trong email
                six_digit_code = re.search(r'\b\d{6}\b', mail['text'])
                if six_digit_code:
                    code = six_digit_code.group()
                    return code  # Trả về mã xác minh
                else:
                    print("No 6-digit code found in this email.")
        time.sleep(1)  # Đợi 1 giây trước khi kiểm tra lại
    except requests.exceptions.RequestException as e:
        print(f"Error fetching emails: {str(e)}")
    return None

def main():
    session_id = input("Enter session_id: ")
    seen_mails = set()  # Tập hợp lưu trữ các email đã xử lý 
    code = check_received_emails("web-test-20250122pRGyt", session_id, seen_mails)
    print(f"Code: {code}")
if __name__ == "__main__":
    main()
