# from langchain.document_loaders import TextLoader
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.llms import OpenAI
# from langchain.chains import ConversationalRetrievalChain
# import os

# loader = TextLoader("static/data/camp_knowledge.txt")
# os.environ['OPENAI_API_KEY'] =
# documents = loader.load()
# text_splitter = CharacterTextSplitter(
#     chunk_size=1000,  separator="\n", chunk_overlap=0)
# documents = text_splitter.split_documents(documents)

# embeddings = OpenAIEmbeddings()
# vectorstore = Chroma.from_documents(documents, embeddings)
# persist_directory = 'static/db'

# embedding = OpenAIEmbeddings()
# vectordb = Chroma.from_documents(
#     documents=documents, embedding=embedding, persist_directory=persist_directory)
# vectordb.persist()
