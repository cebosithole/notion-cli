'''
    contains functions to crud notion databases
    and pages
'''

import click
from notion_client import Client
import helpers
import validators
from models.notion_props import TitleProp

client: Client = Client(auth="secret_2dS1qVP0vQpyqZYuNhTEVnzP1Rim4FKzzLs8ckGOGk1") 


def info():
    users = client.users.list()
    
    count = 1
    for user in users.get("results"):
        print(f''' {count}. Name: {user['name']}, Type: {user['type']}''')
        ++count

# functions related to databases

def create_database(name,parent, list_props, db_type ):
    parent_id = None
    db_properties = helpers.build_db_props(list_props)

    if validators.url(parent):
        parent_id = helpers.get_id_from_notionurl(parent,type="database")
    elif parent in config.shared_notion_databases.keys():
        db_url = config.shared_notion_databases.get(parent)
        parent_id = helpers.get_id_from_notionurl(db_url,type="page")


    
    res = client.databases.create(
        parent = {
            "type": "page_id",
        "page_id": parent_id
        },
        title= [{
            'text':
                {
                    "content": name
                }
        }],
        properties = db_properties
    )

    if res["object"] != "error":
        return {"state": True, "url": res["url"]}
    else:
        return {"state": False}

    


def delete_database(name):
    pass

def update_database(name,new_name, new_props):
    db_title = name,
    if new_name:
        db_title = new_name

    # get id from saved names and urls
    if name in config.shared_notion_databases.keys():
        db_url = config.shared_notion_databases.get(name)
        db_id = helpers.get_id_from_notionurl(db_url)
        
        db_properties = helpers.build_db_props(new_props)
        client.databases.update(
            id=db_id,
            title= [{
            'text':
                {
                    "content": db_title
                }
        }],
        properties = db_properties
    )
    else:
        click.echo("Database not found")

def show_databases():
    print(client.databases.list())


# functions related to pages

def create_page(name, db,filled_props):
    pass

def delete_page(name):
    pass

def update_page(name, new_filled_props):
    pass

def show_pages(db, start, end, order):
    pass
