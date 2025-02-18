import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, CONF_IP_ADDRESS, CONF_PORT, CONF_USERNAME, CONF_PASSWORD

from PyNetio import PyNetio

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Netio integration from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    ip = entry.data.get(CONF_IP_ADDRESS)
    port = entry.data.get(CONF_PORT)
    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)

    def create_client():
        client = PyNetio(ip, port, username, password)
        # Fetch the list of outlets (this should be a blocking call)
        outlets = client.get_outlets()
        return client, outlets

    try:
        client, outlets = await hass.async_add_executor_job(create_client)
    except Exception as e:
        _LOGGER.error("Failed to connect to Netio at %s:%s: %s", ip, port, e)
        return False

    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "outlets": outlets,
    }

    # Forward the setup to the switch platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "switch")
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Netio config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "switch")
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

