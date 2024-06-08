import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from transformers import MarianMTModel, MarianTokenizer
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

LANGUAGES = [
    "de", "en", "fr", "es", "it", "nl", "pt", "ru", "zh"  # Beispielsprachen
    # Fügen Sie hier weitere Sprachcodes hinzu, die von MarianMTModel unterstützt werden
]

def translate_text(text: str, src_lang: str, dest_lang: str) -> str:
    """
    Übersetzt den gegebenen Text von der Quellsprache zur Zielsprache.
    
    :param text: Der zu übersetzende Text.
    :param src_lang: Der Sprachcode der Quellsprache (z.B. 'de' für Deutsch).
    :param dest_lang: Der Sprachcode der Zielsprache (z.B. 'en' für Englisch).
    :return: Der übersetzte Text.
    """
    model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{dest_lang}'  # Modellname basierend auf Quell- und Zielsprache
    tokenizer = MarianTokenizer.from_pretrained(model_name)  # Lädt den Tokenizer für das Modell
    model = MarianMTModel.from_pretrained(model_name)  # Lädt das Modell

    # Tokenisiert den Eingabetext
    tokenized_text = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    translated = model.generate(**tokenized_text)  # Generiert die Übersetzung

    # Dekodiert die generierten Tokens, um den übersetzten Text zu erhalten
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_text  # Gibt den übersetzten Text zurück

