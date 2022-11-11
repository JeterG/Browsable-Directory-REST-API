# Script for making api requests to the rest api once its running.
import os


base_url = "127.0.0.1:8000"
partial_commands = [
    f"{base_url}",
    f"{base_url}/bar",
    f"{base_url}/foo1",
    f"{base_url}/bar/bar1",
    f"-X POST {base_url}/post/new_directory",
    f" -X POST '{base_url}/post/new_directory/new_file.txt?file_or_directory=file&content=NEW%21%21'",
    f" -X PUT '{base_url}/put/new_directory/new_file.txt?file_or_directory=file&content=Continued!'",
    f"{base_url}/new_directory/new_file.txt",
    f" -X PUT '{base_url}/put/new_directory/new_file.txt?file_or_directory=file&content=Overwritten!!&overwite=true'",
    f"{base_url}/new_directory/new_file.txt",
    f"{base_url}/new_directory",
    f"-X DELETE {base_url}/delete/new_directory/new_file.txt",
    f"{base_url}/new_directory",
    f"-X DELETE {base_url}/delete/new_directory",
]
for partial_command in partial_commands:
    command = "curl -s " + partial_command
    print("\n")
    print("COMMAND: ", command)
    os.system(command + "| json_pp")
