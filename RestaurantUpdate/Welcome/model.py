class Department: 
    def __init__(self, name, employee_list) -> None:
        self.__name = name
        self.__employee_list = employee_list

    @property # helps us to put a value into an attribute like it is a variable, so no need for getters
    def name(self):
        return self.__name
    
    @name.setter #now we go for a setter
    def name(self, name):
        self.__name = name

    @property 
    def employee_list(self):
        return self.__employee_list
    
    @employee_list.setter 
    def employee_list(self, employee_list):
        self.__employee_list = employee_list

#Class that will deal the employee info
    
class Employee:
    def __init__(self, name, address, emial, phone_nr) -> None:
        self.__name = name
        self.__address = address
        self.__email = emial
        self.__phone_nr = phone_nr

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
    
    @property 
    def emial(self):
        return self.__email
    @emial.setter 
    def email(self, email):
        self.__email = email
    
    @property 
    def phone_nr(self):
        return self.__phone_nr
    @phone_nr.setter 
    def phone_nr(self, phone_nr):
        self.__phone_nr = phone_nr

class User:

    def __init__(self, username, password) -> None:
        self.__username = username
        self.__password = password
    
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

class Restaurant:
    def __init__(self, name, address, menu_list, table_list) -> None:
        self.__name = name
        self.__address = address
        self.__menu_list = menu_list
        self.__table_list = table_list

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
    def __init__(self, name, menu_item_list) -> None:
        
        self.__name = name
        self.__menu_item_list = menu_item_list

    @property 
    def name(self):
        return self.__name
    @name.setter 
    def name(self, name):
        self.__name = name

    @property
    def menu_item_list(self):
        return self.__menu_item_list
    @menu_item_list.setter
    def menu_item_list(self, menu_item_list):
        self.__menu_item_list = menu_item_list

class MenuItem:
    def __init__(self, id, name, price):
        self.__id = id
        self.__name = name
        self.__price = price

    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, id):
        self.__id = id

    @property 
    def name(self):
        return self.__name 
    @name.setter
    def name(self, name):
        self.__name = name
        
    @property
    def price(self):
        return self.__price
    @price.setter
    def price(self, price):
        self.__price = price
        
