
import click
import helpers


EXPORT_OPTIONS = ["pdf","google-sheets","excel","ics"]

@click.group()
@click.option("--db")
@click.option("--to", type= click.Choice(EXPORT_OPTIONS))
def cli(db,to):
    "Exporting notion pages and databases to various outputs"
    
    db_id = helpers.get_db_id(db_name=db)
    if bool(db_id):
        print("EXporting to "+ to)
    

