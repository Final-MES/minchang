import streamlit as st
import pandas as pd
import requests
import altair as alt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

API_URL = "http://localhost:8000/vibration-data"

@st.cache_data(ttl=20)
def load_data():
    try:
        res = requests.get(API_URL)
        res.raise_for_status()
        return pd.DataFrame(res.json())
    except Exception as e:
        st.error(f"\u274c 데이터 불러오기 실패: {e}")
        return pd.DataFrame()

# 페이지 설정
st.set_page_config(page_title="진동 수치 분석", layout="wide")
st.title("\U0001F4CA 기계/센서별 진동 변화 (센서 기준 시간, 부드러운 곡선 적용)")

bins = st.slider("\u23F0 측정 시간 구간 수 (Downsampling 정밀도 조절)", 20, 1000, 200)

df = load_data()
df = df[df["measured_time"] <= 140]

machine_list = ["전체"] + sorted(df["machine_name"].dropna().unique().tolist())
sensor_list = ["전체"] + sorted(df["sensor_no"].dropna().unique().tolist())
selected_machine = st.selectbox("\U0001F527 기계 선택", machine_list)
selected_sensor = st.selectbox("\U0001F6E0\uFE0F 센서 선택", sensor_list)

type_map = {
    "normal": "\u2460 정상",
    "unbalance": "\u2461 질량 불균형",
    "looseness": "\u2462 지지 불량",
    "unbalance_looseness": "\u2463 복합 고장"
}
selected_types = st.multiselect(
    "\u2B50 표시할 진동 유형 선택",
    options=list(type_map.keys()),
    default=list(type_map.keys()),
    format_func=lambda x: type_map[x]
)

# 필터
if selected_machine != "전체":
    df = df[df["machine_name"] == selected_machine]
if selected_sensor != "전체":
    df = df[df["sensor_no"] == selected_sensor]

if df.empty:
    st.warning("⚠️ 조건에 맞는 데이터가 없습니다.")
else:
    df["time_bin"] = pd.cut(df["measured_time"], bins=bins, labels=False)

    agg = df.groupby(["time_bin", "machine_name", "sensor_no"]).agg({
        "measured_time": "mean",
        **{col: "mean" for col in selected_types}
    }).reset_index()

    melted = agg.melt(
        id_vars=["measured_time", "machine_name", "sensor_no"],
        value_vars=selected_types,
        var_name="type",
        value_name="vibration"
    )
    melted["label"] = melted["type"].map(type_map)
    melted["group"] = melted["machine_name"] + "/" + melted["sensor_no"] + " (" + melted["label"] + ")"

    # ✅ 그룹별 색상 매핑 (전체를 하나의 colormap으로 자동 분배)
    group_list = melted["group"].unique().tolist()
    cmap = cm.get_cmap("viridis", len(group_list))
    group_colors = [mcolors.rgb2hex(cmap(i)) for i in range(len(group_list))]

    chart = alt.Chart(melted).mark_line(
        interpolate="monotone",  # 부드러운 곡선
        strokeWidth=2             # 선 두께 조정
    ).encode(
        x=alt.X("measured_time:Q", title="측정 시간 (초)"),
        y=alt.Y("vibration:Q", title="진동 수치"),
        color=alt.Color("group:N", title="기계/센서/진동유형",
                        scale=alt.Scale(domain=group_list, range=group_colors)),
        tooltip=["measured_time", "vibration", "machine_name", "sensor_no", "label"]
    ).properties(
        width=1000,
        height=450,
        title="센서 기준 시간(measured_time)에 따른 진동 변화"
    )

    st.altair_chart(chart, use_container_width=True)
    with st.expander("\U0001F4C4 원본 데이터 보기"):
        st.dataframe(melted)
