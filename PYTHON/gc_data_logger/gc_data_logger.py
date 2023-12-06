import serial
import matplotlib.pyplot as plt
import keyboard
import time

# Configurazione della porta seriale
ser = serial.Serial('COM5', 9600, timeout=0.1)

# Lista per memorizzare i valori
values = []

def print_menu() :
        # Menu testuale
        print("Menu:")
        print("1. Stampa valori")
        print("2. Plotta valori")
        print("3. Cancella dati")
        print("x. Esci")

while True:

    print_menu()

    choice = input("Inserisci la tua scelta: ")

    try:
        # Leggi il valore dalla seriale
        value = int(ser.readline().decode().strip())
        values.append(value)
    except ValueError as e:
            print(f"Errore nella conversione: {e}")
            print(f"Dati non validi Inviali da arduino : {ser.readline().decode().strip()}")
            time.sleep(0.1)  # Aggiungi un breve ritardo per garantire che l'intero dato sia stato inviato completamente
    
    if choice == '1':
        print("\n >>> Valori :", values)
        print("\n")
    elif choice == '2':
        # Plot dei valori con aggiunta del valore di ogni punto
        plt.plot(values, marker='o', label='Valore')
        for i, val in enumerate(values):
            plt.text(i, val, str(val))
        plt.title("Grafico dei valori del potenziometro")
        plt.xlabel("Tempo")
        plt.ylabel("Valore")
        plt.legend()
        plt.show()
    elif choice == '3':
        # Cancella i dati
        values = []      
        print("\n >>> Dati cancellati.\n")      
    elif choice == 'x' or keyboard.is_pressed('esc') or keyboard.is_pressed('Esc'):
        break
    else:
        print("Scelta non valida. Riprova.")

# Chiudi la porta seriale
ser.close()
