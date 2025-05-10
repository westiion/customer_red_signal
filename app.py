import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime
import io

st.title("🚨 Customer Red Signal 대시보드")
st.write('일단 머신러닝 학습용 데이터셋으로 진행함')

# --- 데이터 불러오기 ---
df = pd.read_csv("dummy_customer_data.csv", encoding='utf-8-sig')

# ✅ unpaid 고객 필터링 및 Excel 다운로드
unpaid_df = df[df['payment_status'] == 'unpaid']
st.header("⚠️ 이탈 위험 고객 (unpaid)")
st.write(unpaid_df)

excel_buffer = io.BytesIO()
with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
    unpaid_df.to_excel(writer, index=False, sheet_name='unpaid_customers')

st.download_button(
    label="📥 이탈 위험 고객 Excel 다운로드",
    data=excel_buffer.getvalue(),
    file_name="unpaid_customers.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# --- 1. 결측치 확인 ---
st.header("1️⃣ 결측치 현황")
missing = df.isnull().sum()
if missing.sum() == 0:
    st.success("✅ 결측치 없음")
else:
    st.warning("⚠️ 결측치 존재")
    st.write(missing)

# --- 2. 전체 평균 시청시간, 나이 ---
st.header("2️⃣ 전체 평균 지표")
col1, col2 = st.columns(2)
col1.metric("평균 시청시간 (분)", f"{df['watch_time'].mean():.2f}")
col2.metric("평균 나이 (세)", f"{df['age'].mean():.2f}")

# --- 3. 결제 상태별 통계 (Altair + interactive) ---
st.header("3️⃣ 결제 상태별 통계")
st.subheader("고객 수")

status_counts = df['payment_status'].value_counts().reset_index()
status_counts.columns = ['payment_status', 'count']

bar_chart = alt.Chart(status_counts).mark_bar().encode(
    x=alt.X('payment_status:N', title='결제 상태'),
    y=alt.Y('count:Q', title='고객 수', scale=alt.Scale(domain=[0, status_counts['count'].max() + 5])),
    tooltip=['payment_status', 'count']
).properties(
    width=500,
    height=300,
    title="결제 상태별 고객 수"
).interactive()

st.altair_chart(bar_chart, use_container_width=True)

st.subheader("평균 나이")
st.write(df.groupby('payment_status')['age'].mean())

st.subheader("평균 시청시간")
st.write(df.groupby('payment_status')['watch_time'].mean())

# --- 4. 선호 장르 분포 (Altair + interactive) ---
st.header("4️⃣ 선호 장르 분포")

genre_counts = df['preferred_category'].value_counts().reset_index()
genre_counts.columns = ['preferred_category', 'count']

genre_chart = alt.Chart(genre_counts).mark_bar().encode(
    x=alt.X('preferred_category:N', title='선호 장르'),
    y=alt.Y('count:Q', title='고객 수'),
    tooltip=['preferred_category', 'count']
).properties(
    width=500,
    height=300,
    title="선호 장르 분포"
).interactive()

st.altair_chart(genre_chart, use_container_width=True)

# --- 5. 평균 로그인 경과일 ---
st.header("5️⃣ 평균 로그인 경과일")
df['last_login'] = pd.to_datetime(df['last_login'])
df['days_since_login'] = (datetime.today() - df['last_login']).dt.days
st.metric("평균 로그인 경과일 (일)", f"{df['days_since_login'].mean():.2f}")

st.subheader("결제 상태별 평균 로그인 경과일")
st.write(df.groupby('payment_status')['days_since_login'].mean())

# --- 6. 이상치 탐지 ---
st.header("6️⃣ 이상치 탐지 (Z-score ±3 기준)")

def detect_outliers_zscore(data, threshold=3):
    mean = np.mean(data)
    std = np.std(data)
    z_scores = [(x - mean) / std for x in data]
    return [i for i, z in enumerate(z_scores) if abs(z) > threshold]

age_outliers = detect_outliers_zscore(df['age'])
watch_outliers = detect_outliers_zscore(df['watch_time'])

st.subheader("나이 이상치")
if age_outliers:
    st.warning(f"⚠️ {len(age_outliers)}건 발견: {age_outliers}")
else:
    st.success("✅ 나이 이상치 없음")

st.subheader("시청시간 이상치")
if watch_outliers:
    st.warning(f"⚠️ {len(watch_outliers)}건 발견: {watch_outliers}")
else:
    st.success("✅ 시청시간 이상치 없음")
