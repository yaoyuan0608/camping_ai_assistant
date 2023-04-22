"""Ask a question to database."""
import faiss
from langchain import OpenAI
from langchain.chains import VectorDBQAWithSourcesChain
import pickle
import argparse
import os

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAPI_KEY")

parser = argparse.ArgumentParser(description='Ask a question.')
parser.add_argument('question', type=str, help='The question to ask')
args = parser.parse_args()

# Load the LangChain.
index = faiss.read_index("docs.index")

# Load the faiss store, which contains the vector store.
with open("faiss_store.pkl", "rb") as f:
    store = pickle.load(f)

store.index = index
chain = VectorDBQAWithSourcesChain.from_llm(llm=OpenAI(temperature=0), vectorstore=store)
result = chain({"question": args.question})
print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")