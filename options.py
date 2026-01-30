from dataclasses import dataclass

from Options import OptionGroup, PerGameCommonOptions, Toggle, DefaultOnToggle

# Flymech (off)
# Randomize Aqueduct Quest (on)
# Randomize Heater Core Quest (off)
# Randomize Ventilation Quest (on) (Reminder that it can only be ventilation quest off with progressive)
# Ultrahard (off)
# Upwarp (on)

class GlitchSmallmech(DefaultOnToggle):
    """
    Includes logic for the Smallmech glitch.
    Disabling it requires the heater core quest to be vanilla.
    """
    display_name = "Use Smallmech"

class GlitchWatermech(Toggle):
    """
    Includes logic for the Watermech glitch.
    Better with "Randomized Aqueduct Quest" off.
    """
    display_name = "Use Watermech"

class GlitchCatTech(DefaultOnToggle):
    """
    Includes logic for some difficult cat mechanics.
    Requires intense mashing.
    Note that this will soon represent all tech difficulties.
    """
    display_name = "Use CatTech"

class NexusStart(DefaultOnToggle):
    """
    Start in the Nexus instead of the Landing Site.
    Allows for some logic checks without rocket. It's recommended to turn CatTech on with this.
    """
    display_name = "Nexus Start"

class UnlockAllWarps(Toggle):
    """
    Allows you to warp to every main area (Landing Site, Aqueducts, Heater Core and Ventilation).
    """
    display_name = "Unlock all warps"

class ForceLocalStart(DefaultOnToggle):
    """
    Makes the Rocket (or if possible, Spin Jump + Dash) a local drop, preventing an early BK.
    """
    display_name = "Force Local Start"

@dataclass
class GatoRobotoOptions(PerGameCommonOptions):
    use_smallmech: GlitchSmallmech
    use_watermech: GlitchWatermech
    use_cattech: GlitchCatTech
    nexus_start: NexusStart
    unlock_all_warps: UnlockAllWarps
    local_start: ForceLocalStart

option_groups = [
    OptionGroup(
        "Expert Logic",
        [GlitchSmallmech, GlitchWatermech, GlitchCatTech, NexusStart, UnlockAllWarps, ForceLocalStart],
    ),
]