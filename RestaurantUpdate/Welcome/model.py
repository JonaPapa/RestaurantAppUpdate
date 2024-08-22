from enum import Enum

class Restaurant:
    def __init__(self, name, info_list, menu_list, table_list, menuitem_list) -> None:
        self.__name = name
        #self.__address = address
        self.__info_list = info_list
        self.__menu_list = menu_list
        self.__table_list = table_list
        self.__menuitem_list = menuitem_list

    @property 
    def name(self):
        return self.__name
    @name.setter 
    def name(self, name):
        self.__name = name

    '''@property 
    def address(self):
        return self.__address
    @address.setter 
    def address(self, address):
        self.__address = address'''

    @property 
    def info_list(self):
        return self.__info_list
    @info_list.setter 
    def info_list(self, info_list):
        self.__info_list = info_list


    @property 
    def menu_list(self):
        return self.__menu_list
    @menu_list.setter 
    def menu_list(self, menu_list):
        self.__menu_list = menu_list

    @property 
    def table_list(self):
        return self.__table_list
    @table_list.setter 
    def table_list(self, table_list):
        self.__table_list = table_list

    @property 
    def menuitem_list(self):
        return self.__menuitem_list
    @menuitem_list.setter 
    def menuitem_list(self, menuitem_list):
        self.__menuitem_list = menuitem_list

class Info:
    def __init__(self, name, address) -> None:
        self.__name = name
        self.__address = address
        

    @property 
    def name(self):
        return self.__name
    @name.setter 
    def name(self, name):
        self.__name = name

    @property 
    def address(self):
        return self.__address
    @address.setter 
    def address(self, address):
        self.__address = address
    
class User:

    def __init__(self, username, password, user_role) -> None:
        self.__username = username
        self.__password = password
        self.__user_role = user_role
    
    @property 
    def username(self):
        return self.__username
    @username.setter 
    def username(self, username):
        self.__username = username
    
    @property 
    def password(self):
        return self.__password
    @password.setter 
    def password(self, password):
        self.__password = password

    @property
    def user_role(self):
        return self.__user_role
    @user_role.setter
    def user_role(self, user_role):
        self.__user_role = user_role



class Table:
    def __init__(self, id, seats):
        self.__id = id
        self.__seats = seats  

    @property 
    def id(self):
        return self.__id
    @id.setter 
    def id(self, id):
        self.__id = id

    @property 
    def seats(self):
        return self.__seats
    @seats.setter 
    def seats(self, seats):
        self.__seats = seats
    
    
class Menu:
    def __init__(self, name, menu_section, menuitem_list) -> None:
        
        self.__name = name
        self.__menu_section = menu_section
        self.__menuitem_list = menuitem_list

    @property 
    def name(self):
        return self.__name
    @name.setter 
    def name(self, value):
        self.__name = value

    @property
    def menu_section(self):
        return self.__menu_section
    @menu_section.setter
    def menu_section(self, value):
        self.__menu_section = value

    @property
    def menuitem_list(self):
        return self.__menuitem_list
    @menuitem_list.setter
    def menuitem_list(self, value):
        self.__menuitem_list = value

class MenuItem:
    def __init__(self, name, description, food):
        
        self.__name = name
        self.__description = description
        self.__food = food

    @property 
    def name(self):
        return self.__name 
    @name.setter
    def name(self, value):
        self.__name = value
        
    @property
    def description(self):
        return self.__description
    @description.setter
    def description(self, value):
        self.__description = value
        
    @property
    def food(self):
        return self.__food
    @food.setter
    def food(self, value):
        self.__food = value
        
