import json
import constants
import click
import notion_crud
import helpers



@click.group()
@click.pass_context
def main(ctx):
    shared_databases : dict = {}

    with open(constants.config_path, 'r') as config_file:
        data = json.load(config_file) 
        shared_databases = data["notion_databases"]

    ctx.ensure_object(dict)
    ctx.obj['Shared_Databases'] = shared_databases

@main.command()
def notion_info():
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
def create_db(parent,db,set_props, db_type):
    click.echo("Creating Database...")

    # perform necessary conversions
    set_props = set_props.split(",")
    
    create_db_res = notion_crud.create_database(name=db,list_props=set_props, parent=parent, db_type=db_type)
    if create_db_res["state"]:
        click.echo("New Database created")
    else:
        click.echo("Database Not Created", color=True)
        click.Abort()
    
    helpers.add_db_url_to_config(db_name=db, url=create_db_res["url"])
    print("Databases saved to config")
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
    help = "new list of properties i.e  --new-prop  title,checkbox",
    required=True,
)
@click.confirmation_option(prompt="This will overwrite db properties, continue?")
def update_db(db,new_name, set_props):
    click.echo("Updating Database")

    # perfom necessary conversions
    set_props = set_props.split(",")
    notion_crud.update_database(name=db,new_name= new_name, new_props=set_props)


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