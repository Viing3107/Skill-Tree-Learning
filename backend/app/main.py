import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.ai_service import generate_skill_tree
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Cho phép frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://skill-tree-learning-gamma.vercel.app","http://localhost:5173/"], # Link vercel sau khi deploy xong
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend is running"}

class SubjectRequest(BaseModel):
    subject: str

@app.post("/generate-skill-tree")
def generate_tree(data: SubjectRequest):
    tree = generate_skill_tree(data.subject)
    return tree

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)