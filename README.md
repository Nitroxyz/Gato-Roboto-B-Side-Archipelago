# Gato Roboto B-Side
This mod integrates the Archipelago Randomizer with Gato Roboto. You can send and recieve items and world progression in a multiworld containing multiple players.
## Installation
1. Get the apworld in the [releases](https://github.com/Nitroxyz/Gato-Roboto-B-Side-Archipelago/releases) and install it in the apworld (you can double-click it if you have the Launcher installed)
2. Get your template via the built-in option in the Archipelago Launcher
3. After installing the apworld, a Gato Roboto Client is available in the Archipelago Launcher
4. Patch the game in the Client by running `/auto_patch`
5. Connect to the multiworld in the Client and open up the game
6. Make sure to delete the current savefile before starting a new randomizer!
# What is different?
You might notice that the mod currently is quite similar to the other randomizer, but it does have a few differences.  
This mod has been created by a different group of people (with multiple speedrunners and people from the original randomizer), with a focus on stability and plans on adding new features not possible in the current randomizer.
## Current main differences
### Settings
- A setting to start in the nexus instead of the landing site, allowing for some rocket-less tech
- A 3-stage difficulty setting, allowing for more unique tech on each tier
- A setting to give you a local rocket, preventing a long BK
### Visual updates
- Added a custom notification when you pick up items
- The warps have gotten a visual overhaul
- The location have been renamed to show coordinates to make it easier to find the item on the map
- The old location cutscene have returned, with slight adjustments
  - Item locations now show one random line from the game ;)
- The client icon has been changed
- The setup guide and game guide has been rewritten
- Progressive items don't have numbers anymore
- Disabled vsync
- If the game isn't synced, it will kick you out into the main menu
### Logic
- A more stable logic which has been tested by speedrunners, with some notable improvements being
  - Smallmech in ventillation
  - Advanced tech to obtain certain items
- Better fine-tuning for item qualities
- No generation failiures
### Bugfixes in the Mod
- Fixed the hot boy being unable to turn into phase 2
- Fixed the heater core potentially crashing/hardlocking if the lava cooled item is recieved
- Fixed a hardlock caused by the hot boys not properly saving themselves
- Items recieved by the apworld won't override cutscenes anymore and thus avoid hardlocks
- Fixed an item cutscenes not properly finishing
- Removed a few memory leaks
- Fixed the syncing issues caused by game id issues
- Fixed some skipped quests not being properly skipped
- Fixed the controlls/settings not carrying over 
### Bugfixes in the Client
- Getting filler/additional items won't cause a desync anymore
- Any issues with the client randomly sending items has been resolved
- Prevented issues caused by the client being closed
- Prevented issues caused by starting a new randomizer run
- The auto patcher has been fixed and works
- Fixed the auto_patch command not filtering out quotes
- Fixed the auto_patch automatically searching for the original installation if you input a bad file path
- Fixed issues caused by receiving duplicates
- Fixed issues by attempting to patch multiple times
### Other (Mostly programming based things)
- Fixed the warps breaking if the landing side warp is missing
- Fixed the Client being able to handle multiples of items
- Improved world generation speeds
## Planned features/current issues
### Current known issues
- Vanilla currently doesn't disable the crash fixes
- Receiving an item in a softlock location might cause the game to hardlock you
- Linux might not be compatible
### Planned features (for the next updates)
- Add a display for event progression
- Improve the item qualities based on settings selected
  - Health upgrades become partially filler on "Smallmech"
  - Check if certain items become useless on certain settings
- Check if any more checks can be adjusted from the fixed heater boys fights
- Check the small error in the Ventilation region access rule
- Add better notifs for events
- Add more warps
- Qol-Coordinates in Sub/Cat
- Automatically updated coordinates
- UT support
  - options
  - map
- Heater Core Mauser fight without smallmech has more logic potentially
- Rename the palettes to their in-game counterpart
- Easy vent access can potentially be done with hopper
- the item receive save fix
### Planned features (for the future)
- Option "all warps unlocked"
  - Merge All Warps and Nexus start and add "Both" option
- Submarine upgrades
- Add option to keep world progression vanilla
- Add local pick-up logic (for faster reaction and offline play)
- Add option to use Flymech (Phase State Glitch)
- Add Bosssanity
- Add Loresanity
- Area randomizer
- Stacked Events (Flooded Ventilation?)
- Add Roomsanity
- Add Room Randomizer
- Add rocketjump-less option
- Warp camera
- Improve the guide and setup page
- Add an icon for the client
- Custom Palette (Archipelago Colors)
- Auto start exe on patch
- Stackable upgrades
# The great people who helped in the project
**Nitroxy:** Speedrunner and programmer; Main dev  
**Tylui:** Original randomizer developer; Provided original logic and helped organize the randomizer  
**Haxaplax:** Speedrunner and randomizer player; Helped with the logic and testing  
**Noah:** Speedrunner; Helped with the logic and modding  
**Cullen:** Original game developer; Helped with game specific issues and making modding a little easier  
**Nick:** Programmer; Provided the original Client and helped with the Mod  
**PoryGone (and others):** Discordian; Helped establish the APworld thread  
**Palex:** Discordian; Helped with testing  
**Slipomatic:** Discordian; Helped with testing