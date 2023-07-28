""" 
@Program: start_form
@Author: Donald Osgood
@Last Date: 2023-07-18 22:11:57
@Purpose:Donald Osgood
"""
import tkinter as tk
from framework import DandeForm, UIHelper, FormWindowType


class Form(DandeForm):
    """_summary_"""

    def __init__(
        self,
        parent,
        font_family,
        form_window_type=FormWindowType.FRAME,
        row=0,
        column=0,
        sticky="nsew",
        name="startForm",
        **kwargs
    ):
        super().__init__(
            parent,
            font_family=font_family,
            name=name,
            form_window_type=form_window_type,
            row=row,
            column=column,
            sticky=sticky,
            **kwargs
        )
     
        # create default label
        helper = UIHelper()
        headerlabel = helper.header_label(
            container=self, text="Welcome to Dandelion", font_family=font_family
        )
        headerlabel.grid(row=0, column=4, padx=10, pady=10)
        welcome_message = helper.default_label(container=self,text= "Hello welcome to Dandelion!\n The one stop cake ordering tool! \n From the menu you can choose place an order, or view current orders?\n ",font_family=font_family)
        welcome_message.grid(row=1, column=4, padx=10, pady=10)