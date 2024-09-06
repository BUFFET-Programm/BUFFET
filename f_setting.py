from b_manage_users import change_name, change_password, name_is_new, current_user_name, user_type
from important_variables import FONT_PATH, LANGUAGE_PATH
import pygame
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from f_components import MDFlatButton
from arabic_reshaper import reshape
from bidi.algorithm import get_display

KV = """
<ApplicationSettings>:
    MDFloatLayout:
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["exit"]
            icon: "location-exit"
            on_release: root.manager.current = "home"
            pos_hint: {'x': 0, 'y': .9}
            size_hint: .2, .1
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["manage_database"]
            icon: "database-cog"
            on_release: root.go_to_database_manager_page()
            pos_hint: {'x': .3, 'y': .65}
            size_hint: .4, .1
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["change_theme"]
            icon: "palette"
            on_release: root.manager.current = "change_theme"
            pos_hint: {'x': .3, 'y': .475}
            size_hint: .4, .1
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["edit_account"]
            icon: "account-cog"
            on_release: root.manager.current = "account_setting"
            pos_hint: {'x': .3, 'y': .3}
            size_hint: .4, .1
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["change_language"]
            icon: "translate"
            on_release: root.change_language()
            pos_hint: {'x': .3, 'y': .125}
            size_hint: .4, .1

<AccountSetting>:
    MDFloatLayout:
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["exit"]
            icon: "location-exit"
            on_release: root.manager.current = "settings"
            pos_hint: {'x': 0, 'y': .9}
            size_hint: .2, .1
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["change_username"]
            icon: "rename-box"
            on_release: root.manager.current = "change_admins_name"
            pos_hint: {'x': .2, 'y': .6}
            size_hint: .6, .2
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["change_password"]
            icon: "key-variant"
            on_release: root.manager.current = "change_admins_password"
            pos_hint: {'x': .2, 'y': .3}
            size_hint: .6, .2

<ChangeAdminsPassword>:
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

<ChangeAdminsName>:
    GridLayout:
        cols: 1
        size_hint: None, None
        size: 400, 100
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        spacing: 25, 25
        MDTextFieldPersian:
            id: new_name
            persian_hint_text: app.language_dialogs["new_username"]
            font_size: 20
            halign: "left"
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["change_username"]
            icon: "rename-box"
            on_release: root.change_name()
"""


class ApplicationSettings(MDScreen):

    def close_app(self, instance):
        self.dialog.dismiss()
        MDApp.get_running_app().stop()

    def cancel(self, instance):
        self.dialog.dismiss()
        with open(LANGUAGE_PATH, "r") as file:
            current_lang = file.read()

        new_lang = "per" if current_lang == "eng" else "eng"

        with open(LANGUAGE_PATH, "w") as file:
            file.write(new_lang)

    def change_language(self):
        with open(LANGUAGE_PATH, "r") as file:
            current_lang = file.read()

        new_lang = "per" if current_lang == "eng" else "eng"

        with open(LANGUAGE_PATH, "w") as file:
            file.write(new_lang)

        persian_text = MDApp.get_running_app(
        ).language_dialogs["reopen_application_alert"]
        text = "[font={}]{}[/font]".format(FONT_PATH,
                                           get_display(reshape(persian_text)))
        self.dialog = MDDialog(
            title=text,
            buttons=[
                MDFlatButton(
                    text=get_display(
                        reshape(MDApp.get_running_app().language_dialogs["cancel"])),
                    font_name=FONT_PATH,
                    on_release=self.cancel
                ),
                MDFlatButton(
                    text=get_display(
                        reshape(MDApp.get_running_app().language_dialogs["close_application"])),
                    font_name=FONT_PATH,
                    on_release=self.close_app
                )
            ]
        )
        self.dialog.open()

    def go_to_database_manager_page(self):
        if user_type(current_user_name()) in ("creator", "admin"):
            self.manager.current = "database_setting"
        else:
            persian_text = MDApp.get_running_app(
            ).language_dialogs["admin_and_manager"]
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


class AccountSetting(MDScreen):
    pass


class ChangeAdminsName(MDScreen):
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
                self.change_name()

    def on_enter(self):
        self.do_shortcuts = True

    def change_name(self):
        if name_is_new(self.ids.new_name.str):
            change_name(current_user_name(), self.ids.new_name.str)
            self.manager.current = "home"
        else:
            persian_text = MDApp.get_running_app().language_dialogs["name_duplicated_error"]
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


class ChangeAdminsPassword(MDScreen):
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
            change_password(self.ids.passwordtwo.text, current_user_name())
            self.manager.current = "home"
