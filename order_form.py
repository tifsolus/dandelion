""" 
@Program: order_form
@Author: Donald Osgood
@Last Date: 2023-07-18 22:11:57
@Purpose:Donald Osgood
"""


import sqlite3
import tkinter as tk
from tkinter import END, font, Spinbox
from tkinter import messagebox

# from tkinter.ttk import Spinbox
from PIL import ImageTk, Image
from tktooltip import ToolTip
from framework import DandeForm, FormWindowType


class Form(DandeForm):
    """_summary_"""

    # move all this to datalayer ran out of time for project
    # Make Connection to a Database
    conn = sqlite3.connect("dandelion.db")
    cur = conn.cursor()

    # Create a Table
    def create_table():
        """_summary_"""
        Form.cur.execute(
            "CREATE TABLE IF NOT EXISTS transactions(id INTEGER,name TEXT,address TEXT,city TEXT, state TEXT, tele TEXT, base TEXT, layers Text, size TEXT)"
        )
        Form.conn.commit()

    # Create an Auto Increment for ID

    def auto_increment():
        """_summary_

        Returns:
            _type_: _description_
        """
        Form.cur.execute("SELECT COUNT(*) FROM transactions")
        return int(Form.cur.fetchone()[0]) + 1

    # Create Function to Insert Data
    def insert_data(name, address, city, state, tele, base, layers, size):
        """_summary_

        Args:
            name (_type_): _description_
            address (_type_): _description_
            city (_type_): _description_
            state (_type_): _description_
            tele (_type_): _description_
            base (_type_): _description_
            layers (_type_): _description_
            size (_type_): _description_
        """
        id = Form.auto_increment()
        Form.cur.execute(
            "INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?,?)",
            (id, name, address, city, state, tele, base, layers, size),
        )
        Form.conn.commit()
        print("---------------------------------------------")
        print("Data have successfully inserted........")
        print("---------------------------------------------")

    def __init__(
        self,
        parent,
        font_family,
        form_window_type=FormWindowType.FRAME,
        row=0,
        column=0,
        sticky="nsew",
        name="orderForm",
        **kwargs,
    ):
        super().__init__(
            parent,
            font_family=font_family,
            name=name,
            form_window_type=form_window_type,
            row=row,
            column=column,
            sticky=sticky,
            **kwargs,
        )

        # # determine wrapper
        # if form_window_type == FormWindowType:
        #     UIHelper().attach_window(parent=parent, title="Place and Order")
        # create default label
        Form.create_table()
        ui_helper = self.ui_helper
        _messagebox = messagebox

        def clear_form():
            clear_text(name_entry)
            clear_text(address_entry)
            clear_text(city_entry)
            clear_text(state_entry)
            clear_text(phone_entry)
            clear_text(size_entry)
            clear_text(base_entry)
            clear_text(layers_entry)

        def clear_text(field, reset_value=""):
            field.delete(0, END)

        # validation funcs
        def validate_default_str(d, i, P, s, S, v, V, W):
            entry = self.parent.nametowidget(W)
            try:
                if not (P):
                    entry.config(background="#FFFF00")
                    return True
                if not (P.isalpha()) and not (P == ""):
                    _messagebox.showerror(message="Only Alpha Allowed")
                    entry.config(
                        "background="  # FFFF00",                                           ,
                    )
                    return False
                else:
                    entry.config(background="greenyellow")
                    return True
            except:
                print("An exception occur#FFFF00")

        def validate_shift(d, i, P, s, S, v, V, W):
            result = P
            entry = self.parent.nametowidget(W)
            if not (result):
                entry.config(background="#FFFF00")
                return True
            # input_data = entry.get()
            if result not in ["S", "M", "L"]:
                entry.config(background="#FFFF00")
                return False
            else:
                entry.config(
                    background="greenyellow",
                )
                return True

        def validate_layers(d, i, P, s, S, v, V, W):
            try:
                entry = self.parent.nametowidget(W)
                if not (P):
                    entry.config(entry.config(background="#FFFF00"))
                    return True
                if P.isalpha():
                    entry.config(entry.config(background="#FFFF00"))
                    return False
                result = int(P)
                if result not in (range(1, 10)):
                    entry.config(background="#FFFF00")
                    return False
                else:
                    entry.config(entry.config(background="greenyellow"))
                    return True
            except:
                print("An exception occur#FFFF00")
                entry.config(entry.config(background="#FFFF00"))
                return False

        def validate_base(d, i, P, s, S, v, V, W):
            try:
                entry = self.parent.nametowidget(W)
                if not (P):
                    entry.config(entry.config(background="#FFFF00"))
                    return True
                if P not in ["Vanilla", "Chocolate", "Almond"]:
                    entry.config(background="#FFFF00")
                    return False
                else:
                    entry.config(background="greenyellow")
                    return True
            except:
                entry.config(entry.config(background="#FFFF00"))
                return False

        # callbacks
        validate_shift_cb = (
            ui_helper.register_call_back(validate_shift),
            "%d",
            "%i",
            "%P",
            "%s",
            "%S",
            "%v",
            "%V",
            "%W",
        )
        validate_layers_cb = (
            ui_helper.register_call_back(validate_layers),
            "%d",
            "%i",
            "%P",
            "%s",
            "%S",
            "%v",
            "%V",
            "%W",
        )
        validate_base_cb = (
            ui_helper.register_call_back(validate_base),
            "%d",
            "%i",
            "%P",
            "%s",
            "%S",
            "%v",
            "%V",
            "%W",
        )
        validate_default_str_cb = (
            ui_helper.register_call_back(validate_default_str),
            "%d",
            "%i",
            "%P",
            "%s",
            "%S",
            "%v",
            "%V",
            "%W",
        )

        header_label = ui_helper.header_label(
            container=self, text="Place your cake order", font_family=font_family
        )
        header_label.grid(row=0, column=1, padx=10, pady=10, columnspan=12)
        # Text for our form
        contact_label = ui_helper.header_label(
            container=self, text="Contact Details:", size=14
        )
        contact_label.grid(row=2, column=1, padx=10, pady=10, columnspan=1)

        name = ui_helper.default_label(container=self, text="Name:")
        phone = ui_helper.default_label(container=self, text="Phone:")
        address = ui_helper.default_label(container=self, text="Address:")
        city = ui_helper.default_label(container=self, text="City:")
        state = ui_helper.default_label(container=self, text="State:")

        # Pack text for our form
        name.grid(row=3, padx=10, column=1, sticky="nw")
        phone.grid(row=4, padx=10, column=1, sticky="nw")
        address.grid(row=5, padx=10, column=1, sticky="nw")
        city.grid(row=6, padx=10, column=1, sticky="nw")
        state.grid(row=7, padx=10, column=1, sticky="nw")

        # Tkinter variable for storing entries

        # Entries for our form

        name_entry = ui_helper.entry(container=self)
        name_entry.config(validate="key", validatecommand=validate_default_str_cb)
        ToolTip(name_entry, msg="Enter Client Name")
        phone_entry = ui_helper.entry(container=self)
        ToolTip(phone_entry, msg="Enter Phone Number")
        address_entry = ui_helper.entry(container=self)
        ToolTip(name_entry, msg="Enter Client Name")
        city_entry = ui_helper.entry(container=self)
        ToolTip(city_entry, msg="Enter Client City")
        state_entry = ui_helper.create_state_spin_box(
            container=self,
            tooltip_msg="Enter Client State",
            validate_key="key",
            validate_command="",
        )
        # state_entry = ui_helper.entry(container=self, textvariable=state_value)
        # ToolTip(state_entry, msg="Enter Client State")

        # # Packing the Entries
        name_entry.grid(row=3, padx=10, column=2)

        phone_entry.grid(row=4, padx=10, column=2)
        address_entry.grid(row=5, padx=10, column=2)
        city_entry.grid(row=6, padx=10, column=2)
        state_entry.grid(row=7, padx=10, column=2)

        details_label = ui_helper.header_label(
            container=self, text="Order Details:", size=14
        )
        details_label.grid(row=2, column=3, padx=10, pady=10, columnspan=1)

        size = ui_helper.default_label(container=self, text="Size(S,M,L):")
        layers = ui_helper.default_label(container=self, text="Layers:(1-10)")
        base = ui_helper.default_label(container=self, text="Base:(Vanilla,Chocolate)")
        # Pack text for our form
        size.grid(row=3, column=3, padx=10, sticky="nw")
        layers.grid(row=4, column=3, padx=10, sticky="nw")
        base.grid(row=5, column=3, padx=10, sticky="nw")

        # Entries for our form
        size_entry = Spinbox(self, values=("S", "M", "L"))
        size_entry.config(validate="key", validatecommand=validate_shift_cb)
        ToolTip(size_entry, msg="Enter Cake Size")

        layers_entry = Spinbox(self, from_=1, to=10)
        layers_entry.config(validate="key", validatecommand=validate_layers_cb)
        ToolTip(layers_entry, msg="Enter layers")

        base_entry = Spinbox(self, values=("Vanilla", "Chocolate", "Almond"))
        base_entry.config(validate="key", validatecommand=validate_base_cb)
        ToolTip(base_entry, msg="Enter Cake Base")

        # # Packing the Entries
        size_entry.grid(row=3, padx=10, column=4)
        layers_entry.grid(row=4, padx=10, column=4)
        base_entry.grid(row=5, padx=10, column=4)

        clear_form()

        # Generate Button
        bg_image = Image.open("order.png")
        bg_photo = ImageTk.PhotoImage(bg_image)

        my_font = font.Font(family=font_family)

        def validate_form():
            valid = True
            try:
                for entry in (name_entry, phone_entry, layers_entry):
                    if entry.get() == "":
                        valid = False
            except:
                valid = False

            if valid:
                # save data
                valid = True
                try:
                    Form.insert_data(
                        name_entry.get(),
                        address_entry.get(),
                        city_entry.get(),
                        state_entry.get(),
                        phone_entry.get(),
                        base_entry.get(),
                        layers_entry.get(),
                        size_entry.get(),
                    )
                    clear_form()
                    ui_helper.attach_window(
                        parent=self.parent.master,
                        title="Confirmation Page",
                        child_form="confirmation_form",
                    )
                except:
                    valid = False
                    _messagebox.showerror(
                        message="Data not saved, error occured! Please contact support at helpme@neverwewillnot.com"
                    )
                    print("An exception occurred")
            else:
                _messagebox.showerror(
                    message="Default fields not populated or properly populated"
                )

        order_button = tk.Button(
            self,
            compound="left",
            font=my_font,
            text="Place Order",
            image=bg_photo,
            background="yellow",
            command=validate_form,
        )

        order_button.image = bg_photo
        order_button.grid(row=12, column=3, padx=20, pady=20, sticky="nw", columnspan=1)
        # Generate Button
        bg_image_clear = Image.open("clear.png")
        bg_photo_clear = ImageTk.PhotoImage(bg_image_clear)

        clear_button = tk.Button(
            self,
            compound="left",
            font=my_font,
            text="Clear",
            image=bg_photo_clear,
            background="yellow",
            command=lambda: clear_form(),
        )
        clear_button.image = bg_photo_clear
        clear_button.grid(row=12, column=4, padx=20, pady=20, sticky="nw", columnspan=1)
