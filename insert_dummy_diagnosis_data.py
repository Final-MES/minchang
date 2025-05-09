import requests
from datetime import datetime, timedelta
import random
from collections import defaultdict

# EC2 FastAPI 서버 주소
API_URL_INSERT = "http://3.34.90.243:8000/vibration-diagnosis/bulk"
API_URL_COUNT = "http://3.34.90.243:8000/vibration-diagnosis"

# 기계별 설정
MACHINE_CONFIG = {
    "g1": {"normal_prob": 0.9, "fault_probs": {1: 0.6, 2: 0.3, 3: 0.1}},
    "g2": {"normal_prob": 0.7, "fault_probs": {2: 0.5, 1: 0.3, 3: 0.2}},
    "g3": {"normal_prob": 0.5, "fault_probs": {3: 0.7, 1: 0.2, 2: 0.1}},
    "g4": {"normal_prob": 0.8, "fault_probs": {1: 0.4, 3: 0.4, 2: 0.2}},
    "g5": {"normal_prob": 0.6, "fault_probs": {2: 0.6, 3: 0.3, 1: 0.1}},
}

# 날짜별 고장율 조정 (2025년 4월 기준)
HIGH_FAULT_DATES = [datetime(2025, 4, 26).date(), datetime(2025, 4, 27).date()]

def weighted_random_choice(weight_dict):
    total = sum(weight_dict.values())
    r = random.uniform(0, total)
    upto = 0
    for k, w in weight_dict.items():
        if upto + w >= r:
            return k
        upto += w
    assert False, "Should not reach here"

def generate_dummy_data(num_records=10000):
    dummy_list = []
    now = datetime(2025, 4, 29, 12, 0, 0)  # 고정 기준 시간
    start_date = now - timedelta(days=7)

    for _ in range(num_records):
        machine = random.choice(list(MACHINE_CONFIG.keys()))
        config = MACHINE_CONFIG[machine]

        # 무작위 시간 생성
        random_seconds = random.randint(0, 7 * 24 * 60 * 60)
        detected_at = start_date + timedelta(seconds=random_seconds)
        detected_date = detected_at.date()

        # 고장 확률 조정
        if detected_date in HIGH_FAULT_DATES:
            normal_prob = config["normal_prob"] * 0.3  # 정상 확률 낮춤
        else:
            normal_prob = config["normal_prob"]

        # 고장 판단
        if random.random() < normal_prob:
            fault_type = 0
        else:
            fault_type = weighted_random_choice(config["fault_probs"])

        dummy_list.append({
            "machine_name": machine,
            "detected_at": detected_at,
            "fault_type": fault_type
        })

    # 시간순 정렬 + ISO 포맷
    dummy_list.sort(key=lambda x: x["detected_at"])
    for d in dummy_list:
        d["detected_at"] = d["detected_at"].isoformat()

    return dummy_list

def upload_batches(data, batch_size=1000):
    total_uploaded = 0
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        response = requests.post(API_URL_INSERT, json=batch)
        if response.status_code == 200:
            total_uploaded += len(batch)
            print(f"✅ 누적 {total_uploaded}개 업로드 완료: {response.json()}")
        else:
            print(f"❌ 업로드 실패 ({i} ~ {i+len(batch)}):", response.status_code, response.text)
            break
    return total_uploaded

def check_total_count():
    try:
        res = requests.get(API_URL_COUNT)
        res.raise_for_status()
        total = len(res.json())
        print(f"📊 현재 진단 데이터 총 {total}건 존재합니다.")
    except Exception as e:
        print(f"❌ 전체 데이터 수 조회 실패: {e}")

if __name__ == "__main__":
    print("🔧 진단 더미 데이터 생성 중...")
    data = generate_dummy_data(10000)
    print("🚀 업로드 시작...")
    upload_batches(data)
    print("🔍 업로드 후 DB 내 총 데이터 수 확인:")
    check_total_count()
