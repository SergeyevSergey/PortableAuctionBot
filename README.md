<h2>Important</h2>

This telegram bot is written on python 3 using Django framework. This is important to <strong>use python 3</strong> and <strong>install requirements</strong>. If you will not follow instructions it may cause an errors.<br>Database located in db.sqlite3 file of project folder.<br>Main script file of the bot is in "your project/lot/management/commands/bot.py"

<h2>Downloading</h2>

<strong>#1</strong> Clone repository:<br>
```git clone https://github.com/SergeyevSergey/PortableAuctionBot.git```<br>
Alternatively you can copy all files and directories and put everything in new Pycharm project or in a new template and open it in VSCode etc.<br>
<strong>#2</strong> Open settings.py in config directory and change variable TELEGRAM_BOT_TOKEN:<br>
```TELEGRAM BOT TOKEN = "your token"```<br>
Then copy path to the media folder in the project and put it in the variable IMAGE_FOLDER in settings.py:<br>
```IMAGE_FOLDER = "path to media folder"```<br>
Note that you should use "/" instead of backslash symbol in your path.<br>
<strong>#3</strong> Install all packages from requirements.txt:<br>
```pip install -r requirements.txt```<br>
<strong>#4</strong> Create new django admin to manage database:<br>
```python manage.py createsuperuser```<br>
And enter required data.<br>
<strong>#5</strong> Make migrations to save all requirements and Django models:<br>
```python manage.py makemigrations```<br>
```python manage.py migrate```<br>
<strong>#6</strong> Launch bot unsing command:<br>
```python manage.py bot```<br>
Open second terminal and enter command to launch django server on localhost:<br>
```python manage.py runserver```<br>
Then open the link in browser and add "/admin" in the end of url, login and now you can manage your database from here.<br><br>
<strong>Now you can freely use this bot!</strong><br><br>
<h2>Problemshooting</h2><br>
If you will get error related to python interpreter try to use python 3.9 and totally remove venv directory from your project and reinstall it using:<br>
```python -m venv venv```<br>
Then repeat all missed steps of downloading.
