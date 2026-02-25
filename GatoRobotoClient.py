from __future__ import annotations
import os
import asyncio
import typing
import bsdiff4
import shutil
import json
import psutil
#import subprocess

import Utils

from NetUtils import NetworkItem, ClientStatus
from worlds import gatoroboto_b_side
from MultiServer import mark_raw
from CommonClient import CommonContext, server_loop, \
    gui_enabled, ClientCommandProcessor, logger, get_base_parser
from Utils import is_linux

verbose = False

def long_file(path):
    """ Creates the full path of the files in the save game folder. """
    # TODO: path.join
    return f"{GatoRobotoPath.save_game_folder()}/{path}"


def safe_delete_file(path):
    """ Safely deletes files in the save game folder. """
    if os.path.exists(long_file(path)):
        os.remove(long_file(path))


def overwrite_file(og_path, new_path):
    """ Forcefully and safely rename a file in the save game folder."""
    if os.path.exists(long_file(og_path)):
        safe_delete_file(new_path)
        os.rename(long_file(og_path), long_file(new_path))


class GatoRobotoPath:
    @classmethod
    def steam_install(cls) -> list[str]:
        if is_linux:
            return [os.path.expanduser("~/.local/share/Steam/steamapps/common/Gato Roboto")]  # running w/ proton

        # default, Utils.is_windows
        return ["C:\\Program Files (x86)\\Steam\\steamapps\\common\\Gato Roboto",
                "C:\\Program Files\\Steam\\steamapps\\common\\Gato Roboto"]

    @classmethod
    def save_game_folder(cls) -> str:
        if is_linux:
            return os.path.expanduser(
                "~/.local/share/Steam/steamapps/compatdata/916730/pfx/drive_c/users/steamuser/AppData/Local/GatoRoboto_patch_1_1/")  # running w/ proton   # TODO: Change to real folder

        # default, Utils.is_windows
        return os.path.expandvars(r"%localappdata%/GatoRoboto_patch_1_1")


class GatoRobotoCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    @staticmethod
    def print_log(msg):
        logger.info(msg)

    @mark_raw
    def _cmd_patch(self, steam_install: str = ""):
        """ Patch the game. """
        if isinstance(self.ctx, GatoRobotoContext):

            #Validate file or set to default path
            steam_install = steam_install.strip(" \"")
            if steam_install == "":
                for possible_install_location in GatoRobotoPath.steam_install():
                    if os.path.exists(possible_install_location):
                        steam_install = possible_install_location
                        break

            #If no valid file error out
            if not os.path.exists(steam_install):
                self.output("ERROR: Cannot find Gato Roboto. Please rerun the command with the correct folder.\n"
                            "command. \"/auto_patch (Steam directory)\" or \"/auto_patch\" for an automatic search.")
            elif not (os.path.isfile(os.path.join(steam_install, "data.win")) or os.path.isfile(os.path.join(steam_install, "ArchipelagoData/data.win"))):
                self.output("ERROR: data.win is missing. Please validate your files.")
            else: #Patch game if valid file
                try:
                    # Save vanilla game data for backup purposes
                    os.makedirs(name=f"{steam_install}/ArchipelagoData", exist_ok=True)
                    if not os.path.exists(f"{steam_install}/ArchipelagoData/data.win"):
                        shutil.copy(f"{steam_install}/data.win", f"{steam_install}/ArchipelagoData/data.win")
                    else:
                        # Revert first, to prevent double patches
                        if os.path.exists(f"{steam_install}/data.win"):
                            os.remove(f"{steam_install}/data.win")
                        shutil.copy(f"{steam_install}/ArchipelagoData/data.win", f"{steam_install}/data.win")

                    def copy_over(source_path, destination_path):
                        data = gatoroboto_b_side.data_path(source_path)
                        with open(destination_path, "wb") as f:
                            f.write(data)

                    # TODO: make full patch work
                    if False:
                        copy_over("data.win", f"{steam_install}/data.win")
                    else:
                        # Write patched game data
                        with open(f"{steam_install}/data.win", "rb") as f:
                            patched_file: bytes = bsdiff4.patch(f.read(), gatoroboto_b_side.data_path("patch.bsdiff"))
                        with open(f"{steam_install}/data.win", "wb") as f:
                            f.write(patched_file)

                    copy_over("warp_pic_ls.png", f"{steam_install}/ArchipelagoData/warp_pic_ls.png")
                    copy_over("warp_pic_nexus.png", f"{steam_install}/ArchipelagoData/warp_pic_nexus.png")
                    self.output("Patching complete!")
                except:
                    self.output("ERROR: Failed to patch data.")

                # TODO: Include auto start
                ''' 
                exe_path = os.path.join(steam_install, "GatoRoboto.exe")
                if not os.path.isfile(exe_path):
                    exe_path = os.path.join(steam_install, "GatoRoboto_patch_1_1.exe")
                    if not os.path.isfile(exe_path):
                        logger.info("No known Gato Roboto executible in the install folder")
                        return
                subprocess.Popen([exe_path, "-game", steam_install])
                '''


