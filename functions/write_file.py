import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_write_file_path = os.path.normpath(os.path.join(working_dir_abs,file_path))
        valid_file_path = os.path.commonpath([target_write_file_path,working_dir_abs]) == working_dir_abs
        if not valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_write_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        parent_dirs = os.path.dirname(target_write_file_path)
        os.makedirs(parent_dirs,exist_ok=True)
        with open(target_write_file_path,"w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error {e}"
    
schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description = "Writes new content to a given file in the working directory (overwrites the content if content alredy present or file already exists)",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path" : types.Schema(
                type = types.Type.STRING,
                description = "The path for the file for which new contents are written"
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description = "The new content to be written to the file"
            ),
        },
        required = ["file_path","content"]
    ),
)
