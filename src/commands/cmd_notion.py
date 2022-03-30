import click
import helpers
from services import notion_svc


class Context:
    def __init__(self) -> None:
        pass


@click.group()
@click.pass_context
def cli(ctx):
    """Interaction with notion directly. """

  
    ctx.obj = Context()


##---------DATABASE COMMANDS--------##

# 1. CREATING DATABASE
@cli.command("create-db")
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
@cli.command("update-db")
@click.option("--db", help="database name", required=True, type=str)
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


##-----------PAGES COMMANDS-----------##

# 1. CREATE PAGE
@cli.command("create-pg")
@click.option("--db", help="database name or url", required=True)
@click.option("--set-props", help="list of properties with values i.e [name=task01,done=True]", default="")
@click.pass_context
def create_pg(ctx, db, set_props):

    print("Creating New Page")
    set_props = set_props.split(",")

    res = notion_svc.create_page(database_name=db, properties=set_props)

    if res["state"]:
        print(" page created")
    else:
        print(" Page Not Created")


# 2. UPDATE PAGE
@cli.command("update-pg")
@click.option("--db", help="database name or url", required=True)
@click.option("--set-props", help="list of properties with values i.e [name=task01,done=True]", default="")
@click.pass_context
def create_pg(ctx, db, set_props):

    print("Updating New Page")
    set_props = set_props.split(",")

    res = notion_svc.update_page(database_name=db, filled_props=set_props)


# 3. DELETE PAGE
@cli.command()
@click.option("--db", help="db name", required=True)
@click.option("--range", help="page id")
@click.option("--show-pgs", is_flag=True, help="Dispalays list of pages to select from", type=click.BOOL, default=False)
@click.pass_context
def delete_pg(ctx, db, range, show_pgs=False):

    print("Deleting Pages")
    res = notion_svc.delete_page(
        database_name=db, rang=range, show_pgs=show_pgs)

    if res["state"]:
        print(res["msg"])
    else:
        print(res["state"])
        print("Pages Not Deleted.")


# 4. SHOW PAGES IN DATABASE
@cli.command("show")
@click.option("--db", help="database name", required=True)
@click.pass_context
def show_pages(ctx, db):
    print(notion_svc.tabulate_db_pgs(db))
    pg_id = input("select page: ")
    #TODO display selected page



#5. Search FOr PAGes
@cli.command("find")
@click.option("-?","--query")
def find(query, db=None):
    """
        Searching for key_word
    """
    if bool(db): # search only the db
        #TODO implement searching
        pass
    else:
        #TODO implement global searching 
        pass