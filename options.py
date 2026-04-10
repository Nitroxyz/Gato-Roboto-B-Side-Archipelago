from dataclasses import dataclass

from Options import OptionGroup, PerGameCommonOptions, Toggle, DefaultOnToggle, Choice, Range, StartInventoryPool


# Flymech (off)
# Ultrahard (off)
# Upwarp (on)

class GlitchSmallmech(Toggle):
    """
    Includes logic for the Smallmech glitch.
    In "Vanilla" difficulty, this will force the Lava Cooled event to be at Cooler.
    """
    display_name = "Use Smallmech"

class GlitchWatermech(Toggle):
    """
    Includes logic for the Watermech glitch.
    """
    display_name = "Use Watermech"

class GlitchGatoTech(Choice):
    """
    Difficulty of strategies.

    "Medium" is recommended for normal players. You might have to do some tricks done in the Any% speedrun if you enable glitches.

    "Hard" includes a bunch of difficult or obscure strategies, which require advanced knowledge.

    "Vanilla" is a special difficulty, with a raised difficulty for the very best. It will:
    - remove the crash fixes in heater core
    - include the logic for the standard cat vent skip and vent mashing
    - assume that you can avoid a hardlock in ventilation by either routing properly or resetting the savefile (not currently!)
    """
    display_name = "Gato Tech"
    option_medium = 1
    option_hard = 2
    option_vanilla_expert = 3

    default = option_medium

class NexusStart(Toggle):
    """
    Start in the Nexus instead of the Landing Site.
    Allows for some logic checks without rocket
    """
    display_name = "Nexus Start"

class AqueductGoal(Range):
    """
    Required amount of "Water Level" required to enter Incubator.
    """
    display_name = "Aqueduct Goal"
    range_start = 0
    range_end = 3
    default = 3

class HeaterCoreGoal(Range):
    """
    Required amount of "Lava Cooled" required to enter Incubator.
    """
    display_name = "Heater Core Goal"
    range_start = 0
    range_end = 1
    default = 1

class VentilationGoal(Range):
    """
    Required amount of "Vent Level" required to enter Incubator.
    """
    display_name = "Ventilation Goal"
    range_start = 0
    range_end = 3
    default = 3

class Loresanity(Toggle):
    """
    Add lore buttons/terminals to the itempool.
    Includes the main terminal in nexus and the two secret lore spot in nexus.
    """
    display_name = "Loresanity"

class ForceLocalStart(DefaultOnToggle):
    """
    Makes the Rocket (or if possible, Spin Jump + Dash) a local drop, preventing an early BK.
    """
    display_name = "Force Local Start"

"""
Allows you to preview more advanced options displayed as yellow "glitched" settings on the Universal Tracker.
You can select which options you want to preview by setting a yaml with the higher diffictulty and putting it in your "Players" folder.
Enable this setting on the player yaml.
"""

class OutOfLogicDisplay(Choice):
    """
    Shows out-of-logic check in the universal tracker.
    Recommended order is: Medium -> Medium all Glitches -> Hard -> Hard all Glitches -> Vanilla all Glitches -> Vanilla
    "all_glitches" shows logic with all glitches enabled.
    "difficulty" shows logic for a difficulty one level higher.
    """
    display_name = "Out-Of-Logic Display"
    option_off = 0
    option_all_glitches = 1
    option_difficulty = 2
    default = option_off

class HealthFiller(Toggle):
    """
    Makes all Health Upgrades filler.
    Use this to allow for extra filler for excluded locations.
    """
    display_name = "Health Filler"

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
    loresanity: Loresanity
    health_filler: HealthFiller
    start_inventory_from_pool: StartInventoryPool
    glitched_logic_display: OutOfLogicDisplay

option_groups = [
    OptionGroup(
        "Logic Options",
        [GlitchSmallmech, GlitchWatermech, GlitchGatoTech, NexusStart],
    ),
    OptionGroup(
        "Goal Options",
        [AqueductGoal, HeaterCoreGoal, VentilationGoal],
    ),
    OptionGroup(
        "Checksanity",
        [Loresanity],
    ),
    OptionGroup(
        "Technical Stuff",
        [ForceLocalStart, OutOfLogicDisplay, HealthFiller],
    ),
]