import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_URL = "http://localhost:8000/vibration-diagnosis"  # FastAPI 진단 데이터 API

st.set_page_config(page_title="🧠 진단 결과 분석", layout="wide")
st.title("📋 설비 진단 결과 요약 및 분포 분석")

@st.cache_data
def load_data():
    res = requests.get(API_URL)
    res.raise_for_status()
    df = pd.DataFrame(res.json())
    df["detected_at"] = pd.to_datetime(df["detected_at"])
    return df

df = load_data()

# 선택용 라벨
fault_labels = {
    0: "정상",
    1: "질량 불균형",
    2: "지지 불량",
    3: "복합 고장"
}

# 토글: 기계, 센서
machines = ["전체"] + sorted(df["machine_name"].unique().tolist())
sensors = ["전체"] + sorted(df["sensor_no"].unique().tolist())

col1, col2 = st.columns(2)
with col1:
    selected_machine = st.selectbox("🔧 기계 선택", machines)
with col2:
    selected_sensor = st.selectbox("📟 센서 선택", sensors)

# 필터링
filtered = df.copy()
if selected_machine != "전체":
    filtered = filtered[filtered["machine_name"] == selected_machine]
if selected_sensor != "전체":
    filtered = filtered[filtered["sensor_no"] == selected_sensor]

# 상태 라벨 매핑
display_df = filtered.copy()
display_df["상태"] = display_df["is_abnormal"].apply(lambda x: "고장" if x == 1 else "정상")
display_df["고장 유형"] = display_df["fault_type"].apply(lambda x: fault_labels.get(x, "알 수 없음"))

# 📑 진단 결과 테이블
st.subheader("📑 진단 결과 테이블")
final_df = display_df[[
    "detected_at", "machine_name", "sensor_no", "상태", "고장 유형"
]].sort_values("detected_at", ascending=False)
st.dataframe(final_df, use_container_width=True)

# ✅ 파이 차트 토글 선택
st.subheader("📊 고장 유형 분포 시각화")
include_normal = st.checkbox("정상 포함", value=True)

if include_normal:
    fault_counts = display_df["고장 유형"].value_counts().reset_index()
    fault_counts.columns = ["고장 유형", "건수"]
    fig = px.pie(fault_counts, names="고장 유형", values="건수", title="전체 고장 유형 분포 (정상 포함)")
else:
    abnormal_only = display_df[display_df["is_abnormal"] == 1]
    fault_counts = abnormal_only["고장 유형"].value_counts().reset_index()
    fault_counts.columns = ["고장 유형", "건수"]
    fig = px.pie(fault_counts, names="고장 유형", values="건수", title="비정상 고장 유형만 분포")

st.plotly_chart(fig, use_container_width=True)

st.info("✅ 진단 결과의 유형 분포를 시각적으로 확인할 수 있습니다.")
