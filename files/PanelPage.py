from PyQt5.QtWidgets import QWidget, QGroupBox, QLineEdit, QVBoxLayout, QGridLayout, QLabel, QSizePolicy
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

        pixel_coordinates_label = QLabel("Position (x,y)")

        self.pixel_value = QLineEdit("Values Info")
        self.pixel_value.setReadOnly(True)
        self.pixel_value.setObjectName("PixelValue")

        pixel_value_label = QLabel("RGB Value")

        pixel_info_box_layout = QGridLayout()
        pixel_info_box_layout.addWidget(self.pixel_coordinates, 0, 0, 1, 1)
        pixel_info_box_layout.addWidget(pixel_coordinates_label, 0, 1, 1, 1)
        pixel_info_box_layout.addWidget(self.pixel_value, 1, 0, 1, 1)
        pixel_info_box_layout.addWidget(pixel_value_label, 1, 1, 1, 1)

        pixel_info_box = QGroupBox(self)
        pixel_info_box.setObjectName("PixelGroupBox")
        pixel_info_box.setTitle("Pixel Information")
        pixel_info_box.setLayout(pixel_info_box_layout)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        info_page_layout = QVBoxLayout(self)
        info_page_layout.setObjectName("InfoPageGrid")
        info_page_layout.addWidget(image_info_box)
        info_page_layout.addWidget(pixel_info_box)
        info_page_layout.addWidget(spacer)


if __name__ == '__main__':

    pass
