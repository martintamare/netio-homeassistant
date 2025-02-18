import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PORT, CONF_USERNAME, CONF_PASSWORD
from .const import DOMAIN, CONF_IP_ADDRESS

# Import the PyNetio library (adjust the import as needed based on the library’s API)
from PyNetio import PyNetio

_LOGGER = logging.getLogger(__name__)

# Define the configuration schema for the config flow
DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_IP_ADDRESS): str,
    vol.Required(CONF_PORT, default=80): int,  # Set a default port if needed
    vol.Required(CONF_USERNAME): str,
    vol.Required(CONF_PASSWORD): str,
})


class NetioConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Netio."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            ip = user_input[CONF_IP_ADDRESS]
            port = user_input[CONF_PORT]
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]
            try:
                # Create the PyNetio client (assumed to be a blocking call)
                client = PyNetio(ip, port, username, password)
                # Try to fetch outlet info in a thread so as not to block the event loop.
                outlets = await self.hass.async_add_executor_job(client.get_outlets)
                if not outlets:
                    errors["base"] = "no_outlets_found"
                else:
                    # If connection and discovery succeed, create the config entry.
                    return self.async_create_entry(title=ip, data=user_input)
            except Exception as e:
                _LOGGER.exception("Error connecting to Netio: %s", e)
                errors["base"] = "cannot_connect"

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)

