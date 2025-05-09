import streamlit as st
import pandas as pd
import requests
import altair as alt
from datetime import datetime

API_URL = "http://localhost:8000/vibration-diagnosis"

# 🗃️ 진단 데이터 불러오기
@st.cache_data(ttl=10)
def load_data(machine_name=None, sensor_no=None, limit=500):
    params = {"limit": limit}
    if machine_name and machine_name != "전체":
        params["machine_name"] = machine_name
    if sensor_no and sensor_no != "전체":
        params["sensor_no"] = sensor_no

    try:
        res = requests.get(API_URL, params=params)
        res.raise_for_status()
        df = pd.DataFrame(res.json())
        return df
    except Exception as e:
        st.error(f"❌ 데이터 불러오기 실패: {e}")
        return pd.DataFrame()

# 🔖 고장 코드 라벨
fault_labels = {
    0: "① 정상 상태",
    1: "② 질량 불균형 (Type 1)",
    2: "③ 지지 불량 (Type 2)",
    3: "④ 복합 고장 (Type 3)"
}

# 🎨 고정 색상
fault_colors = {
    "① 정상 상태": "green",
    "② 질량 불균형 (Type 1)": "orange",
    "③ 지지 불량 (Type 2)": "purple",
    "④ 복합 고장 (Type 3)": "red"
}

# 페이지 설정
st.set_page_config(page_title="📊 진단 결과 시계열 분석", layout="wide")
st.title("📅 진동 상태를 시간대 선형 그래프로 보기 (AI 진단 기반)")

# 슬라이더: 가져올 데이터 수
limit = st.slider("📥 가져올 데이터 수 (최대)", 100, 10000, step=100, value=500)

# 초기 데이터 로딩 (기계/센서 선택용)
raw_df = load_data(limit=limit)

# 기계/센서 리스트 준비
machine_list = ["전체"]
sensor_list = ["전체"]
if not raw_df.empty:
    if "machine_name" in raw_df.columns:
        machine_list += sorted(raw_df["machine_name"].dropna().unique().tolist())
    if "sensor_no" in raw_df.columns:
        sensor_list += sorted(raw_df["sensor_no"].dropna().unique().tolist())

# ✅ UI 구성
selected_machine = st.selectbox("🔧 기계 선택", machine_list)
selected_sensor = st.selectbox("📟 센서 선택", sensor_list)
selected_faults = st.multiselect(
    "⚙️ 진동 상태 선택",
    options=list(fault_labels.keys()),
    default=list(fault_labels.keys()),
    format_func=lambda x: fault_labels[x]
)

# 본 분석용 데이터 로딩
df = load_data(machine_name=selected_machine, sensor_no=selected_sensor, limit=limit)

# 날짜 필터 영역
start_date = end_date = None
if not df.empty and "detected_at" in df.columns:
    df["detected_at"] = pd.to_datetime(df["detected_at"], errors="coerce")
    df = df.dropna(subset=["detected_at"])

    if not df.empty:
        min_date = df["detected_at"].min().date()
        max_date = df["detected_at"].max().date()
        start_date, end_date = st.date_input(
            "📆 분석할 날짜 범위 선택",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    else:
        st.info("📅 날짜 필터를 사용할 수 없습니다. 유효한 'detected_at' 값이 없습니다.")
else:
    st.info("📅 날짜 필터를 사용할 수 없습니다. 데이터가 없습니다.")

# 필터 적용 및 그래프 출력
if df.empty or "fault_type" not in df.columns or start_date is None:
    st.warning("⚠️ 조건에 맞는 데이터가 없거나, 필드가 누락되었습니다.")
else:
    df = df[df["fault_type"].isin(selected_faults)].copy()
    df["fault_label"] = df["fault_type"].map(fault_labels)
    df["count"] = 1
    df = df[(df["detected_at"].dt.date >= start_date) & (df["detected_at"].dt.date <= end_date)]

    # 그래프 그리기
    chart = alt.Chart(df).mark_line().encode(
        x="detected_at:T",
        y="count:Q",
        color=alt.Color("fault_label:N", title="진동 상태",
                        scale=alt.Scale(domain=list(fault_colors.keys()),
                                        range=list(fault_colors.values()))),
        tooltip=["detected_at", "machine_name", "sensor_no", "fault_label"]
    ).properties(
        title="진동 상태 선형 그래프",
        width=1000,
        height=450
    )

    st.altair_chart(chart, use_container_width=True)

    with st.expander("📄 원본 데이터 보기"):
        st.dataframe(df)
