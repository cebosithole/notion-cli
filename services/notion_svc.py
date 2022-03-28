'''
    contains functions to crud notion databases
    and pages
'''


import pprint
import click
from notion_client import Client
from tabulate import tabulate
import helpers
import validators



## NOTION SERVICE CONSTANSTS ###




client: Client = Client(
    auth="secret_2dS1qVP0vQpyqZYuNhTEVnzP1Rim4FKzzLs8ckGOGk1")


def info():
    users = client.users.list()

    count = 1
    for user in users.get("results"):
        print(f''' {count}. Name: {user['name']}, Type: {user['type']}''')
        ++count

### DATABASES ###

def create_database(database_name, parent, list_props):

    parent_id = get_db_id(db_name=parent,type="page")
    db_properties = helpers.build_db_props(list_props)

    if bool(parent_id):
        res = client.databases.create(
            parent={
                "type": "page_id",
                "page_id": parent_id
            },
            title=[{
                'text':
                    {
                        "content": database_name
                    }
            }],
            properties=db_properties
        )

        if res["object"] != "error":
            return {"state": True,"msg":"Database Created.", "url": res["url"]}
        else:
            return {"state": False}

    else:
        return {"state": False, "msg": "ID not found.\n Database Not Created."}


def update_database(database_name, new_name, new_props, cached_databases):
    db_id = get_db_id(db_name=database_name,type="database")
    db_properties = helpers.build_db_props(new_props)

    if bool(db_id):
        if new_name:
            
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
                return {"state": True, "url": res["url"], "msg": "Database Updated."}

    else:
        return {"state": False, "msg": "Database ID Not Found."}  
    



## pages

def create_page( database_name, properties,cached_databases):
    '''
        creates new page in the specified database
    '''
    db_id = get_db_id(db_name=database_name,type="database")
    if bool(db_id):       
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
            return {"state": True,"msg":"Page Created.", 'url': res["url"]}
    else:
        return {"state": False, "msg": "Database ID Not Found"}


def delete_page(database_name, rang, show_pgs=False):
    '''
        archives specified page(s) in a database
        @param database_name
        @param rang the range of pages to be archived
        @param show_pgs boolean flag for displaying page list to allow page selection
    
    '''
    def _delete_page(items):
        with click.progressbar(items,label="Deleting pages...") as items:
            for page in items:
                client.pages.update(    
                    page_id=page["id"],
                    archived=True
                )            

    db_id = get_db_id(db_name=database_name,type="database")

    if bool(db_id):
        # delete by range
        if bool(rang) and bool(show_pgs) == False:
            startIndex, endIndex = [int(X) for x in rang.split("-")]
            fetched_pages = get_database_pages(db_id=db_id,limit=100)

            _delete_page(fetched_pages[startIndex:endIndex])            
            return {"state": True,"msg": "Page(s) Deleted."}

        else:
            # prompt page selection
            selected_pages = __prompt_page_selection(db_id=db_id)

            _delete_page(selected_pages)
            return {"state": True,"msg": "Page(s) Deleted."}


    else:
        return {"state": False, "msg": "Database ID Not Found"}



def update_page(database_name, filled_props, cached_databases):
    '''
        displays a list of pages to select from and update with new props
    '''            
    def _update_page(items,props):
        with click.progressbar(items,label="Updating page(s)") as items:
            for page in items:
                client.pages.update(
                    page_id= page["id"],
                    properties= props
                )

    db_id = get_db_id(db_name=database_name,type="database")
    updated_properties = helpers.convert_str_props_to_notion_db_props(
        database_props= __get_database_props(db_id=db_id,a=2),
        usr_props= filled_props)


    ### prompt page selection
    pages = __prompt_page_selection(db_id)

    _update_page(pages,updated_properties)
    

#4. Display Pages
def tabulate_db_pgs(db_name, items=None):
    db_id = get_db_id(db_name=db_name,type="database")
    list_db_props = __get_database_props(db_id=db_id,a=1).keys()
    fetched_pages = items if bool(items) else get_database_pages(db_id=db_id)
    # create tables
    #  DB Name
    # ------------
    # name  prop01 prop02
    #
    table_header = list(list_db_props)
    table_data = []
    for page in fetched_pages:
        table_row = []
        
        #extracting title
        for prop_name in page["properties"].keys():
            #get type
            prop_type = page["properties"][prop_name].get("type")
            prop_val = page["properties"][prop_name].get(prop_type)

            #add val to table
            #TODO: Turn this into a resuable function
            if prop_type == "title":
                if len(prop_val):
                    prop_val = prop_val[0]["plain_text"]
                

            elif prop_type == "date":
                if bool(prop_val):
                    prop_val = prop_val['start']
                 
            table_row.append(prop_val)
        table_data.append(table_row)
    
    print(f"\n{db_name} TABLE")
    db_table = tabulate(tabular_data=table_data,headers=table_header, showindex="always", tablefmt="fancy_grid")
    return db_table




def __prompt_page_selection(db_id):
    '''
        Displays pages in a table form
        allows selection of pages
        @return list uuids of selected pages
    '''
    fetched_pages = get_database_pages(db_id=db_id) 
    selected_pages = []


    print(tabulate_db_pgs(db_name=db_id,items= fetched_pages))
    choices = [int(x) for x in input("  Select page(s): (i.e 1 or 1-10): ").split("-")]

    # add selected pages
    if len(choices) == 1:
        page = fetched_pages[choices[0]]
        selected_pages.append(page)
    else:
        for i in range(choices[0], choices[1]+1):
            if int(i) < len(fetched_pages):
                selected_pages.append(fetched_pages[int(i)])
    
    return selected_pages


def get_database_pages(db_id, limit=5):
    fetched_pages = client.databases.query(
        database_id=db_id,
        page_size = limit
    )['results']
    pages = []
    
    for page in fetched_pages:
        page_title = page["properties"]["name"]["title"]

        if len(page_title):
            pg_data = {
                "name":page_title[0]['plain_text'],
                "id": page['id'],
                "properties": page['properties']
            }
        else:
            # use page id as name for unamed pages
            pg_data = {
                "name": page['id'],
                "id":page['id'],
                "properties": page["properties"]
            }
        pages.append(pg_data)
    
    return pages #[{name:x,id:y}]





###---------- HELPING FUNCTIONS ----------###
def get_db_id(db_name,type):

    def id_from_notion_url(url,type=type):
        if type=="database":
            return url.split("/")[3][:33]
        if type== "page":
         return url.split("/")[3].split("-")[1]

    db_id = ""
    if validators.url(db_name):
        db_id = id_from_notion_url(db_name)
    elif len(db_name.strip()) == 32:
        db_id = db_name
    else:
        # db_name is just a word.
        # check if name exists in local config and fetch the url
        cached_dbs = helpers.get_local_configs()["notion_databases"]
        if db_name in cached_dbs.keys():
            url = cached_dbs.get(db_name)
            db_id = id_from_notion_url(url)
    
    return db_id


def __get_database_props(db_id, a=0):
    data = client.databases.retrieve(database_id=db_id)
    if data["object"] == "database":
        return data["properties"]
