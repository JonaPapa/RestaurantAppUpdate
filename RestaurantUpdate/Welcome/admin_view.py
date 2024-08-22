from data_provider import DataProvider
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.button import Button
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from admin_controllers import InfoManagerController, MenuManagerController, MenuItemManagerController, TableManagerController, MenuDatabaseManager
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from model import Info, Menu, MenuItem, Table
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.checkbox import CheckBox
from enums import Food


class RestaurantManagerContentPanel:
    selected_row = -1
    restaurant_list = DataProvider().restaurant_list
    info_manager_controller = InfoManagerController()

 
    def create_content_panel(self):
        split_layout_panel = GridLayout(cols=2)
        split_layout_panel.add_widget(self._create_info_input_data_panel())
        split_layout_panel.add_widget(self._create_info_management_panel())
        return split_layout_panel

    #Method to create the panel for restaurant data

    def _create_info_input_data_panel(self):
        input_data_component_panel = GridLayout(cols=1, padding=30, spacing=20)
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = 400

        #Restaurant name
        self.name_input = MDTextField(mode = "rectangle", size_hint = (0.9, 0.1), hint_text='Restaurant name')
        input_data_component_panel.add_widget(self.name_input)
        #Restaurant address
        self.address_input = MDTextField(mode = "rectangle", size_hint = (0.9, 0.1), hint_text='Restaurant address')
        input_data_component_panel.add_widget(self.address_input)
       
        input_data_component_panel.add_widget(self._create_buttons_component_panel())
        return input_data_component_panel

    def _create_info_management_panel(self):
        content_panel = GridLayout(cols=1, spacing=10)
        content_panel.add_widget(self._create_restaurant_selector())
        content_panel.size_hint_x = None
        content_panel.width = 1200
        content_panel.add_widget(self._create_table_panel())
        return content_panel

    def _create_buttons_component_panel(self):
        buttons_component_panel = GridLayout(cols=3, padding=0, spacing=10)
        add_button= Button(text='Add', size_hint=(None,None), size=(100, 40), background_color=(0,1,1,1))
        update_button = Button(text='Update', size_hint=(None,None), size=(100,40), background_color=(0,1,1,1))
        delete_button = Button(text='Delete', size_hint=(None,None), size=(100,40), background_color=(0,1,1,1))
        update_button.bind(on_press = self._update_info)
        add_button.bind(on_press = self._add_info)
        delete_button.bind(on_press = self._delete_info)
        buttons_component_panel.add_widget(add_button)
        buttons_component_panel.add_widget(update_button)
        buttons_component_panel.add_widget(delete_button)
        return buttons_component_panel

    def _create_table_panel(self):
        table_panel = GridLayout(cols=1, padding=10, spacing=0)
        self.info_table = self.create_table()
        table_panel.add_widget(self.info_table)
        self.info_table.bind(on_check_press = self._checked)
        self.info_table.bind(on_row_press = self._on_row_press)

        return table_panel

    def _create_restaurant_selector(self):
        button = Button(text='Restaurant List', size_hint=(1, 0.1), background_color=(0,1,1,1))
        button.bind(on_release=self.show_menu)
        return button

    def create_table(self):
        table_row_data = []

        self.restaurant = self.restaurant_list[0]
        infos = self.restaurant.info_list

        for info in infos:
            table_row_data.append((info.name, info.address))

        self.info_table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y':0.5},
            check=True,
            use_pagination=True,
            rows_num= 10,
            column_data=[
                ("Name", dp(40)),
                ("Address", dp(30))
            ],
            row_data = table_row_data
        )
        return self.info_table


    def show_menu(self, button):
        menu_items=[]
        restaurant_list = self.restaurant_list

        for restaurant in restaurant_list:
            menu_items.append({"viewclass": "OneLineListItem", 
                               "text": restaurant.name,
                               "on_release": lambda r=restaurant: self._update_data_table(r),
                              }
                             )


        self.dropdown = MDDropdownMenu(
            caller=button,
            items = menu_items,
            width_mult=5,
            max_height=dp(150),
        )

        self.dropdown.open()

    def _checked(self, instance_table, current_row):
        selected_info = Info(current_row[0], current_row[1])
        self.name_input.text = str(selected_info.name)
        self.address_input.text = str(selected_info.address)


    def _on_row_press(self, instance, row):
        self.selected_row = int(row.index / len(instance.column_data))


    def _update_data_table(self, restaurant):
        self.restaurant = restaurant

        table_row_data = []
        infos = restaurant.info_list
        for info in infos:
            table_row_data.append(
                (info.name, info.address)
            )

        self.info_table.row_data = table_row_data


    def _add_info(self, instance):
            
        name = self.name_input.text
        address = self.address_input.text

        info_data = []
        info_data.append(name)
        info_data.append(address)


        if self._is_data_valid(info_data):
            self.info_manager_controller.add_info(
                self.restaurant, info_data
            )

            self.info_table.row_data.append((name, address))
            self._clear_input_text_fields()
        else:
            popup = Popup(
                title = "Invalid data",
                content=Label(text="Provide mandatory data to add a new Info"),
                size_hint = (None, None),
                size = (400, 200),
            )
            popup.open()

    def _update_info(self, instance):
        if self.selected_row != -1:
            name = self.name_input.text
            address = self.address_input.text

            info_data = []
            info_data.append(name)
            info_data.append(address)

            if self._is_data_valid(info_data):
                info_to_remove = self.info_table.row_data[self.selected_row]
            # Delete the existing employee data from the department
            del self.info_table.row_data[self.selected_row]
            self.info_manager_controller.delete_info(
                self.restaurant, info_to_remove
            )

            # Add the updated employee data to the department
            self.info_manager_controller.add_info(
                self.restaurant, info_data
            )

            self.info_table.row_data.append([name, address])

            self._clear_input_text_fields()

        else:
            popup = Popup(
                title="Invalid data",
                content=Label(text="Provide mandatory data to update the Info"),
                size_hint=(None, None),
                size=(400, 200),
            )
            popup.open()

    
    def _delete_info(self, instance):
        if self.selected_row != -1:
            info_to_remove = self.info_table.row_data[self.selected_row]
            
            del self.info_table.row_data[self.selected_row]
            self.info_manager_controller.delete_info(
                self.restaurant, info_to_remove
        )

            self._clear_input_text_fields()
        else:
            popup = Popup(
                title="Invalid data",
                content=Label(text="Select any row to delete"),
                size_hint=(None, None),
                size=(400, 200),
        )
            popup.open()


    def _clear_input_text_fields(self):
        self.name_input.text = ""
        self.address_input.text = ""
        self.selected_row = -1

    def _is_data_valid(self, info_data):
        return(
            info_data[0] != "" 
            and info_data[1] != "" 
        )

