import os
import json
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from app.config import MODEL_NAME, SYSTEM_PROMPT
from dotenv import load_dotenv

load_dotenv()

def get_market_report(keyword):
    """키워드에 대한 최신 뉴스를 검색하고 분석 리포트 생성"""

    # 도구 준비 :검색 엔진
    search_tool = DuckDuckGoSearchRun()
    tools = [search_tool]

    # LLM 준비
    llm = ChatOpenAI(model=MODEL_NAME, reasoning_effort="low")

    # 프롬프트 구성
    # Agent는 생각 -> 행동 -> 관찰 과정을 거침
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", f"'{keyword}'에 대한 최신 뉴스나 동향을 검색해서 분석해줘."),
        ("placeholder", "{agent_scratchpad}"), # AI가 검색하고 생각하는 공간
    ])

    # 에이전트 생성
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # 실행
    try:
        # 에이전트가 검색을 수행하고 최종 답변(JSON)을 내놓음
        response = agent_executor.invoke({"input": keyword})

        # JSON 파싱 시도
        output_text = response["output"]
        # 가끔 앞뒤에 설명이 붙을 수 있어 JSON 부분만 찾거나, 바로 로드 시도
        try:
            return json.loads(output_text)
        except json.JSONDecodeError:
            # JSON 파싱 실패 시 텍스트 그대로 반환 (디버깅용)
            return {"error": "JSON 파싱 실패", "raw_text": output_text}
    except Exception as e:
        return {"error": f"에이전트 실행 중 오류: {str(e)}"}