from model import Info, Menu, MenuItem, Table
import psycopg2

class InfoManagerController:

    def add_info(self, restaurant, info_data):
        infos = restaurant.info_list

        new_info = Info(info_data[0], info_data[1])
        infos.append(new_info)

        restaurant.info_list = infos

    def delete_info(self, restaurant, info_data):
        info_list = restaurant.info_list

        for info in info_list:
            if info.name == info_data[0]:
                info_list.remove(info)

    def update_info(self, old_info_data, new_info_data, restaurant):
        self.delete_info(restaurant, old_info_data)
        self.add_info(restaurant, new_info_data)

class MenuManagerController:

    def add_menu(self, restaurant, menu_data):
        menus = restaurant.menu_list

        new_menu = Menu(menu_data[0], menu_data[1], [])
        menus.append(new_menu)

        restaurant.menu_list = menus

    def delete_menu(self, restaurant, menu_data):
        menu_list = restaurant.menu_list

        for menu in menu_list:
            if menu.name == menu_data[0]:
                menu_list.remove(menu)

    def update_menu(self, old_menu_data, new_menu_data, restaurant):
        self.delete_menu(restaurant, old_menu_data)
        self.add_menu(restaurant, new_menu_data)

class MenuDatabaseManager:

    def __init__(self, databasename, user, password, host, port):
        self.connection = psycopg2.connect(dbname = databasename, user = user, password=password, host = host, port = port)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        create_restaurant_table_query = "CREATE TABLE IF NOT EXISTS restaurants ( id SERIAL PRIMARY KEY, name VARCHAR(50))"
        self.cursor.execute(create_restaurant_table_query)
        self.connection.commit()

        create_menu_table_query = "CREATE TABLE IF NOT EXISTS menus ( id SERIAL PRIMARY KEY, name VARCHAR(50), menu_section VARCHAR(150), res_fk INT REFERENCES restaurants(id))"
        self.cursor.execute(create_menu_table_query)
        self.connection.commit()

        create_menuitems_table_query = "CREATE TABLE IF NOT EXISTS menuitems ( id SERIAL PRIMARY KEY, name VARCHAR(50), description VARCHAR(150), food VARCHAR(50), men_fk INT REFERENCES menus(id))"
        self.cursor.execute(create_menuitems_table_query)
        self.connection.commit()


class MenuItemManagerController:
    
    def add_menuitem(self, menu, menuitem_data):
        menuitems = menu.menuitem_list

        new_menuitem = MenuItem(menuitem_data[0], menuitem_data[1], []) #Vendi i memorjes ku vendosen keto te dhena te reja
        menuitems.append(new_menuitem)
        menu.menuitem_list = menuitems #behet updatei

    def delete_menuitem(self, menu, menuitem_name):
        menuitem_list = menu.menuitem_list

        for menuitem in menuitem_list:
            if menuitem.name == menuitem_name:
                menuitem_list.remove(menuitem)
                menu.menuitem_list = menuitem_list
                break

    def update_menuitem(self, old_menuitem_name, new_menuitem_data, menu):
        menuitem_list = menu.menuitem_list

        for menuitem in menuitem_list:
            if menuitem.name == old_menuitem_name:
                menuitem.name = new_menuitem_data[0]
                menuitem.description = new_menuitem_data[1]
                menuitem.food = new_menuitem_data[2]

class TableManagerController:

    def add_table(self, restaurant, table_data):
        tables = restaurant.table_list

        new_table = Table(table_data[0], table_data[1])
        tables.append(new_table)

        restaurant.table_list = tables

    def delete_table(self, restaurant, table_data):
        table_list = restaurant.table_list

        for table in table_list:
            if table.id == table_data[0]:
                table_list.remove(table)

    def update_table(self, old_table_data, new_table_data, restaurant):
        self.delete_table(restaurant, old_table_data)
        self.add_table(restaurant, new_table_data)
