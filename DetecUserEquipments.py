import requests

# Hàm lấy thông tin equipmentId, padName, goodMonthName và hiệu thời gian từ VMOS Cloud
def get_equipment_info(token):
    url = "https://api.vmoscloud.com/vcpcloud/api/userEquipment/list?supplierType=-1&queryAuthorizedEquipments=true"
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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "appVersion": "1004000",
        "channel": "web",
        "clientType": "web",
        "requestsource": "wechat-miniapp",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "token": token
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("code") == 200 and "data" in response_data:
            # Header cho bảng dữ liệu
            print(f"{'Equipment ID':<15} | {'Pad Name':<20} | {'Good Month Name':<15} | {'Time Difference':<25}")
            print("-" * 80)

            # Duyệt qua danh sách thiết bị
            for equipment in response_data["data"]:
                for user_pad in equipment["userPads"]:
                    equipment_id = user_pad.get("equipmentId", "N/A")
                    pad_name = user_pad.get("padName", "N/A")
                    good_month_name = user_pad.get("goodMonthName", "N/A")
                    sign_expiration_time = user_pad.get("signExpirationTimeTamp")
                    ts = response_data.get("ts")  # Lấy giá trị ts từ response

                    # Tính hiệu giữa signExpirationTimeTamp và ts (ms -> ngày, giờ, phút)
                    if sign_expiration_time and ts:
                        time_difference = sign_expiration_time - ts
                        days = time_difference // (1000 * 60 * 60 * 24)
                        hours = (time_difference // (1000 * 60 * 60)) % 24
                        minutes = (time_difference // (1000 * 60)) % 60
                        time_diff_str = f"{days}d {hours}h {minutes}m"
                    else:
                        time_diff_str = "N/A"

                    # Hiển thị dữ liệu trên một hàng ngang
                    print(f"{equipment_id:<15} | {pad_name:<20} | {good_month_name:<15} | {time_diff_str:<25}")
        else:
            print(f"ERROR: Unexpected response structure. Response: {response_data}")
    else:
        print(f"ERROR: Failed to get equipment info. Status code: {response.status_code}, Response: {response.text}")