class MenuManagerContentPanel:
    selected_row = -1  #kjo komande ben te mundur qe ne momentin e startimit te app, asnje komand nuk eshte e selektuar.
    restaurant_list = DataProvider().restaurant_list
    menu_manager_controller = MenuManagerController()

 
    def create_content_panel(self):
        split_layout_panel = GridLayout(cols=2)
        split_layout_panel.add_widget(self._create_menu_input_data_panel())
        split_layout_panel.add_widget(self._create_menu_management_panel())
        return split_layout_panel

    #Method to create the panel for restaurant data

    def _create_menu_input_data_panel(self):
        input_data_component_panel = GridLayout(cols=1, padding=30, spacing=20)
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = 400

        #Menu name
        self.name_input = MDTextField(mode = "rectangle", size_hint = (0.9, 0.1), hint_text='Menu name')
        input_data_component_panel.add_widget(self.name_input)
        self.menu_section_input = MDTextField(mode = "rectangle", size_hint = (0.9, 0.1), hint_text='Menu Section')
        input_data_component_panel.add_widget(self.menu_section_input)
       
        input_data_component_panel.add_widget(self._create_buttons_component_panel())
        return input_data_component_panel

    def _create_menu_management_panel(self):
        content_panel = GridLayout(cols=1, spacing=10)
        content_panel.add_widget(self._create_restaurant_selector())
        content_panel.size_hint_x = None
        content_panel.width = 1200
        content_panel.add_widget(self._create_table_panel())
        return content_panel

    def _create_buttons_component_panel(self):
        buttons_component_panel = GridLayout(cols=3, padding=0, spacing=10)
        add_button= Button(text='Add', size_hint=(None,None), size=(100, 40), background_color=(0,1,1,1))
        update_button = Button(text='Update', size_hint=(None,None), size=(100,40), background_color=(0,1,1,1))
        delete_button = Button(text='Delete', size_hint=(None,None), size=(100,40), background_color=(0,1,1,1))
        update_button.bind(on_press = self._update_menu)
        add_button.bind(on_press = self._add_menu)
        delete_button.bind(on_press = self._delete_menu)
        buttons_component_panel.add_widget(add_button)
        buttons_component_panel.add_widget(update_button)
        buttons_component_panel.add_widget(delete_button)
        return buttons_component_panel

    def _create_table_panel(self):
        table_panel = GridLayout(cols=1, padding=10, spacing=0)
        self.menu_table = self.create_table()
        table_panel.add_widget(self.menu_table)
        self.menu_table.bind(on_check_press = self._checked)
        self.menu_table.bind(on_row_press = self._on_row_press)

        return table_panel

    def _create_restaurant_selector(self):
        button = Button(text='Menu List', size_hint=(1, 0.1), background_color=(0,1,1,1))
        button.bind(on_release=self.show_menu)
        return button

    def create_table(self):
        table_row_data = []

        self.restaurant = self.restaurant_list[0]
        menus = self.restaurant.menu_list

        for menu in menus:
            table_row_data.append((menu.name, menu.menu_section))

        self.menu_table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y':0.5},
            check=True,
            use_pagination=True,
            rows_num= 10,
            column_data=[
                ("Name", dp(40)),
                ("Menu Section", dp(30))
            ],
            row_data = table_row_data
        )
        return self.menu_table


    def show_menu(self, button):
        menu_items=[]
        restaurant_list = self.restaurant_list

        for restaurant in restaurant_list:
            menu_items.append({"viewclass": "OneLineListItem", 
                               "text": restaurant.name,
                               "on_release": lambda r=restaurant: self._update_data_table(r),
                              }
                             )


        self.dropdown = MDDropdownMenu(
            caller=button,
            items = menu_items,
            width_mult=5,
            max_height=dp(150),
        )

        self.dropdown.open()

    def _checked(self, instance_table, current_row):
        selected_menu = Menu(current_row[0], current_row[1], [])
        self.name_input.text = str(selected_menu.name)
        self.menu_section_input.text = str(selected_menu.menu_section)


    def _on_row_press(self, instance, row):
        self.selected_row = int(row.index / len(instance.column_data))


    def _update_data_table(self, restaurant):
        self.restaurant = restaurant

        table_row_data = []
        menus = restaurant.menu_list
        for menu in menus:
            table_row_data.append(
                (menu.name, menu.menu_section)
            )

        self.menu_table.row_data = table_row_data


    def _add_menu(self, instance):
            
        name = self.name_input.text
        menu_section = self.menu_section_input.text

        menu_data = []
        menu_data.append(name)
        menu_data.append(menu_section)


        if self._is_data_valid(menu_data):
            self.menu_manager_controller.add_menu(
                self.restaurant, menu_data
            )

            self.menu_table.row_data.append((name, menu_section))
            self._clear_input_text_fields()
        else:
            popup = Popup(
                title = "Invalid data",
                content=Label(text="Provide mandatory data to add a new Menu"),
                size_hint = (None, None),
                size = (400, 200),
            )
            popup.open()

    def _update_menu(self, instance):
        if self.selected_row != -1:
            name = self.name_input.text
            menu_section = self.menu_section_input.text

            menu_data = []
            menu_data.append(name)
            menu_data.append(menu_section)

            if self._is_data_valid(menu_data):
                menu_to_remove = self.menu_table.row_data[self.selected_row]
            # Delete the existing employee data from the department
            del self.menu_table.row_data[self.selected_row]
            self.menu_manager_controller.delete_menu(
                self.restaurant, menu_to_remove
            )

            # Add the updated employee data to the department
            self.menu_manager_controller.add_menu(
                self.restaurant, menu_data
            )

            self.menu_table.row_data.append([name, menu_section])

            self._clear_input_text_fields()

        else:
            popup = Popup(
                title="Invalid data",
                content=Label(text="Provide mandatory data to update the Menu"),
                size_hint=(None, None),
                size=(400, 200),
            )
            popup.open()

    
    def _delete_menu(self, instance):
        if self.selected_row != -1:
            menu_to_remove = self.menu_table.row_data[self.selected_row]
            
            del self.menu_table.row_data[self.selected_row]
            self.menu_manager_controller.delete_menu(
                self.restaurant, menu_to_remove
        )

            self._clear_input_text_fields()
        else:
            popup = Popup(
                title="Invalid data",
                content=Label(text="Select any row to delete"),
                size_hint=(None, None),
                size=(400, 200),
        )
            popup.open()


    def _clear_input_text_fields(self):
        self.name_input.text = ""
        self.menu_section_input.text = ""
        self.selected_row = -1

    def _is_data_valid(self, menu_data):
        return(
            menu_data[0] != "" 
            and menu_data[1] != "" 
        )
    

