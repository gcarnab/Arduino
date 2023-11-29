import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import math
import serial
import cairosvg
import io

class SolarTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GC Solar Tracker")
        #self.geometry("500x500")  # Set the initial window size

        # Creazione del canvas
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        # Disegna il cerchio numerato
        #self.draw_numbered_circle()

        # Disegna la rosa dei venti
        self.draw_cardinal_points()

        # Load images
        # chage the correct path
        image_base_path = "C:\\GCDATA\\DEV\\vscode-workspace\\Arduino\\PYTHON\\gc_light_follower\\"
        img_arrow_path = image_base_path + "arrow.png"

        # images resizing
        # Carica un'immagine SVG
        svg_data = """
        <svg xmlns="http://www.w3.org/2000/svg" height="128" viewBox="0 -960 960 960" width="128"><path d="m80-80 80-400h640l80 400H80Zm40-720v-80h120v80H120Zm58 640h262v-80H194l-16 80Zm67-427-57-56 85-85 57 56-85 85Zm-35 267h230v-80H226l-16 80Zm270-360q-83 0-141.5-58.5T280-880h80q0 50 35 85t85 35q50 0 85-35t35-85h80q0 83-58.5 141.5T480-680Zm0-200Zm-40 360v-120h80v120h-80Zm80 360h262l-16-80H520v80Zm0-160h230l-16-80H520v80Zm195-267-84-85 56-56 85 84-57 57Zm5-213v-80h120v80H720Z"/></svg>
        """
        # Converti l'SVG in PNG usando CairoSVG
        png_data = cairosvg.svg2png(bytestring=svg_data)

        # Crea un oggetto Image da dati PNG
        png_image = Image.open(io.BytesIO(png_data))

        # Ridimensiona l'immagine
        resized_image = png_image.resize((128, 128), Image.LANCZOS)

        # Converte l'immagine ridimensionata in un oggetto ImageTk.PhotoImage
        self.arrow_image = ImageTk.PhotoImage(resized_image)

        #self.arrow_image = ImageTk.PhotoImage(file=img_arrow_path)

        # Disegna l'immagine della freccia al centro del cerchio
        self.arrow = self.canvas.create_image(200, 200, image=self.arrow_image)

        # Pannello per mostrare i valori delle fotocellule
        self.sensor_panel = tk.LabelFrame(root, text="Valori Arduino", padx=10, pady=10)
        self.sensor_panel.pack(pady=10)

        # Etichette per i valori delle fotocellule
        self.left_sensor_label = tk.Label(self.sensor_panel, text="Fotocellula SX:")
        self.left_sensor_label.grid(row=0, column=0)

        self.right_sensor_label = tk.Label(self.sensor_panel, text="Fotocellula DX:")
        self.right_sensor_label.grid(row=1, column=0)

        self.diff_sensor_label = tk.Label(self.sensor_panel, text="Differenza:")
        self.diff_sensor_label.grid(row=2, column=0)

        self.angle_label = tk.Label(self.sensor_panel, text="Angle:")
        self.angle_label.grid(row=3, column=0)

        # Inizializza la comunicazione seriale
        self.serial_port = serial.Serial('COM4', 9600, timeout=5)

        # Crea un pulsante per chiudere l'applicazione
        self.quit_button = tk.Button(root, text="Quit", command=self.close_serial_and_quit)
        self.quit_button.pack()

        # Aggiorna l'interfaccia grafica leggendo i dati dalla seriale
        self.update_gui()

    def close_serial_and_quit(self):
        self.serial_port.close()
        self.root.quit()

    def draw_numbered_circle(self):
        # Disegna un cerchio numerato con 8 divisioni
        division = 8
        for i in range(division):
            angle_rad = math.radians(i * (360 / division))
            x = 200 + int(150 * math.cos(angle_rad))
            y = 200 - int(150 * math.sin(angle_rad))
            self.canvas.create_text(x, y, text=str(i), fill="black")

    def draw_cardinal_points(self):
        # Disegna i punti cardinali come una rosa dei venti
        for i, cardinal_point in enumerate(["N", "NW", "W", "SW", "S", "SE", "E", "NE"]):
            
            angle_deg = (i + 2 ) * (360 / 8)  # Modifica dell'angolo iniziale per posizionare il Nord in alto
            #angle_rad = math.radians(i * (360 / 8))
            angle_rad = math.radians(angle_deg)
            x = 200 + int(170 * math.cos(angle_rad))
            y = 200 - int(170 * math.sin(angle_rad))
            #print(f"{i} - {x}, {y} - {angle_rad} - {cardinal_point}")
            self.canvas.create_text(x, y, text=cardinal_point, fill="black")

    def update_gui(self):
        # Legge i dati dalla seriale e aggiorna l'interfaccia grafica
        while True:
            try:
                data = self.serial_port.readline().decode().strip()
                values = data.split(',')
                left_sensor_value = int(values[0])
                right_sensor_value = int(values[1])
                diff_sensor_value = int(values[2])
                angle_value = int(values[3])

                self.left_sensor_label.config(text=f"Fotocellula Sinistra: {left_sensor_value}")
                self.right_sensor_label.config(text=f"Fotocellula Destra: {right_sensor_value}")
                self.diff_sensor_label.config(text=f"Differenza: {diff_sensor_value}")
                self.angle_label.config(text=f"Angle: {angle_value}")

                self.update_arrow_position(angle_value)
                self.root.update()
            except ValueError:
                pass

    def update_arrow_position(self, angle):
        # Calcola la nuova posizione dell'immagine della freccia in base all'angolo
        x = 200 + int(150 * math.cos(math.radians(angle)))
        y = 200 - int(150 * math.sin(math.radians(angle)))

        # Aggiorna la posizione dell'immagine
        self.canvas.coords(self.arrow, x, y)

if __name__ == "__main__":
    root = tk.Tk()
    app = SolarTrackerApp(root)
    root.geometry("500x600")
    root.mainloop()
