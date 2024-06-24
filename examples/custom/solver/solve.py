#!/usr/bin/python3
import socket
import subprocess

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(("challenge", 4242))
command = c.recv(4096).decode()

# Split the command into a list of arguments to avoid using shell=True
command_list = command.split()

results = subprocess.run(command_list, capture_output=True, text=True)

with open("flag", "w") as f:
    f.write(results.stdout)
