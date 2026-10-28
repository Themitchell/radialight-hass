"""Unit tests for Radialight climate preset_mode mapping."""

from __future__ import annotations

from unittest.mock import MagicMock

from custom_components.radialight_cloud.climate import RadialightClimate


class _FakeCoordinator:
    def __init__(self, zone: dict) -> None:
        self._zone = zone
        self.last_update_success = True

    def get_zone(self, zone_id: str) -> dict:
        return self._zone


def _climate_for_zone(zone: dict) -> RadialightClimate:
    return RadialightClimate(
        _FakeCoordinator(zone),
        MagicMock(),
        "zone-1",
        zone,
    )


def test_preset_mode_maps_api_mode_comfort() -> None:
    """API zone mode 2 surfaces as HA preset comfort."""
    assert _climate_for_zone({"name": "Drawing", "mode": 2}).preset_mode == "comfort"


def test_preset_mode_maps_api_mode_eco() -> None:
    """API zone mode 3 surfaces as HA preset eco."""
    assert _climate_for_zone({"name": "Drawing", "mode": 3}).preset_mode == "eco"


def test_preset_mode_maps_api_mode_antifreeze() -> None:
    """API zone mode 4 surfaces as HA preset antifreeze."""
    assert _climate_for_zone({"name": "Drawing", "mode": 4}).preset_mode == "antifreeze"


def test_preset_mode_maps_api_mode_program() -> None:
    """API zone mode 5 (Timer) surfaces as HA preset program."""
    assert _climate_for_zone({"name": "Drawing", "mode": 5}).preset_mode == "program"


def test_preset_mode_maps_api_mode_auto() -> None:
    """API zone mode 9 surfaces as HA preset auto."""
    assert _climate_for_zone({"name": "Drawing", "mode": 9}).preset_mode == "auto"
