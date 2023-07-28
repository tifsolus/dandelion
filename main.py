""" 
@Program: Tinkter GUI Temperature
@Author: Donald Osgood
@Last Date: 2023-07-11 18:46:51
@Purpose: A GUI interface to convert celsius to fahrenheit or F to C
"""
import sqlite3
import tkinter as tk
import os
import sys
from tktooltip import ToolTip
import yaml
from PIL import ImageTk, Image
from framework import FormsManager, MenuConfigItem, MenuManager


# function to open a new window
# on a button click

appWidth, appHeight = 800, 650
frameWidth, frameHeight = 800, 650
FONT_FAMILY = "Segoe UI"
BCKGRND_FONT_COLOR = "white"
H1 = 18


class Dict2Class(object):
    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])


class App(tk.Tk):
    """
    main program entry"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)       

        # self.eval('tk::PlaceWindow . center')
        file_path = os.path.join(sys.path[0], "config.yaml")
        file_object = open(file_path, "r")
        config_dict = yaml.load(file_object, Loader=yaml.SafeLoader)

        bg_photo = ImageTk.PhotoImage(Image.open("dandelion.jpg"))

        container = tk.Frame(self, height=frameHeight, width=frameWidth)

        main_canvas = tk.Canvas(self)
        main_canvas.grid(row=0, column=0, columnspan=12, sticky=tk.NSEW)
        main_canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        main_canvas.grid_columnconfigure(0, weight=1)
        main_canvas.grid_rowconfigure(0, weight=1)
        # create tool tips
        ToolTip(main_canvas, msg="Welcome to the app")
        container.grid(columnspan=12, sticky=tk.NSEW)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self._forms_manager = FormsManager(self, start_form="startform")
        self._menu_manager = MenuManager(
            parent=self,
            name="toolbar",
            oncommandhook=self._forms_manager.set_active_form,
        )

        def get_config_item_values(menu_config_item):
            return MenuConfigItem(**menu_config_item)

        def add_form(modulename, classname, container, formitemname):
            module = __import__(modulename)
            form_class = getattr(module, classname)

            self._forms_manager.add(
                form=form_class,
                parent=container,
                font_family=FONT_FAMILY,
                name=formitemname,
            )

        def add_menu_item(menutype, title, name, childforms):
            if menutype == "parent":
                self._menu_manager.add_item(
                    menutype=menutype, title=title, command="", children=childforms
                )
            elif menutype == "exit":
                self._menu_manager.add_item(
                    menutype=menutype,
                    title=title,
                    command=lambda: self.destroy(),
                    children=childforms,
                )
            else:
                self._menu_manager.add_item(
                    menutype=menutype,
                    title=title,
                    command=lambda: self._forms_manager.set_active_form(name),
                )

        for item in config_dict["forms"]:
            # convert to class
            # item_class = Dict2Class(item)

            item_values = get_config_item_values(item)

            if item_values.modulename:
                add_form(
                    modulename=item_values.modulename,
                    classname=item_values.classname,
                    container=container,
                    formitemname=item_values.formitemname,
                )

            if item_values.childitems:
                for child in item_values.childitems:
                    c_item_values = get_config_item_values(child)
                    add_form(
                        modulename=c_item_values.modulename,
                        classname=c_item_values.classname,
                        container=container,
                        formitemname=c_item_values.formitemname,
                    )

            add_menu_item(
                menutype=item_values.menutype,
                title=item_values.title,
                name=item_values.formitemname,
                childforms=item_values.childitems,
            )

        self._forms_manager.show_start_form()
        self.wm_title("Dandelion")
        self.geometry(f"{appWidth}x{appHeight}")
        self.resizable(width=True, height=True)
        self.maxsize(width=appWidth, height=appHeight)

        self.mainloop()

    def toggle_form(self, form_name):
        """_summary_

        Args:
            form_name (_type_): _description_
        """
        # always toggle the start_form to ensure its visible not visible
        self._forms_manager.toggle_form(form_name)


if __name__ == "__main__":
    App()
