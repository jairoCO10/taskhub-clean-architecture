# app/core/entities/user.py
from dataclasses import dataclass
from typing import List, Optional
from . import task

@dataclass
class User:
    id: int
    name: str
    email: str
    tasks: List[task.Task]


@dataclass
class CreateUser:
    id: int
    name: str
    email: str