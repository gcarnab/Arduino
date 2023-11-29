import serial
import tkinter as tk
import cairosvg
from PIL import Image, ImageTk
import io

# Define the serial port and baud rate
port = 'COM4'  # Change this to your Arduino's port
baud_rate = 9600

# Create a serial connection
arduino = serial.Serial(port, baud_rate, timeout=1)

# Function to send command to Arduino
def send_command(command):
    arduino.write(command.encode('utf-8'))

# Function to toggle the LED state
def toggle_led():
    current_state = state_label.cget("text")

    if current_state == "On":
        send_command('0')
        state_label.config(text="Off", image=off_image, font=("Helvetica", 16, "bold italic"))
    else:
        send_command('1')
        state_label.config(text="On", image=on_image, font=("Helvetica", 16, "bold italic"))

# Create the main application window
app = tk.Tk()
app.title("GC Python LED Control")
app.geometry("500x500")  # Set the initial window size

# Load images
base_path = "C:\\GCDATA\\DEV\\vscode-workspace\\Arduino\\PYTHON\\gc_blink\\"
#on_image = tk.PhotoImage(file= base_path + "toggle_on.png")
#off_image = tk.PhotoImage(file= base_path + "toggle_off.png")

# images resizing
# Carica un'immagine SVG
svg_data_on = """
<svg xmlns="http://www.w3.org/2000/svg" height="128" viewBox="0 -960 960 960" width="128"><path d="M280-240q-100 0-170-70T40-480q0-100 70-170t170-70h400q100 0 170 70t70 170q0 100-70 170t-170 70H280Zm0-80h400q66 0 113-47t47-113q0-66-47-113t-113-47H280q-66 0-113 47t-47 113q0 66 47 113t113 47Zm400-40q50 0 85-35t35-85q0-50-35-85t-85-35q-50 0-85 35t-35 85q0 50 35 85t85 35ZM480-480Z"/></svg>
"""

svg_data_off = """
<svg xmlns="http://www.w3.org/2000/svg" height="128" viewBox="0 -960 960 960" width="128"><path d="M280-240q-100 0-170-70T40-480q0-100 70-170t170-70h400q100 0 170 70t70 170q0 100-70 170t-170 70H280Zm0-80h400q66 0 113-47t47-113q0-66-47-113t-113-47H280q-66 0-113 47t-47 113q0 66 47 113t113 47Zm0-40q50 0 85-35t35-85q0-50-35-85t-85-35q-50 0-85 35t-35 85q0 50 35 85t85 35Zm200-120Z"/></svg>
"""

# Converti l'SVG in PNG usando CairoSVG
png_data_on = cairosvg.svg2png(bytestring=svg_data_on)
png_data_off = cairosvg.svg2png(bytestring=svg_data_off)

# Crea un oggetto Image da dati PNG
png_image_on = Image.open(io.BytesIO(png_data_on))
png_image_off = Image.open(io.BytesIO(png_data_off))

# Ridimensiona l'immagine
resized_image_on = png_image_on.resize((128, 128), Image.ANTIALIAS)
resized_image_off = png_image_off.resize((128, 128), Image.ANTIALIAS)

# Converte l'immagine ridimensionata in un oggetto ImageTk.PhotoImage
on_image = ImageTk.PhotoImage(resized_image_on)
off_image = ImageTk.PhotoImage(resized_image_off)

'''
img_on = Image.open(base_path + "toggle_on.svg")
img_off = Image.open(base_path + "toggle_off.png")
img_on_res = img_on.resize((128,64), Image.ANTIALIAS)
img_off_res = img_off.resize((128,64), Image.ANTIALIAS)
on_image= ImageTk.PhotoImage(img_on_res)
off_image= ImageTk.PhotoImage(img_off_res)
'''

# Create a label to display the image
state_label = tk.Label(app, text="Off", image=off_image, compound=tk.TOP, font=("Helvetica", 16, "bold italic"))
state_label.pack(pady=20)
state_label.bind("<Button-1>", lambda event: toggle_led())  # Bind left-click event

# Run the application
app.mainloop()

# Close the serial connection when the GUI is closed
arduino.close()
