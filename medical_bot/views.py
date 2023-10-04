from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import GooglePalmEmbeddings
from langchain.llms import GooglePalm
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import pinecone
import os
import requests
from bs4 import BeautifulSoup
import spacy
from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub
from decouple import config
from rest_framework import response,status
from rest_framework.decorators import api_view

# Retrive Info From Online
def retrieve_data(query,data):
    file = open('data/index.txt','+a') 
    file.write(data)
    
    loader = TextLoader("data/index.txt")
    document = loader.load()
    # os.remove('data/index.txt')
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size =100, chunk_overlap=0, separators=[" ", ",", "\n"])
    docs = text_splitter.split_documents(document)
    
    embedding = HuggingFaceEmbeddings()
    db = FAISS.from_documents(docs, embedding)
    llm=HuggingFaceHub(
        repo_id="google/flan-t5-xxl", 
        model_kwargs={"temperature":0.1, "max_length":40}
        )
    chain = load_qa_chain(llm, chain_type="stuff")
    docs = db.similarity_search(query)
    return chain.run(input_documents=docs, question=query)

# Web Scrapping 
def getdata(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        
            soup = BeautifulSoup(resp.text, 'html.parser')
            p_tags = soup.find_all('p')
            data = ""
            for p_tag in p_tags:
                data = data+p_tag.get_text()
            return data
        
    else:
        print('Failed to retrieve the web page. Status code:', resp.status_code)
        
def modifysentances(sentence):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(sentence)
        important_tokens = []
        for token in doc:
            if not token.is_stop and not token.is_punct and token.text.strip():
                important_tokens.append(token.text)
        
        return important_tokens

def get_top_search_results(query, num_results=10):
    url = f"https://www.google.com/search?q={query}"
    resp = requests.get(url)
    
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        search_results = soup.find_all("a")
        top_results = []
        for link in search_results:
            href = link.get('href')
            if href.startswith("/url?q="):
                url = href.replace("/url?q=", "").split("&")[0]
                top_results.append(url)
        return top_results[:num_results]
    else:
        print("Error: Unable to retrieve search results.")
        return []

def webscrapping(query):
    token = modifysentances(query)
    text = " ".join(token)
    top_results = get_top_search_results(text)
    data = ""
    worked = 0
    if top_results:
        for i, result in enumerate(top_results, start=1):
            if(worked<=1):
                if(getdata(result)):
                    data = data+getdata(result)
                    print(worked)
                    worked += 1
    else:
        return "Problem Occured"
    return retrieve_data(query,data)


loader = PyPDFDirectoryLoader("pdfs")
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
text_chunks = text_splitter.split_documents(data)

embeddings=GooglePalmEmbeddings()

# initialize pinecone
pinecone.init(
    api_key=config('PINECONE_API_KEY'),  # find at app.pinecone.io
    environment=config('PINECONE_API_ENV')  # next to api key in console
)
index_name = "amitava" # put in the name of your pinecone index here

# docsearch = Pinecone.from_texts([t.page_content for t in text_chunks], embeddings, index_name=index_name)

docsearch = Pinecone.from_existing_index(index_name, embeddings)
llm = GooglePalm(temperature=0.1)
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())

prompt_template  = """
Use the following piece of context to answer the question. Please provide a detailed response for each of the question.

{context}

Question: {question}

Answer in Any Language"""

prompt = PromptTemplate(template = prompt_template , input_variables=["context", "question"])


@api_view(['POST'])
def bot_req(request):
    data = request.data
    query = str(data['query'])
    mode = str(data['mode'])
    if(mode == "online"):
        try:
            result =  webscrapping(query)
            return response.Response({'status':200,'message':result},status=status.HTTP_200_OK)
        except:
            return response.Response({'status':500,'message':"Error Occured"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif(mode == "book"):
        try:
            result = qa({'query': query})
            return response.Response({'status':200,'message':result['result']},status=status.HTTP_200_OK)
        except:
            return response.Response({'status':500,'message':"Error Occured"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    else:
        return response.Response({'status':503,'message':"Service Unavailable"},status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        