import cv2
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.graphics.texture import Texture
from kivymd.uix.screen import MDScreen

KV = """
<SetWebcam>:
    MDBoxLayout:
        orientation: 'vertical'
        Image:
            id: image
        MDPersianLabel:
            id: notification
            size_hint: 1, .15
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["try_again"]
            icon: "reload"
            size_hint: 1, .15
            on_release: root.retry()
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["exit"]
            icon: "location-exit"
            size_hint: 1, .15
            on_release: root.manager.current = "home"
"""


class SetWebcam(MDScreen):

    def __init__(self, **kwargs):
        super(SetWebcam, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture("")
        Clock.schedule_interval(self.update, 1 / 10)

    def on_enter(self, *args):
        self.capture = cv2.VideoCapture(0)
        return super().on_enter(*args)

    def on_leave(self, *args):
        self.capture = cv2.VideoCapture("")
        return super().on_leave(*args)

    def retry(self):
        self.capture = cv2.VideoCapture(0)

    def update(self, dt):
        if self.capture.isOpened():
            self.ids.notification.label_text = MDApp.get_running_app().language_dialogs["webcam_is_connected"]
        else:
            self.ids.notification.label_text = MDApp.get_running_app().language_dialogs["webcam_error2"]
        ret, frame = self.capture.read()
        if ret:
            buf = cv2.flip(frame, 0).tostring()
            texture1 = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.ids.image.texture = texture1
