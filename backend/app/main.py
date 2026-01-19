from fastapi import FastAPI
from app.routes import uploads # Importa sua rota
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Minha API para Bot e Web")

# Configura para que as imagens salvas sejam acessíveis via URL pelo Next.js
app.mount("/static", StaticFiles(directory="static"), name="static")

# "Inclui" as rotas do arquivo de uploads na aplicação principal
app.include_router(uploads.router)

@app.get("/")
def read_root():
    return {"message": "API Online"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)