import sys
import cv2 as cv
import qdarktheme
import numpy as np

from PIL import Image as im

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

import ToolButtons

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

# Main Aplication Class
class AppWindow (qtw.QMainWindow, MyFont):

    operations_table = ['x','y']

    # UI Settings
    def __init__(self):
        super(AppWindow, self).__init__()

        # Main Window
        self.setWindowTitle("Flow Finder")
        self.resize(1920,1080)
        self.main_dispaly = qtw.QWidget()

        """Create Display and Docks"""
        # Image Display
        self.image_dispaly = ImageViewer(self)
        self.image_dispaly.setGeometry(qtc.QRect(0 ,0, 40, 100))
        self.image_dispaly.photoClicked.connect(self.photoClicked)
        self.image_dispaly.photoClicked.connect(self.addRoiLable)

        # Tool Panel - Dock Construct 
        self.tool_panel = qtw.QToolBox()
        self.tool_panel.setObjectName("ToolBox")
        self.tool_panel.setEnabled(True)     
        self.tool_panel.setFont(self.calibri_16)

        # List Display - Dock Construct
        self.operations = qtw.QTableView()
        self.operations.setObjectName("Operations Table")
        self.operations.setEnabled(True)  

        # Tool Panel - Page 1
        self.page_1 = qtw.QWidget()
        self.page_1.setGeometry(qtc.QRect(0, 0, 0, 0))
        self.page_1.setObjectName("Page 1")
        #self.page_1_grid = qtw.QGridLayout(self.page)

        # Tool Panel - Page 2
        self.page_2 = qtw.QWidget()
        self.page_2.setGeometry(qtc.QRect(0, 0, 0, 0))
        self.page_2.setObjectName("Page 2")

        # Tool Panel - Adding Pages
        self.tool_panel.addItem(self.page_1, "Basic Operations")
        self.tool_panel.addItem(self.page_2, "Algorithms")

        # Left Dockable
        self.left_dock = qtw.QDockWidget("ToolBox", self)
        self.left_dock.setFont(self.calibri_16)
        self.left_dock.setWidget(self.tool_panel)
        self.left_dock.setFloating(False)
        self.left_dock.setMinimumWidth(300)

        # Right Dockable
        self.right_dock = qtw.QDockWidget("Operation Log", self)
        self.right_dock.setFont(self.calibri_16)
        self.right_dock.setWidget(self.operations)
        self.right_dock.setFloating(False)

        # Docks Position
        self.setCentralWidget(self.image_dispaly)
        self.addDockWidget(qtc.Qt.RightDockWidgetArea, self.right_dock)
        self.addDockWidget(qtc.Qt.LeftDockWidgetArea, self.left_dock)

        # Main Layout
        #layout = qtw.QGridLayout()
        #self.setLayout(layout)

        """Boxes, Buttons, Sliders, etc."""
        # Page 1 Boxes

        # BOX 1
        self.color_box = qtw.QGroupBox(self.page_1)
        self.color_box.setObjectName("color box")
        self.color_box.setTitle("Color based operations")
        self.color_box.setFont(self.calibri_12)
        
        self.pushButton = qtw.QPushButton("Aply Grayscale")
        self.pushButton.clicked.connect(self.convertToGray)
        self.pushButton.setObjectName("pushButton")

        self.pushButton2 = qtw.QPushButton("Show pixel info")
        self.pushButton2.setCheckable(True)
        self.pushButton2.setChecked(False)
        self.pushButton2.clicked.connect(self.SceneDragMode)
        self.pushButton2.setObjectName("pushButton2")

        self.pixPosInfo = qtw.QLineEdit("Position Info")
        self.pixPosInfo.setReadOnly(True)
        self.pixPosInfo.setObjectName("Position info")

        self.pixValueInfo = qtw.QLineEdit("Value Info")
        self.pixValueInfo.setReadOnly(True)
        self.pixValueInfo.setObjectName("Value info")

        self.color_box_grid = qtw.QVBoxLayout()
        self.color_box_grid.addWidget(self.pushButton)
        self.color_box_grid.addWidget(self.pushButton2)
        self.color_box_grid.addWidget(self.pixPosInfo)
        self.color_box_grid.addWidget(self.pixValueInfo)
        self.color_box_grid.addStretch(1)
        self.color_box.setLayout(self.color_box_grid)

        # BOX 2
        self.box2 = qtw.QGroupBox(self.page_1)
        self.box2.setObjectName("Box")
        self.box2.setTitle("Based operations")
        self.box2.setFont(self.calibri_12)

        self.pushButton3 = qtw.QPushButton("Show Grayscale3")
        self.pushButton3.setCheckable(True)
        self.pushButton3.setChecked(False)
        self.pushButton3.setObjectName("pushButton3")

        self.pushButton4 = qtw.QPushButton("Show Grayscale4")
        self.pushButton4.clicked.connect(self.convertToGray)
        self.pushButton4.setObjectName("pushButton4")

        self.box2_grid = qtw.QVBoxLayout()
        self.box2_grid.addWidget(self.pushButton3)
        self.box2_grid.addWidget(self.pushButton4)
        self.box2_grid.addStretch(1)
        self.box2.setLayout(self.box2_grid)

        self.page_1_grid = qtw.QGridLayout(self.page_1)
        self.page_1_grid.setObjectName("Page 1 Grid")
        self.page_1_grid.addWidget(self.color_box, 1, 1)
        self.page_1_grid.addWidget(self.box2,2,1)

        # Menubar Construct
        menubar = self.menuBar()
        menubar.setFont(self.calibri_12)
        file_menu = menubar.addMenu('File')
        file_menu.addAction('Open', self.openFile)
        file_menu.addAction('Save')
        file_menu.addSeparator()
        file_menu.addAction('Exit',self.close)
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
        fname = qtw.QFileDialog.getOpenFileName(self, 'Choose image', 'c:\\','Image files (*.png *.jpg *.jpeg)')
        if not fname[0]:
            pass
        else:
            data = im.fromarray(cv.imread(fname[0]))
            data.save('temp_image.png')
            if fname[0].lower().endswith(('.tiff', '.bmp')):
                sys.exit()
            self.image_dispaly.setPhoto(qtg.QPixmap(fname[0]))
    
    # Grayscale Conversion
    def convertToGray(self):
        
        image = cv.imread('files/temp_image.png')

        if image == None:
            image = cv.imread('temp_image.png')
        else:
            pass

        image_RGB = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        data = im.fromarray(image_RGB)
        data.save('temp_image.png')
        self.image_dispaly.setPhoto(qtg.QPixmap('temp_image.png'))
        
    # Clicked
    def photoClicked(self, pos):
        if self.image_dispaly.dragMode()  == qtw.QGraphicsView.NoDrag:
            self.pixPosInfo.setText('%d, %d' % (pos.x(), pos.y()))

            image = None

            if image == None:
                image = cv.imread('temp_image.png')
                valueblue = image[pos.y(),pos.x(),0]
                valuegreen = image[pos.y(),pos.x(),1]
                valuered = image[pos.y(),pos.x(),2]
            else:
                pass

            self.pixValueInfo.setText('%d, %d, %d' % (valuegreen,valueblue,valuered))


    def addRoiLable(self, pos):
        if self.image_dispaly.dragMode()  == qtw.QGraphicsView.NoDrag:     
            if self.pushButton3.isChecked():
                print("Hey")
                print(pos.x(), pos.y())
                print('%d, %d' % (pos.x(), pos.y()))
                self.image_dispaly._scene.addRect(pos.x(),pos.y(),200,200)

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
    app.setStyleSheet(qdarktheme.load_stylesheet("dark","rounded"))

    FF = AppWindow()
  
    sys.exit(app.exec())