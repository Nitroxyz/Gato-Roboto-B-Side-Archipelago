import pkgutil
import random

from settings import FilePath

from .world import GatoRobotoWorld as GatoRobotoWorld
from worlds.LauncherComponents import launch, components, Component, Type, icon_paths

# Ahit mirror
def launch_client(*args):
    """
    Launch the Gato Roboto Client
    """
    from .GatoRobotoClient import launch as launch_gato
    launch(launch_gato, name="GatoRobotoClient", args=args)

# Apquest mirror
components.append(Component("Gato Roboto B-Side Client",
                            func=launch_client,
                            component_type=Type.CLIENT,
                            icon="gato",
                            supports_uri=True,
                            game_name="Gato Roboto B-Side"))

# AHIT mirror
if random.random() > 0.01:
    icon_paths['gato'] = f"ap:{__name__}/data/main_gato.webp"
else:
    icon_paths['gato'] = f"ap:{__name__}/data/evil_gato.webp"

# Minit mirror
class DataWinFile(FilePath):
    """Path to Minit Vanilla data file"""
    description = "Gato Roboto data.win"
    md5s = [
        "38970C275305CCD7C9ABE9A10817872E",  # steam
        # "",  # epic
        # "",  # itch.io
    ]
    # the hashes for vanilla to be verified by the /patch command
    required = False