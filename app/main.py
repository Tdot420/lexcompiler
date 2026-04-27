from fastapi import FastAPI, UploadFile, File, HTTPException
from app.parser import parse_pdf
from app.compiler import compile_to_graph
from app.inference import run_inference

app = FastAPI()

@app.post("/upload_and_compile")
async def upload_and_compile(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = parse_pdf(content)
        graph = compile_to_graph(text)
        return graph
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/run_inference")
async def inference(data: dict):
    results, meu = run_inference(data["graph"], data["observed_facts"])
    return {
        "posterior_probabilities": results,
        "meu_score": meu
    }