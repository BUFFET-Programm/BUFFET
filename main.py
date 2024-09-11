# In The Name Of God

from time import sleep
import random
import sys
import ctypes

have_error = False
sys.dont_write_bytecode = True

try:
    import cv2
except ModuleNotFoundError:
    have_error = True
    print('opencv module not found. you can install it with run this line in cmd:\npython -m pip install opencv-python')

try:
    import cv2.face 
except ModuleNotFoundError:
    have_error = True
    print('opencv face recognizer not found. you can install it with run this line in cmd:\npython -m pip install opencv-contrib-python')

try:
    from arabic_reshaper import reshape
except ModuleNotFoundError:
    have_error = True
    print('arabic reshaper module not found. you can install it with run this line in cmd:\npython -m pip install arabic-reshaper')

try:
    from bidi.algorithm import get_display
except ModuleNotFoundError:
    have_error = True
    print('bidi module not found. you can install it with run this line in cmd:\npython -m pip install python-bidi')

try:
    import pygame
except ModuleNotFoundError:
    have_error = True
    print('pygame module not found. you can install it with run this line in cmd:\npython -m pip install pygame')

try:
    from kivy.clock import Clock
    from kivy.core.window import Window
    from kivy.lang import Builder
except ModuleNotFoundError:
    have_error = True
    print('kivy module not found. you can install it with run this line in cmd:\npython -m pip install kivy')

try:
    from kivymd.app import MDApp
    from kivymd.icon_definitions import md_icons
    from kivymd.theming import ThemeManager
    from kivymd.uix.button import MDFlatButton
    from kivymd.uix.dialog import MDDialog
    from kivymd.uix.screenmanager import ScreenManager
except ModuleNotFoundError:
    have_error = True
    print('kivymd module not found. you can install it with run this line in cmd:\npython -m pip install kivymd')

try:
    import PIL
except ModuleNotFoundError:
    have_error = True
    print('pillow module not found. you can install it with run this line in cmd:\npython -m pip install pillow')

try:
    import matplotlib
except ModuleNotFoundError:
    have_error = True
    print('matplotlib module not found. you can install it with run this line in cmd:\npython -m pip install matplotlib')

if have_error:
    sleep(60)
    sys.exit()


from f_KV import KV
from important_variables import THEME_PATH, BASE_DIR, COLORS, LANGUAGE_PATH, LANGUAGES_DIALOGS_ENG, LANGUAGES_DIALOGS_PER
from b_handle_file import create_files_and_folders, download_files
from f_components import MDFlatButton
from f_total_log import TotalLog, TotalLogFilter
from f_register import RegisterGetFace, RegisterGetName
from f_login_admins import LoginAdmins
from f_statistics import Statistics
from f_forgot_password import ForgotPassword, ForgotPasswordCode, ForgotPasswordChangePassword
from f_information import Information
from f_delete_data import AskDeleteData
from f_theming import ChangeTheme
from f_set_webcam import SetWebcam
from f_register_admins import RegisterAdminsEmail, RegisterAdminsCode, RegisterAdminsLastStep
from f_home import Home
from f_setting import ApplicationSettings, AccountSetting, ChangeAdminsName, ChangeAdminsPassword
from f_database_setting import DatabaseSetting
from f_login import Login, NotLogined
from f_user_account import UserAccount, Setting, ChangeUserFaceAsk, ChangeUserFaceProcess, ChangeUserName, Log, Filter



sys.dont_write_bytecode
Builder.load_string(KV)


class WindowManager(ScreenManager):
    pass


class MainApp(MDApp):
    FONT_PATH = BASE_DIR + "/extensions/iransans.ttf"
    colors = COLORS

    def list_all_widgets(self, screen_manager):
        all_widgets = []
        for screen in screen_manager.screens:
            all_widgets.extend(self.get_all_widgets(screen))
        
        return all_widgets

    def get_all_widgets(self, widget):
        widgets = []
        for child in widget.children:
            widgets.append(child)
            widgets.extend(self.get_all_widgets(child))
        return widgets

    def reverse_widgets(self, parent=None):
        if parent:
            widgets = self.get_all_widgets(parent)
        else:
            widgets = self.list_all_widgets(self.wm)
        for widget in widgets:
            try:
                widget_name = widget.__class__.__name__
                if widget_name in ("MDBoxLayout", "BoxLayout"):
                    if widget.orientation == "horizontal":
                        widget_children = list(widget.children.copy())
                        widget.clear_widgets()
                        for widget_child in widget_children:
                            widget.add_widget(widget_child)
                if widget_name in ("MDTextField", "MDTextFieldPersian"):
                    if widget.halign != "center":
                        widget.halign = "left"
                current_x = widget.pos_hint['x']
                new_x = 1 - current_x - widget.size_hint[0]
                widget.pos_hint = {'x': new_x, 'y': widget.pos_hint['y']}
            except (AssertionError, KeyError):
                pass

    @staticmethod
    def persian(text):
        return get_display(reshape(text))

    def update(self, dt):
        Window.size = (1000, 700)

    def build(self):
        Clock.schedule_interval(self.update, 1 / 10)
        with open(LANGUAGE_PATH, "r") as file:
            lang = file.read()
        self.language_dialogs = LANGUAGES_DIALOGS_PER if lang == "per" else LANGUAGES_DIALOGS_ENG
        with open(THEME_PATH, "r") as file:
            theme_ = file.read().split(",")
        theme = theme_[0]
        rbcc_ = theme_[2]
        theme_color = theme_[1]
        self.title = self.language_dialogs['title']
        self.theme_cls = ThemeManager()
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = theme
        if rbcc_ == "True":
            self.theme_cls.colors["Light"] = {
                "StatusBar": "E0E0E0",
                "AppBar": "F5F5F5",
                "Background": "E7E7E7",
                "CardsDialogs": "FFFFFF",
                "FlatButtonDown": "cccccc"
            }
            self.theme_cls.colors["Dark"] = {
                "StatusBar": "000000",
                "AppBar": "1f1f1f",
                "Background": "353535",
                "CardsDialogs": "212121",
                "FlatButtonDown": "999999"
            }

        if theme_color == "random":
            self.theme_cls.primary_palette = random.choice(self.colors)
        else:
            self.theme_cls.primary_palette = theme_color
        self.wm = WindowManager()
        self.wm.current = "login_admins"
        if lang == 'eng':
            self.reverse_widgets()
        return self.wm


class ErrorNetConnectionApp(MDApp):

    def close_dialog(self, instance):
        self.dialog.dismiss()
        self.stop()

    def build(self):
        text = "Network connection error. please check your internet connection, then try again."
        self.dialog = MDDialog(
            title=text,
            buttons=[
                MDFlatButton(
                    text="Close the program.",
                    on_release=self.close_dialog
                )
            ]
        )
        self.dialog.open()
        return super().build()


def run_as_admin(cmd_line=None):
    if cmd_line is None:
        cmd_line = sys.argv[0]
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{cmd_line}"', None, 1)
    except Exception as e:
        print(f"Failed to run as admin: {e}")


if __name__ == "__main__":
    # if not ctypes.windll.shell32.IsUserAnAdmin():
    #     run_as_admin(__file__)
    # else:
        create_files_and_folders()
        if download_files():
            Window.set_icon(BASE_DIR+'/extensions/icon.ico')
            app = MainApp()
            app.run()
        else:
            ErrorNetConnectionApp().run()

# End of Program :)
