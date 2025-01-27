import requests

def transfer_device(token, to_email, verify_code, equipment_ids):
    api_url="https://api.vmoscloud.com/vcpcloud/api/userEquipment/makeOverEquipments"

    # Dữ liệu gửi đi
    payload = {
        "makeOverMobilePhone": to_email,
        "verifyCode": verify_code,
        "equipmentIds": equipment_ids,
        "type": 0  # type mặc định = 0
    }

    # Headers cần thiết
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "token": token,  # Thay thế token nếu cần
        "clienttype": "web",
        "appversion": "1004000"
    }

    try:
        # Gửi yêu cầu POST đến API
        response = requests.post(api_url, json=payload, headers=headers)

        # Kiểm tra mã trạng thái
        if response.status_code == 200:
            return 1
        else:
            return 0
    except Exception as e:
        return {"msg": "An error occurred", "error": str(e)}
    
    
def main():
    print(transfer_device("aHU5Sj4euH50FVWT6QnHXkOMeoeDmJI8", "bhuy1212@gmail.com", "427767", [249466]))


if __name__ == "__main__":    
    main()