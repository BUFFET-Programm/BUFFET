from kivymd.uix.screen import MDScreen

KV = """
<Information>:
    MDRectangleFlatIconButton:
        button_text: app.language_dialogs["exit"]
        icon: "location-exit"
        pos_hint: {"x": 0, "y": .9}
        size_hint: .2, .1
        on_release: root.manager.current = "home"
    MDPersianLabel:
        label_text: app.language_dialogs["application_name"]
        font_size: 30
        size_hint: .3, .2
        pos_hint: {"x": .35, "y": .8}
    MDPersianLabel:
        label_text: app.language_dialogs["smart_buffet"]
        font_size: 25
        size_hint: .2, .2
        pos_hint: {"x": .4, "y": .7}
    MDPersianLabel:
        label_text: app.language_dialogs["creators"]
        font_size: 30
        size_hint: .2, .2
        pos_hint: {"x": .4, "y": .55}
    MDPersianLabel:
        label_text: app.language_dialogs["creators_names"]
        font_size: 25
        size_hint: .6, .2
        pos_hint: {"x": .2, "y": .45}
    MDPersianLabel:
        label_text: app.language_dialogs["version_number"]
        font_size: 30
        size_hint: .3, .2
        pos_hint: {"x": .35, "y": .3}
    MDLabel:
        halign: "center"
        text: "3.0.0"
        font_size: 25
        size_hint: .2, .2
        pos_hint: {"x": .4, "y": .2}
"""


class Information(MDScreen):
    pass
