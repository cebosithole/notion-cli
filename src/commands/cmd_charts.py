"""
    Charting Tool for Notion using Seaborn
"""
from email.policy import default
import click
import numpy
import helpers
import matplotlib.pyplot as plt
from services import notion_svc



### chart constants
CHART_TYPES = ["line","bar","pie"]

@click.group()
@click.pass_context
def cli(ctx):
    """
        Generating charts from a notion database
        """
    pass




@cli.command("line")
@click.option("--db")
@click.option("-x")
@click.option("-y")
@click.option("--title")
def line_graph(db,x,y,title):
    # get database items
    db_id = helpers.get_db_id(db_name=db)
    pages = notion_svc.get_database_pages(db_id=db_id,limit=10)
    

    # get co-ordinates
    x_vals = get_values(pages=pages,col_name=x)
    y_vals = get_values(pages=pages,col_name=y)
    print(x_vals)
    print(y_vals)

    # plot charts
    plt.plot(x_vals,y_vals,marker="o")

    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    plt.show()



@cli.command("bar")
@click.option("--db")
@click.option("-x")
@click.option("-y")
@click.option("--title")
@click.pass_context
def bar_graph(ctx,db,x,y,title):
    db_id = helpers.get_db_id(db_name=db)
    pages = notion_svc.get_database_pages(db_id=db_id,limit=10)
    

    # get co-ordinates
    x_vals = get_values(pages=pages,col_name=x)
    y_vals = get_values(pages=pages,col_name=y)
    print(x_vals)
    print(y_vals)

    # plot charts
    plt.bar(x_vals,y_vals)

    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    plt.show()


@cli.command("pie")
@click.option("--db")
@click.option("-x")
@click.option("-y")
@click.option("--title")
@click.pass_context
def pie(ctx,db,x,y,title):
    print("generate pie graph")
    



def get_prop_values(pages,col_name):
    " property values"
    values = []
    for page in pages:
        prop: dict = page.get("properties").get(col_name)
        prop_type = prop.get('type')
        prop_value = prop.get(prop_type)

        values.append(prop_value)
    return numpy.array(values)

        

