import os
import gradio as gr
from main import process_pdf


def run(pdf, user_prompt, schema):
    """
    Pipeline complet :
    PDF + prompt utilisateur + schema JSON → JSON résultat
    """

    if pdf is None:
        return {"error": "Aucun PDF fourni"}

    pdf_path = pdf.name

    try:
        result = process_pdf(pdf_path, user_prompt, schema)
        return result
    except Exception as e:
        return {"error": str(e)}


with gr.Blocks() as app:

    gr.Markdown("# 📄 PDF → JSON Extractor (POC)")

    pdf_input = gr.File(label="Upload PDF")

    prompt_input = gr.Textbox(
        label="Prompt utilisateur",
        placeholder="Ex: extraire les infos importantes du document"
    )

    schema_input = gr.Textbox(
        label="Schéma JSON (fourni par l'utilisateur)",
        value='{"cle": "valeur"}',
        lines=6
    )

    output = gr.JSON(label="Résultat JSON")

    btn = gr.Button("Lancer extraction")

    btn.click(
        fn=run,
        inputs=[pdf_input, prompt_input, schema_input],
        outputs=output
    )

server_name = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
server_port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
app.launch(server_name=server_name, server_port=server_port)