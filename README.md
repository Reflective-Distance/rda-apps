# RDA Mono Repo

Monorepo for all rapid development apps and services. This repository contains multiple applications packaged in a single Docker image.

## Available Applications

- **LLM**: Language Model Playground
- **Notes**: Noteworthy application
- **Sandbox**: Development sandbox environment

## Building the Docker Image

```bash
docker build -t rda-mono .
```

## Running Applications

You can run different applications by overriding the default command when running the Docker container:

```bash
# Run the default app (LLM)
docker run -p 8501:8501 rda-mono

# Run the Notes app
docker run -p 8501:8501 rda-mono /entrypoints/notes.sh

# Run the Sandbox app
docker run -p 8501:8501 rda-mono /entrypoints/sandbox.sh
```

## Development

When developing locally outside of Docker, make sure to set your PYTHONPATH to include both the root directory and the src directory:

```bash
# On Linux/Mac
export PYTHONPATH=/path/to/rda-mono:/path/to/rda-mono/src

# On Windows (PowerShell)
$env:PYTHONPATH = "C:\path\to\rda-mono;C:\path\to\rda-mono\src"
```

## Project Structure

```
rda-mono/
├── entrypoints/       # Entry point scripts for each app
├── src/
│   ├── apps/          # Application-specific code
│   │   ├── llm/       # Language Model Playground
│   │   ├── notes/     # Noteworthy application
│   │   └── sandbox/   # Development sandbox
│   └── utils/         # Shared utilities
└── tests/             # Test suite
```