class MenuItemManagerContentPanel:

    def __init__(self):
        self.menuitem_manager_controller = MenuItemManagerController()
        self.restaurant_list = DataProvider().restaurant_list
        self.restaurant = self.restaurant_list[0]
        self.menu = self.restaurant.menu_list[0]
        self.restaurant_selector = None
        self.menu_selector = None
        self.selected_menuitem = None
        self.selected_row = -1
        self.menu_database_manager = MenuDatabaseManager("python3n", "postgres", "573011", "localhost", 5432)


    def create_content_panel(self):
        split_layout_panel = GridLayout(cols=2)
        split_layout_panel.add_widget(self._create_menu_input_data_panel())
        split_layout_panel.add_widget(self._create_management_panel())
        return split_layout_panel

    def _create_menu_input_data_panel(self):
        input_data_component_panel = GridLayout(cols=1, padding=30, spacing=20)
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = 400
        self.name_input = MDTextField(multiline=True, font_size='18sp', hint_text='Name')
        input_data_component_panel.add_widget(self.name_input)
        self.description_input = MDTextField(multiline=False, font_size='18sp', hint_text='Description')
        input_data_component_panel.add_widget(self.description_input)
        input_data_component_panel.add_widget(self.create_food_input_data_panel())
        input_data_component_panel.add_widget(self._create_buttons_component_panel())
        return input_data_component_panel

    def create_food_input_data_panel(self):
        self.food_input_panel = GridLayout(cols=2, spacing=20)
        self.food_input_panel.size_hint = (None, None)
        food_options = ["Meal", "Drink"]

        for food in food_options:
            checkbox = CheckBox(group='food', active=False, color=(0, 0, 0, 1))
            checkbox_label = Label(text=food, color=(0, 0, 0, 1))
            self.food_input_panel.add_widget(checkbox)
            self.food_input_panel.add_widget(checkbox_label)
        return self.food_input_panel
    
    def _get_selected_food(self):
        for index, child in enumerate(self.food_input_panel.children):
            if isinstance(child, CheckBox) and child.active:
                label_index = index - 1 #shohim ne task priorty a ka femije dhe nese po a e kane checkboxun e selektuar
                if label_index < len(self.food_input_panel.children):
                    label = self.food_input_panel.children[label_index]
                    food_text = label.text.lower() #checks in all the priorty text in caps or not
                    return Food[food_text.upper()]
        return None
    
    def _create_management_panel(self):
        content_panel = GridLayout(cols=1, spacing=10)
        content_panel.size_hint_x = None
        content_panel.width = 800
        content_panel.add_widget(self._create_restaurant_selector())
        content_panel.add_widget(self._create_menu_selector())
        content_panel.add_widget(self.create_table(self.restaurant_list[0].menu_list[0]))
        return content_panel
    
    def _create_buttons_component_panel(self):
        buttons_component_panel = GridLayout(cols=3, padding=0, spacing=10)
        add_button = Button(text='Add', size_hint=(None, None), size=(100, 40), background_color=(0, 1, 1, 1))
        add_button.bind(on_release=self._add_menuitem)
        update_button = Button(text='Update', size_hint=(None, None), size=(100, 40), background_color=(0, 1, 1, 1))
        update_button.bind(on_release=self._update_menuitem)
        delete_button = Button(text='Delete', size_hint=(None, None), size=(100, 40), background_color=(0, 1, 1, 1))
        delete_button.bind(on_release=self._delete_menuitem)
        buttons_component_panel.add_widget(add_button)
        buttons_component_panel.add_widget(update_button)
        buttons_component_panel.add_widget(delete_button)

        return buttons_component_panel

    def _create_restaurant_selector(self):
        button = Button(text='Select a restaurant', size_hint=(1, 0.1), background_color=(0, 1, 1, 1)) #(1, 0.1) = 100 boshti x, 10% boshti y
        button.bind(on_release = self.show_menu)
        return button

    
    def show_menu(self, button):
        menu_items = []
        restaurant_list = self.restaurant_list
        for restaurant in restaurant_list:
            menu_items.append({"viewclass": "OneLineListItem", "text": restaurant.name,
                               "on_release": lambda r=restaurant:self._update_data_table(r)}) #update_menu_list

        self.dropdown = MDDropdownMenu(
            caller=button,
            items=menu_items,
            width_mult=5,
            max_height=dp(150),
        )

        self.dropdown.open()


    def _create_menu_selector(self):
       button = Button(text='Select a menu', size_hint=(1, 0.1), background_color=(0, 1, 1, 1))
       button.bind(on_release=self.show_menu_list)
       return button
    
    def show_menu_list(self, button):
        menu_items = []
        menu_list = self.restaurant.menu_list

        for menu in menu_list:
            menu_items.append({"viewclass": "OneLineListItem", "text": menu.name,
                               "on_release": lambda m=menu: self._update_data_table(m)})

        self.menu_selector = MDDropdownMenu(
            caller=button,
            items=menu_items,
            width_mult=5,
            max_height=dp(150),
        )

        self.menu_selector.open()


    def create_table(self, menu):
        table_row_data = []
        menuitem_list = menu.menuitem_list
       
        for menuitem in menuitem_list:
            table_row_data.append((menuitem.name, menuitem.description, menuitem.food.value))
        self.menuitem_table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            check=True,
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("Name", dp(40)),
                ("Description", dp(50)),
                ("Food", dp(40))
            ],
            row_data = table_row_data
        )
        
        self.menuitem_table.bind(on_check_press = self._checked)
        self.menuitem_table.bind(on_row_press = self._on_row_press)
        return self.menuitem_table
    
    def _checked(self, instance_table, current_row):
        self.selected_menuitem = MenuItem(
            current_row[0], current_row[1], Food[current_row[2]]
        )

        self.name_input.text = str(self.selected_menuitem.name)
        self.description_input.text= str(self.selected_menuitem.description)

        if self.selected_menuitem.food == Food.MEAL:
            print("Meal")
            self.food_input_panel.children[3].active = True #3 1 jane ceshtje indeksimi duke qene se kemi ne taask table shum indeksime te tjera dhe sduam te kemi te njejta

        elif self.selected_menuitem.food == Food.DRINK:
            self.food_input_panel.children[1].active = True

    def _on_row_press(self, instance, row):
        self.selected_row = int(row.index/len(instance.column_data))

    def _clear_input_text_fields(self):
        self.name_input.text = ""
        self.description_input.text = ""
        self.selected_row = -1

    def _is_data_valid(self, task_data):
        return (
            task_data[0] != ""
            and task_data[1] != ""
            and task_data[2] != ""
        )

    def _add_menuitem(self, instance):
        name = self.name_input.text
        description  = self.description_input.text
        food = self._get_selected_food()

        menuitem_data = [name, description, food]

        if self._is_data_valid(menuitem_data):
            self.menuitem_manager_controller.add_menuitem(self.menu, menuitem_data)

            self.menuitem_table.row_data.append([name, description, food.name])
            self._clear_input_text_fields()

        else:
            self._show_error_popup("Invalid data", " Provide mandatory data to add a new Menu item")

    def _update_menuitem(self, instance):
        if self.selected_row != -1: #rreshti i selektuar duhet te jete ne tab.

            name = self.name_input.text
            description = self.description_input.text
            food = self._get_selected_food()

            menuitem_data = [name, description, food]

            if self._is_data_valid(menuitem_data):
                menuitem_to_remove = self.menuitem_table.row_data[self.selected_row]

                del self.menuitem_table.row_data[self.selected_row]

                self.menuitem_manager_controller.update_menuitem(menuitem_to_remove[0], menuitem_data, self.menu)
                self.menuitem_table.row_data.append([name, description, food.name])

                self._clear_input_text_fields()
            else:
                self._show_error_popup("Invalid data", "Provide mandatory data to update the Menu Item")

        else:
            self._show_error_popup("Invalid data", "Select any row to update")

    def _delete_menuitem(self, instance):
        if self.selected_row != -1:
            menuitem_to_remove = self.menuitem_table.row_data[self.selected_row]

            del self.menuitem_table.row_data[self.selected_row]
            self.menuitem_manager_controller.delete_menuitem(self.menu, menuitem_to_remove[0])

            self._clear_input_text_fields()

        else:
            self._show_error_popup("Invalid data", "Select any row to delete")

    def _show_error_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200),
        )
        popup.open()

    def update_menu_list(self, restaurant):

        menu_items = []
        menus = restaurant.menu_list
        for menu in menus:
            menu_items.append({"viewclass": "OneLIneListItem", "text": menu.name,
                            "on_release": lambda m=menu: self.update_menuitem_table(m)})

        self.show_menu_list(None)
        self.menu_selector.items = menu_items
        self.menu_selector.dismiss
        self._update_data_table(menus[0])

    def _update_data_table(self, menu):
        self.menu = menu
        table_row_data = []
        menuitems = menu.menuitem_list 

        for menuitem in menuitems:
            table_row_data.append(
                (menuitem.name, menuitem.description, menuitem.food.value)
            )

        self.menuitem_table.row_data = table_row_data

