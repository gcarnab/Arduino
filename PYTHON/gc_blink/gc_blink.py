import serial
import tkinter as tk

# Define the serial port and baud rate
port = 'COM3'  # Change this to your Arduino's port
baud_rate = 9600

# Create a serial connection
arduino = serial.Serial(port, baud_rate, timeout=1)

# Function to send command to Arduino
def send_command(command):
    arduino.write(command.encode('utf-8'))

# Create the main application window
app = tk.Tk()
app.title("LED Control")

# Function to toggle the LED and update the GUI
def toggle_led():
    if led_button.cget("text") == "Turn On":
        send_command('1')
        led_button.config(text="Turn Off", bg="red", activebackground="darkred")
        led_symbol.config(image=on_image)
    else:
        send_command('0')
        led_button.config(text="Turn On", bg="green", activebackground="darkgreen")
        led_symbol.config(image=off_image)

# Create GUI elements
led_button = tk.Button(app, text="Turn On", command=toggle_led, width=10, height=2, bg="green", activebackground="darkgreen")
led_button.pack(pady=20)

# chage the correct path
image_base_path = "C:\\GCDATA\\DEV\\vscode-workspace\\Arduino\\PYTHON\\gc_blink\\"
img_on_path = image_base_path + "on.png"
img_off_path = image_base_path + "off.png"
on_image = tk.PhotoImage(file=img_on_path)
off_image = tk.PhotoImage(file=img_off_path)

led_symbol = tk.Label(app, image=off_image)
led_symbol.pack()

# Run the application
app.mainloop()

# Close the serial connection when the GUI is closed
arduino.close()
