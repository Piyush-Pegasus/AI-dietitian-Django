from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_community.embeddings import  OllamaEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
import tempfile

load_dotenv()
api_key=os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
# os.environ['GOOGLE_API_KEY' ]= api_key
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")


def get_pdf_text(pdf_docs):
    loader = PyPDFLoader(pdf_docs)
    docs = loader.load()
    return docs


def get_text_chunks(pdf_docs):
    text=get_pdf_text(pdf_docs)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(text)
    return chunks


def get_vector_ollama(pdf):
    doc_chunks= get_text_chunks(pdf)
    embeddings = OllamaEmbeddings()
    vector_store = FAISS.from_documents(doc_chunks, embedding=embeddings)
    # vector_store.save_local("faiss_index")
    return vector_store

def get_vector_google(pdf):
    doc_chunks= get_text_chunks(pdf)
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_documents(doc_chunks, embedding=embeddings)
    return vector_store


def get_deficiencies(pdf):
    prompt_template = ChatPromptTemplate.from_template("""
    You are an expert pathologist.Analyse the report of the patient given as context
    and identify the potential deficiencies, excesses and diseases or health conditions in the key nutrients.                                               
    <context>
    {context}
    </context> 
    User Query :{input}
    """)

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest",
                             temperature=0)
    document_chain= create_stuff_documents_chain(llm, prompt_template)
    vector_store = get_vector_google(pdf)
    retriever=vector_store.as_retriever()
    retriever_chain = create_retrieval_chain(retriever, document_chain)
    # response = retriever_chain.invoke()
    #if question is mandatory the pass find defieciencies in the blood report
    response = retriever_chain.invoke({'input': 'Give me the analysis of the report including deficiencies and excesses in the blood report.Also provide information about any diseases or health conditions in the report.'})
    return response['answer']

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-1.5-pro-latest')
    prompt="""You are an expert dietitian.
   With the input provided from user about his body health, details, food preferences and 
   other details, generate a 7 day diet plan. 
   Think step by step before providing a detailed answer. 
   Strictly Create a personalized diet plan for a user with the input information don't throw errors:"""
    
    response=model.generate_content([prompt,input])
    return response.text

def format_age(age):
      if age is not None:
        return f"age: {age} years"
      return ""

def format_height(height):
      if height is not None:
        return f"height: {height} cm"
      return ""

def format_weight(weight):
      if weight is not None:
        return f"weight: {weight} kgs"
      return ""

def dietplan(request):
    if request.method=='POST':
        data=request.POST
        pdf=request.FILES.get('report')
        print(pdf)
        deficiencies=''
        if pdf is not None:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(pdf.read())
                tmp_file_name = tmp.name
            deficiencies=get_deficiencies(tmp_file_name)
        # deficiencies=get_deficiencies(pdf)
        print(deficiencies)
        age=data['age']
        height=data['height']
        weight=data['weight']
        activity_level=data['activity-level']
        medical_conditions=data['allergies']
        preferences=data['preferences']
        goals=data['goals']
        prompt1="The deficiencies in the report of the person are: "+deficiencies
        prompt_part3 = "User Informatiom:\n"
        prompt_part3 += format_age(age) + "\n"
        prompt_part3 += format_height(height) + "\n"
        prompt_part3 += format_weight(weight) + "\n"
        if(activity_level!=None):
          prompt_part3 +="Activity level: "+activity_level + "\n"
        if(medical_conditions != None):
            prompt_part3 += "Medical conditions: " + medical_conditions + "\n"
        if(preferences != None):
          prompt_part3 += "Dietary preferences: " + preferences + "\n"
        if(goals != None):
            prompt_part3 += "Dietry Goals: " + goals + "\n"
        prompt = prompt1 + prompt_part3
        
        response=get_gemini_repsonse(prompt)
        return JsonResponse({'message':response})
    return render(request,'dietplan.html')