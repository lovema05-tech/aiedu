import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 폰트 설정 (윈도우 환경 한글 깨짐 방지용)
# 웹 배포 시 (Linux 서버) Malgun Gothic이 없을 수 있으나 윈도우 환경 테스트를 위해 설정
plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False) # 마이너스 기호 깨짐 방지

# 메인 화면 구성 - 상단 제목
st.title("데이터 상관관계 분석 대시보드")

# 1. 데이터 로드 (캐싱을 통해 속도 향상)
@st.cache_data
def load_data():
    try:
        # 실습 파일 로딩
        return pd.read_csv("6주차_실습4.csv", encoding="utf-8")
    except Exception as e:
        st.error("데이터 파일을 불러올 수 없습니다. '6주차_실습4.csv'가 존재하는지 확인해주세요.")
        return None

df = load_data()

# 데이터가 성공적으로 로드되었을 경우에만 아래 로직 실행
if df is not None:
    # 2. 사이드바(Sidebar) UI 설정
    st.sidebar.header("그래프 옵션 설정")
    
    # 분석에 사용 가능한 숫자형 컬럼과 색상 구분용 범주형 컬럼 지정
    numeric_cols = ['공부시간', '점수', '출석률', '게임시간', '스트레스지수']
    
    # selectbox를 사용하여 X축, Y축, 색상(범주) 선택
    x_axis = st.sidebar.selectbox("X축으로 사용할 컬럼 선택", numeric_cols, index=0)
    y_axis = st.sidebar.selectbox("Y축으로 사용할 컬럼 선택", numeric_cols, index=1)
    hue_col = st.sidebar.selectbox("색상(범주)으로 구분할 컬럼 선택", ['전공'])
    
    # checkbox를 통해 추세선 표시 여부 선택
    show_trend = st.sidebar.checkbox("추세선(회귀선) 표시 여부", value=False)

    # 3. 데이터 시각화 (산점도) 그려주기
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 추세선 체크 옵션에 따른 그래프 그리기
    if show_trend:
        # 데이터의 전체적인 흐름을 보기 위해 산점도 위에 붉은색 회귀선을 덧그림
        sns.scatterplot(data=df, x=x_axis, y=y_axis, hue=hue_col, ax=ax)
        sns.regplot(data=df, x=x_axis, y=y_axis, scatter=False, ax=ax, color='red')
    else:
        # 일반 산점도만 표시
        sns.scatterplot(data=df, x=x_axis, y=y_axis, hue=hue_col, ax=ax)
    
    # 레이아웃 짤림 방지 (타이틀이나 축이 잘리지 않게 조정)
    plt.tight_layout()
    
    # 완성된 그래프를 Streamlit 메인 화면에 출력
    st.pyplot(fig)
    
    # 4. 상관계수 수치 계산 및 출력 (그래프 하단)
    # 선택된 두 변수 간의 피어슨 상관계수(Correlation Coefficient)를 계산
    corr_value = df[x_axis].corr(df[y_axis])
    
    st.subheader("상관관계 분석 결과")
    st.write(f"**{x_axis}**와(과) **{y_axis}**의 상관계수: `{corr_value:.3f}`")
    
    # 5. 상관계수에 따른 해석 문구 출력 보조 기능
    # 상관계수의 크기에 따라 양/음/무상관 관계를 알기 쉽게 해석하여 표시합니다.
    if corr_value > 0.3:
        st.info("💡 **해석:** 두 변수는 **양(+)의 상관관계**를 가지고 있습니다. (하나가 증가하면 다른 하나도 증가하는 경향이 있습니다.)")
    elif corr_value < -0.3:
        st.warning("💡 **해석:** 두 변수는 **음(-)의 상관관계**를 가지고 있습니다. (하나가 증가하면 다른 하나는 감소하는 경향이 있습니다.)")
    else:
        st.success("💡 **해석:** 두 변수는 뚜렷한 선형 상관관계를 보이지 않습니다.")
