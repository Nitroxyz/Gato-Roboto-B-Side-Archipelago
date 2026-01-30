# Gato Roboto B-Side
This mod integrates the Archipelago Randomizer with Gato Roboto. You can send and recieve items and world progression in a multiworld containing multiple players.
## Installation
1. Get the apworld in the releases and install it in the apworld (you can double-click it if you have the Launcher installed)
2. Get your template via the built-in option in the Archipelago Launcher
3. After installing the apworld, a Gato Roboto Client is available in the Archipelago Launcher
4. Patch the game in the Client by running `/auto_patch`
5. If you want to use the controlls/settings from you original game, copy the `userprefs.json` from `%localappdata%/GatoRoboto_patch_1_1` into `%localappdata%/GatoRoboto`
6. Connect to the multiworld in the Client and open up the game
7. Make sure to delete the current savefile before starting a new randomizer!
# What is different?
You might notice that the mod currently is quite similar to the other randomizer, but it does have a few differences.  
This mod has been created by a different group of people (with multiple speedrunners and people from the original randomizer), with a focus on stability and plans on adding new features not possible in the current randomizer.
## Current Main Features/Differences
### Settings
- A setting to start in the nexus instead of the landing site, allowing for some rocket-less tech
- A setting to unlock all warps, giving early access to all areas
- A setting to give you a local rocket, preventing a long BK
### Logic
- A more stable logic which has been tested by speedrunners, with some notable improvements being
  - Every normal check has been properly tested to be possible
  - Smallmech in ventillation has been accounted for
  - Advanced tech to obtain certain items has been accounted for
  - The logic is actually... beatable :)
- Better fine-tuning for item qualities
- No generation failiures
### Bugfixes in the Client/Mod
- Fixed the hot boy being unable to turn into phase 2
- Fixed the heater core potentially crashing/hardlocking if the lava cooled item is recieved
- Fixed a hardlock caused by the hot boys not properly saving themselves
- Getting filler/additional items won't cause a desync anymore
- Any issues with the client randomly sending items has been resolved
- The auto patcher has been fixed and works as intended
- Prevented issues caused by the client being closed
- Prevented issues caused by starting a new randomizer run
- Items recieved by the apworld won't override cutscenes anymore and thus avoid hardlocks
- Items recieved by the apworld  won't save you in unsafe locations anymore preventing hardlocks
- Fixed an item cutscenes not properly finishing
- Removed a few memory leaks
- Fixed the syncing issues caused by game id issues
- Fixed some skipped quests not being properly skipped
### Features in the Client/Mod
- Locations have been renamed to show the coordinates inside the world
- Added a small freeze when you pick up items to prevent accidental mech exits
- Allows items to have duplicate names, thus removing the confusing numeration for progressive items
- If the game isn't synced, it will kick you out into the main menu
- Disabled vsync
### Other (Mostly programming based things)
- Removed a massive amount of junk code
- Fixed the warps breaking if the landing side warp is missing
- Fixed the Client being able to handle multiples of items
- Improved world generation speeds
## Planned features/current issues
### Current known issues
- The Ventilation warp and Landing Site warp are known to cause unintentional early access
- The Ventilation warp position has been adjusted, but isn't fully safe yet
- The Heater Core Logic needs to be revamped
- While the main crash has been fixed in heater core, the alternate crash still remains
- The userprefs.json file containing your controls and settings is using the inccorect location
### Planned features (for the next updates)
- Improve the item qualities based on settings selected
- Add an easy mode, rocket-less mode and vanilla logic mode
- Fix the warps breaking logic
- Add a display for event progression
- Add a revamped notification system for items recieved
- Improve Logic for Heater Core and Ventillation, creating fixes for some hardlocks
### Planned features (for the future)
- Add option to keep world progression vanilla
- Add local pick-up logic (for faster reaction and offline play)
- Add option to use Flymech (Phase State Glitch)
- Add Bosssanity
- Add Loresanity
- Area randomizer
- Stacked Events (Flooded Ventilation?)
- Add Roomsanity
- Add Room Randomizer
# The great people who helped in the project
**Nitroxy**: Speedrunner and programmer; Main dev  
**Tylui**: Original randomizer developer; Provided original logic and helped organize the randomizer  
**Haxaplax**: Speedrunner and randomizer player; Helped with the logic and testing  
**Noah**: Speedrunner; Helped with the logic and modding  
**Cullen**: Original game developer; Helped with game specific issues and making modding a little easier  
**Nick and Pathkendle**: Programmers; Provided the original Mod/Client and helped with some Client issues  
