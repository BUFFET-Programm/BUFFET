from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.button import MDFlatButton, MDIconButton, MDRectangleFlatIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from important_variables import FONT_PATH

KV = """
#:import images_path kivymd.images_path
#:import md_icons kivymd.icon_definitions.md_icons
<MDRectangleFlatIconButton>:
    button_text: ""
    text: app.persian(self.button_text)
    font_name: app.FONT_PATH
    line_width: dp(1.5)
    icon_size: 25
    md_bg_color: app.theme_cls.primary_color
    text_color: (1, 1, 1, 1) if not self.theme_cls.theme_style == "Dark" else (0, 0, 0, 1)
    icon_color: (1, 1, 1, 1) if not self.theme_cls.theme_style == "Dark" else (0, 0, 0, 1)

<MDPasswordTextField@MDRelativeLayout>:
    text: ""
    hint_text: ""
    font_name_hint_text: ""
    size_hint_y: None
    height: text_field.height

    MDTextField:
        id: text_field
        mode: "rectangle"
        font_name_hint_text: root.font_name_hint_text
        hint_text: root.hint_text
        text: root.text
        on_text: root.text = self.text
        password: True
        icon_left: "key-variant"

    MDIconButton:
        icon: "eye-off"
        pos_hint: {"center_y": .4}
        pos: text_field.width - self.width + dp(4), 0
        theme_text_color: "Hint"
        on_release:
            self.icon = "eye" if self.icon == "eye-off" else "eye-off"
            text_field.password = False if text_field.password is True else True


<MDPersianFlatButton@MDFlatButton>:
    font_name: app.FONT_PATH

<MDItemButton1@MDPersianFlatButton>:
    text_: ""
    text: app.persian(self.text_)
    on_release: app.wm.screens[13].menu_callback(self.text_)

<MDItemButton2@MDPersianFlatButton>:
    text_: ""
    text: app.persian(self.text_)
    on_release: app.wm.screens[6].menu_callback(self.text_)

<MDItemButton3@MDFlatButton>:
    on_release: app.wm.screens[6].menu_callback2(self.text)

<MDItemButton@MDRaisedButton>:
    root_:
    on_release: self.root_.callback_dropdown_item(self.button_text)
    button_text: ""
    text: app.persian(self.button_text)
    font_name: app.FONT_PATH

<MDPersianLabel>:
    label_text: ""
    text: app.persian(self.label_text)
    font_name: app.FONT_PATH
    halign: "center"
    valign: "center"
    color: [1, 1, 1, 1] if app.theme_cls.theme_style == "Dark" else [0, 0, 0, 1]

<MDLabel>:
    color: [1, 1, 1, 1] if app.theme_cls.theme_style == "Dark" else [0, 0, 0, 1]

<MDIconButton>:
    icon_color: [1, 1, 1, 1] if app.theme_cls.theme_style == "Dark" else [0, 0, 0, 1]

<MDTextField>:
    mode: "round"

<MDTextFieldPersian>:
    mode: "rectangle"
    font_name: app.FONT_PATH
    persian_hint_text: ""
    hint_text: app.persian(self.persian_hint_text)
    font_name_hint_text: app.FONT_PATH
    halign: "right"

<MDBoxLayoutNoReverse@MDBoxLayout>:

"""


class MDTextFieldPersian(MDTextField):
    max_chars = NumericProperty(100)  # maximum character allowed
    str = StringProperty()
    valid_chars = StringProperty("all")

    def __init__(self, **kwargs):
        super(MDTextFieldPersian, self).__init__(**kwargs)
        self.text = get_display(reshape(""))

    def insert_text(self, substring, from_undo=False):
        if not from_undo and (len(self.text) + len(substring) > self.max_chars):
            return
        if self.valid_chars != "all":
            if substring in self.valid_chars:
                self.str = self.str+substring
                self.text = get_display(reshape(self.str))
                substring = ""
                super(MDTextFieldPersian, self).insert_text(
                    substring, from_undo)
        else:
            self.str = self.str+substring
            self.text = get_display(reshape(self.str))
            substring = ""
            super(MDTextFieldPersian, self).insert_text(substring, from_undo)

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.str = self.str[0:len(self.str)-1]
        self.text = get_display(reshape(self.str))


class MDPersianLabel(MDLabel):
    label_text = StringProperty("")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font_name = FONT_PATH
        Clock.schedule_interval(self.update, 1 / 30)

    def update(self, dt):
        self.text = get_display(reshape(self.label_text))


class MDIconButton(MDIconButton):
    name = StringProperty("")


class MDFlatButton(MDFlatButton):
    name = StringProperty("")


class MDRectangleFlatIconButton(MDRectangleFlatIconButton):
    name = StringProperty("")
    button_text = StringProperty("")


class MDBoxLayoutNoReverse(MDBoxLayout):
    pass
