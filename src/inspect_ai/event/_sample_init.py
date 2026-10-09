from copy import deepcopy
from typing import Any, Literal

from pydantic import Field, JsonValue, field_validator

from inspect_ai.dataset._dataset import Sample
from inspect_ai.event._base import BaseEvent
from inspect_ai.util._sandbox.environment import SandboxEnvironmentSpec


class SampleInitEvent(BaseEvent):
    """Beginning of processing a Sample."""

    event: Literal["sample_init"] = Field(default="sample_init")
    """Event type."""

    sample: Sample
    """Sample."""

    @field_validator("sample", mode="before")
    @classmethod
    def deserialize_sample_sandbox(cls, value: Any) -> Any:
        """Restore sandbox specs in persisted events before Sample validates inputs."""
        if isinstance(value, dict) and isinstance(value.get("sandbox"), dict):
            return {
                **value,
                "sandbox": SandboxEnvironmentSpec.model_validate(
                    deepcopy(value["sandbox"])
                ),
            }
        return value

    state: JsonValue = None
    """Initial state.

    Defaults to None so events round-trip through log serialization,
    which writes with exclude_none=True (a None state is omitted from
    the written JSON and must not fail validation on read).
    """
