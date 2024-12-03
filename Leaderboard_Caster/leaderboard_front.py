from tkinter import *
from screeninfo import get_monitors


#Gets scrren information eg screen seize
screen_width = get_monitors()[0].width
screen_height = get_monitors()[0].height


#Starts a new window
window = Tk()


#Sets the seize of window
window.geometry(f'{screen_width}x{screen_height}')
window.attributes("-fullscreen", True)
window.configure(bg="Black")

main = Label(text="Caster Leaderboard")
main.config(bg="black", fg="white", font=("Arial Black",60), relief="flat", justify=CENTER)
main.pack()

top = Label(text = "Top three this month:")
top.config(bg="black", fg="white", font=("Arial",30), relief="flat", justify=CENTER)
top.pack(pady = 50)

top_list = Listbox()
top_list.config(bg="black", fg="white", font=("Arial",20), relief="flat")
top_list.insert(1, "1: Axel")
top_list.insert(2, "2: Din mamma")
top_list.insert(3, "3: hahah")
top_list.pack()

window.mainloop()