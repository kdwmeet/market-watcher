import streamlit as st
from app.agent import get_market_report

st.set_page_config(page_title="Market Watcher", layout="wide")

# --- 헤더 ---
st.title("경쟁사 동향 감시 요원")
st.caption("궁금한 기업이나 키워드를 입력하세요. AI 요원이 인터넷을 뒤져서 '일일 브리핑'을 해드립니다,")
st.divider()

# --- 입력 섹션 ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("감시 대상 설정")
    keyword = st.text_input("키워드 입력", placeholder="예: 삼성전자 반도체, OpenAI GPT-5")

    start_btn = st.button("동향 파악 시작", type="primary", width="stretch")
    
    st.info("팁: '구체적인 키워드'를 넣을수록 정확도가 올라갑니다.\n(예: '현대차' -> '현대차 전기차 판매량')")

# --- 결과 섹션 ---
with col2:
    st.subheader("일일 동향 리포트")
    
    if start_btn:
        if not keyword:
            st.warning("키워드를 입력해주세요!")
        else:
            with st.spinner(f"AI 요원이 '{keyword}' 관련 최신 뉴스를 수집 중입니다..."):
                result = get_market_report(keyword)

                if "error" in result:
                    st.error("분석 중 오류가 발생했습니다.")
                    st.code(result.get("raw_text", result["error"]))
                else:
                    # 헤더 정보
                    kwd = result.get("keyword", keyword)
                    sentiment = result.get("sentiment", "중립")

                    # 감정에 따른 아이콘
                    if "긍정" in sentiment: icon = "🟢"
                    elif "부정" in sentiment: icon = "🔴"
                    else: icon = "⚪"

                    st.markdown(f"### 키워드: {kwd} ({icon} {sentiment})")

                    st.divider()

                    # 핵심 요약
                    st.success(f"**3줄 요약:**\n\n{result.get('summary')}")

                    # 주요 뉴스
                    st.markdown("#### 주요 뉴스 헤드라인")
                    events = result.get("key_events", [])
                    for evt in events:
                        st.write(f"- **[{evt.get('source', '뉴스')}** {evt.get('headline')} ({evt.get('date', '최신')})")
                    
                    st.divider()


                    # 영향 분석
                    st.info(f"**시장 영향 분석:**\n\n{result.get('impact_analysis')}")