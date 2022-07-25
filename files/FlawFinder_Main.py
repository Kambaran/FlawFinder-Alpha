import sys
import os
import cv2 as cv
import qdarktheme
import numpy as np

from PIL import Image as im

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

import ToolButtons
from ToolPanel import ToolPanel


# Fonts


class MyFont(object):

    def __init__(self):

        # Calibri, Size 16
        self.calibri_16 = qtg.QFont()
        self.calibri_16.setFamily("Calibri")
        self.calibri_16.setPointSize(16)
        self.calibri_16.setBold(True)
        self.calibri_16.setWeight(80)

        # Calibri, Size 12
        self.calibri_12 = qtg.QFont()
        self.calibri_12.setFamily("Calibri")
        self.calibri_12.setPointSize(12)
        self.calibri_12.setBold(True)
        self.calibri_12.setWeight(65)

# Image Viewer


class ImageViewer(qtw.QGraphicsView):
    photoClicked = qtc.pyqtSignal(qtc.QPoint)
    clickRelesd = qtc.pyqtSignal(qtc.QPoint)

    def __init__(self, parent):
        super(ImageViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = qtw.QGraphicsScene(self)
        self._photo = qtw.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(qtw.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(qtw.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(qtg.QBrush(qtg.QColor(30, 30, 30)))
        self.setFrameShape(qtw.QFrame.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = qtc.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(qtc.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(qtw.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(qtw.QGraphicsView.NoDrag)
            self._photo.setPixmap(qtg.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == qtw.QGraphicsView.ScrollHandDrag:
            self.setDragMode(qtw.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(qtw.QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
        super(ImageViewer, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self._photo.isUnderMouse():
            self.clickRelesd.emit(self.mapToScene(event.pos()).toPoint())

        return super().mouseReleaseEvent(event)

# Main Aplication Class


class AppWindow (qtw.QMainWindow, MyFont):

    _temporary_position = []

    # UI Settings
    def __init__(self):
        super(AppWindow, self).__init__()

        # Main Window
        self.setWindowTitle("Flaw Finder")
        self.resize(1920, 1080)
        self.main_dispaly = qtw.QWidget()

        """Create Display and Docks"""
        # Image Display
        self.image_dispaly = ImageViewer(self)
        self.image_dispaly.setGeometry(qtc.QRect(0, 0, 40, 100))
        self.image_dispaly.photoClicked.connect(self.photoClicked)
        # self.image_dispaly.photoClicked.connect(self.grabCut)
        # self.image_dispaly.clickRelesd.connect(self.addRoiLable)

        # List Display
        self.operations = qtw.QTableView()
        self.operations.setObjectName("Operations Table")
        self.operations.setEnabled(True)

        # Tool Panel
        self.tool_panel = ToolPanel()
        self.tool_panel.page_1.kmenas_applay_button.clicked.connect(
            self.kMeans)

        # Left Dockable
        self.left_dock = qtw.QDockWidget("ToolBox", self)
        self.left_dock.setFont(self.calibri_16)
        self.left_dock.setWidget(self.tool_panel)
        self.left_dock.setFloating(False)
        self.left_dock.setMinimumWidth(320)

        # Right Dockable
        self.right_dock = qtw.QDockWidget("Operations Log", self)
        self.right_dock.setFont(self.calibri_16)
        self.right_dock.setWidget(self.operations)
        self.right_dock.setFloating(False)

        # Docks Position
        self.setCentralWidget(self.image_dispaly)
        self.addDockWidget(qtc.Qt.RightDockWidgetArea, self.right_dock)
        self.addDockWidget(qtc.Qt.LeftDockWidgetArea, self.left_dock)

        # Menubar Construct
        menubar = self.menuBar()
        menubar.setFont(self.calibri_12)
        file_menu = menubar.addMenu('File')
        file_menu.addAction('Open', self.openFile)
        file_menu.addAction('Save', self.saveFile)
        file_menu.addSeparator()
        file_menu.addAction('Exit', self.close)
        file_menu = menubar.addMenu("Help")
        file_menu.addAction("Get Started")
        file_menu.addSeparator()
        file_menu.addAction("About")

        self.BuildToolbar()

        # End UI code
        self.show()

    # Tool Bar

    def BuildToolbar(self):

        # Call Buttons
        fitbutton = ToolButtons._fininview
        fitbutton.clicked.connect(self.FitImage)

        dragbutton = ToolButtons._dragbutton
        dragbutton.clicked.connect(self.SceneDragMode)

        rotatebutton = ToolButtons._rotateclockbutton
        rotatebutton.clicked.connect(self.RotateClockwise)

        rotateantibutton = ToolButtons._rotateanticlockbutton
        rotateantibutton.clicked.connect(self.RotateAntiClockwise)

        # Add Buttons
        toolbar = qtw.QToolBar()
        toolbar.addWidget(fitbutton)
        toolbar.addWidget(dragbutton)
        toolbar.addWidget(rotatebutton)
        toolbar.addWidget(rotateantibutton)

        # Add Toolbar
        self.addToolBar(toolbar)

    """____________App Functions____________"""

    # Menu - File - Open
    def openFile(self):
        fname = qtw.QFileDialog.getOpenFileName(
            self, 'Choose image', 'c:\\', 'Image files (*.png *.jpg *.jpeg)')
        if not fname[0]:
            pass
        else:
            size = os.path.getsize(fname[0])
            name = os.path.basename(fname[0])
            image = cv.imread(fname[0])

            data = im.fromarray(image)
            data.save('temp_image_original.png')

            if fname[0].lower().endswith(('.tiff', '.bmp')):
                sys.exit()

            self.image_dispaly.setPhoto(qtg.QPixmap(fname[0]))
            self.tool_panel.page_0.loaded_image_name.setText(str(name))
            self.tool_panel.page_0.loaded_image_resolution.setText(
                str(image.shape))
            self.tool_panel.page_0.loaded_image_size.setText(str(size))

    # Menu - File - Save
    def saveFile(self):
        filePath, _ = qtw.QFileDialog.getSaveFileName(self, "Save Image", "",
                                                      "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if filePath == "":
            return
        pixmap = qtg.QPixmap(self.image_dispaly.viewport().size())
        self.image_dispaly.viewport().render(pixmap)
        pixmap.save(filePath)
    """
    # Grayscale Conversion
    def convertToGray(self):

        image = cv.imread('files/temp_image_original.png')

        if image == None:
            image = cv.imread('temp_image_original.png')
        else:
            pass

        image_RGB = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        data = im.fromarray(image_RGB)
        data.save('temp_image_grayscale.png')
        self.image_dispaly.setPhoto(qtg.QPixmap('temp_image_grayscale.png'))
    """

    def kMeans(self):

        if self.tool_panel.page_1.current_image_rbutton.isChecked():
            image = cv.imread('temp_image_original.png')
        else:
            image = cv.imread('temp_image_modified.png')
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

        if not image.all() == None:
            clusters = self.tool_panel.page_1.kmeans_clusters.value()
            iterations = self.tool_panel.page_1.kmeans_clusters.value()

            array = image.reshape((-1, 3))
            # Convert pixels to float32
            array = np.float32(array)

            # Function
            criteria = (cv.TERM_CRITERIA_EPS +
                        cv.TERM_CRITERIA_MAX_ITER, iterations, 1.0)
            ret, label, center = cv.kmeans(
                array, clusters, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)

            # Convert to unit8, assemble
            center = np.uint8(center)
            centred = center[label.flatten()]
            output = centred.reshape((image.shape))

            # Save image
            data = im.fromarray(output)
            data.save('temp_image_modified.png')
            self.image_dispaly.setPhoto(qtg.QPixmap('temp_image_modified.png'))
        else:
            # Error message
            message = qtw.QMessageBox()
            message.setIcon(qtw.QMessageBox.Warning)
            message.setText("Assertion Error:")
            message.setInformativeText(
                "Function was unable to assert image values - Image variable is empty. Try with original image.")
            message.setWindowTitle("Error")
            message.exec_()
    """
    def grabCut(self, pos):

        if self.image_dispaly.dragMode() == qtw.QGraphicsView.NoDrag:
            if self.pushButton4.isChecked():
                print(pos.x()-100, pos.y()-100, 200, 200)
                image = cv.imread('temp_image_original.png')
                #
                print('grab')

                img_ivert = cv.bitwise_not(image)
                mask = np.zeros(img_ivert.shape[:2], np.uint8)

                # Background and foreground models
                bgdModel = np.zeros((1, 65), np.float64)
                fgdModel = np.zeros((1, 65), np.float64)
                # Rectangle of semi ROI - manual select
                rect = (pos.x()-100, pos.y()-100, 200, 200)

                # start sectioning
                cv.grabCut(img_ivert, mask, rect, bgdModel,
                           fgdModel, 20, cv.GC_INIT_WITH_RECT)

                # Definite background and probable background
                mask2 = np.where((mask == 2) | (
                    mask == 0), 0, 1).astype('uint8')
                image_grabcut = img_ivert*mask2[:, :, np.newaxis]

                # Save image
                data = im.fromarray(image_grabcut)
                data.save('temp_image_grabcut.png')
                self.image_dispaly.setPhoto(
                    qtg.QPixmap('temp_image_grabcut.png'))
    """

    # Clicked
    def photoClicked(self, pos):
        if self.image_dispaly.dragMode() == qtw.QGraphicsView.NoDrag:
            self.tool_panel.page_0.pixel_coordinates.setText(
                '%d, %d' % (pos.x(), pos.y()))

            print(self._temporary_position)
            self._temporary_position.append(pos.x())
            self._temporary_position.append(pos.y())

            print('%d, %d' % (pos.x(), pos.y()))

            image = None
            image = cv.imread('temp_image_original.png')

            if image.any():
                valueblue = image[pos.y(), pos.x(), 0]
                valuegreen = image[pos.y(), pos.x(), 1]
                valuered = image[pos.y(), pos.x(), 2]
                self.tool_panel.page_0.pixel_value.setText(
                    '%d, %d, %d' % (valuegreen, valueblue, valuered))
            else:
                pass
    """
    def addRoiLable(self, pos):

        flaw_frame = qtg.QPen()
        flaw_frame.setStyle(qtc.Qt.DashLine)
        flaw_frame.setWidth(3)
        flaw_frame.setBrush(qtc.Qt.red)
        flaw_frame.setCapStyle(qtc.Qt.RoundCap)
        flaw_frame.setJoinStyle(qtc.Qt.RoundJoin)

        flaw_description = qtg.QBrush()
        flaw_description.setStyle(qtc.Qt.SolidPattern)
        flaw_description.setColor(qtc.Qt.red)

        if self.image_dispaly.dragMode() == qtw.QGraphicsView.NoDrag:
            if self.pushButton3.isChecked():
                self.image_dispaly._scene.addRect(
                    pos.x()-100, pos.y()-100, 200, 200, flaw_frame)
                self.image_dispaly._scene.addRect(
                    pos.x()+100, pos.y()-100, 200, 200, qtg.QPen(), flaw_description)

                #
                labelka = qtw.QGraphicsSimpleTextItem()
                labelka.setPos(pos.x()+100, pos.y())
                labelka.setText("Labelka")
                self.image_dispaly._scene.addItem(labelka)
    """
    """Toolbar Functions"""

    # Scene - FitIn
    def FitImage(self):
        self.image_dispaly.fitInView()

    # Scene - Dragmode
    def SceneDragMode(self):
        self.image_dispaly.toggleDragMode()

    # Scene - Rotate Right
    def RotateClockwise(self):
        self.image_dispaly.rotate(90)

    # Secene - Rotate Left
    def RotateAntiClockwise(self):
        self.image_dispaly.rotate(-90)


if __name__ == '__main__':

    app = qtw.QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet("dark", "rounded"))

    FF = AppWindow()

    sys.exit(app.exec())
