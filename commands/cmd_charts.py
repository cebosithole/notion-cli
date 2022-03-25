"""
    Charting Tool for Notion using Seaborn
"""
import click
import helpers
import seaborn
import matplotlib.pyplot as plt
from commands.cmd_notion import get_local_configs
from services import notion_svc

@click.group()
@click.pass_context
def charts(ctx):
    print("charting tool")
      # allow other functions to access configs
    ctx.ensure_object(dict)
    ctx.obj["configs"] = get_local_configs()




@charts.command("line")
@click.option("--db")
@click.option("-x")
@click.option("-y")
@click.option("--x2")
@click.option("--y2")
@click.option("--title")
def line_graph(db,x,y,x2,y2,title):
    # get database items
    cached_dbs = get_local_configs()["notion_databases"]
    db_id = helpers.get_db_id(db_name=db,cached_dbs=cached_dbs)
    pages = notion_svc.get_database_pages(db_id=db_id,limit=10)
    

    # get co-ordinates
    x_vals = get_values(pages=pages,col_name=x)
    y_vals = get_values(pages=pages,col_name=y)
    x2,y2 = [],[]
    if (x2 and y2) != None:
        x2 = get_values(pages=pages,col_name=x2)
        y2 = get_values(pages=pages,col_name=y2)



    # plot charts
    axis = setup_chart(labels=[x,y],title=title)
    axis
    plt.plot(x_vals,y_vals,marker="o")

    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    plt.show()



def bar_graph():
    pass

def pie_chart():
    pass
    


def setup_chart():
    a = plt.figure()
    ax = a.add_axes()
    ax.set_title("SOmething")
def get_values(pages,col_name):
    values = []
    for page in pages:
        prop: dict = page.get("properties").get(col_name)
        prop_type = prop.get('type')
        prop_value = prop.get(prop_type)

        values.append(prop_value)
    return values        

        

