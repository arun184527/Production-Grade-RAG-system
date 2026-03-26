import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/chat"


def chat_fn(message):
    try:
        response = requests.post(
            API_URL,
            json={"query": message},
            timeout=60
        )

        data = response.json()

        answer = data.get("answer", "")

        retrieved = "\n\n".join(data.get("retrieved_chunks", []))
        reranked = "\n\n".join(data.get("reranked_chunks", []))

        tokens = f"{data.get('input_tokens', 0)} → {data.get('output_tokens', 0)}"
        latency = f"{data.get('latency', 0):.2f} sec"

    except Exception as e:
        answer = f"Error: {str(e)}"
        retrieved, reranked, tokens, latency = "", "", "", ""

    return answer, retrieved, reranked, tokens, latency


with gr.Blocks() as demo:
    gr.Markdown("# RAG Chatbot Dashboard")

    msg = gr.Textbox(label="Ask Question")
    answer_box = gr.Textbox(label="Answer")

    with gr.Row():
        retrieval_box = gr.Textbox(label="Retrieval", lines=10)
        rerank_box = gr.Textbox(label="Reranking", lines=10)

    with gr.Row():
        tokens_box = gr.Textbox(label="Tokens")
        latency_box = gr.Textbox(label="Latency")

    msg.submit(
        chat_fn,
        msg,
        [answer_box, retrieval_box, rerank_box, tokens_box, latency_box]
    )

demo.launch()