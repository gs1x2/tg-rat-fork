# TGRat

|DISCLAIMER|
|-------------------------------------------------|
By using TG Rat, you agree that you hold responsibility and accountability of any consequences caused by your actions. Furthermore, the program was developed for educational purposes only


## 📌Available Commands
Use "<b>/start</b>" to show list of available commands.
| Commands                             | Action Performs                               |
|--------------------------------------|-----------------------------------------------|
| 📟  Get IP                            | Gets Public IP Information                    |
| 📸  Get Screenshot                    | Gets screenshot                               |
| 📷  Get Pic From Webcam               | Takes picture from webcam                     |
| 👂  Eavesdrop                         | To record audio from the mic with a duration of your choice         |
| 🗣️  Text To Speech on client          | To make the given text to speak               |
| 💬  Send Message To Client            | To open a chat between attacker and target PC |
| 🖥️  Get System Information            | To get system information                     |
| 🗊 Get Specific File                   | To get a single file from victim PC           |
| 🔑  Perform Shell Commands            | To run shell commands                         |
| 🌐  Open Website                      | To open a given website                       |
| 🖲️  Move mouse randomly                | Moves the mouse cursor randomly               |
| ⌨️  Type String                       | To type the given string                      |
| ⚠️  Show Alert Box with given message | Show a warning MessageBox with given message  |
| 📋  Get Clipboard                     | To get the contents in the clipboard          |
| 🗝️  Get Wifi Password                 | To get stored wifi passwords                  |
| 📶 Get Wi-Fi Access Points            | Gets WI-FI Access Points with BSSID (Can be used to get location!)|
| 🗃️ File management          | Complete access to all files on the victim's PC|
| 🗃️ Task management          | Complete access to all processes on the victim's PC|
| 🕑 Export Browser History             | Export Chrome/Edge browser history as raw file or archive |
| ⌨️  Get Keylogger Log                 | Download or clear keylogger log file                     |
| 🟢 Enable Keylogger / 🔴 Disable Keylogger | Enable or disable keylogger in real time             |


## 📎 Features

* Alert on the bot as soon as the victim turns on the computer or opens the virus
* The rat automatically copies itself to another folder and adds itself to the PC startup
* The rat is fully controllable by the telegram bot
* Updated to the latest library versions
* Export browser history (Chrome/Edge) as raw file or archive
* Keylogger:
  * Logs all keystrokes (with layout awareness, readable text)
  * Log file is persistent and survives reboots
  * Log file size limit (configurable, default 30MB)
  * Download or clear log file from bot menu
  * Enable/disable keylogger from bot menu
  * Log format: system keys and text on separate lines, timestamps for inactivity, layout changes marked
  * Automatic notification in bot if new activity appears after a long pause (interval configurable)


## How to setup
First install the necessary libraries using this command

<b>pip install -r requirements.txt</b>

You will need to create a new Telegram BOT follow the steps here to create one! [Follow the steps](https://core.telegram.org/bots#6-botfather)

Before running this program edit the config.py file
* Replace "TOKEN HERE" with your Telegram Bot API key
* Replace "CHATID" with your Telegram Bot's Chat ID.

## Contact

💬 https://t.me/primogirone

thanks to henry-richard7 <3 for the base
