'''
    models notion properties
'''


class NotionBaseProperty:
    def __init__(self, name=None, val=None,prop_type=None) -> None:
        self.name = name
        self._value = val
        self.type = prop_type
        

    def set_value(self, new_val):
        self._value = new_val
   
    def  get_databse_prop_config(self):
        '''returns a map of database property'''
        return {
            self.name: {
                self.type: {}
            }
        }
    def get_prop(self):

        prop_config = self.get_databse_prop_config()
        prop_config[self.name][self.type] = self._value

        return prop_config


class TitleProp(NotionBaseProperty):
    def set_value(self, new_val):
        # self._value = new_val
        self._value = [{
            'text': {
                'content': new_val
            }
        }]

class DateProp(NotionBaseProperty):
    def set_value(self, value):
        self._value = {
                'end': None,
                'start': value,
                'time_zone': None}
            
class NumberProp(NotionBaseProperty):
    def set_value(self, value):
        self._value = int(value)


class CheckboxProp(NotionBaseProperty):
    def set_value(self, value):
     
        self._value = eval(value)


