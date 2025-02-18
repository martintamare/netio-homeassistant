import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, CONF_IP_ADDRESS, CONF_PORT, CONF_USERNAME, CONF_PASSWORD

from Netio import Netio

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Netio integration from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    ip = entry.data.get(CONF_IP_ADDRESS)
    port = entry.data.get(CONF_PORT)
    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)

    def create_client():
        url = f"http://{ip}:{port}/netio.json"
        client = Netio(url, auth_rw=(username, password))
        # Fetch the list of outputs (this should be a blocking call)
        outputs = client.get_outputs()
        return client, outputs

    try:
        client, outputs = await hass.async_add_executor_job(create_client)
    except Exception as e:
        _LOGGER.error("Failed to connect to Netio at %s:%s: %s", ip, port, e)
        return False

    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "outputs": outputs,
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

