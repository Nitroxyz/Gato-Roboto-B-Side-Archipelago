from dataclasses import dataclass

from Options import OptionGroup, PerGameCommonOptions, Toggle, DefaultOnToggle, Choice, Range


# Flymech (off)
# Ultrahard (off)
# Upwarp (on)

class GlitchSmallmech(DefaultOnToggle):
    """
    Includes logic for the Smallmech glitch.
    In "Vanilla" difficulty, this will force the Lava Cooled event to be at Cooler
    """
    display_name = "Use Smallmech"

class GlitchWatermech(DefaultOnToggle):
    """
    Includes logic for the Watermech glitch.
    """
    display_name = "Use Watermech"

class GlitchGatoTech(Choice):
    """
    Difficulty of strategies
    Easy is recommended for normal players
    Hard includes a bunch of unique strategies, which require advanced knowledge
    Vanilla is a special difficulty, which:
    - removes the crash fixes in heater core
    - includes the logic for the standard cat vent skip and vent mashing
    - assumes that you can avoid a hardlock in ventilation by either routing properly or resetting the savefile.
    """
    display_name = "Gato Tech"
    option_medium = 1
    option_hard = 2
    option_vanilla_expert = 3

    default = option_medium

class NexusStart(DefaultOnToggle):
    """
    Start in the Nexus instead of the Landing Site.
    Allows for some logic checks without rocket.
    """
    display_name = "Nexus Start"

class ForceLocalStart(DefaultOnToggle):
    """
    Makes the Rocket (or if possible, Spin Jump + Dash) a local drop, preventing an early BK.
    """
    display_name = "Force Local Start"

class AqueductGoal(Range):
    """
    Required amount of "Water Level" required to enter Incubator.
    """
    display_name = "Aqueduct Goal"
    range_start = 0
    range_end = 3

class HeaterCoreGoal(Range):
    """
    Required amount of "Lava Cooled" required to enter Incubator.
    """
    display_name = "Heater Core Goal"
    range_start = 0
    range_end = 1

class VentilationGoal(Range):
    """
    Required amount of "Vent Level" required to enter Incubator.
    """
    display_name = "Ventilation Goal"
    range_start = 0
    range_end = 3

@dataclass
class GatoRobotoOptions(PerGameCommonOptions):
    use_smallmech: GlitchSmallmech
    use_watermech: GlitchWatermech
    gato_tech: GlitchGatoTech
    nexus_start: NexusStart
    local_start: ForceLocalStart
    aqueduct_goal: AqueductGoal
    heatercore_goal: HeaterCoreGoal
    ventilation_goal: VentilationGoal

option_groups = [
    OptionGroup(
        "Expert Logic",
        [GlitchSmallmech, GlitchWatermech, GlitchGatoTech, NexusStart],
    ),
    OptionGroup(
        "Goal Options",
        [AqueductGoal, HeaterCoreGoal, VentilationGoal],
    ),
    OptionGroup(
        "Technical Stuff",
        [ForceLocalStart],
    ),
]