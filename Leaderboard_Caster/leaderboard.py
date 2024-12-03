#CASTER LEADERBOARD 
#VERSION 0.5.0
#2022-12-05, Johannes Johansson 

from tkinter import *
from screeninfo import get_monitors
import pandas as pd
from PIL import Image, ImageTk


#Gets scrren information eg screen seize
screen_width = get_monitors()[0].width
screen_height = get_monitors()[0].height

#CREATING THE WINDOW FOR THE APPLICATION
window = Tk()
window.title("Leaderboard")
window.config(bg="black")
window.geometry(f'{screen_width}x{screen_height}')
window.attributes("-fullscreen",False)
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

#ADDING CASTER LOGO AT THE TOP
# Create a photoimage object of the image in the path
image1 = Image.open("Logo2016_LowProfile_INV.jpg")
image1 = image1.resize((705,190), Image.Resampling.LANCZOS)
test = ImageTk.PhotoImage(image1)
label1 = Label(image=test)
label1.image = test
label1.config(bg="Black")
# Position image
label1.pack(side=TOP, anchor=N, fill=X)

#Display LEADERBOARD TEXT
titel = Label(text="LEADERBOARD")
titel.config(bg="red", fg="white", font=("Sansation", 30), justify=CENTER)
titel.pack(side=TOP, ipadx=10, ipady=10, anchor=NW, fill=X)

#FOOTER
footer = Label(text="Leaderboard")
footer.config(bg="red", fg="red", font=("Arial", 4), justify=CENTER)
footer.pack(side=BOTTOM, ipadx=10, ipady=10, anchor=SW, fill=BOTH)
        
#Display QUIT BUTTON
#button = Button(text="Quit", font=("Ariel", 20), command=window.destroy, width=10, height=1, bg="black", fg="white")
#button.place(x=screen_width-175, y=screen_height-60)

def update_text():
    #Reading Excel file to pandas Dataframe sorting fastest laptime
    df = pd.read_excel("readme2.xlsx")
    df = df.sort_values(by="LAPTIME", ascending=True)
    # print(df)
    # print(df["NAME"].values)

    #TEXT for 1-25 drivers
    namn = ""
    varvtid = ""
    plats = ""
    #TEXT for 25-50 drivers
    namn1 = ""
    varvtid1 = ""
    plats1 = ""
    #TEXT for 50-75 drivers
    namn2 = ""
    varvtid2 = ""
    plats2 = ""
    #TEXT for 75-100 drivers
    namn3 = ""
    varvtid3 = ""
    plats3 = ""
    count = 1

    #ADDING LEADERBOARD TEXT
    for row in df.iloc:
        if count <= 25:                                     #ADD top 25 drivers to leaderboard text
            if str(row["NAME"]) == None:
                namn = namn + "\n"
                varvtid = varvtid + "\n"
                plats = plats + f"{count} \n"
            else:
                namn = namn +  str(row["NAME"]) + "\n"
                varvtid = varvtid + str(row["LAPTIME"]) + "\n"
                plats = plats + f"{count} \n"
        if count > 25 and count <= 50:                      #ADD top 50 drivers to leaderboard text
            if str(row["NAME"]) == None:
                namn1 = namn1 + "\n"
                varvtid1 = varvtid1 + "\n"
                plats1 = plats1 + f"{count} \n"
            else:
                namn1 = namn1 + str(row["NAME"]) + "\n"
                varvtid1 = varvtid1 + str(row["LAPTIME"]) + "\n"
                plats1 = plats1 + f"{count} \n"
        if count > 50 and count <= 75:                      #ADD top 75 drivers to leaderboard text
            if str(row["NAME"]) == None:
                namn2 = namn2 + "\n"
                varvtid2 = varvtid2 + "\n"
                plats2 = plats2 + f"{count} \n"
            else:
                namn2 = namn2 + str(row["NAME"]) + "\n"
                varvtid2 = varvtid2 + str(row["LAPTIME"]) + "\n"
                plats2 = plats2 + f"{count} \n"
        if count > 75 and count <= 100:                      #ADD top 100 drivers to leaderboard text
            if str(row["NAME"]) == None:
                namn3 = namn3 + "\n"
                varvtid3 = varvtid3 + "\n"
                plats3 = plats3 + f"{count} \n"
            else:
                namn3 = namn3 + str(row["NAME"]) + "\n"
                varvtid3 = varvtid3 + str(row["LAPTIME"]) + "\n"
                plats3 = plats3 + f"{count} \n"
        count += 1
    return namn,varvtid,plats,namn1,plats1,varvtid1,namn2,plats2,varvtid2,namn3,plats3,varvtid3, df

namn,varvtid,plats,namn1,plats1,varvtid1,namn2,plats2,varvtid2,namn3,plats3,varvtid3, df = update_text()


#Leaderboard text color
color1 = "black"
color2 = "white"
#Divider color
color3 = "red"

