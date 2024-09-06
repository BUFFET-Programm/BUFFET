from arabic_reshaper import reshape
from bidi.algorithm import get_display
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
import random
from important_variables import THEME_PATH, FONT_PATH, COLORS

KV = """
<ChangeTheme>:
    MDFloatLayout:
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["exit"]
            icon: "location-exit"
            on_release: root.manager.current = "settings"
            pos_hint: {'x': 0, 'y': .9}
            size_hint: .2, .1
        MDPersianLabel:
            label_text: app.language_dialogs["rbcc"]
            size_hint: .5, .2
            pos_hint: {'x': .1, 'y': .65}
        MDCheckbox:
            id: rbcc
            on_active: root.rbcc()
            size_hint: .2, .2
            pos_hint: {'x': .4, 'y': .65}
        MDPersianLabel:
            label_text: app.language_dialogs["dark_mode"]
            size_hint: .2, .2
            pos_hint: {'x': .725, 'y': .65}
        MDCheckbox:
            id: theme
            on_active: root.change_theme()
            size_hint: .2, .2
            pos_hint: {'x': .8, 'y': .65}
        MDLabel:
            md_bg_color: [0.9568627450980392, 0.2627450980392157, 0.2117647058823529, 1]
            size_hint: .2, .1
            pos_hint: {'x': .725, 'y': .55}
        MDCheckbox:
            id: Red
            group: "theme_color"
            on_active: root.change_theme_color("Red", self)
            size_hint: .2, .2
            pos_hint: {'x': .8, 'y': .5}
        MDLabel:
            md_bg_color: [0.6117647058823529, 0.1529411764705882, 0.6901960784313725, 1]
            size_hint: .2, .1
            pos_hint: {'x': .425, 'y': .55}
        MDCheckbox:
            id: Purple
            group: "theme_color"
            on_active: root.change_theme_color("Purple", self)
            size_hint: .2, .2
            pos_hint: {'x': .5, 'y': .5}
        MDLabel:
            md_bg_color: [0.403921568627451, 0.2274509803921569, 0.7176470588235294, 1]
            size_hint: .2, .1
            pos_hint: {'x': .125, 'y': .55}
        MDCheckbox:
            id: DeepPurple
            group: "theme_color"
            on_active: root.change_theme_color("DeepPurple", self)
            size_hint: .2, .2
            pos_hint: {'x': .2, 'y': .5}
        MDLabel:
            md_bg_color: [0.1294117647058824, 0.5882352941176471, 0.9529411764705882, 1]
            size_hint: .2, .1
            pos_hint: {'x': .725, 'y': .35}
        MDCheckbox:
            id: Blue
            group: "theme_color"
            on_active: root.change_theme_color("Blue", self)
            size_hint: .2, .2
            pos_hint: {'x': .8, 'y': .3}
        MDLabel:
            md_bg_color: [0.0117647058823529, 0.6627450980392157, 0.9568627450980392, 1]
            size_hint: .2, .1
            pos_hint: {'x': .425, 'y': .35}
        MDCheckbox:
            id: LightBlue
            group: "theme_color"
            on_active: root.change_theme_color("LightBlue", self)
            size_hint: .2, .2
            pos_hint: {'x': .5, 'y': .3}
        MDLabel:
            md_bg_color: [0.2980392156862745, 0.6862745098039216, 0.3137254901960784, 1]
            size_hint: .2, .1
            pos_hint: {'x': .125, 'y': .35}
        MDCheckbox:
            id: Green
            group: "theme_color"
            on_active: root.change_theme_color("Green", self)
            size_hint: .2, .2
            pos_hint: {'x': .2, 'y': .3}
        MDLabel:
            md_bg_color: [1, 0.7568627450980392, 0.0274509803921569, 1]
            size_hint: .2, .1
            pos_hint: {'x': .725, 'y': .15}
        MDCheckbox:
            id: Amber
            group: "theme_color"
            on_active: root.change_theme_color("Amber", self)
            size_hint: .2, .2
            pos_hint: {'x': .8, 'y': .1}
        MDLabel:
            md_bg_color: [1, 0.3411764705882353, 0.1333333333333333, 1]
            size_hint: .2, .1
            pos_hint: {'x': .425, 'y': .15}
        MDCheckbox:
            id: DeepOrange
            group: "theme_color"
            on_active: root.change_theme_color("DeepOrange", self)
            size_hint: .2, .2
            pos_hint: {'x': .5, 'y': .1}
        MDPersianLabel:
            label_text: app.language_dialogs["auto"]
            size_hint: .2, .1
            pos_hint: {'x': .125, 'y': .15}
        MDCheckbox:
            id: random
            group: "theme_color"
            on_active: root.change_theme_color("random", self)
            size_hint: .2, .2
            pos_hint: {'x': .2, 'y': .1}
"""


