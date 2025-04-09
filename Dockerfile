# Use a lightweight Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /rda

# Copy requirements first to optimize caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code
COPY src/apps apps
COPY src/utils utils
COPY src/shared shared

# Copy the .config file
COPY .config .

# Set the PYTHONPATH to the working directory
ENV PYTHONPATH=./

# Copy streamlit config file
RUN mkdir -p ./.streamlit
COPY configs/streamlit.config.toml ./.streamlit/config.toml

# Default command (can be overridden at runtime)
CMD ["python", "apps/default.py"]
