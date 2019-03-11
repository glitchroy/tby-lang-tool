import tkinter as tk
from pprint import pprint
import json, os
from tkinter import filedialog
from tby_generate_object_names import create_object_names

root = tk.Tk()
root.withdraw()

IDENTIFIER = "// Maintained by textboxy | tby-lang-tool v0.1-beta"
OBJECT_FOLDER_NAME = "objects"
ROOM_FOLDER_NAME = "rooms"


def load_json(path):
    with open(path) as f:
        data = json.load(f)
    return data


def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def get_instance_params(instance, object_names_dict):
    params = {}
    params["room_id"] = instance["name"]
    params["object_type"] = object_names_dict[ instance["objId"] ]
    params["dialogue"] = []

    return params


def process_layer(layer, object_names_dict):
    layer_all_instances = []

    if "instances" in layer and layer["instances"]: #if instances is not empty
        for inst in layer["instances"]:
            layer_all_instances.append( get_instance_params(inst, object_names_dict) )

    return layer_all_instances


def process_room(room, object_name_dict):
    room_all_layers = {}

    # loop through all layers in room
    for layer in room["layers"]:
        current_layer = process_layer(layer, object_name_dict)
        if current_layer: #if current_layer is not [], e.g. there are instances
            room_all_layers[layer["name"]] = current_layer
        
    return room_all_layers


def generate_lang_file():
    object_names = create_object_names(project_folder + "/" + OBJECT_FOLDER_NAME)

    all_room_data = {}

    for dirpath, dirnames, filenames in os.walk(project_folder + "/" + ROOM_FOLDER_NAME):
        # for every .yy file in /rooms
        for filename in [f for f in filenames if f.endswith(".yy")]:
            full_path = os.path.join(dirpath, filename)
            room_json = load_json(full_path)

            all_room_data[room_json["name"]] = process_room(room_json, object_names)

    save_json(all_room_data, "lang.json")

########
# start executing
project_folder = filedialog.askdirectory(title = "Select project folder")

# sanity checks
if (os.path.isdir(project_folder + "/" + OBJECT_FOLDER_NAME) and os.path.isdir(project_folder + "/" + ROOM_FOLDER_NAME)):
    generate_lang_file()
else:
    print("Please specify a valid project folder.")