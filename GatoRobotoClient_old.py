from __future__ import annotations
import os
import asyncio
import typing
import bsdiff4
import shutil
import json
import psutil
import uuid
import subprocess

import Utils

from NetUtils import NetworkItem, ClientStatus
from worlds import gatoroboto
from MultiServer import mark_raw
from CommonClient import CommonContext, server_loop, \
    gui_enabled, ClientCommandProcessor, logger, get_base_parser
from Utils import async_start, is_linux

"""
Notes on things ive learned:
locations_checked = list maintained by client of locations youve checked
checked_locations = list from server of locations youve checked
"""
verbose=True

class GatoRobotoPath:
    @classmethod
    def steam_install(cls) -> list[str]:
        if is_linux:
            return [os.path.expanduser("~/.local/share/Steam/steamapps/common/Gato Roboto")] # running w/ proton

        # default, Utils.is_windows
        return ["C:\\Program Files (x86)\\Steam\\steamapps\\common\\Gato Roboto", "C:\\Program Files\\Steam\\steamapps\\common\\Gato Roboto"]

    @classmethod
    def save_game_folder(cls) -> str:
        if is_linux:
            return os.path.expanduser("~/.local/share/Steam/steamapps/compatdata/916730/pfx/drive_c/users/steamuser/AppData/Local/GatoRoboto_patch_1_1/archipelago") # running w/ proton

        # default, Utils.is_windows
        return os.path.expandvars(r"%localappdata%/GatoRoboto/")

class GatoRobotoCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx) 

    @staticmethod
    def print_log(msg):
        logger.info(msg)
        
    @mark_raw
    def _cmd_auto_patch(self, steam_install: str  = ""):
        """Patch the game automatically."""
        if isinstance(self.ctx, GatoRobotoContext):
            
            #Validate file or set to default path
            if steam_install == "" or not os.path.exists(steam_install):
                for possible_install_location in GatoRobotoPath.steam_install():
                    if os.path.exists(possible_install_location):
                        steam_install = possible_install_location
                        break
            
            #If no valid file error out
            if (not os.path.exists(steam_install)
                or not os.path.isfile(os.path.join(steam_install, "data.win"))):
                self.output("ERROR: Cannot find Gato Roboto. Please rerun the command with the correct folder."
                            " command. \"/auto_patch (Steam directory)\".")
            #Patch game if valid file
            else:                
                self.ctx.patch_game(steam_install)
                self.output("Patching successful!")#

                exe_path = os.path.join(steam_install, "GatoRoboto.exe")
                if not os.path.isfile(exe_path):
                    exe_path = os.path.join(steam_install, "GatoRoboto_patch_1_1.exe")
                    if not os.path.isfile(exe_path):
                        logger.info("No known Gato Roboto executible in the install folder")
                        return
                subprocess.Popen([exe_path, "-game", steam_install])
                
    def _cmd_resync(self):
        """Manually trigger a resync."""
        if isinstance(self.ctx, GatoRobotoContext):
            self.output(f"Syncing items.")
            self.ctx.syncing = True

class GatoRobotoContext(CommonContext):
    tags: dict = {"AP", "Online"}
    game: str = "Gato Roboto B-Side"
    command_processor: GatoRobotoCommandProcessor = GatoRobotoCommandProcessor
    checks_to_consume: list[NetworkItem] = []
    cur_client_items: list[int] = []
    read_client_items: bool = False
    game_id: str = ""
    cur_start_index: int = 0
    items_handling = 0b111
    
    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game = "Gato Roboto B-Side"
        self.syncing = False
        
    @staticmethod
    def patch_game(filepath):
        # TODO: semi modified patch
        #Save vanilla game data for backup purposes
        os.makedirs(name=f"{filepath}/VanillaData", exist_ok=True)
        shutil.copy(f"{filepath}/data.win", f"{filepath}/VanillaData")
        
        #Write patched game data
        with open(f"{filepath}/data.win", "rb") as f:
            patched_file: bytes = bsdiff4.patch(f.read(), gatoroboto.data_path("patch.bsdiff"))
        with open(f"{filepath}/data.win", "wb") as f:
            f.write(patched_file)




    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd, args):
        #print("Got Package: " + cmd) #remove for final
        
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game
        
        async_start(process_gatoroboto_cmd(self, cmd, args))
        
    async def connect(self, address: typing.Optional[str] = None):
        await super().connect(address)

    async def disconnect(self, allow_autoreconnect: bool = False):
        await super().disconnect(allow_autoreconnect)

    async def connection_closed(self):
        await super().connection_closed()

    async def shutdown(self):
        await super().shutdown()
        
    def run_gui(self):
        from kvui import GameManager

        class UTManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Gato Roboto Client"

        self.ui = UTManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

