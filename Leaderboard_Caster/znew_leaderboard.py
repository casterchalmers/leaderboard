# CASTER LEADERBOARD 
# VERSION 0.8.5
# 2022-12-05, Johannes Johansson 

from screeninfo import get_monitors
import pandas as pd
from PIL import Image, ImageTk
import tkinter as tk

def initialize_leaderboard_window():
    """Initiera leaderboard-fönstret på en specifik skärm."""
    monitors = get_monitors()
    if len(monitors) > 1:
        screen_width = monitors[1].width
        screen_height = monitors[1].height
        window = initialize_window(screen_width, screen_height)
        window.geometry(f"{screen_width}x{screen_height}+{monitors[1].x}+{monitors[1].y}")
    else:
        # Om endast en skärm finns, använd den som standard
        screen_width = monitors[0].width
        screen_height = monitors[0].height
        window = initialize_window(screen_width, screen_height)
    
    logo = add_logo(window)  # Behåll en referens till logotypen för att undvika garbage collection
    fastest_driver_label = create_fastest_driver_label(window)
    title = create_leaderboard_title(window)
    leaderboard_label = create_leaderboard_label(window)
    
    groups = [[], [], [], []]  # Initiera grupperna
    
    return window, fastest_driver_label, leaderboard_label, groups



# Get screen information
def get_screen_info():
    """Hämta information om skärmens bredd och höjd."""
    screen = get_monitors()[0]
    return screen.width, screen.height
# Initialize the GUI window
def initialize_window(screen_width, screen_height):
    """Initiera GUI-fönstret."""
    window = tk.Tk()
    window.title("Leaderboard")
    window.config(bg="black")
    window.geometry(f"{screen_width}x{screen_height}")
    window.attributes("-fullscreen", False)
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)
    return window

