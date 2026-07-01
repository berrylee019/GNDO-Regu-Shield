import streamlit as st
import time
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="GNDO Regu-Shield", layout="wide")

st.title("🛡️ GNDO Regu-Shield: 원전 설계 동결 및 규제 마일스톤 통제 시스템")
st.caption("AP1000 참사 방지를 위한 AI 에이전트 기반 설계 변경 리스크 추적기")

# 세션 상태 초기화 (초기 변경 요청 데이터셋)
if "change_requests" not in st.session_state:
    st.session_state.change_requests = [
        {"ID": "CR-001", "부품/계통": "피동형 냉각수 탱크 밸브 규격 변경", "요청자": "하청 설계 B사", "규제 위험도": "⚠️ 고위험", "상태": "검토중", "예상 지연": "18개월"},
        {"ID": "CR-002", "부품/계통": "격납건물 외벽 콘크리트 배합 수정", "요청자": "시공 C사", "규제 위험도": "🚨 치명적", "상태": "검토중", "예상 지연": "36개월"},
        {"ID": "CR-003", "부품/계통": "제어실 디스플레이 UI 배치 변경", "요청자": "운영 연수팀", "규제 위험도": "✅ 저위험", "상태": "승인", "예상 지연": "0개월"},
    ]

# ----------------- 좌측 통제 패널 -----------------
st.sidebar.header("⚙️ 신규 설계 변경 요청 (Change Order)")
with st.sidebar.form("new_cr_form"):
    component = st.text_input("변경 대상 계통/부품명", placeholder="예: 원자로 냉각재 펌프 밀봉재 변경")
    requested_by = st.selectbox("요청 처", ["원자로 계통 설계팀", "현장 시공사", "해외 공급망 파트너"])
    submit_btn = st.form_submit_button("AI 리스크 분석 실행")

    if submit_btn and component:
        with st.spinner("AI 에이전트가 규제 문서 및 도면 종속성 분석 중..."):
            time.sleep(2)  # RAG 및 에이전트 추론 가상 지연
            # 가상 분석 결과 추가
            new_cr = {
                "ID": f"CR-00{len(st.session_state.change_requests)+1}",
                "부품/계통": component,
                "요청자": requested_by,
                "규제 위험도": "⚠️ 고위험",
                "상태": "검토중",
                "예상 지연": "14개월"
            }
            st.session_state.change_requests.append(new_cr)
            st.success("분석 완료! 대시보드에 반영되었습니다.")

# ----------------- 메인 대시보드 -----------------
# 1. 상단 핵심 지표 지시등 (KPI)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric(label="현재 총 설계 변경 요청(CR)", value=f"{len(st.session_state.change_requests)} 건", delta="+1 건 (최근 24시간)")
with c2:
    st.metric(label="규제 재심사 유발 리스크", value="78%", delta="위험 수준 경보", delta_color="inverse")
with c3:
    st.metric(label="누적 예상 공기 지연 (Ripple Effect)", value="54 개월", delta="보글(Vogtle) 원전 참사 경로 진입 중", delta_color="inverse")
with c4:
    # 설계 동결 강제 스위치
    freeze_status = st.toggle("🚨 SYSTEM DESIGN FREEZE (설계 강제 동결)", value=False)
    if freeze_status:
        st.error("🔒 설계 동결 발동: 모든 신규 변경 승인이 차단됩니다.")

st.markdown("---")

# 2. 실시간 위험 요인 테이블
st.subheader("📋 설계 변경 요청별 규제 리스크 및 연쇄 지연 예측")
df = pd.DataFrame(st.session_state.change_requests)
st.dataframe(df, use_container_width=True)

# 3. AI 에이전트의 심층 연쇄 리스크 브리핑 (이 부분이 핵심 가치)
st.subheader("🧠 AI 에이전트 연쇄 리스크 브리핑 (Ripple-Effect Analysis)")

critical_cr = df[df["규제 위험도"] == "🚨 치명적"]
if not critical_cr.empty:
    with st.expander("🔍 CR-002: 격납건물 외벽 콘크리트 배합 수정 심층 분석 보고서 (클릭하여 확장)", expanded=True):
        st.write("""
        - **KINS 규제 매핑:** 원자력안전법 제21조(건설허가기준) 및 기술기준 규칙 제5조(구조물 안전성)와 정면 충돌 가능성 **94.2%**.
        - **연쇄 타격(Ripple Effect):** 콘크리트 배합 변경 시, 원자로 정밀 정착 볼트의 인장 강도 재계산 필요 ➡️ 배관 계통 설계 수정 ➡️ NRC/KINS 인허가 서류 전면 재제출 필요.
        - **경고 및 제언:** 본 변경 건은 완공을 **최소 36개월 지연**시키고 **2억 달러의 추가 비용**을 발생시킬 수 있습니다. 즉시 **[DESIGN FREEZE]**를 발동하고 기존 배합을 유지할 것을 강력히 권고합니다.
        """)
else:
    st.info("현재 치명적인 규제 위반 리스크를 유발하는 설계 변경 요인이 없습니다.")

# 4. 시각화 그래프
st.subheader("📈 설계 변경 누적에 따른 인허가 리스크 및 비용 예측 트렌드")
chart_data = pd.DataFrame({
    '공정 진행률(%)': [10, 20, 30, 40, 50, 60],
    '정상 예측 비용(억$ )': [5, 10, 15, 20, 25, 30],
    '설계 파편화 반영 비용(억$ )': [5, 12, 19, 28, 42, 65]
})
fig = px.line(chart_data, x='공정 진행률(%)', y=['정상 예측 비용(억$ )', '설계 파편화 반영 비용(억$ )'], 
              title="설계 변경 통제 실패 시 발생하는 '롱테일 리스크(Fat-tail Cost)' 시뮬레이션")
st.plotly_chart(fig, use_container_width=True)
