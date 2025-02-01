import logging
import chainlit as cl
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Chatbot:
    def __init__(self, model_name="deepseek-r1:1.5b", temperature=0.6):
        # Initialize memory to store conversation history
        self.memory = ConversationBufferMemory(return_messages=True)
        
        # Initialize the language model
        self.model = Ollama(
            model=model_name,
            base_url="http://ollama:11434",
            temperature=temperature,
            num_predict=2000
        )
        
        # Define the prompt template for the chatbot
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert AI assistant. 

            Key Guidelines:
            - Use clear, conversational language
            - Explain complex concepts simply
            - Break information into digestible steps
            - Make learning engaging and fun
            - Use age-appropriate examples
            - Encourage curiosity and understanding

            """),
            ("human", "{question}")
        ])

        # Create the processing chain with memory integration
        self.chain = (
            RunnablePassthrough.assign(
                chat_history=self.memory.load_memory_variables  # Load memory for context
            )
            | self.prompt 
            | self.model 
            | StrOutputParser()
        )

@cl.on_chat_start
async def start_chat():
    # Initialize chatbot and store it in session variables
    chatbot = Chatbot()
    cl.user_session.set("chatbot", chatbot.chain)
    cl.user_session.set("chatbot_instance", chatbot)
    cl.user_session.set("clean_response", True)  # Default to clean responses

    # Enhanced welcome message for users
    await cl.Message(
        content="""## 🚀 Let's go! 

### Quick Commands:
- `/toggle_thoughts`: See behind-the-scenes thinking

What topic shall we explore today? 🤔"""
    ).send()

@cl.on_message
async def process_message(message):
    chain = cl.user_session.get("chatbot")
    chatbot = cl.user_session.get("chatbot_instance")
    
    try:
        if not message.content.strip():
            await cl.Message(content="Oops! Looks like your message is empty. What would you like to learn?").send()
            return
        
        # Command handling for toggling thoughts visibility
        if message.content.strip().lower() == "/toggle_thoughts":
            current_setting = cl.user_session.get("clean_response", True)
            new_setting = not current_setting
            cl.user_session.set("clean_response", new_setting)

            response_msg = "🕵️ Thoughts are now " + ("hidden" if new_setting else "visible") + " in responses!"
            await cl.Message(content=response_msg).send()
            return

        logger.info(f"Processing message: {message.content}")
        
        # Invoke the chain with the current message and chat history
        response = await chain.ainvoke({
            "question": message.content,
            "chat_history": chatbot.memory.chat_memory.messages  # Pass chat history for context
        })

        # Clean response based on user preference
        user_prefers_clean_response = cl.user_session.get("clean_response", True)
        clean_response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip() if user_prefers_clean_response else response
        
        # Store messages in memory for future context usage
        chatbot.memory.save_context(
            {"input": message.content}, 
            {"output": clean_response}
        )
        
        logger.info(f"Generated response: {clean_response}")
        
        await cl.Message(content=clean_response).send()
    
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await cl.Message(content="🤖 Oops! Something went a bit wonky. Could you rephrase your question?").send()

if __name__ == "__main__":
    cl.run(host="0.0.0.0", port=3000)
