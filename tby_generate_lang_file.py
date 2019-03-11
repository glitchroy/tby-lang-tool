import tkinter as tk
from pprint import pprint
import json, os
from tkinter import filedialog
from tby_generate_object_names import create_object_names

root = tk.Tk()
root.withdraw()

IDENTIFIER = "// Maintained by textboxy | Parser v0.1-beta"

def load_json(path):
    with open(path) as f:
        data = json.load(f)
    return data


def generate_lang_file():
    object_names = create_object_names(project_folder + "/objects")

    all_room_data = {}

    for dirpath, dirnames, filenames in os.walk(project_folder + "/rooms"):
        # for every .yy file in /rooms
        for filename in [f for f in filenames if f.endswith(".yy")]:
            full_path = os.path.join(dirpath, filename)
            room_json = load_json(full_path)

            room_all_layers = {}

            # loop through all layers in room
            for layer in room_json["layers"]:
                current_layer_all_instances = []
                # loop through all instances in layer
                if "instances" in layer and layer["instances"]: # if instances is not empty
                    for inst in layer["instances"]:
                        current_instance = {}

                        current_instance["room_id"] = inst["name"]
                        current_instance["object_type"] = object_names[inst["objId"]]
                        current_instance["dialogue"] = []

                        current_layer_all_instances.append(current_instance)

                    room_all_layers[layer["name"]] = current_layer_all_instances
                
            all_room_data[room_json["name"]] = room_all_layers

    with open('lang.json', 'w') as f:
        json.dump(all_room_data, f, indent=4)

# execute

project_folder = filedialog.askdirectory(title = "Select project folder")

# sanity checks
if (os.path.isdir(project_folder + "/objects") and os.path.isdir(project_folder + "/rooms")):
    generate_lang_file()
else:
    print("Please specify a valid project folder.")

