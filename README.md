# ContextWeave

Transform unstructured user intent into structured, high-quality AI outputs through iterative refinement

# Prompt Refiner MVP

A simple FastAPI service to refine and execute prompts.

## Usage

Run the server:
```bash
uvicorn main:app --reload
```

Run tests:
```bash
pytest -q
```

Demo:
```bash
python -c "from main import demo; demo()"
```

## Architecture

![Architecture](docs/architecture.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    A[User Input] --> B[FastAPI Service]
    B --> C[Refine Prompt]
    C --> D{Check History & Length}
    D -->|Adjust Confidence| E[Generate Suggestions]
    E --> F[Return Structured Output]
    F --> G[Execution Result]
```

</details>
