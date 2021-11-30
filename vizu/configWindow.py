import os
import sys
from PyQt5.QtWidgets import QLabel, QMessageBox, QVBoxLayout, QWidget, QCheckBox
from PyQt5 import QtCore, uic

sys.path.append("..")
from lib.conf import configManager


# UI file
ui_path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(ui_path,"config.ui")

##
# @brief Class for the Configuration Window
class configWindow(QWidget):

    ##
    # @public
    # @brief    Init
    # @details  Class gets initialized
    def __init__(self):
        super(configWindow, self).__init__()
        uic.loadUi(uiFile, self)

        self.btn_close.clicked.connect(self.closeEvent)
        self.btn_save.clicked.connect(self.saveConfig)

    ## 
    # @public
    # @brief    On Show
    # @details  Interface to show the widget. This is needed
    #           to update the UI/UX depending on the configuration
    #           before the user sees the window.
    def onShow(self):
        print("Show")
        self.loadConfig()
        self.show()

    ##
    # @public 
    # @brief    Load Configuration
    # @details  This interface is ued to load the configuration
    #           from the config file and show it to the user
    #           (configFile -> UI)
    def loadConfig(self):
        print("Load Config")
        self.slid_firewall.setValue(configManager.getConfig(configManager, "firewall"))
        self.slid_killSwitch.setValue(configManager.getConfig(configManager, "killSwitch"))
        self.slid_cyberSec.setValue(configManager.getConfig(configManager, "cyberSec"))
        self.slid_obfuscate.setValue(configManager.getConfig(configManager, "obfuscate"))
        self.slid_notify.setValue(configManager.getConfig(configManager, "notify"))
        self.slid_autoConnect.setValue(configManager.getConfig(configManager, "autoConnect"))
        self.slid_ipv6.setValue(configManager.getConfig(configManager, "ipv6"))
        self.slid_dns.setValue(configManager.getConfig(configManager, "dns"))
        return

    ##
    # @public 
    # @brief    Save Configuration
    # @details  This interface is ued to save the configuration
    #           from the UI to the config file
    #           (UI -> configFile)
    def saveConfig(self):
        print("Save Config")
        configManager.setConfig( configManager,
                                 "firewall",
                                 self.__getSetting(self.slid_firewall.value()) )
        configManager.setConfig( configManager,
                                 "killSwitch",
                                 self.__getSetting(self.slid_killSwitch.value()) )
        configManager.setConfig( configManager,
                                 "cyberSec",
                                 self.__getSetting(self.slid_cyberSec.value()) )
        configManager.setConfig( configManager,
                                 "obfuscate",
                                 self.__getSetting(self.slid_obfuscate.value()) )
        configManager.setConfig( configManager,
                                 "notify",
                                 self.__getSetting(self.slid_notify.value()) )
        configManager.setConfig( configManager,
                                 "autoConnect",
                                 self.__getSetting(self.slid_autoConnect.value()) )
        configManager.setConfig( configManager,
                                 "ipv6",
                                 self.__getSetting(self.slid_ipv6.value()) )
        configManager.setConfig( configManager,
                                 "dns",
                                 self.__getSetting(self.slid_dns.value()) )
        return

    ##
    # @private
    # @overload closeEvent
    # @brief    Close Window
    # @details  Internal method to close the widget.
    #           The user can decide if the configuration should be saved, just closed
    #           or return to the config window.
    def closeEvent(self, event):
        # show message to get if the user wants to save
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure you want to quit? Any unsaved work will be lost.",
            QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel,
            QMessageBox.Save)

        # get the user input
        if reply == QMessageBox.Close:
            self.close()
        elif reply == QMessageBox.Save:
            self.saveConfig()
            self.close
        else:
            event.ignore()
            pass

    ##
    # @brief    Get Value from string
    def __getSetting(self, sliderVal):
        if sliderVal > 0:
            return True
        else:
            return False

