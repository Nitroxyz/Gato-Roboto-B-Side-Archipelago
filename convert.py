with open("gatologic_converted.txt") as f:
    for x in f:
        x = x.strip()
        if len(x) == 0:
            print(x)
            continue
        if x.find(": ") == -1:
            print(x)
            continue
        loc, rule = tuple(x.split(": ", 2))
        print(f"    current_location = world.get_location(\"\033[94m{loc}\033[0m\")\n"
              f"    set_rule(current_location, lambda state: \033[92m{rule}\033[0m)")
