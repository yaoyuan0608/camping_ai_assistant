import faiss
from langchain import OpenAI
from langchain.chains import VectorDBQAWithSourcesChain, ConversationalRetrievalChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
import pickle
import os
import time

class chatbot:
    def __init__(self):
        self.chain = self.load_chain()
        self.generated = []
        self.past = []
        self.time_windows = []
        self.start = time.time()

    def load_chain(self):
        os.environ["OPENAI_API_KEY"] = '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'
        index = faiss.read_index("docs.index")
        with open("faiss_store.pkl", "rb") as f:
            store = pickle.load(f)
        store.index = index
        self.chain = VectorDBQAWithSourcesChain.from_llm(
            llm=OpenAI(temperature=0,max_tokens=1500, model_name='text-davinci-003'), vectorstore=store)
        
    def return_start_time(self):
        return self.start
    
    def output_response(self, input_text):
        result = self.chain({"question": input_text})
        output = result['answer']
        self.past.append(input_text)
        self.generated.append(output)
        self.time_windows.append(time.time())
        return output