def set_game_id(ctx: GatoRobotoContext):
    # send game id for syncing
    json_out: dict = {
        "game_id": ctx.game_id
    }

    item_in_json: str = json.dumps(json_out, indent=4)

    with open(f"{GatoRobotoPath.save_game_folder()}/tmp_id.json", 'w') as f:
        f.write(item_in_json)

    if os.path.exists(f"{GatoRobotoPath.save_game_folder()}/gameid.json"):
        os.remove(f"{GatoRobotoPath.save_game_folder()}/gameid.json")

    os.rename(f"{GatoRobotoPath.save_game_folder()}/tmp_id.json", f"{GatoRobotoPath.save_game_folder()}/gameid.json")

def disconnected_handle(ctx: GatoRobotoContext):
    ctx.command_processor.print_log("Lost Connection to Game")
    ctx.command_processor.print_log("Waiting for Connection to Game")
    ctx.cur_client_items = []
    ctx.read_client_items = False
    set_game_id(ctx)

async def game_watcher(ctx: GatoRobotoContext):

    ctx.command_processor.print_log("Waiting for Connection to Game")

    while not ctx.exit_event.is_set():
        await asyncio.sleep(0.2)

        """
        If the game is offline, update the gameid
        First, we check if the game has restarted. If so, update the client_items based on the init file.
        """
        #read initial data for syncing items with the client
        current_file_short: str = ""
        current_file: str
        try:
            # game initializes. reset file
            current_file_short = "init.json"
            current_file = f"{GatoRobotoPath.save_game_folder()}/{current_file_short}"
            if os.path.exists(current_file):
                if verbose:
                    ctx.command_processor.print_log("Received Init")

                with open(current_file, 'r+') as f:
                    items_init: dict = get_clean_game_comms_file(f)
                    ctx.cur_client_items = []

                    for key in items_init:
                        if key != "game_id":
                            ctx.command_processor.print_log(f"get item {key} {int(items_init[key])} times")
                            for _ in range(int(items_init[key])):
                                ctx.cur_client_items.append(int(key))
                # os.remove(f"{GatoRobotoPath.save_game_folder()}/init.json")
                if os.path.exists(f"{GatoRobotoPath.save_game_folder()}/init_old.json"):
                    os.remove(f"{GatoRobotoPath.save_game_folder()}/init_old.json")
                os.rename(current_file, f"{GatoRobotoPath.save_game_folder()}/init_old.json")
                if os.path.exists(f"{GatoRobotoPath.save_game_folder()}/req_init.json"):
                    os.remove(f"{GatoRobotoPath.save_game_folder()}/req_init.json")
                ctx.read_client_items = True
                ctx.command_processor.print_log("Connected to Game")

            # game disconnects. disconnect handle
            current_file_short = "off.json"
            current_file = f"{GatoRobotoPath.save_game_folder()}/{current_file_short}"
            if os.path.exists(current_file):
                if verbose:
                    ctx.command_processor.print_log("Received off")
                disconnected_handle(ctx)
                os.remove(current_file)

        except PermissionError:
            ctx.command_processor.print_log(
                f"!!File \"{current_file_short}\" is locked by another program, skipping read.!!")
            await asyncio.sleep(0.3)
            continue
        except:
            ctx.command_processor.print_log(f"Something went wrong in \"{current_file_short}\".")
            await asyncio.sleep(0.3)
            continue

        current_file_short = "init.json"
        current_file = f"{GatoRobotoPath.save_game_folder()}/{current_file_short}"
        if os.path.exists(current_file):
            if verbose:
                ctx.command_processor.print_log("Received Init")
            try:
                with open(current_file, 'r+') as f:
                    items_init: dict = get_clean_game_comms_file(f)
                    ctx.cur_client_items = []

                    for key in items_init:
                        if key != "game_id":
                            ctx.command_processor.print_log(f"get item {key} {int(items_init[key])} times")
                            for _ in range(int(items_init[key])):
                                ctx.cur_client_items.append(int(key))
                #os.remove(f"{GatoRobotoPath.save_game_folder()}/init.json")
                if os.path.exists(f"{GatoRobotoPath.save_game_folder()}/init_old.json"):
                    os.remove(f"{GatoRobotoPath.save_game_folder()}/init_old.json")
                os.rename(current_file, f"{GatoRobotoPath.save_game_folder()}/init_old.json")
                if os.path.exists(f"{GatoRobotoPath.save_game_folder()}/req_init.json"):
                    os.remove(f"{GatoRobotoPath.save_game_folder()}/req_init.json")
                ctx.read_client_items = True
                ctx.command_processor.print_log("Connected to Game")
            except PermissionError:
                ctx.command_processor.print_log(f"!!File \"{current_file_short}\" is locked by another program, skipping read.!!")
                await asyncio.sleep(0.3)
                continue
            except Exception as e:
                ctx.command_processor.print_log(f"Something went wrong in \"{current_file_short}\".")
                await asyncio.sleep(0.3)
                continue

        #check if game disconnects
        current_file_short = "off.json"
        current_file = f"{GatoRobotoPath.save_game_folder()}/{current_file_short}"
        if os.path.exists(current_file):
            if verbose:
                ctx.command_processor.print_log("Received off")

            try:
                disconnected_handle(ctx)
                os.remove(current_file)
            except Exception as e:
                ctx.command_processor.print_log(f"Something went wrong in \"{current_file_short}\".")
                await asyncio.sleep(0.3)
                continue

        # handle client restarts and game crashes via exe check
        # check for active process
        flag = False
        for process in psutil.process_iter(attrs=["exe"]):
            try:
                exe_path: str = process.info["exe"]
                if exe_path and "gatoroboto" in exe_path.lower():  # ✅ Check if not None
                    flag = True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        #if client has restarted, re-request init file
        current_file_short = "req_init.json"
        current_file = f"{GatoRobotoPath.save_game_folder()}/{current_file_short}"
        if flag and not ctx.read_client_items and not os.path.exists(current_file):
            if verbose:
                ctx.command_processor.print_log("Client opened with running exe")

            try:
                open(current_file, "a").close()
            except PermissionError:
                ctx.command_processor.print_log(f"!!File \"{current_file_short}\" is locked by another program, skipping read.!!")
                await asyncio.sleep(0.3)
                continue
            except Exception as e:
                ctx.command_processor.print_log(f"Something went wrong in \"{current_file_short}\".")
                await asyncio.sleep(0.3)
                continue

        #handle game restart via hard close or crash
        elif not flag and ctx.read_client_items:
            if verbose:
                ctx.command_processor.print_log("Game closed after initializing")
            disconnected_handle(ctx)

        #watch for received locations from game
        current_file_short = "locations.json"
        current_file = f"{GatoRobotoPath.save_game_folder()}/{current_file_short}"
        if os.path.exists(current_file):
            if verbose:
                ctx.command_processor.print_log("Received locations")

            try:
                with open(current_file, "r+") as f:
                    locations_in: dict = get_clean_game_comms_file(f)

                    sending: list[int] = []

                    for key in locations_in:
                        if str(key).isdigit():
                            if ctx.missing_locations.__contains__(int(key)) and int(locations_in[str(key)]) > 0:
                                print("Found Location to Send")
                                sending.append(int(key))

                    if len(sending) != 0:
                        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": sending}])

                os.remove(f"{GatoRobotoPath.save_game_folder()}/locations.json")
            except PermissionError:
                ctx.command_processor.print_log(f"!!File \"{current_file_short}\" is locked by another program, skipping read.!!")
                await asyncio.sleep(0.3)
                continue
            except TypeError:
                ctx.command_processor.print_log(f"Error in reading file \"{current_file_short}\", skipping read.")
                await asyncio.sleep(0.3)
                continue
            except Exception as e:
                ctx.command_processor.print_log(f"Something went wrong in \"{current_file_short}\".")
                await asyncio.sleep(0.3)
                continue

        #check if wincon present
        current_file_short = "victory.json"
        current_file = f"{GatoRobotoPath.save_game_folder()}/{current_file_short}"
        if os.path.exists(current_file) and not ctx.finished_game:
            try:
                #ctx.command_processor.print_log("Received Victory")
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

                os.remove(current_file)
            except PermissionError:
                ctx.command_processor.print_log(f"!!File \"{current_file_short}\" is locked by another program, skipping read.!!")
                await asyncio.sleep(0.3)
                continue
            except Exception as e:
                ctx.command_processor.print_log(f"Something went wrong in \"{current_file_short}\".")
                await asyncio.sleep(0.3)
                continue

        current_file_short = "cur_region.json"
        current_file = f"{GatoRobotoPath.save_game_folder()}/{current_file_short}"
        if os.path.exists(current_file):
            try:
                #ctx.command_processor.print_log("New Region")
                with open(current_file, "r+") as f:
                    locations_in: dict = get_clean_game_comms_file(f)

                    await ctx.send_msgs([{"cmd": "Bounce", "slots": [ctx.slot],
                        "data": {
                            "type": "MapUpdate",
                            "mapId": int(locations_in["Region"]),
                        }
                    }])

                os.remove(current_file)
            except PermissionError:
                ctx.command_processor.print_log(
                    f"!!File \"{current_file_short}\" is locked by another program, skipping read.!!")
                await asyncio.sleep(0.3)
                continue
            except Exception as e:
                ctx.command_processor.print_log(f"Something went wrong in \"{current_file_short}\".")
                await asyncio.sleep(0.3)
                continue

        #consume items in fifo order, filter out received items (added context to send multiple of a single item)
        #ctx.command_processor.print_log(f"{len(ctx.checks_to_consume)}, {len(ctx.cur_client_items)}")
        current_file_short = "item.json"
        current_file = f"{GatoRobotoPath.save_game_folder()}/{current_file_short}"
        if len(ctx.checks_to_consume) > 0 and ctx.read_client_items and not os.path.exists(current_file):
            try:
                # turn the list of network items into simple id's
                cur_item: NetworkItem
                checks_to_consume: list[int] = [int(cur_item.item) for cur_item in ctx.checks_to_consume]

                # for each item with a smaller count send missing
                for item_check in set(checks_to_consume):
                    recv_count = checks_to_consume.count(item_check)
                    client_count = ctx.cur_client_items.count(item_check)
                    if recv_count > client_count: # TODO: Could be while loop

                        ctx.cur_client_items.append(int(item_check))
                        client_count += 1

                        item_in = {
                            "item": int(item_check),
                            "item_index": len(ctx.cur_client_items)
                        }
                        if verbose:
                            ctx.command_processor.print_log(f"send item: {item_check} : {recv_count}, {client_count} : {len(ctx.checks_to_consume)} {len(ctx.cur_client_items)}")

                        item_in_json: str = json.dumps(item_in, indent=4)

                        with open(f"{GatoRobotoPath.save_game_folder()}/tmp_it.json", 'w') as f:
                            f.write(item_in_json)

                        if os.path.exists(f"{GatoRobotoPath.save_game_folder()}/init.json"):
                            raise Exception
                        os.rename(f"{GatoRobotoPath.save_game_folder()}/tmp_it.json", f"{GatoRobotoPath.save_game_folder()}/items.json")

                        break # TODO: Remove if while loop
            except PermissionError:
                ctx.command_processor.print_log(f"!!File \"{current_file_short}\" is locked by another program, skipping read.!!")
                await asyncio.sleep(0.3)
                continue
            except Exception as e:
                ctx.command_processor.print_log(f"Something went wrong in \"{current_file_short}\".")
                await asyncio.sleep(0.3)
                continue
        #resync, and attempt to send client all items received
        if ctx.syncing:
            ctx.items_received = []
            sync_msg = [{"cmd": "Sync"}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
            
async def process_gatoroboto_cmd(ctx: GatoRobotoContext, cmd: str, args: dict):
    if cmd == "Bounced":
        print(args)
    
    if cmd == "Connected":
        # Do all file init here
        if not os.path.exists(f"{GatoRobotoPath.save_game_folder()}"):
            os.mkdir(f"{GatoRobotoPath.save_game_folder()}")

        game_id: str
        if "game_id" in args["slot_data"]:
            game_id = args["slot_data"]["game_id"]
        else:
            game_id = str(uuid.uuid4())
            args["slot_data"]["game_id"] = game_id
            
        ctx.game_id = "no-id"

        set_game_id(ctx)

    if cmd == "ReceivedItems":
        ctx.command_processor.print_log("Recieved items")
        #ctx.command_processor.print_log(str(args["items"]))
        ctx.watcher_event.set()
        
        start_index: int = args["index"]
        
        if start_index == 0:
            ctx.items_received = []
        elif start_index != len(ctx.items_received):
            ctx.command_processor.print_log("syncing")
            sync_msg = [{"cmd": "Sync"}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks",
                                 "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
        
        if start_index == len(ctx.items_received):
            
            # Send items to items queue
            for item in args["items"]:
                net_item = NetworkItem(*item)
                ctx.checks_to_consume.append(net_item)
            ctx.items_received = ctx.checks_to_consume.copy()
            ctx.cur_start_index = start_index

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
        
        if os.path.exists(f"{GatoRobotoPath.save_game_folder()}/item.json"):
            os.remove(f"{GatoRobotoPath.save_game_folder()}/item.json")
            
        if os.path.exists(f"{GatoRobotoPath.save_game_folder()}/gameid.json"):
            os.remove(f"{GatoRobotoPath.save_game_folder()}/gameid.json")
            
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        asyncio.create_task(
            game_watcher(ctx), name="GatoRobotoProgressionWatcher")

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
        

