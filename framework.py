""" 
@Program: framework
@Author: Donald Osgood
@Last Date: 2023-07-18 22:13:40
@Purpose:Donald Osgood
"""
import importlib
import tkinter as tk
from enum import Enum

from tktooltip import ToolTip


class MenuConfigItem:
    """_summary_"""

    def __init__(
        self,
        formitemname,
        modulename,
        classname,
        menutype,
        childitems,
        commandfunc,
        title="Complete Setup",
    ):
        self.formitemname = formitemname
        self.title = title
        self.modulename = modulename
        self.classname = classname
        self.menutype = menutype
        self.childitems = childitems
        self.commandfunc = commandfunc


class FormWindowType(Enum):
    """_summary_

    Args:
        Enum (_type_): _description_
    """

    FRAME = "frame"
    WINDOW = "window"


class DandeForm(tk.Frame):
    """_summary_

    Args:
        tk (_type_): _description_
    """

    def __init__(
        self,
        parent,
        font_family,
        name,
        form_window_type=FormWindowType.FRAME,
        row=0,
        column=0,
        sticky="nsew",
        **kwargs,
    ):
        super().__init__(parent, name=name, **kwargs)
        self.parent = parent
        self.font_family = font_family
        self.form_window_type = form_window_type
        self.row = row
        self.column = column
        self.sticky = sticky
        self.ui_helper = UIHelper(parent=parent.master)

    def show(self):
        """_summary_"""
        self.grid(row=self.row, column=self.column, sticky=self.sticky)

    def close(self):
        """_summary_"""
        self.grid_forget()


class MenuManager(tk.Menu):
    """_summary_

    Args:
        tk (_type_): _description_
    """

    def __init__(
        self,
        parent,
        name="menu",
        start_menu="",
        menus=[],
        oncommandhook="",
        **kwargs,
    ):
        super().__init__(parent, name=name, **kwargs)
        self.oncommandhook = oncommandhook
        # self.grid(row=row, column=column, sticky=sticky)
        if start_menu:
            # menu = tk.Menu(self, tearoff=0)
            self.add_command(start_menu)
            self.add_separator()
        if menus:
            for menu in menus:
                print(menu)
        parent["menu"] = self
        # parent.config(menu=self)

    def _add_item(self, menu="", menutype="", title="", command="", children=[]):
        # build menus
        if not (menu):
            menu = self
        if menutype == "topform":
            menu.add_command(label=title, command=command)
        elif menutype == "exit":
            menu.add_command(label=title, command=command)
        elif menutype == "startform":
            return menu.add_command(label=title, command=command)
        elif menutype == "parent":
            top_menu_item = tk.Menu(menu)
            menu.add_cascade(label=title, menu=top_menu_item)
            for child in children:
                (
                    formitemname,
                    title,
                    modulename,
                    classname,
                    menutype,
                    childitems,
                    commandfunc,
                ) = child.values()
                self._add_item(
                    menu=top_menu_item,
                    menutype=menutype,
                    title=title,
                    command=lambda: self.oncommandhook(formitemname),
                    children=childitems,
                )

    def add_item(self, menutype, title, command, children=[]):
        """_summary_

        Args:
            type (_type_): _description_
            title (_type_): _description_
            command (_type_): _description_
        """
        self._add_item(
            menutype=menutype, title=title, command=command, children=children
        )

    def add_command_item(self, label, command):
        """_summary_

        Args:
            label (_type_): _description_
            command (_type_): _description_
        """
        self.add_command(label=label, command=command)


