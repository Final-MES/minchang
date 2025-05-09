import streamlit as st
import pandas as pd
import requests
import altair as alt

# 📁 FastAPI에서 GET 요청으로 데이터 불러오기
API_URL = "http://localhost:8000/vibration-data"  # 로컬 FastAPI 서버 주소

@st.cache_data
def load_data(sensor_no=None):
    params = {"sensor_no": sensor_no, "limit": 1000} if sensor_no else {}
    res = requests.get(API_URL, params=params)
    res.raise_for_status()
    df = pd.DataFrame(res.json())
    df["collected_at"] = pd.to_datetime(df["collected_at"])
    return df

# Streamlit 기본 설정
st.set_page_config(page_title="📊 진동 시계열 분석", layout="wide")
st.title("📈 기계별 진동 상태 시계열 분석")

# 📌 센서 선택 UI만 먼저 제공 (데이터 로딩을 늦춤)
sensor_input_df = load_data()  # 전체에서 센서 목록만 파악
sensors = sorted(sensor_input_df["sensor_no"].unique().tolist())
selected_sensor = st.selectbox("📟 분석할 센서를 선택하세요 (최대 1000건)", sensors)

# 선택 시 데이터 요청
if selected_sensor:
    df = load_data(sensor_no=selected_sensor)

    # 📌 상태 항목 및 레이블 정의
    states = ["normal", "unbalance", "looseness", "unbalance_looseness"]
    state_labels = {
        "normal": "정상 상태",
        "unbalance": "질량 불균형",
        "looseness": "지지 불량",
        "unbalance_looseness": "복합 고장"
    }
    selected_states = st.multiselect(
        "📌 진동 상태 선택 (중복 가능)",
        options=states,
        default=states,
        format_func=lambda x: state_labels[x]
    )

    # 📌 데이터 melt → 그래프 시각화용
    melted = df.melt(
        id_vars=["collected_at", "machine_name", "sensor_no"],
        value_vars=selected_states,
        var_name="fault_type",
        value_name="vibration"
    )

    # 📌 겹치는 선 그래프 (연한 색감 + 겹침 표현)
    line_chart = alt.Chart(melted).mark_line(opacity=0.5).encode(
        x="collected_at:T",
        y="vibration:Q",
        color=alt.Color("fault_type:N", scale=alt.Scale(scheme="pastel1")),
        tooltip=["collected_at", "vibration", "fault_type"]
    ).properties(
        width=1000,
        height=500
    )

    st.altair_chart(line_chart, use_container_width=True)

    # 📌 데이터 확인 테이블
    with st.expander("🔍 필터링된 원본 데이터 보기"):
        st.dataframe(melted)
