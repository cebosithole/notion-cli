
import click
import helpers


EXPORT_OPTIONS = ["pdf","google-sheets","excel","ics"]

@click.group()
@click.option("--db",help="database name or url")
@click.option("-r", help="export recursively incl pages")
@click.option("--to",help="file format to export to", type= click.Choice(EXPORT_OPTIONS))
@click.option("--dest", help="PATH to save exports")
def cli(db,r,to,dest):
    "Exporting notion pages and databases to various outputs"
    
    db_id = helpers.get_db_id(db_name=db)
    if bool(db_id):
        print("EXporting to "+ to)
    

