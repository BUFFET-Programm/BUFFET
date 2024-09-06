from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from b_handle_file import delete_all_data

KV = """
<AskDeleteData>:
    FloatLayout:
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["exit"]
            icon: "location-exit"
            pos_hint: {"x": 0, "y": .9}
            size_hint: .2, .1
            on_release: root.manager.current = "home"
        MDPersianLabel:
            label_text: app.language_dialogs["delete_data_title"]
            pos_hint: {"x": 0, "y": .7}
            size_hint: 1, .2
        MDPersianLabel:
            label_text: app.language_dialogs["delete_data_text"]
            pos_hint: {"x": 0, "y": .6}
            size_hint: 1, .2
        MDTextFieldPersian:
            max_chars: 78
            id: text
            halign: "right"
            pos_hint: {"x": .1, "y": .5}
            size_hint: .8, .1
            font_size: 27
            mode: "round"
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["done2"]
            pos_hint: {"x": .1, "y": .1}
            size_hint: .8, .2
            on_release: root.delete_data()
"""


class AskDeleteData(MDScreen):

    def delete_data(self):
        if self.ids.text.str == MDApp.get_running_app().language_dialogs["delete_data_text"]:
            self.ids.text.str = ""
            self.ids.text.text = ""
            delete_all_data()
            self.manager.current = "login_admins"
