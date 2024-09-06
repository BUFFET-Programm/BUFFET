from kivymd.app import MDApp
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.backdrop.backdrop import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dialog import MDDialog
from b_buyer_log import read_logs, delete_log
from b_manage_buyers import read_all_buyers_name
from b_manage_users import current_user_name, user_type
from f_components import MDPersianLabel, MDFlatButton
from important_variables import FONT_PATH
from bidi.algorithm import get_display
from arabic_reshaper import reshape

filter = []
date_filter = []
value_filter = []
type_filter = None
name_filter = None

KV = """
<TotalLog>:
    MDBoxLayout:
        orientation: "vertical"
        MDBoxLayout:
            orientation: "horizontal"
            size_hint: 1, .1
            MDRectangleFlatIconButton:
                button_text: app.language_dialogs["exit"]
                icon: "location-exit"
                on_release: root.manager.current = "statistics"
            MDLabel:
                size_hint: 1, 1
            MDRectangleFlatIconButton:
                button_text: app.language_dialogs["filter"]
                icon: "filter-outline"
                on_release: root.manager.current = "total_log_filter"
            MDLabel:
                size_hint: 1, 1
            MDRectangleFlatIconButton:
                button_text: app.language_dialogs["delete"]
                icon: "delete"
                on_release: root.delete_log()
        MDBoxLayout:
            size_hint_y: .2
            MDPersianLabel:
                label_text: app.language_dialogs["name"]
                size_hint: .1, .2
                font_size: 30
            MDPersianLabel:
                label_text: app.language_dialogs["operation"]
                size_hint: .1, .2
                font_size: 30
            MDPersianLabel:
                label_text: app.language_dialogs["price"]
                size_hint: .1, .2
                font_size: 30
            MDPersianLabel:
                label_text: app.language_dialogs["date"]
                size_hint: .2, .2
                font_size: 30
            MDPersianLabel:
                label_text: app.language_dialogs["products"]
                size_hint: .2, .2
                font_size: 30
        MDBoxLayout:
            orientation: "horizontal"
            MDBoxLayout:
                id: log_name
                orientation: "vertical"
            MDBoxLayout:
                id: log_type
                orientation: "vertical"
            MDBoxLayout:
                id: log_value
                orientation: "vertical"
            MDBoxLayout:
                id: log_date
                size_hint: 2, 1
                orientation: "vertical"
            MDBoxLayout:
                id: log_products
                size_hint: 2, 1
                orientation: "vertical"
        MDBoxLayout:
            orientation: "horizontal"
            size_hint: 1, .1
            MDIconButton:
                icon: "arrow-down"
                on_release: root.scroll_down()
            MDIconButton:
                icon: "arrow-up"
                on_release: root.scroll_up()

<TotalLogFilter>:
    MDFloatLayout:
        MDCheckbox:
            id: check_date
            size_hint: .1, .1
            pos_hint: {'x': .9, 'y': .85}
        MDLabel:
            text: app.persian(app.language_dialogs["date"])
            font_name: app.FONT_PATH
            size_hint: .1, .1
            pos_hint: {'x': .85, 'y': .85}
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["select_date_from"]
            icon: "calendar"
            size_hint: .2, .1
            pos_hint: {'x': .6, 'y': .8}
            on_release: root.set_date_filter()
        MDLabel:
            id: from_date
            size_hint: .2, .1
            pos_hint: {'x': .6, 'y': .7}
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["select_date_to"]
            icon: "calendar"
            size_hint: .2, .1
            pos_hint: {'x': .35, 'y': .8}
            on_release: root.set_date_filter("to")
        MDLabel:
            id: to_date
            size_hint: .2, .1
            pos_hint: {'x': .35, 'y': .7}
        MDCheckbox:
            id: check_type
            on_active: root.set_type_filter(self.active)
            size_hint: .1, .1
            pos_hint: {'x': .9, 'y': .65}
        MDPersianLabel:
            label_text: app.language_dialogs["operation"]
            size_hint: .15, .1
            pos_hint: {'x': .78, 'y': .65}
        MDCheckbox:
            group: "type"
            id: is_buy
            on_active: root.set_type_filter(root.ids.check_type.active)
            size_hint: .1, .1
            pos_hint: {'x': .6, 'y': .6}
        MDCheckbox:
            group: "type"
            id: is_charge
            on_active: root.set_type_filter(root.ids.check_type.active)
            size_hint: .1, .1
            pos_hint: {'x': .3, 'y': .6}
        MDPersianLabel:
            label_text: app.language_dialogs["buy"]
            size_hint: .1, .1
            pos_hint: {'x': .55, 'y': .6}
        MDPersianLabel:
            label_text: app.language_dialogs["charge"]
            size_hint: .1, .1
            pos_hint: {'x': .25, 'y': .6}
        MDCheckbox:
            id: check_value
            size_hint: .1, .1
            pos_hint: {'x': .9, 'y': .45}
        MDPersianLabel:
            label_text: app.language_dialogs["price_log"]
            size_hint: .15, .1
            pos_hint: {'x': .78, 'y': .45}
        MDTextField:
            id: value_from
            font_size: 35
            input_filter: "int"
            size_hint: .3, .1
            pos_hint: {'x': .44, 'y': .4}
        MDTextField:
            id: value_to
            font_size: 35
            input_filter: "int"
            size_hint: .3, .1
            pos_hint: {'x': .04, 'y': .4}
        MDPersianLabel:
            label_text: app.language_dialogs["from"]
            size_hint: .1, .1
            pos_hint: {'x': .7, 'y': .4}
        MDPersianLabel:
            label_text: app.language_dialogs["to"]
            size_hint: .1, .1
            pos_hint: {'x': .3, 'y': .4}
        MDCheckbox:
            id: check_name
            size_hint: .1, .1
            pos_hint: {'x': .9, 'y': .25}
        MDPersianLabel:
            label_text: app.language_dialogs["name"]
            size_hint: .15, .1
            pos_hint: {'x': .78, 'y': .25}
        MDBoxLayout:
            id: names
            size_hint: .3, .25
            pos_hint: {'x': .05, 'y': .15}
        MDPersianLabel:
            id: name_label
            size_hint: .3, .1
            pos_hint: {'x': .4, 'y': .15}
        MDTextFieldPersian:
            mode: "round"
            id: search_buyers
            pos_hint: {"x": .29,"y": .25}
            size_hint: .2, .075
            on_text: root.search_in_buyers(self.str)
            font_size: 30
            halign: "center"
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["cancel"]
            icon: "cancel"
            on_release: root.cancel()
            size_hint: .2, .1
            pos_hint: {'x': .25, 'y': .05}
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["done"]
            icon: "filter"
            on_release: root.set_filter()
            size_hint: .2, .1
            pos_hint: {'x': .05, 'y': .05}
"""


