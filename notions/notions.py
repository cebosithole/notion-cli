from email.policy import default
import json
import constants
import click
import notion_crud
import helpers



@click.group()
@click.pass_context
def main(ctx):
    shared_databases = {}

    with open(constants.config_path, 'r') as config_file:
        data = json.load(config_file) 
        shared_databases = data["notion_databases"]

    ctx.ensure_object(dict)
    ctx.obj['Shared_Databases'] = shared_databases

@main.command()
def info():
    # connected users
    print("Connected Users: ")
    notion_crud.info()

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
    
    create_db_res = notion_crud.create_database(name=db,list_props=set_props, parent=parent, db_type=db_type, shared_dbs=shared_dbs)
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

    res = notion_crud.update_database(db_name=db,new_name= new_name, new_props=set_props, shared_dbs=shared_dbs)
    
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
    "--name",
    help = "page name",
    required = True
)
@click.option(
    "--fill-props",
    help = "list of properties and their new values i.e --fill-props title=name,done=true",
    required = True
)
def add_pg(name, db, fill_props):
    print(f"{name}\n{db}\n{fill_props}")


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
def update_pg(db, fill_props):
    print("Select Page To Update:")

    print(f"{db}\n{fill_props}")


@main.command()
@click.option(
    "--db",
    help = "db name or url",
    required = True
)
@click.option(
    "--range",
    help = " give starting and ending point i.e 5,10 \n sorted by creation_time asc",
    required = True
)
def show_pgs(db,range):
    print("Displays pages from range")

@main.command()
@click.pass_context
def show_dbs(ctx):

    count = 1
    print("List Of Available Databases")
    for key,val in ctx.obj["Shared_Databases"].items():
        click.echo(f"{++count}. Name: {key}, Url: {val}")
    

if __name__ == '__main__':
    main()