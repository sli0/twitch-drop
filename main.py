import webbrowser
import time
import threading
import sys
import os

print_lock = threading.Lock()

def open_link(url, time_between_links):
    webbrowser.open(f"https://www.twitch.tv/{url}")
    time.sleep(time_between_links)  

def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

def update_time_remaining(time_remaining, total_time, url):
    time.sleep(3)
    while time_remaining > -1:
        percent_complete = ((total_time - time_remaining) / total_time) * 100
        if percent_complete > 100:
            percent_complete = 100  
        colored_percent = f"\033[92m{percent_complete:.2f}%\033[0m"
        formatted_time = format_time(time_remaining)

        with print_lock:
            sys.stdout.write(f"\rTime left: {formatted_time} ({colored_percent}) {url} ")
            sys.stdout.flush()
        
        time.sleep(1)
        time_remaining -= 1


    os.system("taskkill /f /im msedge.exe")  
        



def open_links_from_file():
    with open('link.txt', 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]

    link_times = [(line.split()[0], float(line.split()[1])) for line in lines]

    for url, time_between_links in link_times:
        time_remaining = time_between_links * 3600
        total_time = time_remaining  
        time_thread = threading.Thread(target=update_time_remaining, args=(time_remaining, total_time, url,))
        time_thread.start()

        print(f"Opening {url}.", end='', flush=True)
        open_link(url, time_remaining)
        time_thread.join()

        time.sleep(1)

open_links_from_file()

input("all good, good bye. This code was done by sli4 discord : https://discord.gg/p5exCAdQYf ")
