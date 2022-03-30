
from models.notion_props import CheckboxProp, DateProp, NumberProp, TitleProp


notion_props = [
    'title',
    'date',
    'number',
    'checkbox'
]
notion_props_map = {
        "title": TitleProp,
        "number":  NumberProp,
        "checkbox": CheckboxProp,
        "date": DateProp,

    }
notion_db_types = [
    'list',
    'calendar'
]

