import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from env import SupportEnv
from tasks import TASKS
from models import Action

app = FastAPI(title="SupportAgent OpenEnv API")

# Initialize environment with all tasks
env_instance = SupportEnv(TASKS)

class StepRequest(BaseModel):
    action: Action

@app.get("/")
async def root():
    return {
        "status": "online",
        "env": "SupportAgentEnv",
        "version": "1.0.0",
        "message": "Welcome to the SupportAgent OpenEnv API. Use /reset to start."
    }

@app.post("/reset")
async def reset():
    try:
        result = await env_instance.reset()
        # Ensure we return a serializable dict
        obs = result["observation"]
        return {
            "observation": obs.model_dump() if hasattr(obs, 'model_dump') else obs.dict(),
            "reward": float(result["reward"]),
            "done": bool(result["done"]),
            "info": result["info"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

@app.get("/state")
async def state():
    try:
        s = await env_instance.state()
        return s.model_dump() if hasattr(s, 'model_dump') else s.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # HF Spaces use port 7860
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
