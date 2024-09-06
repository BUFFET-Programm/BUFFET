from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from bidi.algorithm import get_display
from arabic_reshaper import reshape
from f_components import MDFlatButton
from important_variables import FONT_PATH
from b_manage_users import user_type, current_user_name

KV = """
<Home>:
    MDFloatLayout:
        MDPersianLabel:
            label_text: app.language_dialogs["welcome"]
            font_size: 25
            halign: "center"
            valign: "center"
            pos_hint: {"x": .3, "y": .7}
            size_hint: .4, .2
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["login"]
            icon: "login"
            pos_hint: {"x": .19, "y": .4}
            size_hint: .3, .2
            on_release: root.manager.current = "login"
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["register"]
            icon: "account-plus"
            pos_hint: {"x": .51, "y": .4}
            size_hint: .3, .2
            on_release: root.manager.current = "register_get_name"
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["delete_data"]
            icon: "delete"
            pos_hint: {"x": 0, "y": 0}
            size_hint: .2, .1
            on_release: root.delete_data()
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["set_webcam"]
            icon: "camera"
            pos_hint: {"x": .19, "y": .18}
            size_hint: .3, .2
            on_release: root.manager.current = "set_webcam"
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["statistics"]
            icon: "chart-bar"
            pos_hint: {"x": .51, "y": .18}
            size_hint: .3, .2
            on_release: root.manager.current = "statistics"
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["settings"]
            icon: "cogs"
            pos_hint: {'x': .75,'y': .9}
            size_hint: .25, .1
            on_release: root.manager.current = "settings"
        MDIconButton:
            icon: "information"
            size_hint: .1, .1
            pos_hint: {"x": .9, "y": 0}
            on_release: root.manager.current = "information"
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["close_application"]
            icon: "close"
            pos_hint: {"x": 0, "y": .9}
            size_hint: .2, .1
            on_release: app.stop()
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["logout"]
            icon: "logout"
            pos_hint: {"x": 0, "y": .75}
            size_hint: .2, .1
            on_release: root.manager.current = "login_admins"
"""


class Home(MDScreen):

    def delete_data(self):
        if user_type(current_user_name()) == "creator":
            self.manager.current = "ask_delete_data"
        else:
            persian_text = MDApp.get_running_app().language_dialogs["only_manager"]
            text = "[font={}]{}[/font]".format(FONT_PATH,
                                               get_display(reshape(persian_text)))
            self.dialog = MDDialog(
                title=text,
                buttons=[
                    MDFlatButton(
                        text=get_display(reshape(MDApp.get_running_app().language_dialogs["i_got_it"])),
                        font_name=FONT_PATH,
                        on_release=lambda instance: self.dialog.dismiss()
                    )
                ]
            )
            self.dialog.open()
