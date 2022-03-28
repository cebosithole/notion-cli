#!/usr/bin/env python3

import json
from commands.cmd_charts import charts
from commands.cmd_notion import notion
import constants
import click
import helpers
from services import notion_svc

@click.group()
@click.pass_context
def notion_app(ctx):
   pass

notion_app.add_command(cmd=notion)
notion_app.add_command(cmd=charts)
if __name__=="__main__":
    notion_app()