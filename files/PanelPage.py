from PyQt5.QtWidgets import QWidget, QGroupBox, QLineEdit, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, QRadioButton, QPushButton, QSpinBox
from PyQt5.QtCore import QRect


class InfoPage(QWidget):

    def __init__(self):
        super(InfoPage, self).__init__()

        # Page settings

        self.setObjectName("InfoPanelPage")
        self.setGeometry(QRect(0, 0, 0, 0))

        # Image info

        self.loaded_image_name = QLineEdit("Loaded Image")
        self.loaded_image_name.setReadOnly(True)
        self.loaded_image_name.setObjectName("ImageNameLine")

        image_name = QLabel("File Name")

        self.loaded_image_resolution = QLineEdit("Image Resolution")
        self.loaded_image_resolution.setReadOnly(True)
        self.loaded_image_resolution.setObjectName("ImageResolutionLine")

        image_resolution = QLabel("Image Resolution")

        self.loaded_image_size = QLineEdit("Image Size")
        self.loaded_image_size.setReadOnly(True)
        self.loaded_image_size.setObjectName("ImageSizeLine")

        image_size = QLabel("Image Size (bytes)")

        image_image_box_layout = QGridLayout()
        image_image_box_layout.addWidget(self.loaded_image_name, 0, 0, 1, 1)
        image_image_box_layout.addWidget(image_name, 0, 1, 1, 1)
        image_image_box_layout.addWidget(
            self.loaded_image_resolution, 1, 0, 1, 1)
        image_image_box_layout.addWidget(image_resolution, 1, 1, 1, 1)
        image_image_box_layout.addWidget(self.loaded_image_size, 2, 0, 1, 1)
        image_image_box_layout.addWidget(image_size, 2, 1, 1, 1)

        image_info_box = QGroupBox()
        image_info_box.setObjectName("InfoGroupBox")
        image_info_box.setTitle("Loaded Image Information")
        image_info_box.setLayout(image_image_box_layout)

        # Pixels info

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

        pixel_info_box = QGroupBox()
        pixel_info_box.setObjectName("PixelGroupBox")
        pixel_info_box.setTitle("Pixel Information")
        pixel_info_box.setLayout(pixel_info_box_layout)

        # Page layout

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        info_page_layout = QVBoxLayout(self)
        info_page_layout.setObjectName("InfoPageGrid")
        info_page_layout.addWidget(image_info_box)
        info_page_layout.addWidget(pixel_info_box)
        info_page_layout.addWidget(spacer)


class KmeansPage(QWidget):

    def __init__(self):
        super(KmeansPage, self).__init__()

        # Page settings

        self.setObjectName("KmeansPanelPage")
        self.setGeometry(QRect(0, 0, 0, 0))

        # Image pick

        self.current_image_rbutton = QRadioButton("Original Image")
        self.current_image_rbutton.setChecked(True)

        self.temp_image_rbutton = QRadioButton("Temporary Image")

        pick_box_layout = QGridLayout()
        pick_box_layout.addWidget(self.current_image_rbutton, 0, 0, 1, 1)
        pick_box_layout.addWidget(self.temp_image_rbutton, 0, 1, 1, 1)

        pick_box = QGroupBox("Imput Image")
        pick_box.setLayout(pick_box_layout)

        # Kmeans settings

        self.kmeans_clusters = QSpinBox()
        self.kmeans_clusters.setRange(2, 20)

        kmeans_clusters_label = QLabel("Number of Clusters")

        self.kmeans_iterations = QSpinBox()
        self.kmeans_iterations.setRange(1, 20)
        self.kmeans_iterations.setValue(10)

        kmeans_iterations_label = QLabel("Number of Iterations")

        kmeans_settings_layout = QGridLayout()
        kmeans_settings_layout.addWidget(self.kmeans_clusters, 0, 0, 1, 1)
        kmeans_settings_layout.addWidget(kmeans_clusters_label, 0, 1, 1, 1)
        kmeans_settings_layout.addWidget(self.kmeans_iterations, 1, 0, 1, 1)
        kmeans_settings_layout.addWidget(kmeans_iterations_label, 1, 1, 1, 1)

        kmeans_settings_box = QGroupBox("Clustering Setings")
        kmeans_settings_box.setLayout(kmeans_settings_layout)

        # Applay kmeans button

        self.kmenas_applay_button = QPushButton("Applay")
        self.kmenas_applay_button.setCheckable(False)
        self.kmenas_applay_button.setObjectName("KmeansApplayButton")

        # Page layout

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        kmeans_page_layout = QVBoxLayout(self)
        kmeans_page_layout.setObjectName("KmeansPageLayout")
        kmeans_page_layout.addWidget(pick_box)
        kmeans_page_layout.addWidget(kmeans_settings_box)
        kmeans_page_layout.addWidget(self.kmenas_applay_button)
        kmeans_page_layout.addWidget(spacer)


class MorphologyPage(QWidget):

    def __init__(self):
        super(MorphologyPage, self).__init__()

        # Page settings

        self.setObjectName("MorphologyPanelPage")
        self.setGeometry(QRect(0, 0, 0, 0))

        # Image pick

        self.current_image_rbutton = QRadioButton("Original Image")
        self.current_image_rbutton.setChecked(True)

        self.temp_image_rbutton = QRadioButton("Temporary Image")

        pick_box_layout = QGridLayout()
        pick_box_layout.addWidget(self.current_image_rbutton, 0, 0, 1, 1)
        pick_box_layout.addWidget(self.temp_image_rbutton, 0, 1, 1, 1)

        pick_box = QGroupBox("Imput Image")
        pick_box.setLayout(pick_box_layout)

        # Applay morphology button

        self.morphology_applay_button = QPushButton("Applay")
        self.morphology_applay_button.setCheckable(False)
        self.morphology_applay_button.setObjectName("MorphologyApplayButton")

        # Page layout

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        morphology_page_layout = QVBoxLayout(self)
        morphology_page_layout.setObjectName("MorphologyPageLayout")
        morphology_page_layout.addWidget(pick_box)
        morphology_page_layout.addWidget(self.morphology_applay_button)
        morphology_page_layout.addWidget(spacer)


if __name__ == '__main__':

    pass
