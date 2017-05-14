from kivy.app import App

# Import configure after App import to customize configuration
import configure

import os
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.clock import Clock, mainthread
from kivy.lang import Builder
import cv2


cur_dir = os.path.dirname(os.path.realpath(__file__))

Builder.load_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'app.kv'))


class VideoPreviewWidget(BoxLayout):

    capture = None
    event_take_video = None
    texture = None

    def __init__(self, **kwargs):
        super(VideoPreviewWidget, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def on_btn_start(self):
        if self.event_take_video is None:
            # Call `self.take_video` 30 times per sec
            self.event_take_video = Clock.schedule_interval(self.take_video, 1.0 / 30.0)
        elif not self.event_take_video.is_triggered:
            self.event_take_video()

    def on_btn_stop(self):
        if self.event_take_video is not None and self.event_take_video.is_triggered:
            self.event_take_video.cancel()

    def frame_to_buf(self, frame):
        if frame is None:
            return
        buf1 = cv2.flip(frame, 0)
        if buf1 is not None:
            buf = buf1.tostring()
            self.texture = Texture.create(size=(640, 480))
            self.texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            return True

    @mainthread
    def update_image(self, *args):
        if self.texture is not None:
            self.ids.img_left.texture = self.texture
        else:
            self.ids.img_left.source = cur_dir + '/img/bad_camera.png'

    def take_video(self, *args):
        """
        Capture video frame and update image widget
        :param args:
        :return:
        """
        try:
            ret, frame = self.capture.read()
            if self.frame_to_buf(frame=frame):
                self.update_image()
            else:
                self.ids.img_left.source = cur_dir + '/img/bad_camera.png'
        except:
            self.ids.img_left.source = cur_dir + '/img/bad_camera.png'

    def on_close(self):
        self.capture.release()


class VideoPreviewApp(App):

    def build(self):
        return VideoPreviewWidget()

    def on_stop(self):
        self.root.on_close()
        super(VideoPreviewApp, self).on_stop()


if __name__ == '__main__':
    VideoPreviewApp().run()
