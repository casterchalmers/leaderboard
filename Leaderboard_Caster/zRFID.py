from tkinter import *
from screeninfo import get_monitors

def initialize_window():
    """Starta och konfigurera huvudfönstret."""
    window = Tk()
    screen_width = get_monitors()[0].width
    screen_height = get_monitors()[0].height
    window.geometry(f'{screen_width}x{screen_height}')
    window.attributes("-fullscreen", True)
    window.configure(bg="Black")
    return window

def configure_inputs_and_labels(window):
    """Konfigurera inmatningsfält och etiketter."""
    user_input = Entry(window, bg='Grey', fg='White', font=('Arial', 60), show='*', relief="flat", state=NORMAL)
    user_name_input = Entry(window, bg='Grey', fg='White', font=('Arial', 60), relief="flat", state=NORMAL)
    answer = Label(window, bg="Black", fg="White", font=("Arial", 30), relief="flat")
    return user_input, user_name_input, answer

def get_rfid():
    """Hämta RFID från användaren."""
    global window
    window = initialize_window()
    user_input, _, answer = configure_inputs_and_labels(window)

    rfid = None

    def handle_rfid_input():
        nonlocal rfid
        rfid = user_input.get()
        if len(rfid) < 4:
            answer.config(text="That's probably not a valid RFID tag!")
        else:
            answer.config(text=f"RFID: {rfid} received.")
            window.after(500, close_window)  # Stäng fönstret efter meddelandet

    button_RFID = Button(window, text="Input RFID", command=handle_rfid_input,
                         height=1, activebackground='Green', bg='Grey', fg='white', font=('Arial', 30))
    
    user_input.place(x=0, y=0)
    button_RFID.place(x=900, y=6)

    window.mainloop()

    return rfid

def get_name():
    """Hämta namn från användaren."""
    global window
    window = initialize_window()
    _, user_name_input, answer = configure_inputs_and_labels(window)

    name = None

    def handle_name_input():
        nonlocal name
        name = user_name_input.get()
        if name:
            answer.config(text=f"Thank you, {name}!")
            window.after(500, close_window)  # Stäng fönstret efter meddelandet
        else:
            answer.config(text="Enter a name!")

    button_name = Button(window, text="Submit Name", command=handle_name_input,
                         height=1, activebackground='Green', bg='Grey', fg='white', font=('Arial', 30))

    user_name_input.place(x=0, y=800)
    button_name.place(x=900, y=805)

    window.mainloop()

    return name

def close_window():
    """Stäng fönstret."""
    if window.winfo_exists():
        window.quit()
        window.destroy()