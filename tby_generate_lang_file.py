import tkinter as tk
from pprint import pprint
import json, os
from tkinter import filedialog
from tby_generate_object_names import create_object_names

root = tk.Tk()
root.withdraw()

IDENTIFIER = "// Maintained by textboxy | tby-lang-tool"
VERSION_INFO = "v0.1.0-beta"
OBJECT_FOLDER_NAME = "objects"
ROOM_FOLDER_NAME = "rooms"
GMS_FILE_ENDING = ".yy"
INSTANCE_CREATION_CODE_PREFIX = "InstanceCreationCode_"
GML_FILE_ENDING = ".gml"


def load_json(path):
    with open(path) as f:
        data = json.load(f)
    return data

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def remove_prefix_suffix(text, prefix, suffix=""):
    if suffix is not "" and text.endswith(suffix):
        text = text[:-len(suffix)]

    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def get_instance_params(instance, object_names_dict, existing_creation_code):
    params = {}
    params["room_id"] = instance["name"]
    params["object_type"] = object_names_dict[ instance["objId"] ]
    params["dialogue"] = []

    # add creation code
    if params["room_id"] in existing_creation_code:
        params["dialogue"] = existing_creation_code[params["room_id"]]

    return params


def process_layer(layer, object_names_dict, existing_creation_code):
    layer_all_instances = []

    if "instances" in layer and layer["instances"]: #if instances is not empty
        for inst in layer["instances"]:
            layer_all_instances.append( get_instance_params(inst, object_names_dict, existing_creation_code) )

    return layer_all_instances


def process_room(room, object_name_dict, existing_creation_code):
    room_all_layers = {}

    # loop through all layers in room
    for layer in room["layers"]:
        current_layer = process_layer(layer, object_name_dict, existing_creation_code)
        if current_layer: #if current_layer is not [], e.g. there are instances
            room_all_layers[layer["name"]] = current_layer
        
    return room_all_layers

def extract_string(str):
    str = str.strip()
    if (str.startswith("[")):
        str = str[1:]
    if (str.startswith("\"")):
        str = str[1:]
    if (str.endswith(",")):
        str = str[:-1]
    if (str.endswith("]")):
        str = str[:-1]
    if (str.endswith("\"")):
        str = str[:-1]

    return str.replace("\"", "'")

def generate_lang_file():
    object_names = create_object_names(project_folder + "/" + OBJECT_FOLDER_NAME, GMS_FILE_ENDING, OBJECT_FOLDER_NAME)

    all_room_data = {}

    existing_creation_code = {}

    for dirpath, dirnames, filenames in os.walk(project_folder + "/" + ROOM_FOLDER_NAME):
        # scan InstanceCreationCode and check if its valid
        for filename in [f for f in filenames if f.endswith(GML_FILE_ENDING)]:
            full_path = os.path.join(dirpath, filename)

            with open(full_path) as gml_file:
                first_line = gml_file.readline().strip()
                if (first_line.startswith(IDENTIFIER)): 
                    cc_instance_id = remove_prefix_suffix(filename, INSTANCE_CREATION_CODE_PREFIX, GML_FILE_ENDING)
                    creation_code_list = [extract_string(line) for line in gml_file][1:-1] # strip newlines and remove first and last entry

                    existing_creation_code[cc_instance_id] = creation_code_list

        # for every .yy file in /rooms
        for filename in [f for f in filenames if f.endswith(GMS_FILE_ENDING)]:
            full_path = os.path.join(dirpath, filename)
            room_json = load_json(full_path)

            all_room_data[room_json["name"]] = process_room(room_json, object_names, existing_creation_code)

    save_json(all_room_data, "lang.json")

########
# start executing
project_folder = filedialog.askdirectory(title = "Select project folder")

# sanity checks
if (os.path.isdir(project_folder + "/" + OBJECT_FOLDER_NAME) and os.path.isdir(project_folder + "/" + ROOM_FOLDER_NAME)):
    generate_lang_file()
else:
    print("Please specify a valid project folder.")