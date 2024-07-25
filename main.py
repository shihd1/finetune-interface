import streamlit as st
import os
import json
from GPTcalls import GPTAssistant
import os
import time
from supabase import create_client

# Initialize session state if not already done
if 'questions' not in st.session_state:
    with open('prompts.json', 'r') as file:
        data = json.load(file)
        data['questions'].append('Create your own')
        st.session_state.questions = data['questions']
        st.session_state.extra_instructions = data['prompts']
if 'answer' not in st.session_state:
    st.session_state.answer=' '

# Page Header Title
st.set_page_config(page_title="Fine-Tuning Survey", layout="wide")
st.header("Fine-Tuning Answer User Survey")

# Question
questions = st.session_state.questions
select_question = st.selectbox("Select a question to answer", options=questions, index=None, key='selection')

if select_question == "Create your own":
    with st.form('question'):
        select_question = st.text_area("Type your question here")
        submitted_custom_question = st.form_submit_button("Submit Question")

if st.button("Refresh Answers"):
    st.rerun()

if select_question:
    with st.form("my_form", clear_on_submit=True):
        complete_prompts = [select_question] + [select_question + " " + prompt for prompt in st.session_state.extra_instructions]

        model = st.secrets["OPENAI_DEPLOY"]
        helper = GPTAssistant(deployment = model)
        index = 0
        size = len(complete_prompts)
        columns = st.columns(len(complete_prompts))
        for index, cp in enumerate(complete_prompts):
            # progress = f"Loading Example Answers: {index-1}/{len(complete_prompts)} Complete"
            # with st.spinner(progress):
            try:
                columns[index].header(f"Answer {index+1:02}")
                columns[index].write_stream(helper.answer_gpt(cp))
            except Exception as e:
                st.write("Enter another question. The one you entered was invalid.")
                st.rerun()

        new_response = st.text_area("Type your response here", height=500, key='answer')

        def reset():
            url = 'https://nhanfdvbgpgcxrqcjful.supabase.co'
            key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5oYW5mZHZiZ3BnY3hycWNqZnVsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjE3NTg1OTksImV4cCI6MjAzNzMzNDU5OX0.dkDZKZvw6deIu-i-yC4TYbeK-ASlEX5fMiYyKy1VmWY'
            supabase = create_client(url, key)
            
            answer = st.session_state.answer

            response = (
                supabase.table("qa-pairs")
                .insert({"id": int(time.time() * 1000), "question": select_question, "answer": answer})
                .execute()
            )

            st.session_state.selection = None

        submitted = st.form_submit_button("Submit", on_click=reset)