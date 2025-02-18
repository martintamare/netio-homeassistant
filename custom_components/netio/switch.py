import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity_platform import async_get_current_platform
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Netio switches from a config entry."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    client = data["client"]
    outputs = data["outputs"]

    switches = []
    for output in outputs:
        # Here we assume each output is a dict with at least an "id" and "name" key.
        switches.append(NetioSwitch(client, output, config_entry))
    async_add_entities(switches, update_before_add=True)


class NetioSwitch(SwitchEntity):
    """Representation of a Netio output as a switch."""

    _services_registered = False  # Class attribute to ensure one-time registration


    def __init__(self, client, output, config_entry):
        """Initialize a Netio switch."""
        self._client = client
        self._output = output  # e.g. {'id': 1, 'name': 'Outlet 1'}
        self._config_entry = config_entry
        self._state = None

    async def async_added_to_hass(self):
        """Register entity services when the entity is added to hass."""
        # Only register the custom services once per platform
        if not NetioSwitch._services_registered:
            platform = async_get_current_platform()
            if platform is not None:
                platform.async_register_entity_service(
                    "reset",
                    {},  # No additional parameters
                    "async_reset",
                )
                NetioSwitch._services_registered = True
            else:
                _LOGGER.error("Failed to get current platform for service registration.")


    @property
    def name(self):
        """Return the name of the switch."""
        return self._output.Name

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self._state

    @property
    def unique_id(self):
        """Return a unique ID for this switch."""
        return f"{self._config_entry.entry_id}_{self._output.ID}"

    @property
    def device_info(self):
        """Return device information about the Netio device."""
        return {
            "identifiers": {(DOMAIN, self._config_entry.entry_id)},
            "name": "Netio Device",
            "manufacturer": "Netio Products",
            "model": "Netio",  # Optionally use a model string if available
        }

    async def async_turn_on(self, **kwargs):
        """Turn the output on."""
        def turn_on():
            self._client.set_output(self._output.ID, 1)
        await self.hass.async_add_executor_job(turn_on)
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the output off."""
        def turn_off():
            self._client.set_output(self._output.ID, 0)
        await self.hass.async_add_executor_job(turn_off)
        self._state = False
        self.async_write_ha_state()

    async def async_reset(self, **kwargs):
        """Reset the output by setting its output to 2."""
        def reset():
            # Set the output state to 2 to trigger a reset.
            self._client.set_output(self._output.ID, 2)
        await self.hass.async_add_executor_job(reset)
        self._state = True
        self.async_write_ha_state()

    async def async_update(self):
        """Retrieve the latest state from the Netio device."""
        def get_state():
            output = self._client.get_output(self._output.ID)
            return output.State
        self._state = await self.hass.async_add_executor_job(get_state)
