import os, os.path, json

def load_json(path):
    with open(path) as f:
        data = json.load(f)
    return data

def create_object_names(object_folder_path, file_ending, object_folder_name):
    object_names = {}

    if (object_folder_path.endswith(object_folder_name) == False):
        print("Could not find object folder.")
    else:
        for dirpath, dirnames, filenames in os.walk(object_folder_path):
            for filename in [f for f in filenames if f.endswith(file_ending)]:
                full_path = os.path.join(dirpath, filename)
                json_data = load_json(full_path)
                object_names[json_data["id"]] = json_data["name"]

    return object_names
    #with open('objects.txt', 'w') as f:
    #    json.dump(object_names, f, indent=4)