""" 
@Program: order_form
@Author: Donald Osgood
@Last Date: 2023-07-18 22:11:57
@Purpose:Donald Osgood
"""
import sqlite3
import tkinter as tk
from tkinter.ttk import Treeview
from framework import DandeForm, UIHelper, FormWindowType


class Form(DandeForm):
    """_summary_"""

    conn = sqlite3.connect("dandelion.db")
    cur = conn.cursor()
    form_rows = []

    def get_data():
        """_summary_"""
        Form.cur.execute("SELECT * FROM transactions")

    def populate_view(tree: Treeview):
        """_summary_
        Args:
            tree (_type_): _description_
        """
        # tree.delete(tree.get_children())
        Form.cur.execute("SELECT * FROM `transactions` ORDER BY `name` ASC")
        fetch = Form.cur.fetchall()
        for data in fetch:
            tree.insert("", "end", values=(data[0],data[1], data[2], data[3],data[4],data[5],data[6],data[7],data[8]))
        Form.cur.close()
        Form.conn.close()

    def __init__(
        self,
        parent,
        font_family,
        form_window_type=FormWindowType.FRAME,
        row=0,
        column=0,
        sticky="nsew",
        name="orderForm",
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

        ui_helper = self.ui_helper
        headerlabel = ui_helper.header_label(
            container=self, text="Your Orders", font_family=font_family
        )
        headerlabel.grid(row=0, column=4, padx=10, pady=10)
        
        tv = Treeview(self, show='headings')
        tv["columns"] = ("id","name", "address", "city","state","telephone","base","layers","size")
        tv.heading("id", text="Order#", anchor="w")
        tv.column("id", anchor="w", width=55)
        tv.heading("name", text="Name")
        tv.column("name", anchor="center", width=70)
        tv.heading("address", text="Address")
        tv.column("address", anchor="center", width=70)
        tv.heading("city", text="City")
        tv.column("city", anchor="center", width=55)
        tv.heading("state", text="State")
        tv.column("state", anchor="center", width=55)
        tv.heading("telephone", text="Tele")
        tv.column("telephone", anchor="center", width=55)
        tv.heading("base", text="Base")
        tv.column("base", anchor="center", width=55)
        tv.heading("layers", text="Layers")
        tv.column("layers", anchor="center", width=25)
        tv.heading("size", text="Size")
        tv.column("size", anchor="center", width=55)
        tv.grid(
            row=1,
            column=1,
            padx=10,
            pady=10,
            sticky=(tk.N, tk.S, tk.W, tk.E),
            columnspan=8,
        )
        self.treeview = tv
        Form.populate_view(tv)
        # Refresh Button
        refresh_button = tk.Button(self, text="Refersh")
        refresh_button.grid(
            row=2, column=1, columnspan=2, padx=20, pady=20, sticky="ew"
        )
