import streamlit as st
import os

# Page Header Title
st.set_page_config(page_title="Fine-Tuning Survey", layout="wide")

st.header("Fine-Tuning Answer User Survey")

# Question
question_list = ["This is a question", "This is another question", "Create your own"]
question = st.selectbox("Select a question to answer", options=question_list, index=None)

if question == "Create your own":
    question = st.text_area("Type your question here")

if question:
    # Generate list of answers here
    example_answer_list = ['a', 'b', 'c', 'd', '54j3ryf8e39dj59u547y6fj594tyuj4958tfyu9t8yjfdt9w845tjf9458y7tk2d389yjtf3otyk3d8wt4j7f3958ty7kd2387tjf8357tkd3284957yjf3985ytkd2834y76kf32809-tk389056y7jg2983ykdt389tj7fy32-897tkf89352y7t4395jtyf98wytkdwetyujfw38utfk3-908tuyjgq30-8utkfw038ytgw8903uyftk0-w85utyjg0w84utk3fw09tfjk380wyjg83w09-kft0-3467hq034j7gyw-8307t4kf3w2047k6fj803-5jy6f8-027j65ft-84jgt']

    columns = st.columns(5)
    for i in range(0, len(columns)):
        columns[i].header(f"Answer {i+1:02}")
        columns[i].write(example_answer_list[i])

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

