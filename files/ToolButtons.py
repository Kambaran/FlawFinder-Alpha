from res import resources
import sys

from PyQt5.QtWidgets import QApplication, QToolButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

app = QApplication(sys.argv)


bw = 44                                # buttonWidth
iw = int(bw*1.1)                       # iconWidth


# Fit Button
_fininview = QToolButton()
_fininview.setText('Fit')
_fininview.setCheckable(False)
_fininview.setChecked(False)
_fininview.setStyleSheet("border :1px solid white")
_fininview.setFixedSize(bw, bw)
_fininview.setIconSize(QSize(iw, iw))
_fininview.setIcon(QIcon(":/icons/fit.png"))
_fininview.setToolTip("Fit button resizes image view to the scene size")

# Drag Button
_dragbutton = QToolButton()
_dragbutton.setText('Drag')
_dragbutton.setCheckable(False)
_dragbutton.setChecked(False)
_dragbutton.setStyleSheet("border :1px solid white")
_dragbutton.setFixedSize(bw, bw)
_dragbutton.setIconSize(QSize(iw, iw))
_dragbutton.setIcon(QIcon(":/icons/drag.png"))
_dragbutton.setToolTip("Drag button alows pannig image over the scene")

# Rotate Clockwise Button
_rotateclockbutton = QToolButton()
_rotateclockbutton.setText('Rotate Clockwise')
_rotateclockbutton.setCheckable(False)
_rotateclockbutton.setChecked(False)
_rotateclockbutton.setStyleSheet("border :1px solid white")
_rotateclockbutton.setFixedSize(bw, bw)
_rotateclockbutton.setIconSize(QSize(iw, iw))
_rotateclockbutton.setIcon(QIcon(":/icons/clock.png"))
_rotateclockbutton.setToolTip("Rotate image 90 degrees clockweise")

# Rotate AntiClockwise Button
_rotateanticlockbutton = QToolButton()
_rotateanticlockbutton.setText('Rotate Anti-Clockwise')
_rotateanticlockbutton.setCheckable(False)
_rotateanticlockbutton.setChecked(False)
_rotateanticlockbutton.setStyleSheet("border :1px solid white")
_rotateanticlockbutton.setFixedSize(bw, bw)
_rotateanticlockbutton.setIconSize(QSize(iw, iw))
_rotateanticlockbutton.setIcon(QIcon(":/icons/anticlock.png"))
_rotateanticlockbutton.setToolTip("Rotate image 90 degrees anticlockweise")


if __name__ == '__main__':

    sys.exit(app.exec())
