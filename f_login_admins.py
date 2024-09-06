from arabic_reshaper import reshape
from bidi.algorithm import get_display
import pygame
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from f_components import MDFlatButton
from kivymd.uix.dialog import MDDialog
from important_variables import FONT_PATH
from b_manage_users import enter_user

KV = """
<LoginAdmins>:
    GridLayout:
        cols: 1
        size_hint: None, None
        size: 400, 100
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        spacing: 25, 25
        MDTextFieldPersian:
            id: user_name
            persian_hint_text: app.language_dialogs["username"]
            halign: "left"
            font_size: 20
        MDPasswordTextField:
            id: password
            hint_text: app.persian(app.language_dialogs["password"])
            font_name_hint_text: app.FONT_PATH
    BoxLayout:
        orientation: 'horizontal'
        size_hint: None, None
        size: 200, 50
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        spacing: 25
        MDFlatButton:
            text: app.persian(app.language_dialogs["register"])
            font_name: app.FONT_PATH
            on_release: root.manager.current = "register_admins_email"
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["enter"]
            icon: "login-variant"
            on_release: root.next_step()
    MDFlatButton:
        text: app.persian(app.language_dialogs["forgot_password"])
        font_name: app.FONT_PATH
        size_hint: None, None
        size: 100, 50
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        on_release: root.manager.current = "forgot_password"
"""


class LoginAdmins(MDScreen):
    do_shortcuts = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event = Clock.schedule_interval(self.update, 1 / 10)

    def on_leave(self, *args):
        self.do_shortcuts = False
        self.ids.user_name.text = ""
        self.ids.user_name.str = ""
        self.ids.password.text = ""
        return super().on_leave(*args)

    def update(self, dt):
        if self.do_shortcuts:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.next_step()

    def on_enter(self):
        self.do_shortcuts = True

    def next_step(self):
        mode = enter_user(self.ids.user_name.str, self.ids.password.text)
        if mode == True:
            self.manager.current = "home"
        else:
            persian_text = ""
            if mode == "internet":
                persian_text = MDApp.get_running_app().language_dialogs["network_error"]
            elif mode == "password" or mode == "name":
                persian_text = MDApp.get_running_app().language_dialogs["name_or_password_error"]
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