class GatoRobotoContext(CommonContext):
    tags: dict = {"AP", "Online"}
    game: str = "Gato Roboto B-Side"
    command_processor: GatoRobotoCommandProcessor = GatoRobotoCommandProcessor
    items_handling = 0b111

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game = "Gato Roboto B-Side"
        self.cur_game_items: list[int] = []
        """ This is used to keep track of all items from the game. """
        self.game_is_initialized: bool = False
        """ This flag depicts wether the game is "connected" and you can send/receive commands. """

    # TODO: Up for removal
    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd, args):
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game
            # Do folder init here
            if not os.path.exists(f"{GatoRobotoPath.save_game_folder()}"):
                os.mkdir(f"{GatoRobotoPath.save_game_folder()}")
            if verbose:
                self.command_processor.print_log("Setting Game ID")
            # send game id (and slot data) for syncing
            if "game_id" not in args["slot_data"]:
                args["slot_data"]["game_id"] = "no-id"
            json_out: dict = args["slot_data"]
            item_in_json: str = json.dumps(json_out, indent=4)
            with open(long_file("tmp_id.json"), 'w') as f:
                f.write(item_in_json)
            overwrite_file("tmp_id.json", "gameid.json")
            self.reconnect_game()

    def run_gui(self):
        from kvui import GameManager

        class UTManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Gato Roboto Client"

        self.ui = UTManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def connection_closed(self):
        self.game_is_initialized = False
        await super().connection_closed()

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.reconnect_game()
        self.locations_checked = set()
        self.finished_game = False
        await super().disconnect()

    def reconnect_game(self):
        """ Custom function; A call to reconnect with the mod. """
        self.game_is_initialized = False
        self.cur_game_items = []
        safe_delete_file("items.json")
        safe_delete_file("init.json")