class TableManagerContentPanel:

    selected_row = -1  #kjo komande ben te mundur qe ne momentin e startimit te app, asnje komand nuk eshte e selektuar.
    restaurant_list = DataProvider().restaurant_list
    table_manager_controller = TableManagerController()

 
    def create_content_panel(self):
        split_layout_panel = GridLayout(cols=2)
        split_layout_panel.add_widget(self._create_table_input_data_panel())
        split_layout_panel.add_widget(self._create_table_management_panel())
        return split_layout_panel

    #Method to create the panel for restaurant data

    def _create_table_input_data_panel(self):
        input_data_component_panel = GridLayout(cols=1, padding=30, spacing=20)
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = 400

        #Menu name
        self.id_input = MDTextField(mode = "rectangle", size_hint = (0.9, 0.1), hint_text='Table id')
        input_data_component_panel.add_widget(self.id_input)
        self.seats_input = MDTextField(mode = "rectangle", size_hint = (0.9, 0.1), hint_text='Table seats')
        input_data_component_panel.add_widget(self.seats_input)
       
        input_data_component_panel.add_widget(self._create_buttons_component_panel())
        return input_data_component_panel

    def _create_table_management_panel(self):
        content_panel = GridLayout(cols=1, spacing=10)
        content_panel.add_widget(self._create_restaurant_selector())
        content_panel.size_hint_x = None
        content_panel.width = 1200
        content_panel.add_widget(self._create_table_panel())
        return content_panel

    def _create_buttons_component_panel(self):
        buttons_component_panel = GridLayout(cols=3, padding=0, spacing=10)
        add_button= Button(text='Add', size_hint=(None,None), size=(100, 40), background_color=(0,1,1,1))
        update_button = Button(text='Update', size_hint=(None,None), size=(100,40), background_color=(0,1,1,1))
        delete_button = Button(text='Delete', size_hint=(None,None), size=(100,40), background_color=(0,1,1,1))
        update_button.bind(on_press = self._update_table)
        add_button.bind(on_press = self._add_table)
        delete_button.bind(on_press = self._delete_table)
        buttons_component_panel.add_widget(add_button)
        buttons_component_panel.add_widget(update_button)
        buttons_component_panel.add_widget(delete_button)
        return buttons_component_panel

    def _create_table_panel(self):
        table_panel = GridLayout(cols=1, padding=10, spacing=0)
        self.table_table = self.create_table()
        table_panel.add_widget(self.table_table)
        self.table_table.bind(on_check_press = self._checked)
        self.table_table.bind(on_row_press = self._on_row_press)

        return table_panel
    
    def _create_restaurant_selector(self):
        button = Button(text='Select a restaurant', size_hint=(1, 0.1), background_color=(0, 1, 1, 1)) #(1, 0.1) = 100 boshti x, 10% boshti y
        button.bind(on_release = self.show_restaurant_list)
        return button
    

    def _create_restaurant_selector(self):
        button = Button(text='Tables List', size_hint=(1, 0.1), background_color=(0,1,1,1))
        button.bind(on_release=self.show_table)
        return button

    def create_table(self):
        table_row_data = []

        self.restaurant = self.restaurant_list[0]
        tables = self.restaurant.table_list

        for table in tables:
            table_row_data.append((table.id, table.seats))

        self.table_table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y':0.5},
            check=True,
            use_pagination=True,
            rows_num= 10,
            column_data=[
                ("ID", dp(40)),
                ("Seats", dp(30))
            ],
            row_data = table_row_data
        )
        return self.table_table


    def show_table(self, button):
        table_items=[]
        restaurant_list = self.restaurant_list

        for restaurant in restaurant_list:
            table_items.append({"viewclass": "OneLineListItem", 
                               "text": restaurant.name,
                               "on_release": lambda r=restaurant: self._update_data_table(r),
                              }
                             )


        self.dropdown = MDDropdownMenu(
            caller=button,
            items = table_items,
            width_mult=5,
            max_height=dp(150),
        )

        self.dropdown.open()

    def _checked(self, instance_table, current_row):
        selected_table = Table(current_row[0], current_row[1])
        self.id_input.text = str(selected_table.id)
        self.seats_input.text = str(selected_table.seats)


    def _on_row_press(self, instance, row):
        self.selected_row = int(row.index / len(instance.column_data))


    def _update_data_table(self, restaurant):
        self.restaurant = restaurant

        table_row_data = []
        tables = restaurant.table_list
        for table in tables:
            table_row_data.append(
                (table.id, table.seats)
            )

        self.table_table.row_data = table_row_data


    def _add_table(self, instance):
            
        id = self.id_input.text
        seats = self.seats_input.text

        table_data = []
        table_data.append(id)
        table_data.append(seats)


        if self._is_data_valid(table_data):
            self.table_manager_controller.add_table(
                self.restaurant, table_data
            )

            self.table_table.row_data.append((id, seats))
            self._clear_input_text_fields()
        else:
            popup = Popup(
                title = "Invalid data",
                content=Label(text="Provide mandatory data to add a new Table Id"),
                size_hint = (None, None),
                size = (400, 200),
            )
            popup.open()

    def _update_table(self, instance):
        if self.selected_row != -1:
            id = self.id_input.text
            seats = self.seats_input.text

            table_data = []
            table_data.append(id)
            table_data.append(seats)

            if self._is_data_valid(table_data):
                table_to_remove = self.table_table.row_data[self.selected_row]
            # Delete the existing employee data from the department
            del self.table_table.row_data[self.selected_row]
            self.table_manager_controller.delete_table(
                self.restaurant, table_to_remove
            )

            # Add the updated employee data to the department
            self.table_manager_controller.add_table(
                self.restaurant, table_data
            )

            self.table_table.row_data.append([id, seats])

            self._clear_input_text_fields()

        else:
            popup = Popup(
                title="Invalid data",
                content=Label(text="Provide mandatory data to update the Table"),
                size_hint=(None, None),
                size=(400, 200),
            )
            popup.open()

    
    def _delete_table(self, instance):
        if self.selected_row != -1:
            table_to_remove = self.table_table.row_data[self.selected_row]
            
            del self.table_table.row_data[self.selected_row]
            self.table_manager_controller.delete_table(
                self.restaurant, table_to_remove
        )

            self._clear_input_text_fields()
        else:
            popup = Popup(
                title="Invalid data",
                content=Label(text="Select any row to delete"),
                size_hint=(None, None),
                size=(400, 200),
        )
            popup.open()


    def _clear_input_text_fields(self):
        self.id_input.text = ""
        self.seats_input.text = ""
        self.selected_row = -1

    def _is_data_valid(self, table_data):
        return(
            table_data[0] != "" 
            and table_data[1] != "" 
        )
