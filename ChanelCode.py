import time
import SmsVerify
import CheckMail

def getChanelCode(token, user_id, email, dropmail_token, seen_mails, session_id):
    # Gửi SMS yêu cầu mã xác minh
    check_send_sms = 0
    while check_send_sms == 0:
        check_send_sms = SmsVerify.send_sms_verify(token, user_id, email)
        time.sleep(1)
    
    # Đợi một chút để email có thể được nhận
    time.sleep(5)
    
    # Kiểm tra mã xác minh đã nhận được từ email
    CodeVerify = CheckMail.check_received_emails(dropmail_token, session_id, seen_mails)
    
    # Gọi hàm Agent_verify để xác minh và lấy response
    response = SmsVerify.Agent_verify(token, user_id, email, CodeVerify)
    
    # Kiểm tra và xử lý phản hồi
    if response and response.get('data'):
        # Trả về channelCode từ dữ liệu của phản hồi
        channel_code = response['data'].get('channelCode')
        if channel_code:
            return channel_code  # Trả về channelCode khi có
        else:
            print("Error: 'channelCode' not found in the response.")
            return None
    else:
        print("Verification failed or no valid response received.")
        return None
