#CASTER LEADERBOARD 
#VERSION 0.8.5
#2022-12-05, Johannes Johansson 

from screeninfo import get_monitors
import pandas as pd
from PIL import Image, ImageTk
import tkinter as tk

# Get screen information
screen_width = get_monitors()[0].width
screen_height = get_monitors()[0].height

# Define groups for the leaderboard
groups = [[], [], [], []]  # Group 1: 1-25, Group 2: 26-50, Group 3: 51-75, Group 4: 76-100

# Create the GUI window
window = tk.Tk()
window.title("Leaderboard")
window.config(bg="black")
window.geometry(f"{screen_width}x{screen_height}")
window.attributes("-fullscreen", False)
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

# Add the caster logo at the top
image = Image.open("Logo2016_LowProfile_INV.jpg")
image = image.resize((750, 202), Image.Resampling.LANCZOS)
logo = ImageTk.PhotoImage(image)
label1 = tk.Label(image=logo, bg="Black")
label1.pack(side=tk.TOP, anchor=tk.N, fill=tk.X)

# Display the fastest driver
fastest_driver_label = tk.Label(text="", bg="black", fg="white", font=("Courier", 14), justify=tk.LEFT)
fastest_driver_label.pack(side=tk.TOP, fill=tk.X)

# Display the leaderboard
title = tk.Label(text="LEADERBOARD", bg="red", fg="white", font=("Sansation", 30), justify=tk.CENTER)
title.pack(side=tk.TOP, ipadx=10, ipady=10, anchor=tk.NW, fill=tk.X)

leaderboard_label = tk.Label(bg="black", fg="white", font=("Courier", 14), justify=tk.LEFT)
leaderboard_label.pack(side=tk.TOP, fill=tk.X)

# Function to update the leaderboard from Excel
def update_leaderboard():
    # Read Excel file and sort by lap time
    df = pd.read_excel("readme2.xlsx")
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

    # Update the top three drivers
    top_three_text = "Top Three Drivers:\n"
    
    top_three_group = sorted(groups[0], key=lambda x: x[1])[:3]  # Get the top three drivers in the group based on lap time
    for position, driver in enumerate(top_three_group, start=1):
        driver_text = f"Position: {position} | Driver: {str(driver[0]):<25s} | Lap Time: {str(driver[1])}\n"
        top_three_text += driver_text

    fastest_driver_label.config(text=top_three_text)



# Function to update the leaderboard display
def update():
    # Loop through pairs of groups (1, 2), (2, 3), and (3, 4)
    for i, (group1, group2) in enumerate(zip(groups[:3], groups[1:4])):
        if len(group1) > 0 or len(group2) > 0:
            leaderboard_text = []
            group1_name = ""
            group2_name = ""
            
            if i == 0:
                group1_name = f"1 - {len(group1)}"
                group2_name = f"26 - {len(group2) + 25}"
            elif i == 1:
                group1_name = f"26 - {len(group1) + 25}"
                group2_name = f"51 - {len(group2) + 50}"
            elif i == 2:
                group1_name = f"51 - {len(group1) + 50}"
                group2_name = f"76 - {len(group2) + 75}"
            
            # Determine the maximum number of drivers in either group
            max_drivers = max(len(group1), len(group2))
            
            leaderboard_text.append(f"{'Drivers ' + group1_name:<94s}Drivers {group2_name}")
            leaderboard_text.append("No. Name Lap Time" + " " * 77 + "No. Name Lap Time")
            leaderboard_text.append("-" * 57 + " " * 37 + "-" * 57)
            
            # Iterate over the range of maximum drivers
            for j in range(max_drivers):
                if j < len(group1):
                    driver1 = group1[j]
                    position1 = driver1[2]
                    name1 = driver1[0]
                    name1 = str(name1)
                    lap_time1 = driver1[1]
                    driver1_str = f"{position1:3d}. {name1[:40]:-<40s} {lap_time1}"

                else:
                    driver1_str = " " * 57
                
                if j < len(group2):
                    driver2 = group2[j]
                    position2 = driver2[2]
                    name2 = driver2[0]
                    lap_time2 = driver2[1]
                    driver2_str = f"{position2:3d}. {name2[:40]:-<40s} {lap_time2}"
                else:
                    driver2_str = ""
                
                leaderboard_text.append(driver1_str + " " * 40 + driver2_str)
            
            leaderboard_label.config(text="\n".join(leaderboard_text))
            window.update()
            
            if i < len(groups):
                window.after(5000)  # Delay between group displays (in milliseconds)
        else:
            if i < len(groups):
                window.after(0)  # Delay between group displays (in milliseconds)



def continuous_update():
    update_leaderboard()
    update()
    window.after(5000, continuous_update) # Update every 10 seconds (in milliseconds)

continuous_update()

window.mainloop()