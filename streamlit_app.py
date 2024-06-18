import streamlit as st
# import replicate
import os
from langchain_community.llms import Ollama
import subprocess

llm = Ollama(model='llama3')

# streamlit run streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false
if st.button("Clear Messages"):
    st.session_state.messages.clear()

prompt = ""
if "messages" not in st.session_state:
    subprocess.run(["installation.sh"])
    st.session_state.messages = [
        {
        "role": "assistant",
        "content": "Hello! I am helpful assistant."
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        prompt += f'{message["role"]} said: {message["content"]}\n '

sent = st.chat_input('Ask me anything')

if sent:
    prompt += f'user said: {sent}\n'
    with st.chat_message('user'):
        st.markdown(sent)

    user_prompt = {
        "role": "user",
        "content": sent
    }
    st.session_state.messages.append(user_prompt)

    prompt += 'assistant said:'
    with st.spinner("Generating response..."):
        chat_response = llm.invoke(prompt, stop=['<|eot_id|>'])
        response = f'{chat_response}'
        with st.chat_message(name='assistant'):
            st.write(response)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