class TotalLog(MDScreen):
    first_item_index = 0
    items = []

    def delete_log(self):
        global filter, date_filter, type_filter, value_filter, name_filter
        if user_type(current_user_name()) == "creator":
            delete_log(self.items)
            filter = []
            date_filter = []
            value_filter = []
            type_filter = None
            name_filter = None
            self.on_enter()
        else:
            persian_text = MDApp.get_running_app(
            ).language_dialogs["only_manager"]
            text = "[font={}]{}[/font]".format(FONT_PATH,
                                               get_display(reshape(persian_text)))
            self.dialog = MDDialog(
                title=text,
                buttons=[
                    MDFlatButton(
                        text=get_display(
                            reshape(
                                MDApp.get_running_app(
                                ).language_dialogs["i_got_it"]
                            )
                        ),
                        font_name=FONT_PATH,
                        on_release=lambda instance: self.dialog.dismiss()
                    )
                ]
            )
            self.dialog.open()

    def scroll_up(self):
        self.first_item_index -= 5
        self.update()

    def scroll_down(self):
        self.first_item_index += 5
        self.update()

    def on_enter(self):
        global filter, date_filter, type_filter, value_filter, name_filter
        self.first_item_index = 0
        try:
            self.items = read_logs(by="all")
            for filter_item in filter:
                if filter_item == "operation":
                    self.items = read_logs(
                        by=filter_item, logs=self.items, operation={"c": "charge", "b": "buy"}[type_filter])

                elif filter_item == "price":
                    self.items = read_logs(
                        by=filter_item, logs=self.items, start_price=value_filter[0], end_price=value_filter[1])

                elif filter_item == "date":
                    self.items = read_logs(
                        by=filter_item, logs=self.items, start_date=date_filter[0], end_date=date_filter[1])

                elif filter_item == "name":
                    self.items = read_logs(
                        by=filter_item, logs=self.items, name=name_filter)
            self.update()
        except:
            self.items = read_logs(by="all")
            self.update()

    def update(self):
        if self.first_item_index < 0:
            self.first_item_index = 0
        self.ids.log_value.clear_widgets()
        self.ids.log_type.clear_widgets()
        self.ids.log_date.clear_widgets()
        self.ids.log_products.clear_widgets()
        self.ids.log_name.clear_widgets()
        products_str = ""
        for item in self.items[self.first_item_index:self.first_item_index + 5]:
            try:
                for product in eval(item[4]):
                    products_str += product + " - "
                products_str = products_str[:-3]
            except:
                pass
            products_str = "------" if products_str == "" else products_str
            self.ids.log_products.add_widget(MDPersianLabel(
                label_text=products_str, size_hint=(1, 1)))
            products_str = ""
            self.ids.log_value.add_widget(
                MDLabel(text=str(item[2]), size_hint=(1, 1), halign="center"))
            self.ids.log_type.add_widget(MDPersianLabel(
                label_text=MDApp.get_running_app().language_dialogs["buy_or_charge"][item[1]], size_hint=(1, 1)))
            self.ids.log_name.add_widget(MDPersianLabel(
                label_text=item[0], size_hint=(1, 1)))
            self.ids.log_date.add_widget(
                MDLabel(text=str(item[3]), size_hint=(1, 1), halign="center"))


