import requests
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import EntityCategory

SCAN_INTERVAL = timedelta(hours=3)

async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities([CeskeSvatkyVseVJedom()], True)

class CeskeSvatkyVseVJedom(SensorEntity):
    def __init__(self):
        self._attr_name = "Český kalendář"
        self._attr_unique_id = "cesky_kalendar_unique_v1"
        self._state = None
        self._attrs = {}

    @property
    def state(self): return self._state

    @property
    def extra_state_attributes(self): return self._attrs

    def update(self):
        try:
            r = requests.get("https://svatky.vsevjednom.cz/api/v1/holidays/today", timeout=10)
            data = r.json()
            self._state = data.get("name")
            self._attrs = {
                "je_statni_svatek": data.get("is_holiday"),
                "datum": data.get("date"),
                "nazev_svatku": data.get("holiday_name") if data.get("is_holiday") else "Pracovní den"
            }
        except Exception:
            self._state = "Chyba API"
