import voluptuous as vol
import aiohttp
from .inverter import InverterPost
from .utils import (
    div10,
    div100,
    twoway_div10,
    to_signed,
    pv_energy,
    twoway_div100,
    total_energy,
    discharge_energy,
    charge_energy,
    feedin_energy,
    consumption,
    eps_total_energy,
)


class X3HybridG4(InverterPost):
    """X3 hybrid G4 v3.003.02"""

    # pylint: disable=duplicate-code
    _schema = vol.Schema(
        {
            vol.Required("type"): vol.All(int, 14),
            vol.Required("sn"): str,
            vol.Required("ver"): str,
            vol.Required("Data"): vol.Schema(
                vol.All(
                    [vol.Coerce(float)],
                    vol.Length(min=200, max=200),
                )
            ),
            vol.Required("Information"): vol.Schema(
                vol.All(vol.Length(min=10, max=10))
            ),
        },
        extra=vol.REMOVE_EXTRA,
    )

    _sensor_map = {
        "Network Voltage Phase 1": (0, "V", div10),
        "Network Voltage Phase 2": (1, "V", div10),
        "Network Voltage Phase 3": (2, "V", div10),
        "Output Current Phase 1": (3, "A", twoway_div10),
        "Output Current Phase 2": (4, "A", twoway_div10),
        "Output Current Phase 3": (5, "A", twoway_div10),
        "Power Now Phase 1": (6, "W", to_signed),
        "Power Now Phase 2": (7, "W", to_signed),
        "Power Now Phase 3": (8, "W", to_signed),
        "AC Power": (9, "W", to_signed),
        "PV1 Voltage": (10, "V", div10),
        "PV2 Voltage": (11, "V", div10),
        "PV1 Current": (12, "A", div10),
        "PV2 Current": (13, "A", div10),
        "PV1 Power": (14, "W"),
        "PV2 Power": (15, "W"),
        "Grid Frequency Phase 1": (16, "Hz", div100),
        "Grid Frequency Phase 2": (17, "Hz", div100),
        "Grid Frequency Phase 3": (18, "Hz", div100),
        # "Total Energy": (19, "kWh", total_energy),
        # "Total Energy Resets": (20, ""),
        # "Today's Energy": (21, "kWh", div10),
        "Battery Voltage": (24, "V", div100),
        "Battery Current": (25, "A", twoway_div100),
        "Battery Power": (26, "W", to_signed),
        "Battery Temperature": (27, "C"),
        "Battery Remaining Capacity": (28, "%"),
        "Total Battery Discharge Energy": (30, "kWh", discharge_energy),
        "Total Battery Discharge Energy Resets": (31, ""),
        "Battery Remaining Energy": (32, "kWh", div10),
        "EPS Frequency": (63, "Hz", div100),
        "Exported Power": (65, "W", to_signed),
        "Total PV Energy": (68, "kWh", div10),
        # "Total Feed-in Energy Resets": (68, ""),
        # "Total Consumption Resets": (70, ""),
        "Today's PV Energy": (70, "kWh", div10),
        "Total Battery Charge Energy": (87, "kWh", div10),
        "Total Feed-in Energy": (86, "kWh", div100),
        "Total Consumption": (88, "kWh", div10),
        "Total PV Energy Resets": (90, ""),
        "EPS Total Energy": (110, "kWh", eps_total_energy),
        "EPS Total Energy Resets": (111, "Hz"),
        "Today's Battery Discharge Energy": (113, "kWh", div10),
        "Today's Battery Charge Energy": (114, "kWh", div10),
    }
    # pylint: enable=duplicate-code
    @classmethod
    async def make_request(cls, host, port=80, pwd="", headers=None):
        data = "optType=ReadRealTimeData, pwd={}".format(pwd)  # x-www-form-urlencoded
        base = "http://{}:{}/"
        url = base.format(host, port)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as req:
                resp = await req.read()

        return cls.handle_response(resp)
