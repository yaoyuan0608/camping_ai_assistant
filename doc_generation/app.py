from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
import gradio as gr
import openai
import sys
import os

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAPI_KEY")

def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index = GPTSimpleVectorIndex.from_documents(
        documents, service_context=service_context
    )

    index.save_to_disk('index.json')

    return index

def check(input_response):
    prompt = 'Does the sentence associated with camping? return the score from 0 to 1' + input_response.response
    messages = [{ "role": "user", "content": prompt}]
         
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = messages,
        temperature = 0
    )
    prob = response.choices[0]['message']['content']
    tries = 0
    while tries < 3:
        try:
            prob = float(prob)
            break
        except:
            prob = response.choices[0]['message']['content']
            tries += 1

    if prob < 0.:
        return False
    else:
        return True
    
def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    if check(response):
        return response.response
    else:
        return "I don't know what you are talking about, try again!"

iface = gr.Interface(fn=chatbot,
                     inputs=gr.inputs.Textbox(lines=7, label="Enter your text"),
                     outputs="text",
                     title="Custom-trained AI Chatbot")

index = construct_index("docs")
iface.launch(share=True)