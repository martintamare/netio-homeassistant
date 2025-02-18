from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN
# Import any additional modules you need

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Netio switches from a config entry."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    client = data["client"]
    outlets = data["outlets"]

    switches = []
    for outlet in outlets:
        # Here we assume each outlet is a dict with at least an "id" and "name" key.
        switches.append(NetioSwitch(client, outlet, config_entry))
    async_add_entities(switches, update_before_add=True)


class NetioSwitch(SwitchEntity):
    """Representation of a Netio outlet as a switch."""

    def __init__(self, client, outlet, config_entry):
        """Initialize a Netio switch."""
        self._client = client
        self._outlet = outlet  # e.g. {'id': 1, 'name': 'Outlet 1'}
        self._config_entry = config_entry
        self._state = None

    @property
    def name(self):
        """Return the name of the switch."""
        return self._outlet.get("name", f"Outlet {self._outlet.get('id')}")

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self._state

    @property
    def unique_id(self):
        """Return a unique ID for this switch."""
        return f"{self._config_entry.entry_id}_{self._outlet.get('id')}"

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
        """Turn the outlet on."""
        def turn_on():
            # Adjust this call based on the PyNetio API
            self._client.set_outlet(self._outlet.get("id"), True)
        await self.hass.async_add_executor_job(turn_on)
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the outlet off."""
        def turn_off():
            # Adjust this call based on the PyNetio API
            self._client.set_outlet(self._outlet.get("id"), False)
        await self.hass.async_add_executor_job(turn_off)
        self._state = False
        self.async_write_ha_state()

    async def async_update(self):
        """Retrieve the latest state from the Netio device."""
        def get_state():
            # Adjust this call if the PyNetio library provides a way to get the current state
            return self._client.get_outlet_state(self._outlet.get("id"))
        self._state = await self.hass.async_add_executor_job(get_state)

