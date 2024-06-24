import subprocess

# Command to list the screens and retrieve their names and status
cmd = "screen -ls"

def get_screen_data():
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
