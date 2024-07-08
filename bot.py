from openai import OpenAI
import streamlit as st
from PIL import Image
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
import os
from PIL import Image
logo_path = '/Users/muhammadahmed/Desktop/Projects/foxtrot/f.png'  # Replace with the path to your team logo
logo = Image.open(logo_path)

# Load scraped content from the file
with open("/Users/muhammadahmed/Desktop/Projects/foxtrot/scrape.txt", "r", encoding="utf-8") as file:
    model = file.read()

# Set OpenAI API key (replace with your actual key)
os.environ["OPENAI_API_KEY"] = ""





import streamlit as st


from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template





def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    
    if "conversation_log" not in st.session_state:
        st.session_state.conversation_log = []

  
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    # Log user's question and bot's response
    user_message = {'role': 'user', 'content': user_question}
    bot_message = {'role': 'bot', 'content': response['chat_history'][-1].content}
    st.session_state.conversation_log.append(user_message)
    st.session_state.conversation_log.append(bot_message)

    # Display the conversation log
    for message in st.session_state.conversation_log:
        if message['role'] == 'user':
            st.write(user_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)


if(model!=None):
    
    st.set_page_config(page_title="Team Foxtrot Chatbot")
                       
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
        
    st.image(logo, caption="Team Foxtrot", use_column_width=True)    
   

    st.header("Team Foxtrot Chatbot")
    user_question = st.text_input("Ask a question about the team")
    if user_question:
        handle_userinput(user_question)

    if(model!=None):
       
       
        if (model!=None):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = model

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)


