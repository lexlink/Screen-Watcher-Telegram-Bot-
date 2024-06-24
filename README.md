<p># Screen Manager Telegram Bot</p>
<p>This bot helps you manage your screen sessions in Linux. You can use it to list your screens, run scripts in a screen session, and check the status of your screens.</p>
<p><br></p>
<p>If one of the screens fail , telegram bot informs you. Right from the bot menu - you can restart the script.</p>
<p><br></p>
<p><br></p>
<p>#How to use</p>
<p><br></p>
<p>To use the bot, first send it the /start command. This will start the bot and give you a list of available commands.</p>
<p><br></p>
<p>To list your screens, send the /list command. This will show you a list of all your screens, including their names and status.</p>
<p><br></p>
<p>To run a script in a screen session, send the /run command followed by the name of the script. The bot will create a new screen session and run the script in it.</p>
<p><br></p>
<p>To check the status of a screen, send the /status command followed by the ID of the screen. The bot will return the status of the screen, such as whether it is attached or detached.</p>
<p><br></p>
<p>#Code Explanation</p>
<p>The provided Python script does the following:</p>
<p><br></p>
<p>Imports the necessary module subprocess to interact with the command-line.</p>
<p>Defines a command to list the screens and retrieve their names and status.</p>
<p>Defines a function get_screen_data() to extract screen information from the command output.</p>
<p>Executes the command using subprocess.check_output() and captures the output.</p>
<p>Processes the output to extract relevant information about each screen, including its ID, name, and status.</p>
<p>Returns a list of dictionaries, each representing a detached screen&apos;s information.</p>
<p><br></p>
<p>&nbsp;</p>
<p>/list</p>
<p>This is the list of screens:</p>
<p>Screen ID: 87888, Name: &quot;NAME OF THE SCREEN&quot;, Status: Detached</p>
<p>Screen ID: 44215, Name: &quot;NAME OF THE SCREEN&quot;, Status: Detached</p>
<p>Screen ID: 44204, Name: &quot;NAME OF THE SCREEN&quot;, Status: Detached</p>
<p>Screen ID: 44182, Name: &quot;NAME OF THE SCREEN&quot;, Status: Detached</p>
<p>Screen ID: 1333, Name: &quot;NAME OF THE SCREEN&quot;, Status: Detached</p>
