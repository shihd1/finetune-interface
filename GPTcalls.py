import os
import openai
from dotenv import load_dotenv

class GPTAssistant:
    def __init__(self, deployment):
        load_dotenv(override=True)
        self.endpoint = os.environ.get("OPENAI_URL")
        self.api_key = os.environ.get("OPEN_AI_KEY")
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
            ]
        )
        return response.choices[0].message.content
    
if __name__ == "__main__":
    load_dotenv()
    model = os.environ.get("OPENAI_DEPLOY")
    helper = GPTAssistant(deployment = model)
    print(helper.answer_gpt("What troubleshooting steps should I take if my centrifugal pump is experiencing low flow?"))