import tkinter as tk
from tkinter import scrolledtext
import re


def read_clients(file_path):
    """Citește clienții din fișier și returnează o listă de clienți pentru anul specificat."""
    try:
        with open(file_path, 'r') as f:
            clients = []
            for line in f:
                # Extrage data și numele clientului din linie
                match = re.match(r'^[DS] (\d{2}/\d{2}/\d{4}) (.+?)\s+\d+\.\d+\s+.+$', line.strip())
                if match:
                    date_str, client_name = match.groups()
                    day, month, year = map(int, date_str.split('/'))
                    clients.append((client_name, year, month, line.strip()))  # Salvează întreaga linie
            return clients
    except Exception as e:
        show_result_window(f"Eroare: Nu am putut citi fișierul: {e}")
        return []


def show_result_window(message):
    """Afișează rezultatul într-o fereastră personalizată."""
    result_window = tk.Toplevel(root)
    result_window.title("Rezultate")
    result_window.geometry("1000x800")  # Setează dimensiunea dorită

    # Setează fontul dorit
    font_style = ("Arial", 14)  # Aici poți modifica fontul și dimensiunea

    text_area = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=70, height=25, font=font_style)  # Dimensiuni mărite
    text_area.pack(padx=100, pady=(10, 10))

    text_area.insert(tk.END, message)  # Adaugă mesajul în fereastră
    text_area.config(state=tk.DISABLED)  # Dezactivează editarea

    close_button = tk.Button(result_window, text="Închide", command=result_window.destroy)
    close_button.pack(pady=(10,0))


def compare_clients(start_date, end_date):
    """Compară clienții din cele două fișiere și extrage cei care nu au venit în anul următor."""
    # Parsează datele de început și sfârșit
    try:
        start_month, start_year = map(int, start_date.split('/'))
        end_month, end_year = map(int, end_date.split('/'))
    except ValueError:
        show_result_window("Eroare: Formatul datei trebuie să fie MM/YYYY.")
        return

    clients_2023 = read_clients('revizii1.txt')
    clients_2024 = read_clients('revizii2.txt')

    # Extrage clienții din anul specificat
    clients_start_year_set = {
        client for client in clients_2023
        if client[1] == start_year and client[2] == start_month
    }

    clients_end_year_set = {
        client for client in clients_2024
        if client[1] == end_year and client[2] == end_month
    }

    # Extrage clienții care au venit în anul de început dar nu în anul de sfârșit
    missing_clients = sorted(
        [client[3] for client in clients_start_year_set if client not in clients_end_year_set]
    )

    # Scrie rezultatul într-un fișier
    with open('missing_clients.txt', 'w') as f:
        for client in missing_clients:
            f.write(client + '\n')

    # Afișează clienții lipsă într-o fereastră personalizată
    if missing_clients:
        result_text = f"Am găsit {len(missing_clients)} clienți lipsă:\n" + "\n".join(missing_clients)
    else:
        result_text = "Nu am găsit clienți lipsă."

    show_result_window(result_text)


def reset_fields():
    """Resetează câmpurile de input."""
    start_date_entry.delete("1.0", tk.END)
    end_date_entry.delete("1.0", tk.END)


# Configurare GUI
root = tk.Tk()
root.title("Comparare Clienți")
root.geometry("400x400")

# Câmpuri de input pentru date
tk.Label(root, text="Data început (MM/YYYY):").pack()
start_date_entry = tk.Text(root, width=20, height=2, font=("Arial", 18))  # Marime text camp input
start_date_entry.pack()

tk.Label(root, text="Data sfârșit (MM/YYYY):").pack()
end_date_entry = tk.Text(root, width=20, height=2, font=("Arial", 18))
end_date_entry.pack()

# Buton pentru comparare
compare_button = tk.Button(root, text="Compară Clienți",
                           command=lambda: compare_clients(start_date_entry.get("1.0", tk.END).strip(),
                                                           end_date_entry.get("1.0", tk.END).strip()))
compare_button.pack()

# Buton pentru resetare
reset_button = tk.Button(root, text="Resetare", command=reset_fields)
reset_button.pack()

root.mainloop()
