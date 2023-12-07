from langchain.chat_models import ChatOpenAI

import streamlit as st

# Parse .env file
from dotenv import dotenv_values

from prompts.index import get_all_configs, get_prompter

config = dotenv_values(".env")
OPENAI_API_KEY = config['OPENAI_API_KEY']

configs = get_all_configs()

# Setup model
def reset():
    st.session_state.model = ChatOpenAI(streaming=True, model=st.session_state.config['model'], temperature=st.session_state.config['temperature'], openai_api_key=OPENAI_API_KEY)

    Prompter = get_prompter(st.session_state.config['topic'], st.session_state.config['subtopic'])
    st.session_state.prompter = Prompter(st.session_state.model, st.session_state.config)

    first_message = {'message': st.session_state.prompter.first_message(), 'is_user': False}
    st.session_state.chat_history = [first_message]

def main():
    st.title('English Learning Chatbot')

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        
    with st.sidebar:
        topic = st.radio("Select a topic", configs.keys())
        subtopic = st.selectbox('Choose a Subtopic', configs[topic])

        st.markdown('---')

        with st.expander("Developer Config", expanded=False):
            model = st.selectbox('Select ChatGPT Model', ['gpt-4-1106-preview', 'gpt-3.5-turbo-1106', 'gpt-4', 'gpt-3.5-turbo'])
            temperature = st.slider('Select Temperature', min_value=0.0, max_value=2.0, value=1.0)

            st.button('Reset Chat History', on_click=reset)

        # Set config
        if 'config' not in st.session_state or st.session_state.config['topic'] != topic or st.session_state.config['subtopic'] != subtopic or st.session_state.config['model'] != model or st.session_state.config['temperature'] != temperature:
            st.session_state.config = {
                'topic': topic,
                'subtopic': subtopic,
                'model': model,
                'temperature': temperature
            }
            reset()

    # Chat area
    user_message = st.chat_input("Type your message here:")
    if user_message:
        st.session_state.chat_history.append({'message': user_message, 'is_user': True})

        # Run model
        prompter = st.session_state.prompter
        response_message = prompter(st.session_state.chat_history)
        st.session_state.chat_history.append(response_message)

    # Display chat messages
    for chat in st.session_state.chat_history:
        with st.chat_message("user" if chat['is_user'] else "assistant"):
            st.write(chat['message'])
            if 'audio' in chat:
                st.audio(chat['audio'], format='mp3')

if __name__ == '__main__':
    main()
