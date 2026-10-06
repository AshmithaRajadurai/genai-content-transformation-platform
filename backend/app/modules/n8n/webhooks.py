from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class N8nWebhookPayload(BaseModel):
    """Payload contract sent to n8n webhook for LLM orchestration."""
    workflow_id: Optional[str] = Field(None, description="Optional target n8n workflow identifier")
    channel_id: str = Field(..., description="Target channel format ID")
    system_prompt: str = Field(..., description="System prompt instructions")
    user_prompt: str = Field(..., description="Formatted user prompt")
    context_data: Dict[str, Any] = Field(default_factory=dict, description="Structured NLP and context metadata")
    temperature: float = Field(default=0.7, description="Generation temperature")
    max_tokens: int = Field(default=1500, description="Max token limit")


class N8nWebhookResponse(BaseModel):
    """Contract received from n8n webhook after orchestration workflow completion."""
    status: str = Field("success", description="Workflow execution status")
    channel_id: str = Field(..., description="Target channel ID")
    generated_content: str = Field(..., description="LLM generated content from n8n node")
    provider_used: str = Field("n8n_ollama", description="Provider executed in n8n")
    model_used: str = Field("llama3", description="Model executed in n8n")
    tokens_used: int = Field(default=0, description="Tokens reported by n8n workflow")
    execution_id: Optional[str] = Field(None, description="n8n execution ID")
