import streamlit as st
import os
import json
from GPTcalls import GPTAssistant

if 'selected_question' not in st.session_state:
    st.session_state.selected_question = ""

# Load json
with open('prompts.json', 'r') as file:
    data = json.load(file)
questions = data['questions']
questions.append('Create your own')
prompts = data['prompts']

# Page Header Title
st.set_page_config(page_title="Fine-Tuning Survey", layout="wide")
st.header("Fine-Tuning Answer User Survey")

# Question
select_question = st.selectbox("Select a question to answer", options=questions, index=None)

if select_question == "Create your own":
    select_question = st.text_area("Type your question here")

if select_question and select_question != st.session_state.selected_question:
    st.session_state.selected_question = select_question
    # Generate list of answers here
    complete_prompts = [select_question] + [select_question + " " + prompt for prompt in prompts]
    answers = []

    model = os.environ.get("OPENAI_DEPLOY")
    helper = GPTAssistant(deployment = model)
    with st.spinner("Loading Example Answers"):
        for cp in complete_prompts:
                answers.append(helper.answer_gpt(cp))

    columns = st.columns(len(answers))
    for i in range(0, len(columns)):
        columns[i].header(f"Answer {i+1:02}")
        columns[i].write(answers[i])

# Answer
answer = st.text_area("Type your response here", height=500)

# Submit
submitted = st.button("Submit")
if submitted or answer:
    output = f"Answer submitted! You wrote {len(answer)} characters"
    st.write(output)
    # Do the saving to json file
    file_name = select_question[:-1]+'.json'
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
            data['answer'].append(answer)
    else:
        data = {}
        data['question'] = select_question
        data['answer'] = [answer]
    
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

