#STEP 1 -Creating the App's login page.

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# Define the main screen
class Login(Screen):
    pass

# Define the secondary screen
class HomeScreen(Screen):
    pass

# Screen manager
class ScreenManagement(ScreenManager):
    pass

# Main app class
class RestaurantAppUpdate(MDApp):
    def build(self):
        return Builder.load_file('RestaurantAppUpdate.kv')

#if __name__ == "__main__": #It's a way for the script to "ask itself" if it is the main module being executed or if it's being used by another script as a module.
RestaurantAppUpdate().run()
