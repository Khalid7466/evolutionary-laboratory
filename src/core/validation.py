from __future__ import annotations

from typing import Any, Iterable, Mapping


class SpecError(ValueError):
	pass


def require(condition: bool, message: str) -> None:
	if not condition:
		raise SpecError(message)


def require_keys(mapping: Mapping[str, Any], keys: Iterable[str], context: str) -> None:
	for key in keys:
		if key not in mapping:
			raise SpecError(f"Missing '{key}' in {context}.")


def normalize_choice(value: Any, mapping: Mapping[str, str], field_name: str) -> str:
	if not isinstance(value, str):
		raise SpecError(f"{field_name} must be a string.")
	normalized = value.strip().lower()
	if normalized not in mapping:
		choices = ", ".join(sorted(mapping.keys()))
		raise SpecError(f"Unsupported {field_name}: {value}. Choices: {choices}.")
	return mapping[normalized]
