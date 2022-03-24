#!/usr/bin/env python3

import json
from commands.cmd_notion import notion
import constants
import click
import helpers
from services import notion_svc

@click.group()
@click.pass_context
def main(ctx):
   pass

main.add_command(cmd=notion)

@main.command()
def info():
    # connected users
    print("Connected Users: ")
    notion_svc.info()

# crud functions
@main.command()
@click.option(
    "--parent",
    help="id/url of the parent page to add db in",
    default="338be0dd0d584ea5befdc6c84ccea7a7"

)
@click.option(
    "--db",
    help = "db name or url",
    required = True)
@click.option(
    "--set-props",
    help = "add list of properties i.e --props title,checkbox",
    required = True)
@click.option(
    "--db_type",
    help = "type of database",
    default = "list",
    type = click.Choice(constants.notion_db_types),

)

@click.pass_context
def create_db(ctx,parent,db,set_props, db_type):
    click.echo("Creating Database...")
    
    shared_dbs = ctx.obj["Shared_Databases"]
    set_props = set_props.split(",") # props should be [name=title,done=checkbox]
    
    create_db_res = notion_svc.create_database(name=db,list_props=set_props, parent=parent, db_type=db_type, cached_databases=shared_dbs)
    if create_db_res["state"]:
        click.echo("New Database Created")
    else:
        click.echo("Database Not Created", color=True)
        click.Abort()
    
    helpers.add_db_to_config(db_name=db, url=create_db_res["url"])
    print("Database url added to config.json")
    print("Done.")


@main.command()
@click.option(
    "--db",
    help = "db name or url",
    required = True
)
@click.option(
    "--new-name",
    help = "new db name",

)
@click.option(
    "--set-props",
    default = "test=testval",
    help = "new list of properties i.e  --new-prop  title,checkbox",
    
)
@click.confirmation_option(prompt="This will overwrite db properties, continue?")
@click.pass_context
def update_db(ctx,db,new_name, set_props):
    click.echo("Updating Database")
    
    shared_dbs = ctx.obj["Shared_Databases"]
    set_props = set_props.split(",")

    res = notion_svc.update_database(database_name=db,new_name= new_name, new_props=set_props, cached_databases=shared_dbs)
    
    if res["state"]:
        print("Database Updated")
        # changed old name to new name in config
        if(res["changed_title"]):
            helpers.add_db_to_config(db_name=new_name,url=shared_dbs[db])
            helpers.delete_db_from_config(db_name=db)
            click.echo("Database name changed in config")


    else:
        print("Database Not Updated")
    print("Done")


@main.command()
@click.option(
    "--db",
    help = "db name or url",
    required = True
)

@click.option(
    "--fill-props",
    help = "list of properties and their new values i.e --fill-props title=name,done=true",
    required = True
)
@click.pass_context
def add_pg(ctx, db, fill_props):
    print("Creating New Page")
    res = notion_svc.create_page(database_name=db,properties=fill_props, cached_databases= ctx.obj["Shared_Databases"])

    if res["state"]:
        click.echo("Page Added.")


@main.command()
@click.option(
    "--db",
    help = "db name or url",
    required = True
)
@click.option(
    "--fill-props",
    help = "list of properties to update with new given values",
    required = True
)
@click.pass_context
def update_pg(ctx,db, fill_props):
    notion_svc.update_page(database_name=db,new_filled_props=fill_props,cached_databases=ctx.obj['Shared_Databases'])

@main.command()
@click.option("--db",help="db name",required= True)
@click.option("--range", help="page id")
@click.option("--show-pgs", is_flag=True,help="Dispalays list of pages to select from", type=click.BOOL, default=False)
@click.confirmation_option(prompt="This will archive the selected pages, continue?")
@click.pass_context
def delete_pg(ctx,db,show_pgs, range):

    print("Deleting Pages")
    res = notion_svc.delete_page(database_name=db,rang=range,display_pgs=show_pgs, cached_databases=ctx.obj["Shared_Databases"])


@main.command()
@click.pass_context
def show_dbs(ctx):

    count = 1
    print("List Of Available Databases")
    for key,val in ctx.obj["Shared_Databases"].items():
        click.echo(f"{++count}. Name: {key}, Url: {val}")
    

if __name__ == '__main__':
    main()