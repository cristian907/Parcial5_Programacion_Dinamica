"""Application layer DTOs (Data Transfer Objects)."""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ShortestPathRequestDTO:
    """Input parameters for shortest path solvers."""
    source: int
    destination: int


@dataclass
class KnapsackRequestDTO:
    """Input parameters for cargo volume solver."""
    capacity: float
    allow_repetition: bool = False


@dataclass
class EdgeDTO:
    source: int
    target: int
    weight: float


@dataclass
class ItemDTO:
    id: int
    name: str
    weight: float
    price: float
