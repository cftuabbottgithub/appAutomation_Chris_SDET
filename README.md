# appAutomation_Chris_SDET

## Setup

### Install Appium
Use the command ```npm i --location=global appium``` to install (node.js should be installed first)

### Install the Appium Python client and HTMLTestRunner
Use the command ```pip install Appium-Python-Client``` to install the Python client.

Use the command ```pip install HTMLTestRunner-rv``` to install HTMLTestRunner which generates the HTML output report.

### Running Appium server
In the terminal, use the command ```appium --allow-insecure chromedriver_autodownload```.
This allows Appium to automatically download chromedriver when interacting with a WebView.

The server should be running at the default port (4723).

### Running the Android emulator and installing the apk file
After the Android virtual device is created, launch the emulator from Android Studio device manager.

To install the apk file onto the device, drag the apk onto the emulator window.

Move the app icon onto the device home screen as shown (I was having some issues launching the app from Appium directly)

![Device Home Screen](https://github.com/cftuabbottgithub/appAutomation_Chris_SDET/blob/main/emulator_screenshot.png)
### Running the script
Use the command ```python general_store_test.py``` to run the script from the main project directory.

### Screen recording
<a href="https://drive.google.com/file/d/1nEpM84pVOH9_1llrdNZ1CcT7dqFR2qnt/view?usp=share_link">Video</a>