class ChangeTheme(MDScreen):
    open_dialog = True

    def on_enter(self, *args):
        with open(THEME_PATH, "r") as file:
            theme = file.read().split(",")[0]
        if theme == "Dark":
            self.ids.theme.active = True
        else:
            self.ids.theme.active = False
        with open(THEME_PATH, "r") as file:
            rbcc = file.read().split(",")[2]
        if rbcc == "True":
            self.open_dialog = False
            self.ids.rbcc.active = True
        else:
            self.ids.rbcc.active = False
        with open(THEME_PATH, "r") as file:
            theme_color = file.read().split(",")[1]
        self.ids[theme_color].active = True
        return super().on_enter(*args)

    def close_app(self, instance):
        self.dialog.dismiss()
        MDApp.get_running_app().stop()

    def cancel(self, instance):
        self.dialog.dismiss()
        self.open_dialog = False
        current_choose = self.ids.rbcc.active
        self.ids.rbcc.active = False if current_choose else True

    def rbcc(self):
        if self.ids.rbcc.active:
            with open(THEME_PATH, "r") as file:
                theme = file.read().split(",")
            theme[2] = "True"
            with open(THEME_PATH, "w") as file:
                file.write(",".join(theme))
        else:
            with open(THEME_PATH, "r") as file:
                theme = file.read().split(",")
            theme[2] = "False"
            with open(THEME_PATH, "w") as file:
                file.write(",".join(theme))
        persian_text = MDApp.get_running_app().language_dialogs["reopen_application_alert"]
        text = "[font={}]{}[/font]".format(FONT_PATH,
                                           get_display(reshape(persian_text)))
        self.dialog = MDDialog(
            title=text,
            buttons=[
                MDFlatButton(
                    text=get_display(reshape(MDApp.get_running_app().language_dialogs["cancel"])),
                    font_name=FONT_PATH,
                    on_release=self.cancel
                ),
                MDFlatButton(
                    text=get_display(reshape(MDApp.get_running_app().language_dialogs["close_application"])),
                    font_name=FONT_PATH,
                    on_release=self.close_app
                )
            ]
        )
        if self.open_dialog:
            self.dialog.open()
        current_open_dialog = self.open_dialog
        self.open_dialog = False if current_open_dialog else True

    def change_theme(self):
        if self.ids.theme.active:
            with open(THEME_PATH, "r") as file:
                theme = file.read().split(",")
            theme[0] =  """Dark"""
            with open(THEME_PATH, "w") as file:
                file.write(",".join(theme))
                MDApp.get_running_app().theme_cls.theme_style = "Dark"
        else:
            with open(THEME_PATH, "r") as file:
                theme = file.read().split(",")
            theme[0] = "Light"
            with open(THEME_PATH, "w") as file:
                file.write(",".join(theme))
                MDApp.get_running_app().theme_cls.theme_style = "Light"

    def change_theme_color(self, color, button):
        if button.active:
            with open(THEME_PATH, "r") as file:
                theme = file.read().split(",")
            theme[1] = color
            with open(THEME_PATH, "w") as file:
                file.write(",".join(theme))
                if color != "random":
                    MDApp.get_running_app().theme_cls.primary_palette = color
                else:
                    MDApp.get_running_app().theme_cls.primary_palette = random.choice(COLORS)
