import requests
import logging
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity

_LOGGER = logging.getLogger(__name__)
# Aktualizace každé 3 hodiny
SCAN_INTERVAL = timedelta(hours=3)

async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities([CeskeSvatkySensor()], True)

class CeskeSvatkySensor(SensorEntity):
    def __init__(self):
        self._attr_name = "Český kalendář"
        self._attr_unique_id = "cesky_kalendar_v1"
        self._state = None
        self._attributes = {}

    @property
    def native_value(self):
        """Tohle zobrazí jméno jako hlavní stav entity."""
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self):
        try:
            # Volání API pro dnešní den
            r = requests.get("https://svatky.vsevjednom.cz/api/v1/holidays/today", timeout=10)
            data = r.json()
            
            # Lidské jméno (např. "Daniel")
            self._state = data.get("name")
            
            # Ostatní informace do atributů
            self._attributes = {
                "je_statni_svatek": data.get("is_holiday"),
                "datum": data.get("date"),
                "svatek_popis": data.get("holiday_name") if data.get("is_holiday") else "Běžný pracovní den"
            }
            _LOGGER.info("Data z API úspěšně načtena: %s", self._state)
        except Exception as e:
            _LOGGER.error("Chyba při aktualizaci svátků: %s", e)
            self._state = "Chyba API"