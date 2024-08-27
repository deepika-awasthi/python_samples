# models.py
from pydantic import BaseModel
from enum import Enum
from typing import Dict

# Define Enum for LlmProviders
class LlmProviders(str, Enum):
    AZURE = "azure"
    OPENAI = "openai"

# Define SkillRun class as a BaseModel
class SkillRun(BaseModel):
    flavoredSkillId: str
    organization_slug: str
    secrets: Dict[str, str]
    llm_provider: LlmProviders

# Define Params and Args classes
class TransferToHumanCSSkillParams(BaseModel):
    pass

class TransferToHumanCSSkillArgs(BaseModel):
    account_id: str
    conversation_id: str
    chat_history: str
    time_para_receber: str
    locale: str

# Combine Params and Args into a single class inheriting from SkillRun
class TransferToHumanCSSkillParamsAndArgs(SkillRun):
    args: TransferToHumanCSSkillArgs
    params: TransferToHumanCSSkillParams

    class Config:
        arbitrary_types_allowed = True
