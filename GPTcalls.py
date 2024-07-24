import os
import openai
import streamlit as st

class GPTAssistant:
    def __init__(self, deployment):
        self.endpoint = st.secrets["OPENAI_URL"]
        self.api_key = st.secrets["OPEN_AI_KEY"]
        self.deployment = deployment
        self.client = openai.AzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
            api_version="2024-02-01",
        )
    
    def answer_gpt(self, prompt):
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": f"""
                    You are a process engineer assistant who is experienced with working at a chemical plant.
                """},
                {"role": "user", "content": prompt}
            ],
            stream=True,
        )
        return response
    
# if __name__ == "__main__":
    # load_dotenv()
    # model = os.environ.get("OPENAI_DEPLOY")
    # helper = GPTAssistant(deployment = model)
    # print(helper.answer_gpt("What troubleshooting steps should I take if my centrifugal pump is experiencing low flow?"))