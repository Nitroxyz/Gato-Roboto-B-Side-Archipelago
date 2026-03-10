# Gato Roboto B-Side
This mod integrates the Archipelago Randomizer with Gato Roboto. You can send and receive items and world progression in a multiworld containing multiple players.
## Installation
1. Get the apworld in the [releases](https://github.com/Nitroxyz/Gato-Roboto-B-Side-Archipelago/releases) and install it in the apworld (double-click it if you have the Launcher installed)
2. Get your template via "Generate Template Option" or "Options Creator" button in the Archipelago Launcher
3. After installing the apworld, a Gato Roboto B-Side Client is available in the Archipelago Launcher
4. Patch the game in the Client by running `/patch` (add directory path if you don't want to modify the default steam installation)
5. Connect to the Multiworld in the Client and open up the game
6. Make sure to delete the current savefile before starting a new randomizer!
7. If you are unsure about which locations are in logic or not, you can use the universal tracker with a built-in map!
# Current main differences
This mod has been created by a different group of people (with multiple speedrunners and people from the original randomizer), with a focus on stability and plans on adding new features not possible in the current randomizer.
## Unique Settings
- Nexus Start: Start in the nexus instead of landing site, allowing for some rocket-less tech
- Gato Tech: A 3-stage difficulty setting, allowing for more unique and advanced tech on each tier
- Loresanity: Adds the Lore buttons as checks to the game
- Early Goals: Adjust how many event items you need, allowing for quicker randomizers
- Local Rocket: Gives you a local rocket, preventing a long BK
## Visual updates
- Pickup Notification: Added a custom notification when you pick up items which doesn't interrupt your gameplay
- Warp Overhaul: The warps have been fancy'd up to teleport your in style. Also prevents issues with warps breaking the logic
- Coordinate Locations: The location have been renamed to show coordinates to make it easier to find the item on the map
- Item name improvement: Progressive items don't have numbers anymore; VHS item names are shorter
- Old locations: The old location cutscene have returned, with slight adjustments. Item locations now show one random line from the game when you pick up an item ;)
## Logic
A more stable logic which has been tested by a group of experienced speedrunners and challenge players.
- Better logic for Glitches
- Smallmech in ventillation
- Advanced tech to obtain certain items
- Better fine-tuning for item qualities
- No generation failiures
## Universal Tracker support
Thanks to the Poptracker Integration it will not show a full map of the game with each check with logic!  
Also includes yamlless support so you can generate the tracker without having to use a yaml and use weighted yamls
## Other features
- New client icon: New client icon with a small chance for a shiny evil icon
- Rewritten guides: The setup guide and game guide has been rewritten
- No vsync: Disabled vsync
- Run sync: If the game isn't synced, it will kick you out into the main menu
## Bugfixes in the Mod
- Fixed the hot boy being unable to turn into phase 2
- Fixed the heater core potentially crashing/hardlocking if the lava cooled item is recieved
- Fixed a hardlock caused by the hot boys not properly saving themselves
- Items recieved by the apworld won't override cutscenes anymore and thus avoid hardlocks
- Fixed an item cutscenes not properly finishing
- Removed a few memory leaks
- Fixed the syncing issues caused by game id issues
- Fixed some skipped quests not being properly skipped
- Fixed the controlls/settings not carrying over 
## Bugfixes in the Client
- Getting filler/additional items won't cause a desync anymore
- Any issues with the client randomly sending items has been resolved
- Prevented issues caused by the client being closed
- Prevented issues caused by starting a new randomizer run
- The auto patcher has been fixed and works
- Fixed the auto_patch command not filtering out quotes
- Fixed the auto_patch automatically searching for the original installation if you input a bad file path
- Fixed issues caused by receiving duplicates
- Fixed issues by attempting to patch multiple times
## Other (Mostly programming based things)
- Fixed the warps breaking if the landing side warp is missing
- Fixed the Client being able to handle multiples of items
- Improved world generation speeds
# Planned features
## Planned features (for the next updates)
- Add "progressive" to event names
- Partial health filler
- The main terminal tells you how many levels you know for each
- Add a display for event progression
- (bug) Saving in an unsafe spot can cause a hardlock
- (bug) Coordinate improvements
  - Qol-Coordinates in Sub/Cat
  - Automatically updated coordinates
## Planned features (for the future)
- "Both" option for starting location
- Change storage file to the archipelago folder
- Heater Core Mauser fight without smallmech has more logic potential
- Improve the item qualities based on settings selected
  - Health upgrades become partially filler on "Smallmech"
  - Check if certain items become useless on certain settings
- Add Hotboy checks/items to logic
- Add Vanilla "Bottom Open" Route (and "Small Bouncer" Route) for Ventilation
- Progressive Rocket
- Add rocketjump-less option
- (bug) It isn't able to detect if you are on a different run
- Add better notifs for events
- Add more warps pictures
- Main menu touch-up (show connected and other stuff on the file)
- UT support
  - /explain function
  - "out-of-logic"/"glitched" logic
  - /get_logical_path
- Add Bosssanity
- Auto start exe on patch
- Fix Hotboy Flows locking when lava is cooled
- (bug) Win warp back
- Improve the guide and setup page
- Cursed Rocket (1 shot)
- Change to rulebuilder
## Potentially Planned
- Add local pick-up logic (for faster reaction and offline play)
- Submarine upgrades
- Custom Palette (Archipelago Colors)
- Add option for Flymech (Phase State Glitch)
- Stackable upgrades
- Stacked Events (Flooded Ventilation?)
- Add option to keep world progression vanilla
- Add Roomsanity
- Add Room Randomizer
- Warp camera
- In-Game Tracker (on the map)
- Curses
- Deathlink
- Add VHS 1 to the itempool
# The great people who helped in the project
**Nitroxy:** Speedrunner and programmer; Main dev  
**Tylui:** Original randomizer developer; Provided original logic and helped organize the randomizer  
**Haxaplax:** Speedrunner and randomizer player; Helped with the logic and testing  
**Noah:** Speedrunner; Helped with the logic and modding  
**Cullen:** Original game developer; Helped with game specific issues and making modding a little easier  

**Nick:** Programmer; Provided the original Client and helped with the Mod  
**PoryGone:** Discordian; Helped establish the APworld thread  
**Palex:** Discordian; Helped with testing and helped create UT support  
**Slipomatic:** Discordian; Helped with testing and suggestions  
**Faris:** Discordian; Helped with setting up UT support  
**Ixrec:** Discordian; Helped with setting up UT support  
**Mysteryem**: Discordian; Helped with fixing the Client  