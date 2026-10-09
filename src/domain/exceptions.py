"""Domain exceptions."""


class DomainException(Exception):
    """Base domain exception."""
    pass


class GraphError(DomainException):
    """Exception raised when graph validation or traversal fails."""
    pass


class NegativeCycleError(GraphError):
    """Raised when a negative cost cycle is detected."""
    pass


class NodeNotFoundError(GraphError):
    """Raised when a requested node does not exist in the graph."""
    pass


class PathNotFoundError(GraphError):
    """Raised when no valid path exists between source and destination."""
    pass


class KnapsackError(DomainException):
    """Exception raised when Cargo Volume problem parameters are invalid."""
    pass
