# tby-lang-tool

The purpose of this tool is to generate a human-readable outline of an entire GMS2 project, sorted by rooms, layers and instances.
This structure can then be used to add dialogue to every instance and import the changes back in.  
Ideally, using this tool, no strings have to be hard-coded into the project itself, helping with translation and proofreading.

This tool is written in `Python 3.6.7` and intended for the use with [textboxy](https://github.com/glitchroy/textboxy).

## Usage
For now, please call `tby_generate_lang_file.py` on the command line, like this
```
$ python tby_generate_lang_file.py
```

You will be prompted to specify your project directory. The tool will scan the `/objects`-directory to build a list of object names and their unique identifiers and will then scan the `/room`-directory for every instance. It will output everything into a `lang.json` file.
