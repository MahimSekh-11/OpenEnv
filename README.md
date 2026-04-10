---
title: SupportAgent OpenEnv
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
app_port: 7860
tags:
  - openenv
---

# SupportAgentEnv: Customer Support Triage & Response

A real-world OpenEnv environment for evaluating AI agents on customer support tasks.

## Environment Description
This environment simulates a customer support dashboard where an agent must:
1. **Categorize** incoming tickets.
2. **Respond** to customers with helpful information.
3. **Close** tickets once resolved.

## Action Space
The agent can perform three types of actions:
- `categorize`: Assigns a category (billing, technical, account, shipping, general).
- `respond`: Sends a text message to the customer.
- `close`: Finalizes the ticket and triggers evaluation.

## Observation Space
- `ticket_id`: Unique identifier.
- `content`: The raw text of the customer's request.
- `history`: A log of all interactions (system messages and agent actions).
- `available_categories`: List of valid categories.
- `status`: Current status of the ticket (open/closed).

## Tasks
1. **password_reset** (Easy): A simple request to reset a password.
2. **billing_update** (Medium): Guiding a user to the billing portal.
3. **complex_shipping_issue** (Hard): A multi-part request involving order delays, refunds, and address updates.

## Setup & Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables:
   - `OPENAI_API_KEY`: Your API key.
   - `MODEL_NAME`: The model to test (e.g., `gpt-4o`).
3. Run inference: `python inference.py`

## Baseline Scores
- Easy: 1.0
- Medium: 0.8
- Hard: 0.5 (Estimated for current frontier models)

## OpenEnv Compliance
This environment follows the OpenEnv specification with typed models and standard API endpoints.
