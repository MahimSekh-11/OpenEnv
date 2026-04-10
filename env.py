import asyncio
from typing import List, Dict, Any, Optional
from models import Action, Observation, Reward, State

class SupportEnv:
    def __init__(self, tasks: List[Dict[str, Any]]):
        self.tasks = tasks
        self.current_task_index = 0
        self.history = []
        self.is_done = False
        self.score = 0.0
        self.categories = ["billing", "technical", "account", "shipping", "general"]
        self.reset_state()

    def reset_state(self):
        self.current_task = self.tasks[self.current_task_index]
        self.history = [{"role": "system", "content": f"New ticket received: {self.current_task['content']}"}]
        self.is_done = False
        self.current_status = "open"
        self.assigned_category = None

    async def reset(self) -> Dict[str, Any]:
        self.reset_state()
        return {
            "observation": self._get_obs(),
            "reward": 0.0,
            "done": False,
            "info": {}
        }

    def _get_obs(self) -> Observation:
        return Observation(
            ticket_id=str(self.current_task_index),
            content=self.current_task["content"],
            history=self.history,
            available_categories=self.categories,
            status=self.current_status
        )

    async def step(self, action: Action) -> Dict[str, Any]:
        if self.is_done:
            return {"observation": self._get_obs(), "reward": 0.0, "done": True, "info": {}}

        reward_val = 0.0
        explanation = ""

        if action.action_type == "categorize":
            if action.category in self.categories:
                self.assigned_category = action.category
                self.history.append({"role": "agent", "content": f"Categorized as: {action.category}"})
                # Partial reward for correct categorization (max 0.2)
                if action.category == self.current_task["expected_category"]:
                    reward_val = 0.2
                    explanation = "Correct category assigned."
                else:
                    reward_val = 0.0
                    explanation = f"Incorrect category. Expected {self.current_task['expected_category']}."
            else:
                explanation = "Invalid category."

        elif action.action_type == "respond":
            if not action.message:
                explanation = "Empty message."
            else:
                self.history.append({"role": "agent", "content": f"Response: {action.message}"})
                # Check if response contains keywords (max 0.3)
                keywords = self.current_task.get("required_keywords", [])
                if not keywords:
                    reward_val = 0.3
                    explanation = "Response sent."
                else:
                    matches = [k for k in keywords if k.lower() in action.message.lower()]
                    reward_val = 0.3 * (len(matches) / len(keywords))
                    explanation = f"Response addressed {len(matches)}/{len(keywords)} key points."

        elif action.action_type == "close":
            self.current_status = "closed"
            self.is_done = True
            # Final grading (max 0.5)
            final_bonus = self.current_task["grader"](self) * 0.5
            reward_val = final_bonus
            explanation = "Ticket closed. Final evaluation complete."
            self.score += reward_val

        return {
            "observation": self._get_obs(),
            "reward": float(reward_val),
            "done": bool(self.is_done),
            "info": {"explanation": explanation}
        }

        return {
            "observation": self._get_obs(),
            "reward": reward_val,
            "done": self.is_done,
            "info": {"explanation": explanation}
        }

    async def state(self) -> State:
        return State(
            current_ticket_index=self.current_task_index,
            tickets=self.tasks,
            history=self.history,
            is_done=self.is_done,
            score=self.score
        )

    async def close(self):
        pass
