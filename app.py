import streamlit as st
import pandas as pd
from datetime import date, datetime

st.set_page_config(page_title="스마트 일정 & 프로젝트 비서", layout="wide", page_icon="📅")

st.title("📅 스마트 일정 및 프로젝트 비서 대시보드")

# --- 데이터 초기화 (세션 관리) ---
if 'personal_schedules' not in st.session_state:
    st.session_state.personal_schedules = pd.DataFrame([
        {"날짜": "2026-10-12", "일정명": "건강검진 예약", "카테고리": "건강", "상태": "진행중"},
        {"날짜": "2026-10-24", "일정명": "친구 결혼식", "카테고리": "경조사", "상태": "대기"}
    ])

if 'projects_tasks' not in st.session_state:
    st.session_state.projects_tasks = pd.DataFrame([
        {"프로젝트": "프로젝트 A: 웹사이트 개편", "세부 업무명": "메인 페이지 설계", "담당자": "김철수", "우선순위": "높음", "마감일": "2026-10-10", "상태": "완료"},
        {"프로젝트": "프로젝트 A: 웹사이트 개편", "세부 업무명": "프론트엔드 개발", "담당자": "이영희", "우선순위": "높음", "마감일": "2026-10-18", "상태": "진행중"},
        {"프로젝트": "프로젝트 B: 마케팅 캠페인", "세부 업무명": "고객 설문지 작성", "담당자": "김철수", "우선순위": "보통", "마감일": "2026-11-05", "상태": "대기"}
    ])

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📆 2개월 달력 뷰", "👤 개인 일정 관리", "💼 프로젝트 세부업무"])

# --- TAB 1: 오늘 기준 2개월 달력/일정 뷰 ---
with tab1:
    today = date.today()
    curr_year, curr_month = today.year, today.month
    next_month = curr_month + 1 if curr_month < 12 else 1
    next_year = curr_year if curr_month < 12 else curr_year + 1

    st.subheader(f"🗓️ {curr_year}년 {curr_month}월 ~ {next_year}년 {next_month}월 (2개월 스케줄)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"📌 **{curr_year}년 {curr_month}월**")
        curr_str = f"{curr_year}-{curr_month:02d}"
        
        st.markdown("**[개인 일정]**")
        p_curr = st.session_state.personal_schedules[st.session_state.personal_schedules['날짜'].str.startswith(curr_str)]
        st.dataframe(p_curr, use_container_width=True)
        
        st.markdown("**[프로젝트 마감 업무]**")
        t_curr = st.session_state.projects_tasks[st.session_state.projects_tasks['마감일'].str.startswith(curr_str)]
        st.dataframe(t_curr[['마감일', '프로젝트', '세부 업무명', '상태']], use_container_width=True)

    with col2:
        st.success(f"📌 **{next_year}년 {next_month}월**")
        next_str = f"{next_year}-{next_month:02d}"
        
        st.markdown("**[개인 일정]**")
        p_next = st.session_state.personal_schedules[st.session_state.personal_schedules['날짜'].str.startswith(next_str)]
        st.dataframe(p_next, use_container_width=True)
        
        st.markdown("**[프로젝트 마감 업무]**")
        t_next = st.session_state.projects_tasks[st.session_state.projects_tasks['마감일'].str.startswith(next_str)]
        st.dataframe(t_next[['마감일', '프로젝트', '세부 업무명', '상태']], use_container_width=True)

# --- TAB 2: 개인 일정 ---
with tab2:
    st.subheader("👤 개인 일정 추가 & 관리")
    with st.form("add_p_form"):
        p_date = st.date_input("날짜", date.today())
        p_title = st.text_input("일정명")
        p_cat = st.selectbox("카테고리", ["건강", "경조사", "운동", "개인약속", "기타"])
        if st.form_submit_button("일정 추가") and p_title:
            new_p = pd.DataFrame([{"날짜": str(p_date), "일정명": p_title, "카테고리": p_cat, "상태": "대기"}])
            st.session_state.personal_schedules = pd.concat([st.session_state.personal_schedules, new_p], ignore_index=True)
            st.success("등록되었습니다!")
            st.rerun()

    st.dataframe(st.session_state.personal_schedules, use_container_width=True)

# --- TAB 3: 프로젝트 업무 ---
with tab3:
    st.subheader("💼 프로젝트별 세부 업무 관리")
    proj_list = list(st.session_state.projects_tasks['프로젝트'].unique())
    selected_proj = st.selectbox("프로젝트 선택", proj_list)
    
    with st.form("add_t_form"):
        sub_title = st.text_input("세부 업무명")
        sub_owner = st.text_input("담당자")
        sub_due = st.date_input("마감일", date.today())
        if st.form_submit_button("세부 업무 추가") and sub_title:
            new_t = pd.DataFrame([{
                "프로젝트": selected_proj, "세부 업무명": sub_title,
                "담당자": sub_owner, "우선순위": "보통", "마감일": str(sub_due), "상태": "대기"
            }])
            st.session_state.projects_tasks = pd.concat([st.session_state.projects_tasks, new_t], ignore_index=True)
            st.success("추가되었습니다!")
            st.rerun()

    filtered = st.session_state.projects_tasks[st.session_state.projects_tasks['프로젝트'] == selected_proj]
    st.dataframe(filtered, use_container_width=True)
