from arabic_reshaper import reshape
from bidi.algorithm import get_display
import pygame
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from f_components import MDFlatButton
from important_variables import FONT_PATH
from b_manage_users import email_is_new, register_user, send_code_for_verification

email_code = 0
email = ""

KV = """
<RegisterAdminsEmail>:
    GridLayout:
        cols: 1
        size_hint: None, None
        size: 400, 100
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        spacing: 25, 25
        MDTextFieldPersian:
            id: email
            halign: "left"
            persian_hint_text: app.language_dialogs["email"]
            font_size: 20
    BoxLayout:
        orientation: 'horizontal'
        size_hint: None, None
        size: 200, 50
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        spacing: 25
        MDFlatButton:
            text: app.persian(app.language_dialogs["enter"])
            font_name: app.FONT_PATH
            on_release: root.manager.current = "login_admins"
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["send_code"]
            icon: "send"
            on_release: root.send_code()

<RegisterAdminsCode>:
    GridLayout:
        cols: 1
        size_hint: None, None
        size: 400, 100
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        spacing: 25, 25
        MDTextFieldPersian:
            id: code
            halign: "left"
            persian_hint_text: app.language_dialogs["code"]
            font_size: 20
    BoxLayout:
        orientation: 'horizontal'
        size_hint: None, None
        size: 200, 50
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        spacing: 25
        MDFlatButton:
            text: app.persian(app.language_dialogs["change_email"])
            font_name: app.FONT_PATH
            on_release: root.manager.current = "register_admins_email"
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["check_code"]
            icon: "check"
            on_release: root.check_code()

<RegisterAdminsLastStep>:
    GridLayout:
        cols: 1
        size_hint: None, None
        size: 400, 100
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        spacing: 25, 25
        MDTextFieldPersian:
            id: user_name
            halign: "left"
            persian_hint_text: app.language_dialogs["username"]
            font_size: 20
        MDPasswordTextField:
            id: password
            hint_text: app.persian(app.language_dialogs["password"])
            font_name_hint_text: app.FONT_PATH
        MDPasswordTextField:
            id: passwordtwo
            hint_text: app.persian(app.language_dialogs["confirm_password"])
            font_name_hint_text: app.FONT_PATH
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["register"]
            icon: "account-plus"
            on_release: root.register()
"""


class RegisterAdminsEmail(MDScreen):
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
        global email_code, email
        email = self.ids.email.str
        if email_is_new(email):
            email_code = send_code_for_verification(self.ids.email.str)
            if email_code:
                self.manager.current = "register_admins_code"
            else:
                persian_title = MDApp.get_running_app(
                ).language_dialogs["error"]
                title = "[font={}]{}[/font]".format(FONT_PATH,
                                                    get_display(reshape(persian_title)))
                persian_text = MDApp.get_running_app(
                ).language_dialogs["network_or_email_error"]
                text = "[font={}]{}[/font]".format(FONT_PATH,
                                                   get_display(reshape(persian_text)))
                self.dialog = MDDialog(
                    title=title,
                    text=text,
                    buttons=[
                        MDFlatButton(
                            text=get_display(
                                reshape(MDApp.get_running_app().language_dialogs["i_got_it"])),
                            font_name=FONT_PATH,
                            on_release=lambda instance: self.dialog.dismiss()
                        )
                    ]
                )
                self.dialog.open()
        else:
            persian_text = MDApp.get_running_app(
            ).language_dialogs["email_duplicated_error"]
            text = "[font={}]{}[/font]".format(FONT_PATH,
                                               get_display(reshape(persian_text)))
            self.dialog = MDDialog(
                title=text,
                buttons=[
                    MDFlatButton(
                        text=get_display(
                            reshape(
                            MDApp.get_running_app().language_dialogs["i_got_it"]
                            )
                        ),
                        font_name=FONT_PATH,
                        on_release=lambda instance: self.dialog.dismiss()
                    )
                ]
            )
            self.dialog.open()


class RegisterAdminsCode(MDScreen):
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
        global email_code
        if self.ids.code.str == str(email_code):
            self.manager.current = "register_admins_last_step"
        else:
            persian_text = MDApp.get_running_app(
            ).language_dialogs["code_error"]
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


class RegisterAdminsLastStep(MDScreen):
    do_shortcuts = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event = Clock.schedule_interval(self.update, 1 / 10)

    def on_leave(self, *args):
        self.do_shortcuts = False
        self.ids.user_name.text = ""
        self.ids.user_name.str = ""
        self.ids.password.text = ""
        self.ids.passwordtwo.text = ""
        return super().on_leave(*args)

    def update(self, dt):
        if self.do_shortcuts:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.register()

    def on_enter(self):
        self.do_shortcuts = True

    def register(self):
        global email
        if self.ids.password.text != "" and self.ids.passwordtwo.text != "" and self.ids.user_name.str != "" and self.ids.password.text == self.ids.passwordtwo.text:
            if register_user(self.ids.user_name.str, self.ids.password.text, email):
                self.manager.current = "login_admins"
            else:
                persian_text = MDApp.get_running_app(
                ).language_dialogs["name_duplicated_error"]
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
        else:
            persian_text = MDApp.get_running_app().language_dialogs["name_and_password_error"]
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
