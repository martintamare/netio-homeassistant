import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PORT, CONF_USERNAME, CONF_PASSWORD
from .const import DOMAIN, CONF_IP_ADDRESS

from Netio import Netio

_LOGGER = logging.getLogger(__name__)

# Define the configuration schema for the config flow
DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_IP_ADDRESS): str,
    vol.Required(CONF_PORT, default=80): int,  # Set a default port if needed
    vol.Required(CONF_USERNAME): str,
    vol.Required(CONF_PASSWORD): str,
})

class NetioBinder():
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username,
        self.password = password

    @property
    def client(self):
        url = f"http://{self.ip}:{self.port}/netio.json"
        return Netio(url, auth_rw=(self.username, self.password))

    def get_outputs(self):
        return self.client.get_outputs()


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
                # Create the Netio client (assumed to be a blocking call)
                client = NetioBinder(ip, port, username, password)
                # Try to fetch output info in a thread so as not to block the event loop.
                outputs = await self.hass.async_add_executor_job(client.get_outputs)
                if not outputs:
                    errors["base"] = "no_outputs_found"
                else:
                    # If connection and discovery succeed, create the config entry.
                    return self.async_create_entry(title=ip, data=user_input)
            except Exception as e:
                _LOGGER.exception("Error connecting to Netio: %s", e)
                errors["base"] = "cannot_connect"

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)

