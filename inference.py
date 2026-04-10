import asyncio
import os
import json
import textwrap
from typing import List, Optional
from openai import OpenAI

# Import our environment
from env import SupportEnv
from tasks import TASKS
from models import Action

# Configuration from environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY")

MAX_STEPS = 5
TEMPERATURE = 0.0

SYSTEM_PROMPT = textwrap.dedent(
    """
    You are a customer support AI agent. Your goal is to triage and resolve tickets.
    Available actions:
    1. Categorize the ticket: {"action_type": "categorize", "category": "..."}
    2. Respond to the customer: {"action_type": "respond", "message": "..."}
    3. Close the ticket: {"action_type": "close"}
    
    Categories: billing, technical, account, shipping, general.
    
    Always output valid JSON representing the action.
    """
).strip()

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )

def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

async def run_task(client: OpenAI, task_index: int):
    # Initialize environment with the specific task
    env = SupportEnv([TASKS[task_index]])
    task = TASKS[task_index]
    
    log_start(task=task["name"], env="SupportAgentEnv", model=MODEL_NAME)
    
    rewards = []
    steps_taken = 0
    
    try:
        reset_result = await env.reset()
        obs = reset_result["observation"]
        
        for step in range(1, MAX_STEPS + 1):
            # Build prompt
            history_str = json.dumps(obs.history, indent=2)
            user_prompt = f"Current Ticket Content: {obs.content}\nHistory: {history_str}\nStatus: {obs.status}\nWhat is your next action?"
            
            try:
                completion = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=TEMPERATURE,
                    response_format={"type": "json_object"}
                )
                action_data = json.loads(completion.choices[0].message.content)
                action = Action(**action_data)
            except Exception as e:
                log_step(step=step, action="error", reward=0.0, done=True, error=str(e))
                break

            step_result = await env.step(action)
            obs = step_result["observation"]
            reward = step_result["reward"]
            done = step_result["done"]
            
            rewards.append(reward)
            steps_taken = step
            
            log_step(step=step, action=json.dumps(action_data), reward=reward, done=done, error=None)
            
            if done:
                break
        
        final_score = sum(rewards)
        # Normalize score to [0, 1] - for this env, max reward is roughly 1.0 per task
        final_score = min(max(final_score, 0.0), 1.0)
        log_end(success=(final_score > 0.7), steps=steps_taken, score=final_score, rewards=rewards)
        
    except Exception as e:
        log_end(success=False, steps=steps_taken, score=0.0, rewards=rewards)
        print(f"Error: {e}")

async def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    for i in range(len(TASKS)):
        await run_task(client, i)

if __name__ == "__main__":
    asyncio.run(main())
