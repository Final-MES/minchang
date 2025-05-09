import os
import pandas as pd
import requests
from datetime import datetime
import time

# 📁 CSV 데이터 폴더 경로
FOLDER_PATH = "C:/Users/minch/Desktop/Dataset_회전기계 고장유형 AI 데이터셋/data"
API_URL = "http://localhost:8000/vibration-data/bulk"
BATCH_SIZE = 200  # ⚙️ 한 번에 전송할 row 수

def upload_bulk(df, machine_name, sensor_no):
    bulk_data = []
    success, total = 0, 0

    for idx, row in df.iterrows():
        total += 1
        bulk_data.append({
            "machine_name": machine_name,
            "sensor_no": sensor_no,
            "measured_time": float(row[0]),
            "collected_at": datetime.now().isoformat(),
            "normal": float(row[1]),
            "unbalance": float(row[2]),
            "looseness": float(row[3]),
            "unbalance_looseness": float(row[4])
        })

        if len(bulk_data) >= BATCH_SIZE:
            res = requests.post(API_URL, json=bulk_data)
            if res.status_code == 200:
                inserted = res.json().get("inserted", 0)
                success += inserted
                print(f"[✅] {inserted}/{BATCH_SIZE} inserted (row {idx+1})")
            else:
                print(f"[❌] 실패 → {res.status_code}: {res.text}")
            bulk_data.clear()

    # ✅ 무조건 마지막까지 완료 로그 출력
    if bulk_data or total % BATCH_SIZE == 0:
        res = requests.post(API_URL, json=bulk_data)
        if res.status_code == 200:
            inserted = res.json().get("inserted", 0)
            success += inserted
            print(f"[✅] 마지막 {inserted}개 전송 완료")
        else:
            print(f"[❌] 마지막 전송 실패 → {res.status_code}: {res.text}")

    print(f"[📦] {machine_name}-{sensor_no} → 전체: {total}건, 성공: {success}건")

def main():
    start_time = time.time()

    for filename in os.listdir(FOLDER_PATH):
        if not filename.endswith(".csv"):
            continue

        file_path = os.path.join(FOLDER_PATH, filename)
        parts = filename.replace(".csv", "").split("_")
        machine_name = parts[0]
        sensor_no = parts[1]

        print(f"[🚀] 업로드 시작: {filename}")
        df = pd.read_csv(file_path, header=None)
        upload_bulk(df, machine_name, sensor_no)

    elapsed = round(time.time() - start_time, 2)
    print(f"\n🎉 전체 업로드 완료! ⏱️ 소요 시간: {elapsed}초")

if __name__ == "__main__":
    main()