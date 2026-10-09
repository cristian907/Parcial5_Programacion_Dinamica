"""Domain models, value objects, and result structures."""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from .entities import Item


@dataclass
class StageTableRow:
    """A row in a classical Operations Research DP stage decision table."""
    state: int
    candidate_decisions: List[int]
    evaluations: Dict[int, float]  # decision -> evaluated cost
    optimal_cost: float
    optimal_decision: Optional[int]


@dataclass
class StageTable:
    """Represents a full stage table in Dynamic Programming."""
    stage_number: int
    stage_name: str
    description: str
    rows: List[StageTableRow] = field(default_factory=list)


@dataclass
class ShortestPathResult:
    """Full outcome of solving a shortest path problem."""
    algorithm_name: str
    source: int
    destination: int
    total_cost: float
    optimal_path: List[int]
    stages: List[StageTable] = field(default_factory=list)
    intermediate_data: Dict[str, Any] = field(default_factory=dict)
    explanation: str = ""


@dataclass
class KnapsackResult:
    """Full outcome of solving the Cargo Volume (Knapsack) problem."""
    algorithm_name: str
    capacity: float
    selected_items: List[Item]
    item_counts: Dict[int, int]  # item_id -> quantity selected
    total_weight: float
    total_value: float
    slack_capacity: float  # Capacity left unused
    dp_table: List[List[float]] = field(default_factory=list)  # 2D table [stage][weight]
    weights_header: List[float] = field(default_factory=list)
    items_header: List[str] = field(default_factory=list)
    stage_explanations: List[str] = field(default_factory=list)
    conclusion: str = ""


@dataclass
class AlgorithmComparison:
    """Comparative analysis among shortest path algorithms."""
    summary: str
    algorithms_evaluated: List[str]
    costs: Dict[str, float]
    paths: Dict[str, List[int]]
    complexities: Dict[str, str]
    theoretical_notes: str
