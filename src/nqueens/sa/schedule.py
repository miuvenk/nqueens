# src/nqueens/sa/schedule.py
from __future__ import annotations
from dataclasses import dataclass, field

__all__ = [
    "GeometricSchedule",
    "LinearSchedule",
    "LogarithmicSchedule",
    "make_schedule",
]


@dataclass
class GeometricSchedule:
    """
    Classic geometric cooling: T_k = T0 * alpha^k
    - T0    : initial temperature (> 0)
    - alpha : decay factor in (0, 1)  (e.g., 0.98)
    - Tmin  : stopping threshold for temperature
    """
    T0: float = 1.5
    alpha: float = 0.98
    Tmin: float = 1e-3

    T: float = field(init=False)

    def __post_init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        """Reset temperature to T0."""
        self.T = float(self.T0)

    def current(self) -> float:
        """Return current temperature."""
        return self.T

    def step(self) -> float:
        """Advance one step in the schedule and return the new temperature."""
        self.T *= self.alpha
        return self.T

    def done(self) -> bool:
        """Return True if the schedule is finished (temperature too low)."""
        return self.T <= self.Tmin


@dataclass
class LinearSchedule:
    """
    Linear cooling: T_k = max(Tmin, T0 - k * delta)
    - T0    : initial temperature (> 0)
    - delta : linear decrement per step (> 0)
    - Tmin  : stopping threshold for temperature
    """
    T0: float = 2.0
    delta: float = 1e-3
    Tmin: float = 1e-3

    T: float = field(init=False)

    def __post_init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.T = float(self.T0)

    def current(self) -> float:
        return self.T

    def step(self) -> float:
        self.T = max(self.Tmin, self.T - self.delta)
        return self.T

    def done(self) -> bool:
        return self.T <= self.Tmin


@dataclass
class LogarithmicSchedule:
    """
    Logarithmic (harmonic) cooling: T_k = T0 / (1 + beta * k)
    - T0   : initial temperature (> 0)
    - beta : decay rate (> 0)
    - Tmin : stopping threshold
    """
    T0: float = 2.0
    beta: float = 1e-2
    Tmin: float = 1e-3

    k: int = field(default=0, init=False)
    T: float = field(init=False)

    def __post_init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.k = 0
        self.T = float(self.T0)

    def current(self) -> float:
        return self.T

    def step(self) -> float:
        self.k += 1
        self.T = self.T0 / (1.0 + self.beta * self.k)
        return self.T

    def done(self) -> bool:
        return self.T <= self.Tmin


def make_schedule(kind: str = "geometric", **kwargs):
    """
    Convenience factory to create a schedule by name.
    kind in {"geometric", "linear", "log", "logarithmic"}.
    Example:
        sched = make_schedule("geometric", T0=1.5, alpha=0.98, Tmin=1e-3)
    """
    k = kind.lower()
    if k in ("geom", "geometric"):
        return GeometricSchedule(**kwargs)
    if k in ("lin", "linear"):
        return LinearSchedule(**kwargs)
    if k in ("log", "logarithmic"):
        return LogarithmicSchedule(**kwargs)
    raise ValueError(f"Unknown schedule kind: {kind}")
