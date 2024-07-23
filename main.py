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

# Page Header Title
st.set_page_config(page_title="Fine-Tuning Survey", layout="wide")
st.header("Fine-Tuning Answer User Survey")

# Question
questions = st.session_state.questions
select_question = st.selectbox("Select a question to answer", options=questions, index=None)

if select_question == "Create your own":
    with st.form('question'):
        select_question = st.text_area("Type your question here")
        submitted_custom_question = st.form_submit_button("Submit Question")

if st.button("Refresh Answers"):
    st.rerun()

if select_question:
    with st.form("my_form"):
        complete_prompts = [select_question] + [select_question + " " + prompt for prompt in st.session_state.extra_instructions]
        answers = []

        model = st.secrets["OPENAI_DEPLOY"]
        helper = GPTAssistant(deployment = model)
        index = 0
        size = len(complete_prompts)
        for index, cp in enumerate(complete_prompts, start=1):
            progress = f"Loading Example Answers: {(index * 100) // len(complete_prompts)}% Complete"
            with st.spinner(progress):
                try:
                    answers.append(helper.answer_gpt(cp))
                except Exception as e:
                    st.write("Enter another question. The one you entered was invalid.")
                    st.rerun()

        if answers:
            columns = st.columns(len(answers))
            for i in range(0, len(columns)):
                columns[i].header(f"Answer {i+1:02}")
                columns[i].write(answers[i])

        new_response = st.text_area("Type your response here", height=500)

        submitted = st.form_submit_button("Submit")

        if submitted:
            url = 'https://nhanfdvbgpgcxrqcjful.supabase.co'
            key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5oYW5mZHZiZ3BnY3hycWNqZnVsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjE3NTg1OTksImV4cCI6MjAzNzMzNDU5OX0.dkDZKZvw6deIu-i-yC4TYbeK-ASlEX5fMiYyKy1VmWY'
            supabase = create_client(url, key)
            
            response = (
                supabase.table("qa-pairs")
                .insert({"id": int(time.time() * 1000), "question": select_question, "answer": new_response})
                .execute()
            )

            st.write(f"Answer submitted! You wrote {len(new_response)} characters")