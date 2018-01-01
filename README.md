## V2Ray-shell [alpha-version](https://en.wiktionary.org/wiki/alpha_version)

### Project description
   A [GUI](https://en.wikipedia.org/wiki/Graphical_user_interface) for [V2Ray-core](https://github.com/v2ray/v2ray-core).<br>
   This [script](https://en.wikipedia.org/wiki/Scripting_language) is written in [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro). It is still under test and the basic functions have been completed.<br>And PyQt is available for Windows, UNIX/Linux, Mac OS X and the Sharp Zaurus.<br>That means you can use this script on many platforms.
   
### Before use V2Ray-shell
   1. [install Python](https://tutorial.djangogirls.org/en/python_installation/) with pip. ([pip](https://pip.pypa.io/en/stable/), which can download and install other Python packages.) <br>Python version higher than 3.5 is recommended.
   2. [install PyQt5](http://pyqt.sourceforge.net/Docs/PyQt5/installation.html) in [command line](https://tutorial.djangogirls.org/en/intro_to_command_line/) as [root](http://www.linfo.org/root.html) or [administrator](https://technet.microsoft.com/en-us/library/cc947813%28v%3Dws.10%29.aspx).(Of course you can also use this script on the command line to install PyQt5 as root or administrator permission.)
   > `pip3 install PyQt5`
   3. in UNIX/Linux, Mac OS X make sure scripts have [execute permission](https://superuser.com/questions/117704/what-does-the-execute-permission-do). such like below: 
   > `chmod +x v2ray-shell.pyw ./src/bridgehouse/bridge.py`

### How use it
   1. run v2ray-shell.pyw
   2. in the system tray find v2ray-shell icon, right click show panel.
   3. in the v2ray-shell panel, find the menu "options->Preferences", set v2ray file path. and click "aplly and close" button
   4. in the v2ray-shell panel, find the menu "File->Add V2Ray-core config file", and add the v2ray-core's config.json file to panel.
   5. in the v2ray-shell panel, click the v2ray-shell icon (a darkgreen rocket), enable this config.json.
   6. and find the black triangle, click it to run v2ray-core.
   7. in the v2ray-shell panel, find the menu "File->Save V2Ray-shell config file", click it to save v2ray-shell config file.

### LICENSE
see the LICENSE file details.