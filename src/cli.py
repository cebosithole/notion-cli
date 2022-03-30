#!/usr/bin/env python3

import click
import os

commands_folder = os.path.join(os.path.dirname(__file__),"commands")
print(commands_folder)
class CLI(click.MultiCommand):

   def list_commands(self, ctx):
       commands = []
       for filename in os.listdir(commands_folder):
          if filename.startswith("cmd_"):
             commands.append(filename[4:-3])
       commands.sort()
       
       return commands

   def get_command(self,ctx,name):
      try:
           nod = __import__(f"commands.cmd_{name}",None,None,["cli"])
      except ImportError:
         return
      return nod.cli





main_cli = CLI()

if __name__ == "__main__":
   main_cli()