# Market Watcher (경쟁사 동향 감시 및 분석 에이전트)

## 1. 프로젝트 개요

Market Watcher는 사용자가 지정한 키워드(기업명, 산업 분야, 특정 기술 등)에 대한 최신 웹 뉴스를 실시간으로 수집하고 분석하여, 비즈니스 인사이트가 담긴 '일일 동향 리포트'를 자동으로 생성하는 AI 에이전트입니다.

기존의 정적인 데이터베이스 조회 방식(RAG)과 달리, AI가 인터넷 검색 도구(Web Search Tool)를 스스로 사용하여 최신 정보를 능동적으로 탐색하는 에이전트(Agent) 기술이 적용되었습니다. OpenAI의 **gpt-5-mini** 모델이 수집된 비정형 뉴스 데이터를 분석하여 핵심 요약, 시장 영향도, 여론(Sentiment)을 구조화된 데이터로 제공합니다.

### 주요 기능
* **Autonomous Web Search:** LangChain 에이전트가 DuckDuckGo 검색 엔진을 활용하여 키워드와 관련된 최신 뉴스 및 아티클을 자동으로 수집.
* **Market Intelligence:** 단순한 뉴스 나열이 아닌, 3줄 핵심 요약 및 업계에 미칠 파급 효과(Impact Analysis) 도출.
* **Sentiment Analysis:** 수집된 정보의 뉘앙스를 분석하여 시장의 여론을 긍정/부정/중립으로 평가.
* **Structured Reporting:** 분석 결과를 JSON 포맷으로 정형화하여 가독성 높은 대시보드 형태로 시각화.

## 2. 시스템 아키텍처

본 시스템은 '인지(Thought) - 행동(Action) - 관찰(Observation)'의 루프를 수행하는 ReAct(Reasoning + Acting) 패턴의 에이전트로 설계되었습니다.

1.  **Input:** 사용자가 분석하고 싶은 관심 키워드 입력.
2.  **Reasoning:** 에이전트가 키워드 분석을 위해 어떤 정보를 검색해야 할지 계획 수립.
3.  **Action (Tool Usage):** `DuckDuckGoSearchRun` 도구를 호출하여 실제 웹 검색 수행.
4.  **Observation:** 검색 결과(뉴스 제목, 요약, 링크)를 확보.
5.  **Synthesis:** **gpt-5-mini** 모델이 수집된 정보를 종합하여 전략기획팀장 페르소나에 맞춰 리포트 작성.
6.  **Output:** 최종 분석 결과를 JSON 구조로 반환 및 UI 렌더링.

## 3. 기술 스택

* **Language:** Python 3.10 이상
* **LLM:** OpenAI **gpt-5-mini**
* **Orchestration:** LangChain (AgentExecutor)
* **Search Tool:** DuckDuckGo Search (langchain-community)
* **Web Framework:** Streamlit
* **Configuration:** python-dotenv

## 4. 프로젝트 구조

에이전트 설정, 프롬프트 엔지니어링, UI 로직을 분리한 모듈형 구조입니다.

```text
market-watcher/
├── .env                  # 환경 변수 (API Key)
├── requirements.txt      # 의존성 패키지 목록
├── main.py               # 애플리케이션 진입점 및 리포트 대시보드 UI
└── app/
    ├── __init__.py
    ├── config.py         # 시장 분석가 페르소나 및 시스템 프롬프트 정의
    └── agent.py          # 웹 검색 도구가 장착된 LangChain 에이전트 로직
```

## 5. 설치 및 실행 가이드
### 5.1. 사전 준비
Python 환경이 설치되어 있어야 합니다. 터미널에서 저장소를 복제하고 프로젝트 디렉토리로 이동하십시오.

```Bash
git clone [레포지토리 주소]
cd market-watcher
```
### 5.2. 의존성 설치
LangChain 및 검색 도구 사용을 위한 라이브러리를 설치합니다.

```Bash
pip install -r requirements.txt
```
### 5.3. 환경 변수 설정
프로젝트 루트 경로에 .env 파일을 생성하고, 유효한 OpenAI API 키를 입력하십시오.

```Ini, TOML
OPENAI_API_KEY=sk-your-api-key-here
```
### 5.4. 실행
Streamlit 애플리케이션을 실행합니다.

```Bash
streamlit run main.py
```
## 6. 출력 데이터 사양 (JSON Schema)
에이전트는 분석 결과를 다음과 같은 JSON 구조로 반환합니다. 이를 통해 슬랙(Slack) 봇 연동이나 이메일 자동 발송 시스템으로 확장할 수 있습니다.

```JSON
{
  "keyword": "테슬라 전기차 가격 정책",
  "summary": "테슬라가 시장 점유율 방어를 위해 모델 Y의 가격을 인하했습니다. 이는 중국 전기차 업체들의 저가 공세에 대응하기 위한 전략으로 분석됩니다.",
  "key_events": [
    {
      "headline": "테슬라, 모델Y 가격 또 인하... 치킨게임 재점화",
      "source": "경제뉴스",
      "date": "2024-02-12"
    }
  ],
  "impact_analysis": "이번 가격 인하는 경쟁사들의 마진율 압박으로 이어질 것이며, 전기차 시장 전반의 가격 경쟁을 심화시킬 것으로 전망됩니다.",
  "sentiment": "중립 (소비자 긍정, 투자자 우려)"
}
```

## 7. 실행 화면