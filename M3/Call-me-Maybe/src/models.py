from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Any


class VocabMap():
    pass


class ParamType(str, Enum):
    NUMBER = "number"
    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"


class ParamSchema(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: ParamType
    pass


class ReturnSchema(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: ParamType


class FunctionDefinition(BaseModel):
    name: str
    description: str = ""
    parameters: dict[str, ParamSchema] = {}
    returns: ReturnSchema | None = None


class FunctionCall(BaseModel):
    name: str
    prompt: str
    parameters: dict[str, Any]


class StepType(str, Enum):
    PROMPT = "prompt"

    LITERAL = "literal"
    FUNCTION_NAME_CHOICE = "function_name_choice"
    PARAM_VALUE = "param_value"


class GrammarStep(BaseModel):
    type: StepType
    literal_text: str = ""
    param_name: str | None = None
    param_type: str | None = None
