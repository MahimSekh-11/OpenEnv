FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# OpenEnv metadata
LABEL openenv=true
EXPOSE 7860

# Set default port for HF Spaces
ENV PORT=7860

CMD ["python", "server/app.py"]