# Add the caster logo
def add_logo(window):
    """Lägg till Caster-logotypen längst upp i GUI:t."""
    image = Image.open("Logo2016_LowProfile_INV.jpg")
    image = image.resize((750, 202), Image.Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(image)
    label1 = tk.Label(image=logo, bg="Black")
    label1.pack(side=tk.TOP, anchor=tk.N, fill=tk.X)
    return logo  # Behövs för att hålla referensen till bilden

# Display the fastest driver
def create_fastest_driver_label(window):
    """Skapa etiketten för att visa de snabbaste förarna."""
    fastest_driver_label = tk.Label(text="", bg="black", fg="white", font=("Courier", 14), justify=tk.LEFT)
    fastest_driver_label.pack(side=tk.TOP, fill=tk.X)
    return fastest_driver_label

# Create leaderboard title
def create_leaderboard_title(window):
    """Skapa titeln för leaderboarden."""
    title = tk.Label(text="LEADERBOARD", bg="red", fg="white", font=("Sansation", 30), justify=tk.CENTER)
    title.pack(side=tk.TOP, ipadx=10, ipady=10, anchor=tk.NW, fill=tk.X)
    return title

# Create leaderboard label
def create_leaderboard_label(window):
    """Skapa etiketten för att visa leaderboarden."""
    leaderboard_label = tk.Label(bg="black", fg="white", font=("Courier", 14), justify=tk.LEFT)
    leaderboard_label.pack(side=tk.TOP, fill=tk.X)
    return leaderboard_label

# Update the leaderboard from Excel
def update_leaderboard(groups, excel_filename):
    """Uppdatera leaderboarden från en Excel-fil och sortera den efter varvtid."""
    df = pd.read_excel(f"{excel_filename}")
    df = df.sort_values(by="LAPTIME", ascending=True)

    # Clear the groups
    for group in groups:
        group.clear()

    # Populate the groups with driver names, lap times, and positions
    for i, row in enumerate(df.itertuples()):
        if i >= 100:
            break
        group = i // 25
        groups[group].append([row.NAME, row.LAPTIME, i + 1])

# Display the top three drivers
def update_top_three(fastest_driver_label, groups):
    """Visa de tre snabbaste förarna."""
    top_three_text = "Top Three Drivers:\n"
    
    top_three_group = sorted(groups[0], key=lambda x: x[1])[:3]  # Get the top three drivers in the group based on lap time
    for position, driver in enumerate(top_three_group, start=1):
        driver_text = f"Position: {position} | Driver: {str(driver[0]):<25s} | Lap Time: {str(driver[1])}\n"
        top_three_text += driver_text

    fastest_driver_label.config(text=top_three_text)

# Update the leaderboard display
def update_leaderboard_display(window, leaderboard_label, groups):
    """Uppdatera visningen av leaderboarden."""
    for i, (group1, group2) in enumerate(zip(groups[:3], groups[1:4])):
        if len(group1) > 0 or len(group2) > 0:
            leaderboard_text = []
            group1_name, group2_name = get_group_names(i, len(group1), len(group2))

            max_drivers = max(len(group1), len(group2))
            
            leaderboard_text.append(f"{'Drivers ' + group1_name:<94s}Drivers {group2_name}")
            leaderboard_text.append("No. Name Lap Time" + " " * 77 + "No. Name Lap Time")
            leaderboard_text.append("-" * 57 + " " * 37 + "-" * 57)
            
            # Iterate over the range of maximum drivers
            for j in range(max_drivers):
                driver1_str = get_driver_str(group1, j)
                driver2_str = get_driver_str(group2, j)
                
                leaderboard_text.append(driver1_str + " " * 40 + driver2_str)
            
            leaderboard_label.config(text="\n".join(leaderboard_text))
            window.update()
            
            if i < len(groups):
                window.after(5000)  # Delay between group displays (in milliseconds)
        else:
            if i < len(groups):
                window.after(0)  # Delay between group displays (in milliseconds)

def get_group_names(i, len_group1, len_group2):
    """Hämta namn för grupper baserat på deras index och längd."""
    if i == 0:
        group1_name = f"1 - {len_group1}"
        group2_name = f"26 - {len_group2 + 25}"
    elif i == 1:
        group1_name = f"26 - {len_group1 + 25}"
        group2_name = f"51 - {len_group2 + 50}"
    elif i == 2:
        group1_name = f"51 - {len_group1 + 50}"
        group2_name = f"76 - {len_group2 + 75}"
    return group1_name, group2_name

def get_driver_str(group, j):
    """Returnera en formaterad sträng för en förare i en grupp."""
    if j < len(group):
        driver = group[j]
        position = driver[2]
        name = str(driver[0])  # Säkerställ att name är en sträng
        lap_time = driver[1]
        driver_str = f"{position:3d}. {name[:40]:-<40s} {lap_time}"
    else:
        driver_str = " " * 57
    return driver_str

# Continuous update function
def continuous_update(window, fastest_driver_label, leaderboard_label, groups, excel_filename):
    """Kontinuerlig uppdatering av leaderboarden."""
    if not window.winfo_exists():
        print("Window no longer exists, stopping updates.")
        return
    
    # Regular updates
    update_leaderboard(groups, excel_filename)
    if fastest_driver_label.winfo_exists():
        update_top_three(fastest_driver_label, groups)
    if leaderboard_label.winfo_exists():
        update_leaderboard_display(window, leaderboard_label, groups)
    
    # Schedule next update only if window still exists
    if window.winfo_exists():
        window.after(1000, continuous_update, window, fastest_driver_label, leaderboard_label, groups, excel_filename)

'''
def main():
    screen_width, screen_height = get_screen_info()
    window = initialize_window(screen_width, screen_height)
    
    logo = add_logo(window)  # Keep a reference to the logo to avoid garbage collection
    fastest_driver_label = create_fastest_driver_label(window)
    title = create_leaderboard_title(window)
    leaderboard_label = create_leaderboard_label(window)
    
    groups = [[], [], [], []]  # Initialize the groups
    continuous_update(window, fastest_driver_label, leaderboard_label, groups, excel_filename)
    
    window.mainloop()

if __name__ == "__main__":
    main()'''
