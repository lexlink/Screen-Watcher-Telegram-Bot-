import telegram
from telegram import Bot, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
import time
import subprocess

bot_token = 'XXXXXXXXXXXXXXXXXXX' # TELEGRAM BOT TOKEN
chat_id = 'XXXXXXXXXX' # YOUR CHAT ID

# Create a bot instance
bot = Bot(token=bot_token)

COMMANDS = [
    ['/list', '/run']
]

def send_message(text):
    bot.send_message(chat_id=chat_id, text=text, reply_markup=ReplyKeyboardMarkup(COMMANDS, one_time_keyboard=True))

def disable_chat_input(update, context):
    context.bot.send_message(chat_id=chat_id, text="Input is disabled.", reply_markup=ReplyKeyboardRemove())

def start(update: Update, context):
    send_message("Bot is started!")
    send_message("Here's the list of available commands:")
    send_message("/list - Get the list of screens")
    send_message("/run - Run a screen")

def list_screens(update: Update, context):
    current_data = get_screen_data()
    send_message("This is the list of screens:")
    for screen_info in current_data:
        send_message(f"Screen ID: {screen_info['id']}, Name: {screen_info['name']}, Status: {screen_info['status']}")

def run_screen(update: Update, context):
    # Create keyboard buttons for each script
    buttons = [
        KeyboardButton("NAME OF THE SCRIPT"),
        KeyboardButton("NAME OF THE SCRIPT"),
        KeyboardButton("NAME OF THE SCRIPT"),
        KeyboardButton("NAME OF THE SCRIPT"),
        KeyboardButton("cancel", text_color="red")
    ]

    # Create a single row keyboard with the script buttons
    keyboard = ReplyKeyboardMarkup([buttons], one_time_keyboard=True)

    # Send the keyboard to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please choose which process to start:", reply_markup=keyboard)

def handle_run_screen(update: Update, context):
    script_name = update.message.text

    if script_name == "cancel":
        send_message("Run process canceled.")
    else:
        script_path = f"/home/link/sh-scripts/{script_name}.sh"

        try:
            subprocess.check_output(script_path, shell=True, text=True)
            send_message(f"Script '{script_name}' has been executed.")
        except Exception as e:
            send_message(f"An error occurred while executing the script '{script_name}': {str(e)}")

def get_screen_data():
    try:
        cmd = "screen -ls"
        # Execute the command and capture the output
        output = subprocess.check_output(cmd, shell=True, text=True)

        # Split the output into lines
        lines = output.strip().split("\n")

        # Extract the relevant information from each line
        screens = []
        for line in lines:
            parts = line.split(" ")
            if len(parts) >= 2:
                screen_info = parts[0].split(".", 1)
                if len(screen_info) >= 2:
                    screen_id = screen_info[0].strip()
                    screen_name = screen_info[1].split("\t")[0]
                    screen_status_parts = parts[1].strip().strip("()").split("\t")
                    if len(screen_status_parts) >= 2:
                        screen_status = "Detached"
                    else:
                        screen_status = parts[1].strip().strip("()")
                    screens.append({"id": screen_id, "name": screen_name, "status": screen_status})

        return screens
    except Exception as e:
        # Handle the exception (e.g., print an error message, log the error, etc.)
        print(f"An error occurred while getting screen data: {e}")
        return []

def check_for_conditions():
    # Initialize the stored data
    stored_data = {}
    killed_screens = set()

    # Run the code every 20 seconds
    while True:
        # Get the current screen data
        current_data = get_screen_data()

        # Compare current data with stored data and print changes
        for screen in current_data:
            screen_id = screen["id"]
            if screen_id not in stored_data:
                # New screen detected
                send_message(f"New screen: {screen}")
                # Update the stored data
                stored_data[screen_id] = screen
            else:
                stored_screen = stored_data[screen_id]
                if screen["status"] != stored_screen["status"]:
                    # Screen status changed
                    send_message(f"Screen status changed: {stored_screen['status']} -> {screen['status']}")
                    # Update the stored data
                    stored_data[screen_id] = screen
                if screen["id"] != stored_screen["id"]:
                    # Screen ID changed
                    send_message(f"Screen ID changed: {stored_screen['id']} -> {screen['id']}")
                    # Update the stored data
                    stored_data[screen_id] = screen

        # Check if the number of screens has changed
        num_screens = len(current_data)
        prev_num_screens = stored_data.get("number_of_screens")
        if prev_num_screens is not None and num_screens != prev_num_screens:
            send_message(f"Number of screens changed to {num_screens}")
            list_screens(None, None)  # Call the list_screens function to list the screens

        # Check for screens that were removed (killed)
        for screen_id, stored_screen in stored_data.items():
            if screen_id != "number_of_screens" and screen_id not in (screen["id"] for screen in current_data):
                if screen_id not in killed_screens:
                    # Screen was killed
                    send_message(f"Screen killed: {stored_screen['name']}")
                    # Call the list_screens function to list the screens
                    killed_screens.add(screen_id)

        # Update the number of screens in the stored data
        stored_data["number_of_screens"] = num_screens

        # Wait for 20 seconds
        time.sleep(20)

def main() -> None:
    # Create the updater and dispatcher
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    # Add command handlers
    start_handler = CommandHandler('start', start)
    list_handler = CommandHandler('list', list_screens)
    run_handler = CommandHandler('run', run_screen)
    handle_run_handler = MessageHandler(Filters.text & ~Filters.command, handle_run_screen)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(list_handler)
    dispatcher.add_handler(run_handler)
    dispatcher.add_handler(handle_run_handler)

    # Start the bot
    updater.start_polling()
    check_for_conditions()


if __name__ == '__main__':
    main()
