from b_total_view import show_the_most_purchased_products, buffet_log_as_chart
from kivymd.uix.screen import MDScreen

KV = """
<Statistics>:
    MDFloatLayout:
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["exit"]
            icon: "location-exit"
            pos_hint: {"x": 0, "y": .9}
            size_hint: .2, .1
            on_release: root.manager.current = "home"
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["most_popular_products"]
            icon: "heart"
            pos_hint: {"x": .2, "y": .7}
            size_hint: .6, .1
            on_release: root.show_the_most_purchased_products()
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["transaction_history"]
            icon: "history"
            pos_hint: {"x": .2, "y": .5}
            size_hint: .6, .1
            on_release: root.manager.current = "total_log"
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["buffet_log_as_chart"]
            icon: "chart-areaspline"
            pos_hint: {"x": .2, "y": .3}
            size_hint: .6, .1
            on_release: root.buffet_log_as_chart()
"""


class Statistics(MDScreen):
    def show_the_most_purchased_products(self):
        show_the_most_purchased_products()
    def buffet_log_as_chart(self):
        buffet_log_as_chart()

