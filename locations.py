from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import GatoRobotoWorld

LOCATION_NAME_TO_ID = {
	"VHS (Landing Site-1810)": 11810,
	"Health Upgrade (Landing Site-1812)": 11812,
	"VHS (Landing Site-0710)": 10710,
	"Health Upgrade (Landing Site-0408)": 10408,
	"Rocket (Landing Site-0814)": 10814,
	"Decoder (Landing Site-0807)": 10807,
	"VHS (Aqueducts-2106)": 12106,
	"Water Level (Aqueducts-1908)": 11908,
	"Health Upgrade (Aqueducts-0406)": 10406,
	"Health Upgrade (Aqueducts-1606)": 11606,
	"Spin Jump (Aqueducts-2410)": 12410,
	"VHS (Aqueducts-0707)": 10707,
	"Water Level (Aqueducts-1603)": 11603, # and 1503
	"VHS (Aqueducts-1106)": 11106,
	"Water Level (Aqueducts-0204)": 10204,
	"Health Upgrade (Nexus-2314)": 12314,
	"VHS (Nexus-0914)": 10914,
	"Health Upgrade (Nexus-1014)": 11014,
	"VHS (Nexus-2113)": 12113,
	"VHS (Nexus-1413)": 11413,
	"VHS (Heater Core-0414)": 10414,
	"VHS (Heater Core-1916)": 11916,
	"Cooler (Heater Core-0113)": 10113,
	"VHS (Heater Core-1318)": 11318, # also 1319
	"Dash (Heater Core-1114)": 11114,
	"Health Upgrade (Heater Core-1713)": 11713,
	"Health Upgrade (Heater Core-0417)": 10417,
    "Hotboy 1 (Heater Core-0019)": 10019,
    "Hotboy 2 (Heater Core-0313)": 10313,
    "Lava Cooled (Heater Core-0015)": 10015,
	"Bigshot (Ventilation-1718)": 11718,
	"VHS (Ventilation-0517)": 10517,
	"VHS (Ventilation-1613)": 11613,
	"Health Upgrade (Ventilation-0815)": 10815,
    "Vent Level (Ventilation-1113)": 11113, # also 1112
    "Vent Level (Ventilation-1122)": 11122,
    "Vent Level (Ventilation-0521)": 10521,
	"Health Upgrade (Incubator-2413)": 12413,
	"VHS (Incubator-1513)": 11513,
    "Rebba quest 1 (Nexus-1716)": 11716,
    "Rebba quest 2 (Nexus-1716)": 21716,
}

class GatoRobotoLocation(Location):
    game = "Gato Roboto B-Side"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def create_all_locations(world: GatoRobotoWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: GatoRobotoWorld) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    landing_site = world.get_region("Landing Site")
    nexus = world.get_region("Nexus")
    aqueducts = world.get_region("Aqueducts")
    heater_core = world.get_region("Heater Core")
    ventilation = world.get_region("Ventilation")
    incubator = world.get_region("Incubator")

    landing_site_list = ['VHS (Landing Site-1810)', 'Health Upgrade (Landing Site-1812)', 'VHS (Landing Site-0710)', 'Health Upgrade (Landing Site-0408)', 'Rocket (Landing Site-0814)', 'Decoder (Landing Site-0807)']
    nexus_list = ['Health Upgrade (Nexus-2314)', 'VHS (Nexus-0914)', 'Health Upgrade (Nexus-1014)', 'VHS (Nexus-2113)', 'VHS (Nexus-1413)', "Rebba quest 1 (Nexus-1716)", "Rebba quest 2 (Nexus-1716)"]
    aqueducts_list = ['VHS (Aqueducts-2106)', 'Water Level (Aqueducts-1908)', 'Health Upgrade (Aqueducts-0406)', 'Health Upgrade (Aqueducts-1606)', 'Spin Jump (Aqueducts-2410)', 'VHS (Aqueducts-0707)', 'Water Level (Aqueducts-1603)', 'VHS (Aqueducts-1106)', 'Water Level (Aqueducts-0204)']
    heater_core_list = ['VHS (Heater Core-0414)', 'VHS (Heater Core-1916)', 'Cooler (Heater Core-0113)', 'VHS (Heater Core-1318)', 'Dash (Heater Core-1114)', 'Health Upgrade (Heater Core-1713)', 'Health Upgrade (Heater Core-0417)', "Hotboy 1 (Heater Core-0019)", "Hotboy 2 (Heater Core-0313)", "Lava Cooled (Heater Core-0015)"]
    ventilation_list = ['Bigshot (Ventilation-1718)', 'VHS (Ventilation-0517)', 'VHS (Ventilation-1613)', 'Health Upgrade (Ventilation-0815)', "Vent Level (Ventilation-1113)", "Vent Level (Ventilation-1122)", "Vent Level (Ventilation-0521)"]
    incubator_list = ['Health Upgrade (Incubator-2413)', 'VHS (Incubator-1513)']

    landing_site.add_locations(get_location_names_with_ids(landing_site_list), GatoRobotoLocation)
    nexus.add_locations(get_location_names_with_ids(nexus_list), GatoRobotoLocation)
    aqueducts.add_locations(get_location_names_with_ids(aqueducts_list), GatoRobotoLocation)
    heater_core.add_locations(get_location_names_with_ids(heater_core_list), GatoRobotoLocation)
    ventilation.add_locations(get_location_names_with_ids(ventilation_list), GatoRobotoLocation)
    incubator.add_locations(get_location_names_with_ids(incubator_list), GatoRobotoLocation)

def create_events(world: GatoRobotoWorld) -> None:
    nexus = world.get_region("Nexus")
    ventilation = world.get_region("Ventilation")
    incubator = world.get_region("Incubator")

    nexus.add_event("Completed all areas (Nexus)", "<Completed all areas>", location_type=GatoRobotoLocation, item_type=items.GatoRobotoItem, show_in_spoiler=False)

    if world.options.use_smallmech:
        ventilation.add_event("Smallmech entry (Ventilation)", "<Smallmech entry>", location_type=GatoRobotoLocation, item_type=items.GatoRobotoItem, show_in_spoiler=False)

    incubator.add_event("Victory", "Victory", location_type=GatoRobotoLocation, item_type=items.GatoRobotoItem, show_in_spoiler=False)

