from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from crew import run_article_generation

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TopicRequest(BaseModel):
    topic: str

@app.post("/generate_article")
async def generate_article(req: TopicRequest): # funcao que recebe o topico e retorna o artigo
    article = run_article_generation(req.topic) # .req funciona como um dicionario que recebe o topico
    # Aqui você pode adicionar lógica adicional, como salvar o artigo gerado em um banco de dados
    
    return {"article": article}
