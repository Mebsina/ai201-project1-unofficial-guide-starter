"""
app.py: Gradio web interface for the Unofficial Guide.

Usage:
    python app.py             # then open http://localhost:7860
"""

import gradio as gr

from query import ask


def handle_query(question: str):
    if not question or not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"  {s}" for s in result["sources"]) or "(no sources used)"
    return result["answer"], sources


with gr.Blocks(title="The Unofficial Guide — UT Dallas CS") as demo:
    gr.Markdown("# The Unofficial Guide\nAsk anything about UT Dallas CS professors.")
    inp = gr.Textbox(label="Your question", placeholder="e.g. What should students watch out for in Professor Karrah's class?")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=4)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()
