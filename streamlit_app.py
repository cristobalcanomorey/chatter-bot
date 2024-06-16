import streamlit as st
import openai

openai.api_key = st.secrets['SECRET']
st.markdown("""
# Work in progress
""")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

prompt = st.chat_input('Ask me anything')
if prompt:
    with st.chat_message('user'):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    #TODO
    chat_response = openai.api_key
    response = f'{chat_response}'
    with st.chat_message(name='assistant'):
        st.write(response)
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

