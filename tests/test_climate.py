"""Unit tests for Radialight climate preset_mode mapping."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

from custom_components.radialight_cloud.climate import (
    RadialightClimate,
    _PRESET_TO_MODE,
)
from custom_components.radialight_cloud.const import PRESET_COMFORT


class _FakeCoordinator:
    def __init__(self, zone: dict) -> None:
        self._zone = zone
        self.last_update_success = True
        self.async_request_refresh = AsyncMock()

    def get_zone(self, zone_id: str) -> dict:
        return self._zone


def _zone(**overrides: object) -> dict:
    zone = {
        "name": "Drawing",
        "mode": 5,
        "tComfort": 200,
        "tECO": 100,
        "window": 0,
        "pir": 0,
        "lock": 0,
        "program": {"id": "prog-1"},
    }
    zone.update(overrides)
    return zone


def _climate_for_zone(zone: dict, api: MagicMock | None = None) -> RadialightClimate:
    return RadialightClimate(
        _FakeCoordinator(zone),
        api or MagicMock(),
        "zone-1",
        zone,
    )


def test_preset_mode_maps_api_mode_comfort() -> None:
    """API zone mode 2 surfaces as HA preset comfort."""
    assert _climate_for_zone(_zone(mode=2)).preset_mode == "comfort"


def test_preset_mode_maps_api_mode_eco() -> None:
    """API zone mode 3 surfaces as HA preset eco."""
    assert _climate_for_zone(_zone(mode=3)).preset_mode == "eco"


def test_preset_mode_maps_api_mode_antifreeze() -> None:
    """API zone mode 4 surfaces as HA preset antifreeze."""
    assert _climate_for_zone(_zone(mode=4)).preset_mode == "antifreeze"


def test_preset_mode_maps_api_mode_program() -> None:
    """API zone mode 5 (Timer) surfaces as HA preset program."""
    assert _climate_for_zone(_zone(mode=5)).preset_mode == "program"


def test_preset_mode_maps_api_mode_auto() -> None:
    """API zone mode 9 surfaces as HA preset auto."""
    assert _climate_for_zone(_zone(mode=9)).preset_mode == "auto"


async def test_set_preset_mode_comfort_writes_api_mode() -> None:
    """Selecting comfort writes the mapped zone mode via set_zone_setpoint."""
    api = MagicMock()
    api.set_zone_setpoint = AsyncMock()
    zone = _zone(mode=5)
    entity = _climate_for_zone(zone, api=api)

    await entity.async_set_preset_mode(PRESET_COMFORT)

    api.set_zone_setpoint.assert_awaited_once_with(
        "zone-1",
        zone["program"]["id"],
        zone["tComfort"],
        zone["tECO"],
        zone["window"],
        _PRESET_TO_MODE[PRESET_COMFORT],
        zone["pir"],
        zone["lock"],
    )
    api.clear_override.assert_not_called()
