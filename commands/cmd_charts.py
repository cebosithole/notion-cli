"""
    Charting Tool for Notion using Seaborn
"""
from email.policy import default
import click
import helpers
import matplotlib.pyplot as plt
from commands.cmd_notion import get_local_configs
from services import notion_svc


### chart constants
CHART_TYPES = ["line","bar","pie"]

@click.group()
@click.pass_context
def charts(ctx):
    print("charting tool")
      # allow other functions to access configs
    ctx.ensure_object(dict)
    ctx.obj["configs"] = get_local_configs()




@charts.command("line")
@click.option("--db")
@click.option("--type", default="line", type=click.Choice(CHART_TYPES))
@click.option("-x")
@click.option("-y")
@click.option("--x2")
@click.option("--y2")
@click.option("--title")
def plot(ctx,type,db,x,y,title):
    print("Creating A Chart")
    
    if type == CHART_TYPES[0]: #line
        line_graph()
    elif type == CHART_TYPES[1]: # bar
        bar_graph()
    elif type == CHART_TYPES[2]: # pie
        pie()
    else:
        print(f"Chart Type Not Recognised.\nuse only one these : {CHART_TYPES}")



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
    plt.plot(x_vals,y_vals,marker="o")

    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    plt.show()




def bar_graph(ctx,db,x,y):
    print("Generates bar graph")




def pie(ctx,db,x,y):
    print("generate pie graph")
    



def get_values(pages,col_name):
    values = []
    for page in pages:
        prop: dict = page.get("properties").get(col_name)
        prop_type = prop.get('type')
        prop_value = prop.get(prop_type)

        values.append(prop_value)
    return values        

        

