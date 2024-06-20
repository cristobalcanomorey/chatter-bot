import streamlit as st
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

# Load pre-trained model for understanding user queries
@st.cache_resource
def load_model(model_name):
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer, nlp

model_name = "deepset/roberta-base-squad2"
model, tokenizer, nlp = load_model(model_name)
manual_context = None
curriculum_data = {
    "Especialization": "Cristóbal Cano is specialized in an AI and Big Data with a background in web development.",
    "Education": "He completed a specialized course in AI and Big Data at IEDIB (2023-2024), a higher degree in web application development at Ies Son Ferrer (2018-2020), and a medium degree in microcomputer systems and networks at Ies Son Ferrer (2015-2018).",
    "AI_skills": "His AI skills include machine learning, deep learning, model deployment, data preprocessing, natural language processing, computer vision, and reinforcement learning.",
    "AI_tools": "He is proficient with tools like Gradio, Streamlit, Python, Docker, Poetry, Flask, Azure, and Knime.",
    "Big_Data_skills": "In Big Data, he has skills in data visualization, distributed computing, data quality monitoring, data warehousing, and business intelligence.",
    "Big_Data_Tools": " He works with tools such as PowerBI, ETL, OLTP/OLAP, Neo4j, MongoDB, Apache Hadoop, Azure Databricks, and others.",
    "Web_developer_skills": "As a web developer, he has experience with HTML, CSS, JavaScript, PHP, MySQL, and various frameworks like WordPress and Joomla.",
    "Job_experience": "He has professional experience as a web application developer at IB3 Televisió (July 2022 - July 2023), where he implemented new web designs and developed applications using PHP and WordPress.",
    "Languages_spoken": "He is fluent in Catalan and Spanish, has intermediate English proficiency",
    "Hobbies": "He enjoys playing the electric guitar, watching YouTube, and dancing Salsa and Bachata.",
    "Contact_information": "Contact: tofolcanodam@gmail.com, LinkedIn: https://www.linkedin.com/in/cristobal-cano-morey/"
}

# Summarized Curriculum
# summarized_curriculum = """
# Cristóbal Cano is an AI and Big Data specialist with a background in web development. 
# He completed a specialized course in AI and Big Data at IEDIB (2023-2024), a higher degree in web application development at Ies Son Ferrer (2018-2020), 
# and a medium degree in microcomputer systems and networks at Ies Son Ferrer (2015-2018).

# His AI skills include machine learning, deep learning, model deployment, data preprocessing, natural language processing, computer vision, and reinforcement learning. 
# He is proficient with tools like Gradio, Streamlit, Python, Docker, Poetry, Flask, Azure, and Knime.

# In Big Data, he has skills in data visualization, distributed computing, data quality monitoring, data warehousing, and business intelligence. 
# He works with tools such as PowerBI, ETL, OLTP/OLAP, Neo4j, MongoDB, Apache Hadoop, Azure Databricks, and others.

# As a web developer, he has experience with HTML, CSS, JavaScript, PHP, MySQL, and various frameworks like WordPress and Joomla. 
# He has professional experience as a web application developer at IB3 Televisió (July 2022 - July 2023), where he implemented new web designs and developed applications using PHP and WordPress.

# He is fluent in Catalan and Spanish, has intermediate English proficiency, and enjoys playing the electric guitar, watching YouTube, and dancing Salsa and Bachata.

# Contact: tofolcanodam@gmail.com, LinkedIn: https://www.linkedin.com/in/cristobal-cano-morey/
# """

if st.button("Clear Messages"):
    st.session_state.messages.clear()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am a helpful assistant. You can ask me questions about Cristóbal Cano's curriculum."
        }
    ]

# Display chat messages from session state
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

def list_to_natural_language(lst):
    if not lst:
        return "empty list"
    elif len(lst) == 1:
        return lst[0]
    else:
        return ', '.join(lst[:-1]) + ' and ' + lst[-1]

list_of_contexts = list(curriculum_data.keys())
available_categories = list_to_natural_language(list_of_contexts)

def get_context(prompt):
    query = f'What is the only correct category for the following question? Question: "{prompt}"'
    model_name = "deepset/roberta-base-squad2"
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
    QA_input = {
        'question': query,
        'context': available_categories
    }
    res = nlp(QA_input)

    context_obtained = res['answer']

    print(f'Context: {context_obtained}')
    context = context_obtained
    return curriculum_data[context] if context in list_of_contexts else None

def generate_response(prompt, context):
    model_name = "deepset/roberta-base-squad2"
    if context:
        nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
        QA_input = {
            'question': prompt,
            'context': context
        }
        res = nlp(QA_input)
        full_res = f'AI Generated response: {res["answer"]}'
        return full_res, context
    else:
        return None, None

def send_AI_response(response, clarification):
    with st.chat_message(name='assistant'):
        st.write(response)
        st.write(clarification)
    
def log_AI_response(response):
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
# Initialize session state
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

if 'manual_context' not in st.session_state:
    st.session_state.sent = ""

if 'messages' not in st.session_state:
    st.session_state.messages = []

def default():
    print('-default-')
    st.session_state.submitted = False
    st.session_state.sent = ""
# default()
def handle_message(sent):
    with st.chat_message('user'):
        st.markdown(sent)
    
    user_message = {
        "role": "user",
        "content": sent
    }
    st.session_state.messages.append(user_message)

    with st.spinner("Generating response..."):
        context = get_context(sent)

        if st.session_state.submitted:
            print('submitted')
            context = curriculum_data[st.session_state.submitted]
            response, context = generate_response(sent, context)
            clarification = f'Context: "{context}"'
            send_AI_response(response, clarification)
            log_AI_response(response)
            log_AI_response(clarification)
            st.session_state.submitted = False
            st.session_state.sent = ''
        elif context:
            print('context')
            response, context = generate_response(sent, context)
            clarification = f'Context: "{context}"'
            send_AI_response(response, clarification)
            log_AI_response(response)
            log_AI_response(clarification)
        else:
            print('else')
            st.session_state.sent = sent
            st.session_state.submitted = False
            st.rerun()

def handle_form_submit(manual_context):
    print('form sub')
    st.session_state.submitted = manual_context
    st.rerun()

sent = st.chat_input('Ask me anything about the curriculum')
if sent:
    handle_message(sent)
elif st.session_state.sent and st.session_state.submitted:
    handle_message(st.session_state.sent)

# Check if we need to show the form
if st.session_state.sent and not st.session_state.submitted:
    list_expanded = [''] + list_of_contexts
    with st.form(key="manual_context_form"):
        manual_context = st.selectbox(
            "I'm not the smartest AI... What is this question about?",
            options=tuple(list_expanded)
        )
        submit = st.form_submit_button(label='Submit')

        if submit:
            handle_form_submit(manual_context)