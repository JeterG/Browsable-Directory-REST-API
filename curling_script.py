import os
import subprocess
from pprint import pprint

base_url = "127.0.0.1:8000"
partial_commands = [
    f"{base_url}",
    f"{base_url}/bar",
    f"{base_url}/foo1",
    f"{base_url}/bar/bar1",
    f'-X "DELETE" {base_url}/delete/foo2',
]
for partial_command in partial_commands:
    command = "curl -s " + partial_command
    print("\n")
    print("COMMAND: ", command)
    os.system(command + "  | json_pp")
