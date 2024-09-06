from arabic_reshaper import reshape
from bidi.algorithm import get_display
import pygame
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from f_components import MDFlatButton
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from important_variables import FONT_PATH
from b_manage_users import change_password, forget_password

email_code = 0
user_name_ = ""

KV = """
<ForgotPassword>:
    GridLayout:
        cols: 1
        size_hint: None, None
        size: 400, 100
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        spacing: 25, 25
        MDTextFieldPersian:
            halign: "left"
            id: user_name
            persian_hint_text: app.language_dialogs["username"]
            font_size: 20
    BoxLayout:
        orientation: 'horizontal'
        size_hint: None, None
        size: 200, 50
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        spacing: 25
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["send_code"]
            icon: "send"
            on_release: root.send_code()

<ForgotPasswordCode>:
    GridLayout:
        cols: 1
        size_hint: None, None
        size: 400, 100
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        spacing: 25, 25
        MDTextFieldPersian:
            id: code
            persian_hint_text: app.language_dialogs["code"]
            font_size: 20
            halign: "left"
    BoxLayout:
        orientation: 'horizontal'
        size_hint: None, None
        size: 200, 50
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        spacing: 25
        MDFlatButton:
            text: app.persian(app.language_dialogs["change_name"])
            font_name: app.FONT_PATH
            on_release: root.manager.current = "forgot_password"
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["check_code"]
            icon: "check"
            on_release: root.check_code()

<ForgotPasswordChangePassword>:
    GridLayout:
        cols: 1
        size_hint: None, None
        size: 400, 100
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        spacing: 25, 25
        MDPasswordTextField:
            id: password
            hint_text: app.persian(app.language_dialogs["password"])
            font_name_hint_text: app.FONT_PATH
        MDPasswordTextField:
            id: passwordtwo
            hint_text: app.persian(app.language_dialogs["confirm_password"])
            font_name_hint_text: app.FONT_PATH
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["change_password"]
            icon: "key-variant"
            on_release: root.change_password()
"""


class ForgotPassword(MDScreen):
    do_shortcuts = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event = Clock.schedule_interval(self.update, 1 / 10)

    def on_leave(self, *args):
        self.do_shortcuts = False
        return super().on_leave(*args)

    def update(self, dt):
        if self.do_shortcuts:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.send_code()

    def on_enter(self):
        self.do_shortcuts = True

    def send_code(self):
        code = forget_password(self.ids.user_name.str)
        if code == False:
            persian_text = MDApp.get_running_app().language_dialogs["network_error"]
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
        elif code == "name":
            persian_text = MDApp.get_running_app().language_dialogs["name_error"]
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
        else:
            global email_code, user_name_
            user_name_ = self.ids.user_name.str
            email_code = code
            self.manager.current = "forgot_password_code"


class ForgotPasswordCode(MDScreen):
    do_shortcuts = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event = Clock.schedule_interval(self.update, 1 / 10)

    def on_leave(self, *args):
        self.do_shortcuts = False
        return super().on_leave(*args)

    def update(self, dt):
        if self.do_shortcuts:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.check_code()

    def on_enter(self):
        self.do_shortcuts = True

    def check_code(self):
        if self.ids.code.str == str(email_code):
            self.manager.current = "forgot_password_change_password"
        else:
            persian_text = MDApp.get_running_app().language_dialogs["code_error"]
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


class ForgotPasswordChangePassword(MDScreen):
    do_shortcuts = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event = Clock.schedule_interval(self.update, 1 / 10)

    def on_leave(self, *args):
        self.do_shortcuts = False
        return super().on_leave(*args)

    def update(self, dt):
        if self.do_shortcuts:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.change_password()

    def on_enter(self):
        self.do_shortcuts = True

    def change_password(self):
        if self.ids.password.text != "" and self.ids.passwordtwo.text != "" and self.ids.password.text == self.ids.passwordtwo.text:
            change_password(self.ids.passwordtwo.text, user_name_)
            self.manager.current = "login_admins"

