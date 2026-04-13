import streamlit as st

# 초기 데이터 세팅
if 'logs' not in st.session_state:
    st.session_state.logs = [
        {"title": "소년이 온다", "author": "한강", "review": "한 인간의 죽음이 아니라, 우리가 외면해온 역사와 고통을 정면으로 마주하게 만드는 작품"},
        {"title": "데미안", "author": "헤르만 헤세", "review": "자아를 찾는 성장 이야기, “새는 알을 깨고 나온다” 구절 인상적"},
        {"title": "파이썬으로 시작하는 데이터 분석", "author": "웨스 맥키니", "review": "실무 중심의 데이터 분석 입문서, pandas 라이브러리 이해에 도움"}
    ]

st.title("독서 기록장")

# 새로운 독서 기록을 입력받기 위한 입력 폼
with st.form("book_form", clear_on_submit=True):
    title_input = st.text_input("책 제목")
    author_input = st.text_input("저자명")
    review_input = st.text_area("한줄 감상")
    submitted = st.form_submit_button("추가")
    
    # 폼 전송 시, 모든 필드가 채워져 있을 경우 실행
    if submitted and title_input and author_input and review_input:
        # 최근 기록이 맨 위에 보이도록 리스트의 최상단(0번 인덱스)에 새 데이터 삽입
        st.session_state.logs.insert(0, {
            "title": title_input,
            "author": author_input,
            "review": review_input
        })

st.subheader("저장된 기록")

# 저장된 독서 기록 반복 출력 (최근부터 출력됨)
for log in st.session_state.logs:
    st.write(f"**책 제목:** {log['title']}")
    st.write(f"**저자명:** {log['author']}")
    st.write(f"**한줄 감상:** {log['review']}")
    st.divider()
