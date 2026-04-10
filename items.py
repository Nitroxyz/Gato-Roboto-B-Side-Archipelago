from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import GatoRobotoWorld

ITEM_NAME_TO_ID = {
    "Rocket": 10210,
    "Spin Jump": 10215,
    "Dash": 10216,
    "Hopper": 10214,
    "Cooler": 10211,
    "Decoder": 10209,
    "Big Shot": 10212,
    "Repeater": 10213,

    "Bark Palette": 10002,
    "Nicotine Palette": 10003,
    "Starboard Palette": 10004,
    "Coffee Stain Palette": 10005,
    "Virtual Cat Palette": 10006,
    "Port Palette": 10007,
    "Meowtrix Palette": 10008,
    "Goop Palette": 10009,
    "Urine Palette": 10010,
    "Tamagato Palette": 10011,
    "Gris Palette": 10012,
    "Chewed Gum Palette": 10013,
    "Swamp Matcha Palette": 10014,
    "Grape Palette": 10015,

    "Health Upgrade": 10208,
    "Progressive Water Level": 10237,
    "Hotboy defeated": 10254,
    "Lava Cooled": 10257,
    "Progressive Vent Level": 10268,
    "Cute Meow": 10001,

    "UT Out of Logic": 6900,
}

VHS = (
    "Bark Palette",
    "Nicotine Palette",
    "Starboard Palette",
    "Coffee Stain Palette",
    "Virtual Cat Palette",
    "Port Palette",
    "Meowtrix Palette",
    "Goop Palette",
    "Urine Palette",
    "Tamagato Palette",
    "Gris Palette",
    "Chewed Gum Palette",
    "Swamp Matcha Palette",
    "Grape Palette"
)

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Rocket": ItemClassification.progression | ItemClassification.useful,
    "Spin Jump": ItemClassification.progression,
    "Dash": ItemClassification.progression,
    "Hopper": ItemClassification.progression,
    "Cooler": ItemClassification.progression,
    "Decoder": ItemClassification.progression,
    "Big Shot": ItemClassification.useful,
    "Repeater": ItemClassification.useful,
    "Health Upgrade": ItemClassification.useful,
    "Progressive Water Level": ItemClassification.progression,
    "Hotboy defeated": ItemClassification.progression,
    "Lava Cooled": ItemClassification.progression,
    "Progressive Vent Level": ItemClassification.progression_skip_balancing,
    "Cute Meow": ItemClassification.filler,

    "UT Out of Logic": ItemClassification.progression,
}
for vhs in VHS:
    DEFAULT_ITEM_CLASSIFICATIONS[vhs] = ItemClassification.progression_deprioritized_skip_balancing

class GatoRobotoItem(Item):
    game = "Gato Roboto B-Side"


def create_item_with_correct_classification(world: GatoRobotoWorld, name: str) -> GatoRobotoItem:
    # Our world class must have a create_item() function that can create any of our items by name at any time.
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    return GatoRobotoItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_item_with_alternate_classification(world: GatoRobotoWorld, name: str, classification: ItemClassification) -> GatoRobotoItem:
    return GatoRobotoItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: GatoRobotoWorld) -> None:
    itempool: list[Item] = [
        world.create_item("Rocket"),
        world.create_item("Spin Jump"),
        world.create_item("Cooler"),
        world.create_item("Dash"),
        world.create_item("Hopper"),
        world.create_item("Decoder"),
        world.create_item("Repeater"),
    ]
    if world.options.use_smallmech:
        itempool.append(world.create_item_alt("Big Shot", ItemClassification.trap))
    else:
        itempool.append(world.create_item("Big Shot"))

    itempool += [world.create_item_alt(vhs, ItemClassification.progression_deprioritized_skip_balancing) for vhs in VHS]
    if world.options.health_filler:
        itempool += [world.create_item_alt("Health Upgrade", ItemClassification.filler) for _ in range(10)]
    else:
        itempool += [world.create_item("Health Upgrade") for _ in range(10)]
    itempool += [world.create_item("Progressive Water Level") for _ in range(3)]
    itempool += [world.create_item("Progressive Vent Level") for _ in range(3)]

    # lava cooled check
    if world.options.gato_tech == 3 and not world.options.use_smallmech:
        # Lock it!
        lava_cooled = world.get_location("Cooler (Heater Core-0113)")
        lava_cooled.place_locked_item(world.create_item("Lava Cooled"))
    else:
        itempool.append(world.create_item("Lava Cooled"))

    # Lock the hot boys
    lava_cooled = world.get_location("Hotboy 1 (Heater Core-0019)")
    lava_cooled.place_locked_item(world.create_item("Hotboy defeated"))
    lava_cooled = world.get_location("Hotboy 2 (Heater Core-0313)")
    lava_cooled.place_locked_item(world.create_item("Hotboy defeated"))

    # filler check
    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    # Anyway. With our world's itempool finalized, we now need to submit it to the multiworld itempool.
    # This is how the generator actually knows about the existence of our items.
    world.multiworld.itempool += itempool


def generate_early(world: GatoRobotoWorld) -> None:
    ''' Make sure that the Rocket gets spawned early '''

    # Early Starter items
    if world.options.local_start:
        world.multiworld.local_early_items[world.player]["Rocket"] = 1
    else:
        world.multiworld.early_items[world.player]["Rocket"] = 1