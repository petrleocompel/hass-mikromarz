
from .const import DOMAIN
from .mikromarz_api import MikromarzApi
from homeassistant.const import CONF_HOST
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv

from typing import Any, Optional

import voluptuous as vol


CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): cv.string,
    }
)


class MikromarzCustomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Mikromarz Custom config flow."""

    data: Optional[dict[str, Any]]

    async def async_step_user(self, user_input: Optional[dict[str, Any]] = None):
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                MikromarzApi(user_input[CONF_HOST])
            except ValueError:
                errors["base"] = "auth"
            if not errors:
                self.data = user_input
                return self.async_create_entry(title="Mikromarz", data=self.data, description=self.data[CONF_HOST])

        return self.async_show_form(
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
        )
