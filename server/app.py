from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import os

from support.env import SupportEnv
from support.tasks import TASKS
from support.models import Action

app = FastAPI(title="SupportAgent OpenEnv API")

# Initialize environment with all tasks
env_instance = SupportEnv(TASKS)

class StepRequest(BaseModel):
    action: Action

# API Routes
@app.get("/api/health")
@app.get("/health")
async def health():
    return {"status": "online", "env": "SupportAgentEnv"}

class ResetRequest(BaseModel):
    task_name: Optional[str] = None

@app.post("/api/reset")
@app.post("/reset")
async def reset(request: Optional[ResetRequest] = None):
    try:
        task_name = request.task_name if request else None
        result = await env_instance.reset(task_name)
        obs = result["observation"]
        return {
            "observation": obs.model_dump() if hasattr(obs, 'model_dump') else obs.dict(),
            "reward": float(result["reward"]),
            "done": bool(result["done"]),
            "info": result["info"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/step")
@app.post("/step")
async def step(request: StepRequest):
    try:
        result = await env_instance.step(request.action)
        obs = result["observation"]
        return {
            "observation": obs.model_dump() if hasattr(obs, 'model_dump') else obs.dict(),
            "reward": float(result["reward"]),
            "done": bool(result["done"]),
            "info": result["info"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/state")
@app.get("/state")
async def state():
    try:
        s = await env_instance.state()
        return s.model_dump() if hasattr(s, 'model_dump') else s.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve Frontend
dist_path = os.path.join(os.getcwd(), "dist")
if os.path.exists(dist_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(dist_path, "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # If the path looks like an API call, let it fall through
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404)
        
        # Serve index.html for all other routes
        index_file = os.path.join(dist_path, "index.html")
        return FileResponse(index_file)
else:
    @app.get("/")
    async def root():
        return {"message": "Frontend not built. Run 'npm run build' first.", "api_status": "online"}

def main():
    port = int(os.getenv("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
