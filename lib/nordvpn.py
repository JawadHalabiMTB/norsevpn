import os, sys, string

import lib.general as general
from lib.conf import configManager

##
# @brief Class for the NordVPN Cli functions
class nordvpn():


    ##
    # @brief    Check Nordvpn installation
    # @details  This interface is used to get if nordvpn-cli is installed on this system
    #
    # @returns  Returns boolish value if nordvpn-cli is installed
    # @retval   False   nordvpn is not installed
    # @retval   True    nordvpn is installed
    def checkInstall(self):
        installed = False
        res = general.getOSString("nordvpn -v")
        if "NordVPN Version" in res:
            installed = True
        return installed

    ##
    # @brief    Check Nordvpn connection
    # @details  This interface is used to get if the user is currently connected to the nordvpn servers
    #
    # @returns  Returns boolish value if nordvpn-cli is connected
    # @retval   False   nordvpn is not connected
    # @retval   True    nordvpn is connected
    def isConnected(self):
        connected = False
        res = general.getOSString("nordvpn status")
        if "Connected" in res:
            connected = True
        return connected

    ## 
    # @public
    # @brief    Connect to the vpn
    # @details  This interface is used to connect to a nordvpn server. 
    #           With the given parameter it can be defined which country and city is used.
    # @note     If country and city are not given then the nordvpn-cli will use the default one.
    #
    # @param    cnt    Wanted country
    # @param    cty    Wanted city
    def connect(self, cnt="", cty=""):
        self.__setSettings(self)        # set the user wanted settings
        general.getOSString("nordvpn c " + cnt + "" + cty)
        return

    ## 
    # @public
    # @brief    Disconnect from the vpn
    # @details  This interface is used to disconnect the nordvpn server. 
    def disconnect(self):
        self.__setDefaultSettings(self)         # return to default settings
        general.getOSString("nordvpn d")
        return

    ## 
    # @public
    # @brief    Status from the vpn
    # @details  This interface is used to disconnect the nordvpn server. 
    def getStatus(self):
        return general.getOSString("nordvpn status")

    def __setSettings(self):
        self.__setBoolSetting(self, "firewall", configManager.getConfig(configManager, "firewall"))
        self.__setBoolSetting(self, "killswitch", configManager.getConfig(configManager, "killswitch"))
        self.__setBoolSetting(self, "cybersec", configManager.getConfig(configManager, "cybersec"))
        self.__setBoolSetting(self, "autoconnect", configManager.getConfig(configManager, "autoconnect"))
        self.__setBoolSetting(self, "obfuscate", configManager.getConfig(configManager, "obfuscate"))
        self.__setBoolSetting(self, "notify", configManager.getConfig(configManager, "notify"))
        self.__setBoolSetting(self, "ipv6", configManager.getConfig(configManager, "ipv6"))
        self.__setBoolSetting(self, "dns", configManager.getConfig(configManager, "dns"))

    def __setDefaultSettings(self):
        self.__setBoolSetting(self, "firewall", True)
        self.__setBoolSetting(self, "killswitch", False)
        self.__setBoolSetting(self, "cybersec", False)
        self.__setBoolSetting(self, "autoconnect", False)
        self.__setBoolSetting(self, "obfuscate", False)
        self.__setBoolSetting(self, "notify", False)
        self.__setBoolSetting(self, "ipv6", False)
        self.__setBoolSetting(self, "dns", False)

    def __setBoolSetting(self, setting, val):
        general.getOSString("nordvpn set " + setting + " "+ str(val))