class FormsManager:
    """_summary_"""

    def __init__(self, top, start_form="", *args, **kwargs):
        self.forms = {}
        self.top = top
        self.active_form = ""
        self.start_form = start_form

    def add(self, form: DandeForm, parent, font_family, name, at_row=0, at_col=0):
        """_summary_

        Args:
            form (DandeForm): _description_
            parent (_type_): _description_
            font_family (_type_): _description_
        """
        _form = form(parent, font_family, name=name, row=at_row, column=at_col)
        self.forms.update(
            {f"{_form._name}": {"parent": parent._name, "visible": False}}
        )

    def get_container(self, container_name):
        """_summary_

        Args:
            container_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.top.nametowidget(name=container_name)

    def get_form_attrs(self, form_name):
        """_summary_

        Args:
            form_name (_type_): _description_
        """
        return self.forms[form_name]

    def get_form(self, form_name):
        """_summary_

        Args:
            form_name (_type_): _description_
        """
        parent_name = self.get_form_attrs(form_name)["parent"]
        parent_form = self.get_container(container_name=parent_name)
        return parent_form.nametowidget(form_name)

    def is_form_visible(self, form_name):
        """_summary_

        Args:
            form_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.get_form_attrs(form_name)["visible"]

    def get_active_form(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.get_form(self.active_form)

    def get_start_form(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.get_form(self.start_form)

    def set_active_form(self, form_name):
        """_summary_

        Args:
            form_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        form = self.get_form(form_name)
        if not (self.active_form == form_name):
            self.close_active_form()
            self.active_form = form_name
            form.show()
            return 1
        else:
            return 0

    def toggle_form(self, form_name):
        """_summary_

        Args:
            form (_type_): _description_
        """
        form = self.get_form(form_name)
        if self.active_form == form_name or form.grid_info():
            self.active_form = ""
            form.close()
            if self.start_form:
                self.show_start_form()
            return 0
        else:
            self.close_active_form()
            self.active_form = form_name
            form.show()
            return 1

    def close_active_form(self):
        """_summary_"""
        if self.active_form:
            self.get_active_form().close()

    def show_start_form(self):
        """_summary_"""
        self.active_form = self.start_form
        self.close_active_form()
        self.get_active_form().show()


class UsStateSpinBox(tk.Spinbox):
    """
    Spinbox for displaying a list of state values
    Args:
        tk (_type_): inherits spinbox class
    """

    def __init__(
        self,
        parent,      
        tooltip_msg,
        validate_key="key",
        validate_command="",
        **kwargs,
    ):
        super().__init__(master=parent, **kwargs)
        pacakge_with_locales_module = importlib.import_module("data.locales_us")
        # print(pacakge_with_locales_module.states)
        locales = getattr(pacakge_with_locales_module, "Locales")
        self._parent = parent
        locale_states = locales().get_states(doreverse=False)
        self.config(values=locale_states)
        ToolTip(self, msg=tooltip_msg)

        def validate_base(d, i, P, s, S, v, V, W):
            result = P
            entry = self
            # input_data = entry.get()
            if result not in locale_states:
                # entry.config(foreground="red")
                return False
            else:
                entry.config(
                    foreground="green",
                )
                return True

        if not (validate_command):
            validate_cb = (
                parent.ui_helper.register_call_back(validate_base),
                "%d",
                "%i",
                "%P",
                "%s",
                "%S",
                "%v",
                "%V",
                "%W",
            )
            self.config(validate=validate_key, validatecommand=validate_cb)


class UIHelper:
    """_summary_"""

    _font_family = "Segoe UI"
    _default_weight = "normal"
    _default_label_size = 12
    _h_1 = 18

    def __init__(
        self,
        font_family=_font_family,
        weight=_default_weight,
        default_label_size=_default_label_size,
        h_1=_h_1,
        parent="",
        *args,
        **kwargs,
    ):
        _font_family = font_family
        _default_weight = weight
        _default_label_size = default_label_size
        _h_1 = h_1
        self._parent = parent

    def create_state_spin_box(
        self,
        container,      
        tooltip_msg,
        validate_key="key",
        validate_command="",
    ):
        """_summary_

        Returns:
            _type_: _description_
        """
        return UsStateSpinBox(
            parent=container,            
            tooltip_msg=tooltip_msg,
            validate_key=validate_key,
            validate_command=validate_command,
        )

    def string_var(self, container):
        """_summary_

        Returns:
            _type_: _description_
        """
        return tk.StringVar(master=container).get()

    def entry(self, container):
        """_summary_

        Args:
            textvariable (_type_): _description_

        Returns:
            _type_: _description_
        """
        return tk.Entry(master=container)

    def default_label(
        self,
        container,
        text,
        font_family=_font_family,
        size=_default_label_size,
        weight=_default_weight,
    ):
        """
        Creates a default label

        Args:
            container (frame): frame for element to be added to
            text (string): label text

        Returns:
            label: return the label
        """
        label = tk.Label(container, text=text, font=(font_family, size, weight))
        return label

    def header_label(
        self, container, text, font_family=_font_family, size=_h_1, weight="bold"
    ):
        """
        Creates a H1 header

        Args:
            container (frame): frame for element to be added to
            text (string): label text

        Returns:
            label: return the label
        """
        return tk.Label(container, text=text, font=(font_family, size, weight))

    def get_result_value(self, field):
        """get result value"""
        return field.get()

    def set_result_value(self, field, value):
        """get result value"""
        field["text"] = value

    def register_call_back(self, call_back):
        _call_back = self._parent.register(call_back)
        return _call_back

    def attach_window(self, parent, title, child_form):
        """_summary_

        Args:
            parent (_type_): _description_
            title (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Toplevel object which will
        # be treated as a new window
        new_window = tk.Toplevel(parent)

        # sets the title of the
        # Toplevel widget
        new_window.title(f'{title}')

        # sets the geometry of toplevel
        new_window.geometry("650x500")
        form = importlib.import_module(child_form)
        confirmation_form = form.Form(parent=new_window, font_family=self._font_family)
        confirmation_form.grid()
        new_window.wm_transient(parent)
        new_window.wm_focusmodel(model="active")
        
        parent.eval('tk::PlaceWindow . center')

        return new_window