def open_file():
    # Öffnet einen Dateidialog, um eine Datei auszuwählen
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")])
    if file_path:  # Wenn eine Datei ausgewählt wurde
        if file_path.endswith('.txt'):  # Wenn die Datei eine Textdatei ist
            with open(file_path, 'r', encoding='utf-8') as file:  # Öffnet die Datei zum Lesen
                text = file.read()  # Liest den gesamten Text aus der Datei
        elif file_path.endswith('.pdf'):  # Wenn die Datei eine PDF-Datei ist
            text = extract_text_from_pdf(file_path)  # Extrahiert Text aus der PDF-Datei
        input_textbox.delete(1.0, tk.END)  # Löscht den aktuellen Inhalt der Eingabetextbox
        input_textbox.insert(tk.END, text)  # Fügt den extrahierten Text in die Eingabetextbox ein

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extrahiert Text aus einer PDF-Datei.
    
    :param pdf_path: Der Pfad zur PDF-Datei.
    :return: Der extrahierte Text.
    """
    text = ""  # Initialisiert eine leere Zeichenkette für den Text
    with open(pdf_path, "rb") as file:  # Öffnet die PDF-Datei zum Lesen im Binärmodus
        reader = PdfReader(file)  # Erstellt einen PdfReader-Objekt
        for page in reader.pages:  # Durchläuft jede Seite der PDF-Datei
            text += page.extract_text()  # Fügt den extrahierten Text zur Zeichenkette hinzu
    return text  # Gibt den gesamten extrahierten Text zurück

def translate_file():
    src_lang = src_lang_combobox.get()  # Holt den ausgewählten Sprachcode der Quellsprache
    dest_lang = dest_lang_combobox.get()  # Holt den ausgewählten Sprachcode der Zielsprache
    
    if not src_lang or not dest_lang:  # Überprüft, ob eine Sprache nicht ausgewählt wurde
        messagebox.showwarning("Warnung", "Bitte wählen Sie sowohl die Quell- als auch die Zielsprache aus.")  # Zeigt eine Warnung an
        return

    text = input_textbox.get(1.0, tk.END).strip()  # Holt den Text aus der Eingabetextbox und entfernt überflüssige Leerzeichen
    if text:  # Überprüft, ob der Text nicht leer ist
        paragraphs = text.split('\n')  # Teilt den Text in Absätze auf
        translated_paragraphs = []  # Initialisiert eine Liste für die übersetzten Absätze

        for paragraph in paragraphs:  # Durchläuft jeden Absatz
            if paragraph.strip():  # Übersetzt nur nicht-leere Absätze
                translated_paragraph = translate_text(paragraph, src_lang, dest_lang)  # Übersetzt den Absatz
                translated_paragraphs.append(translated_paragraph)  # Fügt den übersetzten Absatz zur Liste hinzu

        translated_text = '\n'.join(translated_paragraphs)  # Verbindet die übersetzten Absätze zu einem Text
        output_textbox.delete(1.0, tk.END)  # Löscht den aktuellen Inhalt der Ausgabetextbox
        output_textbox.insert(tk.END, translated_text)  # Fügt den übersetzten Text in die Ausgabetextbox ein
    else:
        messagebox.showwarning("Warnung", "Die Eingabetextbox ist leer.")  # Zeigt eine Warnung an, wenn die Eingabetextbox leer ist

def save_as_pdf():
    text = output_textbox.get(1.0, tk.END).strip()  # Holt den Text aus der Ausgabetextbox und entfernt überflüssige Leerzeichen
    if text:  # Überprüft, ob der Text nicht leer ist
        # Öffnet einen Dialog zum Speichern der Datei
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:  # Wenn ein Speicherort ausgewählt wurde
            c = canvas.Canvas(file_path, pagesize=letter)  # Erstellt ein Canvas-Objekt für die PDF-Erstellung
            width, height = letter  # Holt die Breite und Höhe der Seite
            y = height - 72  # Startposition von oben
            max_line_length = 85  # Maximale Zeichenlänge pro Zeile (abhängig von der Schriftgröße und Seitengröße)

            for line in text.split('\n'):  # Durchläuft jede Zeile des Textes
                while len(line) > max_line_length:  # Wenn die Zeile länger als die maximale Länge ist
                    c.drawString(72, y, line[:max_line_length])  # Zeichnet den Teil der Zeile auf das PDF
                    line = line[max_line_length:]  # Schneidet den gezeichneten Teil der Zeile ab
                    y -= 12  # Abstand zwischen den Zeilen
                    if y < 72:  # Wenn der Platz auf der Seite nicht ausreicht
                        c.showPage()  # Erstellt eine neue Seite
                        y = height - 72  # Setzt die Startposition zurück

                c.drawString(72, y, line)  # Zeichnet die restliche Zeile auf das PDF
                y -= 12  # Abstand zwischen den Zeilen
                if y < 72:  # Wenn der Platz auf der Seite nicht ausreicht
                    c.showPage()  # Erstellt eine neue Seite
                    y = height - 72  # Setzt die Startposition zurück

            c.save()  # Speichert die PDF-Datei
            messagebox.showinfo("Erfolg", f"Übersetzter Text wurde in {file_path} gespeichert.")  # Zeigt eine Erfolgsmeldung an
    else:
        messagebox.showwarning("Warnung", "Die Ausgabetextbox ist leer.")  # Zeigt eine Warnung an, wenn die Ausgabetextbox leer ist

def paste_from_clipboard():
    clipboard_text = root.clipboard_get()  # Holt den Text aus der Zwischenablage
    input_textbox.delete(1.0, tk.END)  # Löscht den aktuellen Inhalt der Eingabetextbox
    input_textbox.insert(tk.END, clipboard_text)  # Fügt den Text aus der Zwischenablage in die Eingabetextbox ein

# GUI Setup
root = tk.Tk()  # Erstellt das Hauptfenster
root.title("Text Übersetzer")  # Setzt den Titel des Fensters

frame = tk.Frame(root, padx=10, pady=10)  # Erstellt einen Rahmen zur Anordnung der Widgets
frame.pack(padx=10, pady=10)  # Packt den Rahmen in das Hauptfenster

src_lang_label = tk.Label(frame, text="Quellsprache:")  # Erstellt ein Label für die Quellsprache
src_lang_label.grid(row=0, column=0, pady=5)  # Positioniert das Label im Raster
src_lang_combobox = ttk.Combobox(frame, values=LANGUAGES)  # Erstellt ein Dropdown-Menü für die Quellsprache
src_lang_combobox.grid(row=0, column=1, pady=5)  # Positioniert das Dropdown-Menü im Raster

dest_lang_label = tk.Label(frame, text="Zielsprache:")  # Erstellt ein Label für die Zielsprache
dest_lang_label.grid(row=0, column=2, pady=5)  # Positioniert das Label im Raster
dest_lang_combobox = ttk.Combobox(frame, values=LANGUAGES)  # Erstellt ein Dropdown-Menü für die Zielsprache
dest_lang_combobox.grid(row=0, column=3, pady=5)  # Positioniert das Dropdown-Menü im Raster

open_file_button = tk.Button(frame, text="Datei öffnen", command=open_file)  # Erstellt einen Button zum Öffnen einer Datei
open_file_button.grid(row=1, column=0, columnspan=2, pady=5)  # Positioniert den Button im Raster

translate_button = tk.Button(frame, text="Übersetzen", command=translate_file)  # Erstellt einen Button zum Übersetzen
translate_button.grid(row=1, column=2, columnspan=2, pady=5)  # Positioniert den Button im Raster

paste_button = tk.Button(frame, text="Aus Zwischenablage einfügen", command=paste_from_clipboard)  # Erstellt einen Button zum Einfügen aus der Zwischenablage
paste_button.grid(row=2, column=0, columnspan=4, pady=5)  # Positioniert den Button im Raster

save_pdf_button = tk.Button(frame, text="Als PDF speichern", command=save_as_pdf)  # Erstellt einen Button zum Speichern als PDF
save_pdf_button.grid(row=3, column=0, columnspan=4, pady=5)  # Positioniert den Button im Raster

text_frame = tk.Frame(root)  # Erstellt einen Rahmen für die Textboxen
text_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)  # Packt den Rahmen in das Hauptfenster

input_textbox = tk.Text(text_frame, wrap=tk.WORD, width=40, height=20)  # Erstellt eine Textbox für den Eingabetext
input_textbox.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)  # Positioniert die Textbox im Rahmen

output_textbox = tk.Text(text_frame, wrap=tk.WORD, width=40, height=20)  # Erstellt eine Textbox für den Ausgabetext
output_textbox.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)  # Positioniert die Textbox im Rahmen

root.mainloop()  # Startet die Hauptschleife der GUI
