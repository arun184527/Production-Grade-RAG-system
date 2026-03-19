import gradio as gr
import requests
API_URL = "https://unmaniacal-bicentric-brian.ngrok-free.dev/chat"

def chat(user_message, history):
    try:
        response = requests.post(
            API_URL,
            json={"query": user_message}
        )

        answer = response.json()["response"]

    except:
        answer = "Error connecting to server"

    history.append((user_message, answer))
    return "", history
with gr.Blocks() as demo:
    gr.Markdown("##  RAG Chatbot (Your Data)")

    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask something...")

    msg.submit(chat, [msg, chatbot], [msg, chatbot])

demo.launch()