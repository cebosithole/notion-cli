import json
import constants
from typing import List
from models.notion_props import *

notion_props_map = {
        "title": TitleProp,
        "number":  NumberProp,
        "checkbox": CheckboxProp,
        "date": DateProp,

    }

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
        prop_name,prop_type  =  item.split("=")

        new_prop = notion_props_map.get(prop_type, NotionBaseProperty)(
            name=prop_name,
            prop_type= prop_type
        )
        
        db_props.update(new_prop.get_databse_prop_config())

    return db_props    
    
def map_to_notion_json_prop(db_props: dict, usr_filled_props: dict):
    
    converted_props = {}
    
    for usr_prop_name in usr_filled_props.keys(): 
        if usr_prop_name in db_props.keys():
            # get corresponding notion prop and init
            # set notipn prop val to users
            usr_prop_type = db_props.get(usr_prop_name)['type']
    
            notion_prop = notion_props_map.get(usr_prop_type,NotionBaseProperty)(
                name=usr_prop_name,prop_type=usr_prop_type)
            notion_prop.set_value(usr_filled_props.get(usr_prop_name))


            converted_props.update(notion_prop.get_prop())

    return converted_props





def get_id_from_notionurl(url: str, type: str):
    if type=="database":
        return url.split("/")[3][:32]
    if type== "page":
        return url.split("/")[3].split("-")[1]
    


def save_db_url_to_config(db_name, url):
    with open(constants.config_path, "w") as config_file:
        data = json.dumo(
            {db_name:url},
            config_file)


