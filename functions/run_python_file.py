import os
import subprocess
from google.genai import types

def run_python_file(working_directory,file_path,args=None):
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs_path,file_path))
        valid_file_path = os.path.commonpath([working_dir_abs_path,target_file_path])==working_dir_abs_path
        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file_path]
        if args:
            command.extend(args)
        result = subprocess.run(
            command,
            cwd = working_dir_abs_path,
            capture_output = True,
            text = True,
            timeout = 30
        )
        output_string = ""
        if result.returncode != 0:
            output_string += f"Process exited with code {result.returncode}"
        if not result.stdout and not result.stderr:
            output_string += f"No output produced"
        if result.stdout:
            output_string += f"STDOUT:{result.stdout}"
        if result.stderr:
            output_string += f"STDERR:{result.stderr}"
        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description = "Runs a given python file as a subprocess clearly listing out output and error statements along with exit codes when needed",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path" : types.Schema(
                type = types.Type.STRING,
                description = "The path for the python file which is intended to be ran"
            ),
            "args" : types.Schema(
                type = types.Type.ARRAY,
                description = "Optional arguments which can be passed which are added to our commad(by default its none)",
                items = types.Schema(
                    type = types.Type.STRING,
                    description = "Arguments passed along with the command used to run the pythin file"
                ),
            ),
        },
        required = ["file_path"]
    ),
)
    
    

