from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.history_aware_retriever import create_history_aware_retriever
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def qa_agent(openai_api_key, chat_history, uploaded_file, question):

    model = ChatOpenAI(model="gpt-4o-mini", openai_api_key=openai_api_key)
    file_content = uploaded_file.read()
    temp_file_path = "temp.pdf"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file_content)
    loader = PyPDFLoader(temp_file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        separators=["\n", ".", "!", "?",","," ", ""]
    )
    text = text_splitter.split_documents(docs)
    embedding_model = OpenAIEmbeddings()
    db = FAISS.from_documents(text, embedding_model)
    retriever = db.as_retriever()

    history_prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        ("system", "Given the history, summarize and conclude it. Rephase the user's input into a standalone query.")
    ])

    retriever_chain = create_history_aware_retriever(model, retriever, history_prompt)

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the question base on this context: {context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

    doc_chain = create_stuff_documents_chain(model, qa_prompt)

    chain = create_retrieval_chain(retriever_chain, doc_chain)

    response = chain.invoke({
        "input": question,
        "chat_history": chat_history
    })

    #clean up temp file
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

    return response["answer"]




