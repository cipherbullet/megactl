from typing import Optional, Dict, Any
from pydantic import BaseModel


class Resource(BaseModel):
    kind: str
    name: Optional[str]
    namespace: str = "default"


class Intent(BaseModel):
    kubectl: str
    action: str
    resource: Resource
    dry_run: bool = False
    parameters: Dict[str, Any] = {}
    options: Dict[str, Any] = {}
    extras: Dict[str, Any] = {}