#DISPLAYING TEXT
# HEADER THIS IS NOT THE SOLUTION, DONT JUDGE ME HARD CODING IT WORKS   
#header1 = Label(text="Position \t   Name \t\t Laptime")                                                                                                                                                                                                                      ")
#header1.config(bg="green", fg="black", font=("Ariel", 18), justify=CENTER)
#header1.pack(ipadx=10, ipady=1, side=TOP, anchor=NW)
pos1 = Label(text=plats)                                                        #Display top 25 drivers to leaderboard
pos1.config(bg=color1, fg=color2, font=("Ariel", 19), justify=CENTER)
pos1.pack(ipadx=10, ipady=2, side=LEFT, anchor=NW, fill=BOTH, expand=True)
nam1 = Label(text=namn)
nam1.config(bg=color1, fg=color2, font=("Ariel", 19), justify=CENTER)
nam1.pack(ipadx=10, ipady=2, side=LEFT, anchor=NW, fill=BOTH,expand=True)
var1 = Label(text=varvtid)
var1.config(bg=color1, fg=color2, font=("Ariel", 19), justify=CENTER)
var1.pack(ipadx=10, ipady=2, side=LEFT, anchor=NW, fill=BOTH,expand=True)
                                                               #Display top 50 drivers to leaderboard
divider = Label(text=X)
divider.config(bg=color3, fg=color3, font=("Ariel", 19), justify=CENTER)
divider.pack(ipadx=2, ipady=2, side=LEFT, anchor=NW, fill=Y)
pos2 = Label(text=plats1)
pos2.config(bg=color1, fg=color2, font=("Ariel", 19), justify=CENTER)
pos2.pack(ipadx=10, ipady=2, side=LEFT, anchor=NW, fill=BOTH,expand=True)
nam2 = Label(text=namn1)
nam2.config(bg=color1, fg=color2, font=("Ariel", 19), justify=CENTER)
nam2.pack(ipadx=10, ipady=2, side=LEFT, anchor=NW, fill=BOTH,expand=True)
var2 = Label(text=varvtid1)
var2.config(bg=color1, fg=color2, font=("Ariel", 19), justify=CENTER)
var2.pack(ipadx=10, ipady=2, side=LEFT, anchor=NW, fill=BOTH,expand=True)
                                                              #Display top 75 drivers to leaderboard
divider = Label(text=X)
divider.config(bg=color3, fg=color3, font=("Ariel", 19), justify=CENTER)
divider.pack(ipadx=2, ipady=2, side=LEFT, anchor=NW, fill=Y)
pos3 = Label(text=plats2)
pos3.config(bg=color1, fg=color2, font=("Ariel", 19), justify=CENTER)
pos3.pack(ipadx=10, ipady=2, side=LEFT, anchor=NW, fill=BOTH, expand=True)
nam3 = Label(text=namn2)
nam3.config(bg=color1, fg=color2, font=("Ariel", 19), justify=CENTER)
nam3.pack(ipadx=10, ipady=2, side=LEFT, anchor=NW, fill=BOTH, expand=True)
var3 = Label(text=varvtid2)
var3.config(bg=color1, fg=color2, font=("Ariel", 19), justify=CENTER)
var3.pack(ipadx=10, ipady=2, side=LEFT, anchor=NW, fill=BOTH, expand=True)
                                                               #Display top 75 drivers to leaderboard
divider = Label(text=X)
divider.config(bg=color3, fg=color3, font=("Ariel", 19), justify=CENTER)
divider.pack(ipadx=2, ipady=2, side=LEFT, anchor=NW, fill=Y)
pos4 = Label(text=plats3)
pos4.config(bg=color1, fg=color2, font=("Ariel", 19), justify=CENTER)
pos4.pack(ipadx=10, ipady=2, side=LEFT, anchor=NW, fill=BOTH, expand=True)
nam4 = Label(text=namn3)
nam4.config(bg=color1, fg=color2, font=("Ariel", 19), justify=CENTER)
nam4.pack(ipadx=10, ipady=2, side=LEFT, anchor=NW, fill=BOTH, expand=True)
var4 = Label(text=varvtid3)
var4.config(bg=color1, fg=color2, font=("Ariel", 19), justify=CENTER)
var4.pack(ipadx=10, ipady=2, side=LEFT, anchor=NW, fill=BOTH, expand=True)

#UPDATE the leaderboard text 
def update_leaderboard():
    namn,varvtid,plats,namn1,plats1,varvtid1,namn2,plats2,varvtid2,namn3,plats3,varvtid3, df = update_text()
    pos1.config(text=plats)
    nam1.config(text=namn)
    var1.config(text=varvtid)
    pos2.config(text=plats1, bg=color1, fg=color2)
    nam2.config(text=namn1, bg=color1, fg=color2)
    var2.config(text=varvtid1, bg=color1, fg=color2)
    pos3.config(text=plats2, bg=color1, fg=color2)
    nam3.config(text=namn2,bg=color1, fg=color2 )
    var3.config(text=varvtid2, bg=color1, fg=color2)
    pos4.config(text=plats3, bg=color1, fg=color2)
    nam4.config(text=namn3, bg=color1, fg=color2)
    var4.config(text=varvtid3, bg=color1, fg=color2)
    window.after(1000,update_leaderboard)
window.after(1000,update_leaderboard)

window.mainloop()