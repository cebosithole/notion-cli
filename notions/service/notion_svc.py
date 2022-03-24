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

### DATABASES ###

def create_database(name, parent, list_props, db_type, cached_databases: dict):
    parent_id = None
    db_properties = helpers.build_db_props(list_props)

    if validators.url(parent):
        parent_id = helpers.get_id_from_notionurl(parent, type="database")
    elif parent in cached_databases.keys():
        db_url = cached_databases.get(parent)
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



def update_database(database_name, new_name, new_props, cached_databases):

    res = {}
    # get id from saved names and urls
    if database_name in cached_databases.keys():
        db_url = cached_databases.get(database_name)
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
                        "content": database_name
                    }
                }],
                properties=db_properties

            )
            if res["object"] != "error":
                return {"state": True, "changed_title": False}
    else:
        click.echo("Database not found")
        return {"state": False}  
    



## pages

def create_page( database_name, properties,cached_databases):
    '''
        creates new page in the specified database
    '''
    if database_name in cached_databases.keys():
        db_url = cached_databases.get(database_name)
        db_id = helpers.get_id_from_notionurl(db_url, type= "database")
        
        res = client.pages.create(
            parent={
                "type": "database_id",
                "database_id": db_id
            },
             properties = helpers.convert_str_props_to_notion_db_props(
            usr_props= properties,
            database_props= __get_database_props(db_id=db_id)
        ),
        )

        if res['object']!='error':
            return {"state": True, 'page_url': res["url"]}
    else:
        click.echo("Databases Not Found", err=True)
        return {"state": False}


def delete_page(database_name, rang, cached_databases, display_pgs: bool):
    if validators.url(database_name) != True:
        url = cached_databases[database_name]
        database_name = helpers.get_id_from_notionurl(url,type="database")
        
        
    if rang !=None and display_pgs == False:
        # deletes pages from spcified range
        start,end = [int(x) for x  in rang.split("-")]
        selected_pages = __get_db_pages(database_name)

        for index,page in enumerate(selected_pages):
            if(validators.between(index, min=start,max=end)):
                client.pages.update(
                    page_id=page['id'],
                    archived= True
                )
                print(f"    Deleted {page['name']}")
            
    else:
        selected_pages = __prompt_page_selection(database_name)
        for page in selected_pages:
            client.pages.update(
                page_id=page['id'],
                archived= True
            )
            print(f"    Deleted {page['name']}")




def update_page(database_name, new_filled_props, cached_databases):
    updated_properties ={}
    if validators.url(database_name) != True:
        url = cached_databases[database_name]
        database_name =  helpers.get_id_from_notionurl(url,type="database")
        updated_properties = helpers.convert_str_props_to_notion_db_props(
            database_props= __get_database_props(db_id=database_name),
            usr_props= new_filled_props)
    
    ###page selection
    pages = __prompt_page_selection(database_name)

    for page  in pages:
        client.pages.update(
            page_id=page['id'],
            properties = updated_properties
        )
    print(f"Updated {page['name']}")




def __get_database_props(db_id):
    database_json = client.databases.retrieve(database_id=db_id)
    return database_json["properties"]

def __prompt_page_selection(db_id):
    pages = __get_db_pages(db_id=db_id) 
    selected_pages = []
    for index,page in enumerate(pages):
       print(f"    {index}. {page['name']}")

    choices = [int(x) for x in input("  Select page(s): (i.e 1 or 1-10): ").split("-")]

    # add selected pages
    if len(choices) == 1:
        page = pages[choices[0]]
        selected_pages.append(page)
    else:
        for i in range(choices[0], choices[1]):
            if int(i) < len(pages):
                selected_pages.append(pages[int(i)])
    
    return selected_pages

   
def __get_db_pages(db_id):

    fetched_pages = client.databases.query(
        database_id=db_id,
        page_size = 5  # TODO: MAKE DYNAMIC
    )['results']
    pages = []
   
    for page in fetched_pages:
        page_title = page["properties"]["name"]["title"]

        if len(page_title):
            pg_data = {
                "name":page['properties']['name']['title'][0]['plain_text'],
                "id": page['id']
            }
        else:
            # use page id as name for unamed pages
            pg_data = {
                "name": page['id'],
                "id":page['id']
            }
        pages.append(pg_data)
    
    return pages #[{name:x,id:y}]






    




