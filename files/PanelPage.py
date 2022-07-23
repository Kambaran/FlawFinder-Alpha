from PyQt5.QtWidgets import QWidget, QGroupBox, QLineEdit, QVBoxLayout, QGridLayout, QLabel
from PyQt5.QtCore import QRect


class InfoPage(QWidget):

    def __init__(self):
        super(InfoPage, self).__init__()

        self.setGeometry(QRect(0, 0, 0, 0))
        self.setObjectName("InfoPanelPage")

        image_info_box = QGroupBox(self)
        image_info_box.setObjectName("InfoGroupBox")
        image_info_box.setTitle("Image Information")

        self.pixel_coordinates = QLineEdit("Position Info")
        self.pixel_coordinates.setReadOnly(True)
        self.pixel_coordinates.setObjectName("PixelPositionCoordinates")

        pixel_coordinates_label = QLabel("Pixel")

        self.pixel_value = QLineEdit("Values Info")
        self.pixel_value.setReadOnly(True)
        self.pixel_value.setObjectName("PixelValue")

        pixel_info_box_layout = QGridLayout()
        pixel_info_box_layout.addWidget(self.pixel_coordinates, 0, 0, 1, 1)
        pixel_info_box_layout.addWidget(pixel_coordinates_label, 0, 1, 1, 1)
        pixel_info_box_layout.addWidget(self.pixel_value, 1, 0, 1, 1)

        pixel_info_box = QGroupBox(self)
        pixel_info_box.setObjectName("PixelGroupBox")
        pixel_info_box.setTitle("Pixel Information")
        pixel_info_box.setLayout(pixel_info_box_layout)

        info_page_layout = QGridLayout(self)
        info_page_layout.setObjectName("InfoPageGrid")
        info_page_layout.addWidget(pixel_info_box, 1, 1)
        info_page_layout.addWidget(image_info_box, 2, 1)


if __name__ == '__main__':

    pass
