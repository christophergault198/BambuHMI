import sys
import vlc
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer  # Updated import
from ui_components import BambuLabHMI
from functions.refresh_tokens import refresh_camera_tokens

class LiveCameraView(QWidget):
    def __init__(self, parent=None):
        super(LiveCameraView, self).__init__(parent)
        self.setWindowTitle("Live Camera")
        self.setGeometry(100, 100, 640, 480)
        self.vlc_instance = vlc.Instance('--verbose=1')
        self.player = self.vlc_instance.media_player_new()

        # Create a basic layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a frame to render video on (this is a dummy widget for VLC)
        self.video_frame = QWidget(self)
        layout.addWidget(self.video_frame)

        # Set VLC to render video on the frame (QWidget)
        if sys.platform.startswith('linux'):  # for Linux using the X Server
            self.player.set_xwindow(self.video_frame.winId())
        elif sys.platform == "win32":  # for Windows
            self.player.set_hwnd(self.video_frame.winId())
        elif sys.platform == "darwin":  # for MacOS
            self.player.set_nsobject(int(self.video_frame.winId()))

        self.updateMedia()  # Initial media update

        # Setup timer to refresh the video frame every 500ms
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateMedia)
        self.timer.start(500)  # Time in milliseconds

    def updateMedia(self):
        token = refresh_camera_tokens()
        media_url = f'http://192.168.9.62:8123/api/camera_proxy/camera.192_168_9_78?token={token}'
        # Increase caching value (e.g., to 3000 milliseconds)
        media = self.vlc_instance.media_new(media_url, 'network-caching=3000')
        self.player.set_media(media)
        if not self.player.is_playing():
            self.player.play()
       # print("Debug: Camera Updated")

    def play(self):
        self.player.play()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BambuLabHMI()
    ex.show()

    # Create and show the live camera view
    live_camera_view = LiveCameraView()
    live_camera_view.show()
    live_camera_view.play()

    sys.exit(app.exec_())