# All the communication happens here
async def game_watcher(ctx: GatoRobotoContext):
    ctx.command_processor.print_log("Waiting for Connection to Game")

    while not ctx.exit_event.is_set():
        await asyncio.sleep(0.2)
        # If not connected
        if not (ctx.server and ctx.server.socket):
            ctx.game_is_initialized = False
            await asyncio.sleep(2)
            continue
        current_file_short: str = "outer"
        """ Used in debugging to find the section of the error """
        try:
            # TODO: Replace ai junk
            # handle client restarts and game crashes via exe check. if so
            # check for active process
            current_file_short = "active process check"
            running = False
            for process in psutil.process_iter(attrs=["exe"]):
                try:
                    exe_path: str = process.info["exe"]
                    if exe_path and "gatoroboto" in exe_path.lower():  # ✅ Check if not None
                        running = True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

            # game is not running. disconnect when needed
            if not running or os.path.exists(long_file("off.json")):
                if ctx.game_is_initialized:
                    if verbose:
                        ctx.command_processor.print_log(f"Game isn't active anymore {not running} {os.path.exists(long_file('off.json'))}")

                    ctx.command_processor.print_log("Lost Connection to Game")
                    ctx.reconnect_game()
                    ctx.command_processor.print_log("Waiting for Connection to Game")
                #continue # rest of code should be skipped
            #else: assume running

            current_file_short = "init.json"
            if os.path.exists(long_file(current_file_short)):
                # if init file exists, read it
                if verbose:
                    ctx.command_processor.print_log("Received Init")

                ctx.cur_game_items = []
                with open(long_file(current_file_short), 'r+') as f:
                    items_init: dict = get_clean_game_comms_file(f)

                key: str
                for key in items_init:
                    if key.isnumeric():
                        if verbose:
                            ctx.command_processor.print_log(f"get item {key} {int(items_init[key])} times")
                        for _ in range(int(items_init[key])):
                            ctx.cur_game_items.append(int(key))
                safe_delete_file("req_init.json")
                safe_delete_file("items.json")
                overwrite_file(current_file_short, "init_old.json")
                safe_delete_file(current_file_short)
                ctx.game_is_initialized = True
                ctx.command_processor.print_log("Connected to Game")
            else:
                # if init file is missing
                if not ctx.game_is_initialized:
                    # if game isn't initialized, request init
                    # game is already running. request another initialize
                    current_file_short = "req_init.json"
                    if not os.path.exists(long_file(current_file_short)):
                        if verbose:
                            ctx.command_processor.print_log("Client opened with running exe")

                        open(long_file(current_file_short), "a").close()
                else:
                    # if game is initialized, do everything else
                    # watch for received locations from game
                    current_file_short = "locations.json"
                    if os.path.exists(long_file(current_file_short)):
                        if verbose:
                            ctx.command_processor.print_log("Received locations")

                        with open(long_file(current_file_short), "r+") as f:
                            locations_in: dict = get_clean_game_comms_file(f)

                        sending = False
                        for key in locations_in:
                            if str(key).isdigit():
                                if int(key) in ctx.missing_locations and int(locations_in[str(key)]) > 0:
                                    ctx.locations_checked.add(int(key))
                                    sending = True

                        if sending:
                            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(ctx.locations_checked)}])
                        else:
                            safe_delete_file(current_file_short)  # TODO: Test removal
                            if verbose:
                                ctx.command_processor.print_log("Finished receiving locations")

                    # handle win send
                    current_file_short = "victory.json"
                    if os.path.exists(long_file(current_file_short)):
                        if verbose:
                            ctx.command_processor.print_log("Received Victory")
                        if not ctx.finished_game:
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                            ctx.finished_game = True
                        safe_delete_file(current_file_short)

                    # send items
                    current_file_short = "items.json"
                    if len(ctx.items_received) > 0 and not os.path.exists(long_file(current_file_short)):
                        # turn the list of network items into simple id's
                        cur_item: NetworkItem
                        items_received: list[int] = [int(cur_item.item) for cur_item in ctx.items_received]

                        # for each item with a smaller count send missing
                        for item_check in set(items_received):
                            recv_count = items_received.count(item_check)
                            client_count = ctx.cur_game_items.count(item_check)
                            if recv_count > client_count:  # TODO: Could be while loop

                                ctx.cur_game_items.append(int(item_check))
                                client_count += 1

                                item_in = {
                                    "item": int(item_check),
                                    "item_index": len(ctx.cur_game_items)
                                }
                                if verbose:
                                    ctx.command_processor.print_log(f"send item: {item_check} : {recv_count}, {client_count} : {len(ctx.items_received)} {len(ctx.cur_game_items)}")

                                item_in_json: str = json.dumps(item_in, indent=4)
                                with open(long_file("tmp_it.json"), 'w') as f:
                                    f.write(item_in_json)

                                if os.path.exists(long_file("init.json")):
                                    raise RuntimeError
                                overwrite_file("tmp_it.json", current_file_short)

                                break  # TODO: Remove if while loop

        except PermissionError:
            ctx.command_processor.print_log(f"!!File in \"{current_file_short}\" is locked by another program!!")
            await asyncio.sleep(0.3)
            continue
        except Exception as e:
            ctx.command_processor.print_log(f"Something else went wrong in \"{current_file_short}\". Exception type {type(e)}")
            await asyncio.sleep(0.3)
            continue

def get_clean_game_comms_file(f) -> dict | None:
    content = f.read()

    cleaned_content = content.replace("\x00", "").strip()

    if not cleaned_content.endswith("}"):
        cleaned_content += "}"

    try:
        cleaned_json: dict = json.loads(cleaned_content)
    except json.JSONDecodeError:
        print("Error: Invalid JSON file, unable to fix.")
        return None

    if content != cleaned_content:
        f.seek(0)
        f.truncate()
        f.write(cleaned_content)
        print("JSON file cleaned successfully.")

    return cleaned_json


def launch():
    async def _main():
        ctx = GatoRobotoContext(None, None)

        #safe_delete_file("gameid.json")
        safe_delete_file("victory.json")

        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        asyncio.create_task(game_watcher(ctx), name="GatoRobotoProgressionWatcher")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    Utils.init_logging("GatoRobotoClient", exception_logger="Client")
    import colorama

    colorama.init()

    asyncio.run(_main())
    colorama.deinit()

    parser = get_base_parser(description="Gato Roboto Client, for text interfacing.")
    args = parser.parse_args()
