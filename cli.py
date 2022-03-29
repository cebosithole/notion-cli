#!/usr/bin/env python3

import json
from commands.cmd_charts import cli
from commands.cmd_notion import cli
import constants
import click
import helpers
import os
from services import notion_svc

commands_folder = os.path.join(os.path.dirname(__file__),"commands")

class CLI(click.MultiCommand):

   def list_commands(self, ctx):
       commands = []
       for filename in os.listdir(commands_folder):
          if filename.startswith("cmd_"):
             commands.append(filename[4:-3])
       commands.sort()
       print(commands)
       return commands

   def get_command(self,ctx,name):
      try:
           nod = __import__(f"commands.cmd_{name}",None,None,["cli"])
      except ImportError:
         return
      return nod.cli





cli = CLI()

if __name__=="__main__":
    cli()