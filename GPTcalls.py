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
        response = self.client.chat.completions.create(
            model = self.deployment,
            messages=[
                {"role": "system", "content": f"""
                You serve as a tool for filtering, organizing and structuring texts.
                """},
                {"role": "user", "content": f"""
                A large document was divided into parts and the inputs are:
                Previous: Part of the previous text partition.
                Actual: Partition the current text.
                Next: Part of the following text partition.
                The strategy is to use the current partition with parts of the texts that surround it to create context.
                You must rewrite the text considering the information provided in order to filter the text in order to generate a consolidated and clean text output.
                Follow the following instructions:
                1. Try to maintain the structure of the text provided as much as possible.
                2. When identifying that this is information about the cover, back cover, summary, dedication, Epigraph, Preface and Presentation of a document, article or book, do not include this information.
                3. Please do not reference Figures, Tables, Sections and Images in the generated text (e.g.: "As seen in Figure x ...", "As seen in Table x ...", "This text presents ...")
                4. When checking unfinished information, remove it.
                5. Do not include information about authors.
                6. Prioritize maintaining a good context.
                Given this information:
                * Previous text: {previous}
                * Actual text: {actual}
                * Next text: {next}
                Create output text taking into account the guidelines above.
                """}
            ]
        )
        return response.choices[0].message.content