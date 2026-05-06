# Use a small Python image (slim to save space)
FROM python:3.11-slim

# Create a directory and set it as the home directory
WORKDIR /app

# Copy the requirements file before copying everything else
# This means if we change code but not req, then only code is updated
COPY requirements.txt .

# Install dependencies (no cache to reduce image size)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . . 

# Run this command when the container starts each time
# app.main:app means look in app folder for main.py file, and look in main for variable app (app = FastAPI())
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]