import os
import json
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs,file_path))
        valid_target_path = os.path.commonpath([working_dir_abs,target_file_path]) == working_dir_abs
        if not valid_target_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open("config.json","r") as f:
            config_contents = json.load(f)
        with open(target_file_path, "r") as f:
            content = f.read(config_contents["MAX_CHARS"])
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {config_contents["MAX_CHARS"]} characters]'
        return content
    except Exception as e:
        return f"Error: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description = "Returns the content of a given file present in the given working directory",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path" : types.Schema(
                type = types.Type.STRING,
                description = "The path of the file whose contents have to be extracted"
            ),
        },
        required = ["file_path"]
    ),
)


    

