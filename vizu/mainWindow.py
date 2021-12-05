# imports
import logging
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMessageBox, QTreeWidgetItem, QWidget, QInputDialog, QLineEdit, QFileDialog, QCheckBox

sys.path.append("..")
from lib.nordvpn import nordvpn as nordvpn
from lib.conf import configManager
from vizu.configWindow import configWindow

# UI file
uiFile = "vizu/norsevpn.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(uiFile)


##
# @brief mainWindow class
class mainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    # private vars
    __isConnected = False


    ##
    # @public
    # @brief    Init
    # @details  Initialization of the class
    #
    # @param    self    Object itself
    def __init__(self):
        # create the instance of the Qt window
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.configWidget = configWindow()
        self.setupUi(self)

        # init timer for periodical calls
        self.__init_timer()
        self.__init_textBrowser()

        # button initialization
        self.btn_connect.clicked.connect(self.__btnConnect)
        self.btn_debug.clicked.connect(self.__debug)
        self.btn_config.clicked.connect(self.__btnConfig)
        self.tree_location.itemClicked.connect(self.__locationSelection)

        # load tree view
        configManager.updateLocations(configManager)    # update the locations inside the json
        self.__fillLocationTree()

        logging.info("Installed: " + str(nordvpn.checkInstall(nordvpn)))
        logging.info("Connected: " + str(nordvpn.isConnected(nordvpn)))

    ##
    # @private
    # @brief    Init Timer
    # @details  This private method is used to initialize the timers for the periodical calls
    def __init_timer(self):
        # QTimer for the GUI updater
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000) # time in ms
        self.timer.timeout.connect(self.__update)
        self.timer.start()

        self.cooldownTimer = QtCore.QTimer(self)
        self.cooldownTimer.timeout.connect(self.__cooldownEnd)
        self.cooldownTimer.setInterval(3000) # time in ms
        self.cooldownTimer.setSingleShot(True)  # timer runs only once if startet

    def __init_textBrowser(self):
        self.textBrowser.setAcceptRichText(True)

    ##
    # @private
    # @brief    Updater
    # @details  This private method is called periodically by the QTimer
    @QtCore.pyqtSlot()
    def __update(self):
        # update the private variable
        self.__isConnected = nordvpn.isConnected(nordvpn)

        # update the checkbox
        self.cb_connected.setChecked(self.__isConnected)
        # update the text on the button depending on the connection state
        if self.__isConnected:
            self.btn_connect.setText("Disconnect")
        else:
            self.btn_connect.setText("Connect")
            
        # update the vpn status from console
        self.__updateTextBrowser()

    ##
    # @private
    # @overload closeEvent
    # @brief    Close Window
    # @details  Internal method to close the widget.
    #           If the window should close, the vpn connection gets disconnected.
    def closeEvent(self, event):
        # show message to get if the user wants to save
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure you want to quit? VPN will disconnect.",
            QMessageBox.Close | QMessageBox.Cancel,
            QMessageBox.Cancel)

        # get the user input
        if reply == QMessageBox.Close:
            nordvpn.disconnect(nordvpn)     # disconnect the vpn
            # close all sub windows and this window
            if self.configWidget.isVisible():
                self.configWidget.close()
            self.close()
        else:
            event.ignore()
            pass

    ##
    # @private
    # @brief    Connect button click event
    # @details  This private method is called if the user clicks on the connect/disconnect buttin
    #           depending on the vpn state the nordvpn module is called to connect or disconnect
    def __btnConnect(self):
        # call interface depending on the vpn status
        if self.__isConnected:
            nordvpn.disconnect(nordvpn)
        else:
            nordvpn.connect( nordvpn, 
                             configManager.getConfig(configManager, "selected_country"),
                             configManager.getConfig(configManager, "selected_city"))
            self.__cooldownStart()

    def __btnConfig(self):
        self.configWidget.onShow()

    def __debug(self):
        logging.info("Debug")
        logging.info(configManager.updateLocations(configManager))
    
    def __updateTextBrowser(self):
        htmlText = nordvpn.getStatus(nordvpn)
        htmlText = htmlText.replace("\t", "")
        htmlText = htmlText.replace("-", "")
        htmlText = htmlText.replace("\n", "<br>")
        self.textBrowser.clearHistory()
        self.textBrowser.setHtml(htmlText)

    def __fillLocationTree(self):
        data = configManager.getLocationDict(configManager)
        items = []
        for key, values in data.items():
            item = QTreeWidgetItem([key])
            for value in values:
                child = QTreeWidgetItem(value)
                item.addChild(child)
            items.append(item)
        self.tree_location.insertTopLevelItems(0, items)

    def __locationSelection(self):
        item = self.tree_location.currentItem()
        par = item.parent()

        if type(par) is not QTreeWidgetItem:
            cnt = item.text(0)
            cty = ""
        else:
            cnt = par.text(0)
            cty = item.text(0)
        configManager.setConfig(configManager, "selected_country",cnt)
        configManager.setConfig(configManager, "selected_city",cty)
        if self.__isConnected:
            # vpn is currently connected, change location of the fly
            nordvpn.connect( nordvpn, 
                            cnt,
                            cty)
            self.__cooldownStart()

    def __cooldownStart(self):
        logging.info("Cooldown Start")
        self.cooldownTimer.start()

        # disable interactions
        self.tree_location.setDisabled(True)
        self.btn_connect.setDisabled(True)

    def __cooldownEnd(self):
        logging.info("CoolDown End")

        # Enable all interactions again
        self.tree_location.setDisabled(False)
        self.btn_connect.setDisabled(False)


