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
- Improved world generation speeds
## Universal Tracker support
Thanks to the Poptracker Integration it will not show a full map of the game with each check with logic!  
Also includes yamlless support so you can generate the tracker without having to use a yaml and use weighted yamls
## Other features
- Seperated Heater Core items: LavaCooled is now seperated from FlowsCleared (Hotboys)
- New client icon: New client icon with a small chance for a shiny evil icon
- Rewritten guides: The setup guide and game guide has been rewritten
- No vsync: Disabled vsync
- Run sync: If the game isn't synced, it will kick you out into the main menu
## Bugfixes in the Mod
- Fixed the hot boy being unable to turn into phase 2
- Fixed the heater core crashing/hardlocking if the lava cooled item is recieved
- Fixed a hardlock caused by the hot boys not properly saving themselves
- Fixed the hot zone effect not being applied properly
- Fixed an item cutscenes not properly finishing
- Removed a few memory leaks
- Fixed the syncing issues caused by game id issues
- Fixed some skipped quests not being properly skipped
- Fixed the controlls/settings not carrying over 
- (WIP) Items recieved by the apworld won't override cutscenes anymore and thus avoid hardlocks
- Fixed logic issues caused by an unsafe warp system
## Bugfixes in the Client
- Getting filler/additional items won't cause a desync anymore
  - Allows the use of "Starting Inventory"
  - Allows the use of "Itemlink"
- Any issues with the client randomly sending items has been resolved
- Prevented issues caused by the client being closed
- Prevented issues caused by starting a new randomizer run
- The auto patcher has been fixed and works
  - Fixed the patch command being unable to find the original installation
  - Fixed the patch command not filtering out quotes
  - Fixed the patch automatically searching for the original installation if you input a bad file path
  - Fixed data corruption caused by attempting to patch multiple times
- Fixed issues caused by receiving duplicates