class TotalLogFilter(MDScreen):
    date_filter = {"from": "", "to": ""}
    date_filter_type = None
    name_filter = None
    names = []

    def on_enter(self):
        self.names = []
        self.names += read_all_buyers_name()
        self.ids.names.clear_widgets()
        layout = MDBoxLayout(spacing=5, size_hint_y=None,
                             orientation="vertical")
        layout.bind(minimum_height=layout.setter("height"))
        for name in self.names:
            if name != "":
                sub_layout = MDBoxLayout(
                    orientation="horizontal", size_hint_y=None, height=40)
                btn = MDFlatButton(name=name, text=get_display(reshape(
                    name)), font_name=FONT_PATH, on_release=self.set_name_filter)
                sub_layout.add_widget(btn)
                layout.add_widget(sub_layout)
        root = MDScrollView(size_hint=(.5, .5), pos_hint={"x": 0, "y": .2})
        root.add_widget(layout)
        self.ids.names.add_widget(root)

    def open_picker(self):
        self.picker = MDDatePicker()
        self.picker.on_ok_button_pressed = lambda: self.get_date(
            self.picker.year, self.picker.month, self.picker.sel_day)
        self.picker.open()

    def get_date(self, year, month, day):
        self.picker.dismiss()
        self.date_filter[self.date_filter_type] = f"{year}-{month}-{day}"
        self.ids.from_date.text = self.date_filter["from"]
        self.ids.to_date.text = self.date_filter["to"]

    def set_date_filter(self, type="from"):
        if self.ids.check_date.active:
            self.date_filter_type = type
            self.open_picker()

    def set_type_filter(self, active):
        if not active:
            self.ids.is_buy.active = False
            self.ids.is_charge.active = False

    def set_name_filter(self, instance):
        self.name_filter = instance.name

    def cancel(self):
        global filter, date_filter, type_filter, value_filter, name_filter
        filter = []
        date_filter = []
        value_filter = []
        type_filter = None
        name_filter = None
        self.manager.current = "total_log"

    def set_filter(self):
        global filter, date_filter, type_filter, value_filter, name_filter
        filter = []
        date_filter = []
        value_filter = []
        type_filter = None
        name_filter = None
        for checkbox_id in ("check_type", "check_date", "check_value", "check_name"):
            if self.ids[checkbox_id].active:
                filter.append({"type": "operation", "value": "price", "date": "date", "name": "name"}
                              [checkbox_id.replace("check_", "")])
        date_filter += [self.ids.from_date.text, self.ids.to_date.text]
        value_filter += [self.ids.value_from.text, self.ids.value_to.text]
        type_filter = "b" if self.ids.is_buy.active else "c" if self.ids.is_charge.active else None
        name_filter = self.name_filter
        self.manager.current = "total_log"

    def search_in_buyers(self, text):
        self.names = []
        text = text
        for name in read_all_buyers_name():
            if text in name:
                self.names.append(name)
        self.ids.names.clear_widgets()
        layout = MDBoxLayout(spacing=5, size_hint_y=None,
                             orientation="vertical")
        layout.bind(minimum_height=layout.setter("height"))
        for name in self.names:
            if name != "":
                sub_layout = MDBoxLayout(
                    orientation="horizontal", size_hint_y=None, height=40)
                btn = MDFlatButton(name=name, text=get_display(reshape(
                    name)), font_name=FONT_PATH, on_release=self.set_name_filter)
                sub_layout.add_widget(btn)
                layout.add_widget(sub_layout)
        root = MDScrollView(size_hint=(.5, .5), pos_hint={"x": 0, "y": .2})
        root.add_widget(layout)
        self.ids.names.add_widget(root)
