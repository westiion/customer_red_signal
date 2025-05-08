import streamlit as st
import pandas as pd
import joblib
import openai

st.title("Customer Red Signal 대시보드")

uploaded_file=st.file_uploader("고객 데이터를 업로드하세요", type=["csv"])
if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df=pd.read_csv(uploaded_file)

st.set_page_config(page_title="Customer Red Signal 대시보드",layout="wide")

st.sidebar.header("메뉴")

option=st.sidebar.selectbox(
    "분석 항목 선택", 
    ["프로젝트 소개", "고객 데이터 분석","이탈 예측","GPT메시지 생성"]
)

#프로젝트 소개
if option=="프로젝트 소개":
    st.write("프로젝트명: Customer Red Signal")
    st.write("구독형 서비스 고객의 이탈 가능성을 사전에 예측하고, 맞춤 메시지를 생성하여 전송하는 서비스입니다.")

#고객 데이터 분석
elif option=="고객 데이터 분석":
    st.write("고객 데이터 요약")
    #예제 데이터(실제 데)

#예제 버튼
if st.button("GPT 메시지 요청"):
    st.write("GPT API로 메시지를 요청했습니다!")