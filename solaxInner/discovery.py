from .inverter import Inverter, InverterError
from .x3_hybrid_g4 import X3HybridG4

# registry of inverters
REGISTRY = [X3HybridG4]


class DiscoveryError(Exception):
    """Raised when unable to discover inverter"""


async def discover(host, port, pwd="") -> Inverter:
    failures = []
    for inverter in REGISTRY:
        i = inverter(host, port, pwd)
        try:
            await i.get_data()
            return i
        except InverterError as ex:
            failures.append(ex)
    msg = (
        "Unable to connect to the inverter at "
        f"host={host} port={port}, or your inverter is not supported yet.\n"
        "Please see https://github.com/squishykid/solax/wiki/DiscoveryError\n"
        f"Failures={str(failures)}"
    )
    raise DiscoveryError(msg)
