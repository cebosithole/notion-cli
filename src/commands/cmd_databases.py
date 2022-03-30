import click
import helpers
from services import notion_svc

class Context:
    def __init__(self) -> None:
        pass


@click.group()
@click.pass_context
def cli(ctx):
    """Interaction with notion database"""

  
    ctx.obj = Context()


##---------DATABASE COMMANDS--------##

# 1. CREATING DATABASE
@cli.command("create",help="Creates new databases in the specified parent")
@click.option("-p", "--parent", help="id or name of the parent page", required=True, type=str)
@click.option("--db", help="database name", required=True, type=str)
@click.option("--props", help="list of properties i.e name=title,done=checkbox")
@click.pass_context
def create_database(ctx, parent, db, props,):

    print("Creating New Database")
    props = props.split(",")
    res = notion_svc.create_database(
        parent=parent, database_name=db, list_props=props)

    if res["state"]:
        print(res["msg"])
        # save new database to json
        helpers.add_db_to_config(db_name=db, url=res["url"])

    else:
        print(res["msg"])
        print(" Database Not Created")

    print("Done.")


# 2.UPDATING DATABASES
@cli.command("update", help="Updates database attributes")
@click.option("--db", help="Database name", required=True, type=str)
@click.option("--new-name", help="new name of the database")
@click.option("--props", help="list of properties i.e name=title,done=checkbox", default="")
@click.pass_context
def update_db(ctx, db, new_name, props):

    print("Updating Database.")

    props = props.split(",")

    res = notion_svc.update_database(
        database_name=db, new_name=new_name, new_props=props)

    if res["state"]:
        print(res["msg"])
        # save new database name to config.json
        if(bool(new_name)):
            helpers.add_db_to_config(db_name=new_name, url=ctx.obj.cached_db)
            helpers.delete_db_from_config(db_name=db)

    else:
        print(" Database Not Updated")
    print("Done")

# 3. SHOW DATABASE
@cli.command("show", help="Displays database as table")
@click.option("--db", help="database name", required=True)
@click.pass_context
def show(ctx, db):
    print(notion_svc.tabulate_db_pgs(db))
    


#4. Search Database
@cli.command("search",  help="Searches for pages containing query")
@click.option("--db", help="Database name or url")
@click.option("--query")
def search_db(db,query):
    #TODO: implement searching db
    pass
