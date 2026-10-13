"""MVP: Prompt Refiner Service.

A simple service that refines user prompts
and executes them in a sandboxed manner.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="Prompt Refiner MVP")


class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="The user's prompt.")
    history: Optional[List[str]] = Field(default_factory=list)


class RefinedPrompt(BaseModel):
    prompt: str
    confidence: float
    suggestions: List[str]


class ExecutionResult(BaseModel):
    status: str
    output: str
    suggestions: List[str]


def refine_prompt_text(prompt: str, history: List[str]) -> RefinedPrompt:
    """Refine a prompt based on history."""
    suggestions = []
    confidence = 0.5
    
    if not history:
        suggestions.append("Add previous context for better results")
        confidence += 0.1
    
    if len(prompt) < 10:
        suggestions.append("Expand prompt for clarity")
        confidence += 0.1
    
    refined = f"[Context: {' '.join(history) if history else 'No prior context.'}] [Goal: {prompt}]"
    return RefinedPrompt(
        prompt=refined,
        confidence=min(confidence, 1.0),
        suggestions=suggestions
    )


def execute_prompt(prompt: str) -> ExecutionResult:
    """Execute a prompt safely."""
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    
    # Simulate execution
    output = f"Executed: {prompt}"
    return ExecutionResult(
        status="success",
        output=output,
        suggestions=["Save this result"]
    )


@app.post("/refine", response_model=RefinedPrompt)
def refine(request: PromptRequest):
    """Refine a prompt."""
    return refine_prompt_text(request.prompt, request.history)


@app.post("/execute", response_model=ExecutionResult)
def execute(request: PromptRequest):
    """Execute a refined prompt."""
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    return execute_prompt(request.prompt)


def demo():
    """Run a demo of the service."""
    from fastapi.testclient import TestClient
    client = TestClient(app)
    
    # Test refine
    res = client.post("/refine", json={"prompt": "Hello", "history": []})
    print(f"Refine Status: {res.status_code}")
    print(f"Refine Body: {res.json()}")
    
    # Test execute
    res = client.post("/execute", json={"prompt": "Test Task"})
    print(f"Execute Status: {res.status_code}")
    print(f"Execute Body: {res.json()}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
