"""
    contains command-line commands for interacting
    with notion
"""

from email.policy import default
import json
import click
import constants
import helpers
from services import notion_svc

def get_local_configs() -> dict:
    config = {}

    with open(constants.config_path,'r') as config_file:
        config  = json.load(config_file)
        
    return config
    


@click.group()
@click.pass_context
def notion(ctx):
    """
        Group of functions to interact with notion
    """
    
    # allow other functions to access configs
    ctx.ensure_object(dict)
    ctx.obj["configs"] = get_local_configs()


##---------DATABASE COMMANDS--------##

#1. CREATING DATABASE
@notion.command("create-db")
@click.option("-p","--parent", help="id or name of the parent page", required=True, type=str)
@click.option("--db", help="database name", required=True,type=str)
@click.option("--type", help="type of database to create", type=click.Choice(choices=constants.notion_db_types),default="list")
@click.option("--props", help="list of properties i.e name=title,done=checkbox")
@click.pass_context
def create_database(ctx,parent, db,type, props,):
    
    print("Creating New Database")
    cached_dbs =  ctx.obj["configs"]["notion_databases"]
    props = props.split(",")
    res =  notion_svc.create_database(parent=parent,name=db,list_props=props, cached_databases=cached_dbs,db_type=type)
    
    if res["state"]:
        print(f" {db} Created.")
        # save new database to json
        helpers.add_db_to_config(db_name=db,url=res["url"])
        
        
    else:
        print(" Database Not Created")
    
    print("Done.")


#2.UPDATING DATABASES
@notion.command("update-db")
@click.option("--db", help="database name", required=True,type=str)
@click.option("--new-name", help="new name of the database")
@click.option("--props", help="list of properties i.e name=title,done=checkbox", default="")
@click.pass_context
def update_db(ctx,db,new_name, props):
    
    print("Updating Database.")
    
    cached_dbs = ctx.obj["configs"]["notion_databases"]
    props = props.split(",")

    res = notion_svc.update_database(database_name=db,new_name= new_name, new_props=props, cached_databases=cached_dbs)
    
    if res["state"]:
        print(f" {db} Updated.")
        # save new database name to config.json
        if(res["changed_title"]):
            helpers.add_db_to_config(db_name=new_name,url=cached_dbs[db])
            helpers.delete_db_from_config(db_name=db)
        


    else:
        print(" Database Not Updated")
    print("Done")



##-----------PAGES COMMANDS-----------##

#1. CREATE PAGE


#2. UPDATE PAGE


#3. DELETE PAGE

@notion.command()
def notion_info():
    print("notion shit")