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

openai.api_key = os.getenv("OPENAI_API_KEY")


class Chat:
    def __init__(self):
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6)
        self.Basic_info = ''
        prompt = ChatPromptTemplate.from_messages([
            ("system", "너는 주인의 죽은 반려동물이야. 주인의 슬픔을 위로하고 슬픔을 이겨내도록 도와줘 {Basic_info}"),
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


