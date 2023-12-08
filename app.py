import time
from langchain.chat_models import ChatOpenAI
from dotenv import dotenv_values
import streamlit as st
import base64

from prompts.base import BasePrompter
from prompts.index import get_all_configs, get_prompter

# Parse .env file
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

def autoplay_audio(audio):
    b64 = base64.b64encode(audio).decode()
    md = f"""
        <audio controls autoplay="true" style="width: 100%">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
    st.session_state.autoplay_audio_ref = st.markdown(
        md,
        unsafe_allow_html=True,
    )

def render_message(message, is_last=False):
    with st.chat_message("user" if message['is_user'] else "assistant"):
        st.write(message['message'])

        if 'audio' in message:
            if is_last:
                autoplay_audio(message['audio'])
            else:
                st.audio(message['audio'], format='mp3')

        if 'image' in message:
            st.image(message['image'])

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
            
    # Display chat messages
    for message in st.session_state.chat_history:
        render_message(message)

    # Chat area
    user_message = st.chat_input("Type your message here:")
    if user_message:
        # Delete autoplay audio component
        if 'autoplay_audio_ref' in st.session_state:
            st.session_state.autoplay_audio_ref.empty()

        st.session_state.chat_history.append({'message': user_message, 'is_user': True})
        render_message(st.session_state.chat_history[-1])
        
        if user_message == 'sleep':
            time.sleep(60)

        # Run model
        with st.spinner('Thinking...'):
            prompter: BasePrompter = st.session_state.prompter
            response_message = prompter(st.session_state.chat_history)
            st.session_state.chat_history.append(response_message)
        render_message(st.session_state.chat_history[-1], is_last=True)

        

if __name__ == '__main__':
    main()
