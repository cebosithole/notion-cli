'''
    contains functions to crud notion databases
    and pages
'''

import click
from notion_client import Client
import helpers
import validators

client: Client = Client(
    auth="secret_2dS1qVP0vQpyqZYuNhTEVnzP1Rim4FKzzLs8ckGOGk1")


def info():
    users = client.users.list()

    count = 1
    for user in users.get("results"):
        print(f''' {count}. Name: {user['name']}, Type: {user['type']}''')
        ++count

# functions related to databases


def create_database(name, parent, list_props, db_type, shared_dbs: dict):
    parent_id = None
    db_properties = helpers.build_db_props(list_props)

    if validators.url(parent):
        parent_id = helpers.get_id_from_notionurl(parent, type="database")
    elif parent in shared_dbs.keys():
        db_url = shared_dbs.get(parent)
        parent_id = helpers.get_id_from_notionurl(db_url, type="page")

    res = client.databases.create(
        parent={
            "type": "page_id",
            "page_id": parent_id
        },
        title=[{
            'text':
                {
                    "content": name
                }
        }],
        properties=db_properties
    )

    if res["object"] != "error":
        return {"state": True, "url": res["url"]}
    else:
        return {"state": False}


def delete_database(name):
    pass


def update_database(db_name, new_name, new_props, shared_dbs: dict):

    res = {}
    # get id from saved names and urls
    if db_name in shared_dbs.keys():
        db_url = shared_dbs.get(db_name)
        db_id = helpers.get_id_from_notionurl(db_url, type="database")
        db_properties = helpers.build_db_props(new_props)

        if new_name:
            print(new_name)
            res = client.databases.update(
                database_id=db_id,
                title=[{
                    'text': {
                        "content": new_name
                    }
                }],
                properties=db_properties
            )
            if res['object'] != "error":
                return {"state": True, "changed_title": True}
        else:

            res = client.databases.update(
                database_id=db_id,
                title=[{
                    'text': {
                        "content": db_name
                    }
                }],
                properties=db_properties

            )
            if res["object"] != "error":
                return {"state": True, "changed_title": False}
    else:
        click.echo("Database not found")
        return {"state": False}  
    


def show_databases():
    print(client.databases.list())


# functions related to pages

def create_page(name, db, filled_props):
    pass


def delete_page(name):
    pass


def update_page(name, new_filled_props):
    pass


def show_pages(db, start, end, order):
    pass
