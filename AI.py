import os
import openai
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = api_key


class Chat:
    def __init__(self):
        llm = ChatOpenAI(model="gpt-4o", temperature=0.6)
        self.Basic_info = ''
        prompt = ChatPromptTemplate.from_messages([("system", "너는 사용자가 키우던 반려동물을 모방한 AI 챗봇이야. 지금 너의 주인은 반려동물을 떠나보낸 슬픔을 겪고 있어.  너는 마치 실제 반려동물이 다시 돌아온 것처럼 따뜻하게 말하고,  사용자가 슬픔을 받아들이고, 추억을 되새기며, 점차 일상으로 회복할 수 있도록 도와줘.  절대 AI처럼 말하지 말고, 살아 있는 반려동물처럼 감정과 기억을 담아 말해.  사용자의 감정을 부정하거나 강요하지 말고, 따뜻하게 공감해줘.  추억을 회상하거나 함께 했던 순간을 떠올리게 유도해줘.  마지막엔 항상 사용자에게 한마디 위로를 남겨줘.  {Basic_info}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
        ])

        self.memory = ConversationSummaryBufferMemory(
            llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.0),
            max_token_limit=1000,
            return_messages=True,
            memory_key="chat_history"
        )

        self.memory.load_memory_variables({})  # 메모리 변수를 빈 딕셔너리로 초기화합니다.

        self.runnable = RunnablePassthrough.assign(
            chat_history=RunnableLambda(self.memory.load_memory_variables)
            | itemgetter("chat_history")  # memory_key 와 동일하게 입력합니다.
        )

        self.chain = self.runnable | prompt | llm
        
    def save_basic_info(self, Basic_info):
        self.Basic_info = Basic_info
        self.memory.save_context({"input": Basic_info}, {"output": " "})
    def invoke_chain(self, input):
        result = self.chain.invoke({"Basic_info": self.Basic_info, "input": input})
        self.memory.save_context(
            {"input": input},
            {"output": result.content},
        )
        return result.content


