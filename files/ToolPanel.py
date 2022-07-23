import sys

from PyQt5.QtWidgets import QWidget, QToolBox
from PyQt5.QtCore import QRect

from PanelPage import InfoPage


class ToolPanelPage(QWidget):

    def __init__(self):
        super(ToolPanelPage, self).__init__()

        self.setGeometry(QRect(0, 0, 0, 0))
        self.setObjectName("ToolPanelPage")


class ToolPanel(QToolBox):

    def __init__(self):
        super(ToolPanel, self).__init__()

        self.setObjectName("ToolBox")
        self.setEnabled(True)

        self.pages = [InfoPage(), ToolPanelPage(), ToolPanelPage(
        ), ToolPanelPage(), ToolPanelPage(), ToolPanelPage()]

        page_name = [
            "Image Information",
            "Color Quantization",
            "Morphology",
            "GrabCut Algorithm",
            "Simple Blob Detector",
            "Labeling",
        ]

        """Alternative
        self.toolbox_page = {n: pages for n in page_name}
        for keys, vals in self.toolbox_page.items():
            self.addItem(vals, keys)
        """

        self.toolbox_page = {i: j for (j, i) in zip(self.pages, page_name)}
        for keys, vals in self.toolbox_page.items():
            self.addItem(vals, keys)


if __name__ == '__main__':

    pass
