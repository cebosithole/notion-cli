import json
import sys

import click
import validators
import constants
from typing import List
from models.notion_props import *

notion_props_map = {
        "title": TitleProp,
        "number":  NumberProp,
        "checkbox": CheckboxProp,
        "date": DateProp,

    }

def get_local_configs() -> dict:
    config = {}

    with open(constants.config_path,'r') as config_file:
        config  = json.load(config_file)
        
    return config

def build_db_props(list_props: List):
    '''
        converts list of items to notion database props
        
        parameters
        -----------
        list_props: list,
            list of props i.e [name_prop=prop_type, name_prop=prop_type]
    '''

    db_props = {}

    for item in list_props:
        
        if "=" in item:
            prop_name,prop_type  =  item.split("=")

            new_prop = notion_props_map.get(prop_type, NotionBaseProperty)(
                name=prop_name,
                prop_type= prop_type
            )
            
            db_props.update(new_prop.get_databse_prop_config())

    return db_props    



def convert_str_props_to_notion_db_props(database_props: dict, usr_props: str)-> dict: 
    '''
        example: name=todo,done=True -> {}
    '''
    
    usr_props_dict = list_to_dict(usr_props)
    converted_props = {}
    
    for usr_prop_name, usr_prop_value in usr_props_dict.items():

        prop_exist =  True if database_props[usr_prop_name] != None  else False
        
        
        if prop_exist:
            prop_type = database_props.get(usr_prop_name)["type"]
            filled_notion_prop = notion_props_map.get(prop_type,NotionBaseProperty)(
                name=usr_prop_name,
                prop_type=prop_type
            )
            filled_notion_prop.set_value(usr_prop_value)
            
            converted_props.update(filled_notion_prop.get_prop())
        else:
            print(f"No Property Named {usr_prop_name} Found In Database")
            sys.exit()
    
    return converted_props
    
def list_to_dict(data:list):
    # data = [key=val, key=val]
    dict_data = {}
    for item in data:
        if "=" in item:
            key,val = item.split("=")
            new_dict = {key:val}

            dict_data.update(new_dict)

    return dict_data
    
    
    
    

def get_id_from_notionurl(url: str, type: str):
    if type=="database":
        return url.split("/")[3][:33]
    if type== "page":
        return url.split("/")[3].split("-")[1]
    

def get_db_id(db_name, cached_dbs:dict):
    db_id = ""
    if validators.url(db_name):
        db_id = get_id_from_notionurl(url=db_name,type="database")

    else:
        if db_name in cached_dbs.keys():
            db_url = cached_dbs[db_name]
            db_id = get_id_from_notionurl(url=db_url, type="database")
        else:
            print("")

    return db_id

def add_db_to_config(db_name, url):
    data = {}

    with open(constants.config_path) as config_file:
        data = json.load(config_file)
        #add data
        data["notion_databases"].update({db_name:url})
    
    #save
    with open(constants.config_path, "w+") as config_file:
        json.dump(data, config_file)
        print(" config.json updated.")


def delete_db_from_config(db_name):
    data = {}

    with open(constants.config_path) as config_file:
        data = json.load(config_file)
        #add data
        data["notion_databases"].pop(db_name)
    
    #save
    with open(constants.config_path, "w+") as config_file:
        json.dump(data, config_file)