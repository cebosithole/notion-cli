import click
from services import notion_svc


@click.group()
def cli():
    "Interacting with notion pages"
    pass


##-----------PAGES COMMANDS-----------##

# 1. CREATE PAGE
@cli.command("create",help="Creates new page in the specified database")
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
@cli.command("update",help="Updates the select page in the database")
@click.option("--db", help="Database name or url", required=True)
@click.option("--set-props", help="list of properties with values i.e [name=task01,done=True]", default="")
@click.pass_context
def update_pg(ctx, db, set_props):

    print("Updating New Page")
    set_props = set_props.split(",")

    res = notion_svc.update_page(database_name=db, filled_props=set_props)


# 3. DELETE PAGE
@cli.command("delete",help="Archives page in database")
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

#4. SHOW PAGE


@cli.command("show", help="Displays a page")
@click.option("--db", help="database name or url", required=True)
@click.option("--index", help="page index/id")
def show(db, index):
    pages = notion_svc.get_database_pages(
        db_id=notion_svc.get_db_id(db, type="database"))
    #TODO: Implement page display


#5. WRITE TO PAGE
@cli.command("edit", help="Displays a page")
@click.option("--db", help="database name or url", required=True)
@click.option("--index", help="page index/id")
def edit_page_content(db, index):
    #TODO: Implement
    pass


