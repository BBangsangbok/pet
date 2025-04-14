import AI
import streamlit as st
from dotenv import load_dotenv 
import os 


load_dotenv()

# 사이드바 메뉴를 통해 페이지 선택
menu = st.sidebar.selectbox("메뉴 선택", ("채팅하기", "커뮤니티"))


def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_started" not in st.session_state:
        st.session_state.session_started = False

def chat_history():
    for message in st.session_state.messages:
        display_chat_message(message["content"], message["is_user"])

def display_chat_message(message, is_user=False):
    """Display a chat message with the appropriate styling."""
    if is_user:
        with st.chat_message("user", avatar="😀"):
            st.markdown(message)
    else:
        with st.chat_message("assistant", avatar="😾"):
            st.markdown(message)

@st.cache_resource
def load_model():
    chat = AI.Chat()
    return chat
chat = load_model()

if menu == "채팅하기":
    st.title("PetBeyond")
    st.write("키우던 아이랑 이야기해보세요!")
    initialize_session_state()
    # 챗 대화 내역을 저장하는 리스트 초기화
    if pet_survey:=st.text_input("반려동물의 종류, 이름, 성별, 품종, 크기, 성격, 색깔등 자세하게 입력하세요"):
        chat.save_basic_info(pet_survey)
        st.markdown(f"**반려동물의 기본 정보**: \n{pet_survey}")
    # 채팅 입력창과 전송 버튼
        chat_history()
    if input := st.chat_input("반려동물에게 물어보고 싶은 것을 입력하세요"):
        st.session_state.messages.append({"content": input, "is_user": True})
        display_chat_message(input, is_user=True)
        answer = chat.invoke_chain(input)
        st.session_state.messages.append({"content": answer, "is_user": False})
        display_chat_message(answer, is_user=False)

elif menu == "커뮤니티":
    st.title("커뮤니티")
    st.write("PetBeyond 이용자들을 위한 커뮤니티 공간입니다. 여러분의 경험과 이야기를 공유해 보세요.")
    
    # 게시글 저장 리스트 초기화
    if 'community_posts' not in st.session_state:
        st.session_state.community_posts = []
    
    # 게시글 작성 폼
    with st.form("post_form"):
        title = st.text_input("제목", key="title")
        content = st.text_area("게시글 내용", key="content")
        submitted = st.form_submit_button("게시")
        if submitted:
            if title and content:
                # 게시글 임시 저장
                st.session_state.community_posts.append({
                    "title": title,
                    "content": content
                })
                st.success("게시글이 등록되었습니다.")
            else:
                st.error("제목과 내용을 모두 입력해주세요.")
    
    st.markdown("### 등록된 게시글")
    # 등록된 게시글 목록 출력
    if st.session_state.community_posts:
        for post in st.session_state.community_posts:
            st.markdown(f"**{post['title']}**")
            st.write(post['content'])
            st.markdown("---")
    else:
        st.info("아직 게시글이 없습니다.")
