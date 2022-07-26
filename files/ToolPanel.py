from PyQt5.QtWidgets import QWidget, QToolBox
from PyQt5.QtCore import QRect


from PanelPage import InfoPage, KmeansPage, MorphologyPage


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

        self.page_0 = InfoPage()
        self.page_1 = KmeansPage()
        self.page_2 = MorphologyPage()
        self.page_3 = ToolPanelPage()
        self.page_4 = ToolPanelPage()
        self.page_5 = ToolPanelPage()

        self.pages = [
            self.page_0, 
            self.page_1, 
            self.page_2,
            self.page_3, 
            self.page_4, 
            self.page_5
        ]

        page_name = [
            "Image Information",
            "Color Quantization",
            "Morphology",
            "GrabCut Algorithm",
            "Simple Blob Detector",
            "Labeling",
        ]

        self.toolbox_page = {i: j for (j, i) in zip(self.pages, page_name)}
        for keys, vals in self.toolbox_page.items():
            self.addItem(vals, keys)


if __name__ == '__main__':

    pass
