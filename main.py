import streamlit as st
import os
import json
from GPTcalls import GPTAssistant

# Load json
with open('prompts.json', 'r') as file:
    data = json.load(file)
questions = data['questions']
prompts = data['prompts']

# Page Header Title
st.set_page_config(page_title="Fine-Tuning Survey", layout="wide")
st.header("Fine-Tuning Answer User Survey")

# Question
select_question = st.selectbox("Select a question to answer", options=questions, index=None)

if select_question == "Create your own":
    question = st.text_area("Type your question here")

if select_question:
    # Generate list of answers here
    complete_prompts = [select_question] + [select_question + " " + prompt for prompt in prompts]
    answers = []

    model = os.environ.get("OPENAI_DEPLOY")
    helper = GPTAssistant(deployment = model)
    for cp in complete_prompts:
        answers.append(helper.answer_gpt(cp))

    columns = st.columns(len(questions))
    for i in range(0, len(columns)):
        columns[i].header(f"Answer {i+1:02}")
        columns[i].write(answers[i])

# Answer
answer = st.text_area("Type your response here")

# Submit
if answer:
    output = f"Answer submitted! You entered: {answer}"
    st.write(output)
    # Do the saving to json file
    answer = ''

# # Submit
# submitted = st.button("Submit")
# if submitted:
#     st.write("Answer submitted!")
#     # Do the saving to json file
#     submitted = False

