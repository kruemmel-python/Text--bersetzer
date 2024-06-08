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
    model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{dest_lang}'
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    # Tokenize the input text
    tokenized_text = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    translated = model.generate(**tokenized_text)

    # Decode the generated tokens to get the translated text
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_text

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")])
    if file_path:
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        elif file_path.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        input_textbox.delete(1.0, tk.END)
        input_textbox.insert(tk.END, text)

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extrahiert Text aus einer PDF-Datei.
    
    :param pdf_path: Der Pfad zur PDF-Datei.
    :return: Der extrahierte Text.
    """
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def translate_file():
    src_lang = src_lang_combobox.get()
    dest_lang = dest_lang_combobox.get()
    
    if not src_lang or not dest_lang:
        messagebox.showwarning("Warnung", "Bitte wählen Sie sowohl die Quell- als auch die Zielsprache aus.")
        return

    text = input_textbox.get(1.0, tk.END).strip()
    if text:
        paragraphs = text.split('\n')
        translated_paragraphs = []

        for paragraph in paragraphs:
            if paragraph.strip():  # Nur nicht-leere Absätze übersetzen
                translated_paragraph = translate_text(paragraph, src_lang, dest_lang)
                translated_paragraphs.append(translated_paragraph)

        translated_text = '\n'.join(translated_paragraphs)
        output_textbox.delete(1.0, tk.END)
        output_textbox.insert(tk.END, translated_text)
    else:
        messagebox.showwarning("Warnung", "Die Eingabetextbox ist leer.")

def save_as_pdf():
    text = output_textbox.get(1.0, tk.END).strip()
    if text:
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter
            y = height - 72  # Startposition von oben
            for line in text.split('\n'):
                c.drawString(72, y, line)
                y -= 12  # Abstand zwischen den Zeilen
                if y < 72:  # Neue Seite bei Bedarf
                    c.showPage()
                    y = height - 72
            c.save()
            messagebox.showinfo("Erfolg", f"Übersetzter Text wurde in {file_path} gespeichert.")
    else:
        messagebox.showwarning("Warnung", "Die Ausgabetextbox ist leer.")

def paste_from_clipboard():
    clipboard_text = root.clipboard_get()
    input_textbox.delete(1.0, tk.END)
    input_textbox.insert(tk.END, clipboard_text)

# GUI Setup
root = tk.Tk()
root.title("Text Übersetzer")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

src_lang_label = tk.Label(frame, text="Quellsprache:")
src_lang_label.grid(row=0, column=0, pady=5)
src_lang_combobox = ttk.Combobox(frame, values=LANGUAGES)
src_lang_combobox.grid(row=0, column=1, pady=5)

dest_lang_label = tk.Label(frame, text="Zielsprache:")
dest_lang_label.grid(row=0, column=2, pady=5)
dest_lang_combobox = ttk.Combobox(frame, values=LANGUAGES)
dest_lang_combobox.grid(row=0, column=3, pady=5)

open_file_button = tk.Button(frame, text="Datei öffnen", command=open_file)
open_file_button.grid(row=1, column=0, columnspan=2, pady=5)

translate_button = tk.Button(frame, text="Übersetzen", command=translate_file)
translate_button.grid(row=1, column=2, columnspan=2, pady=5)

paste_button = tk.Button(frame, text="Aus Zwischenablage einfügen", command=paste_from_clipboard)
paste_button.grid(row=2, column=0, columnspan=4, pady=5)

save_pdf_button = tk.Button(frame, text="Als PDF speichern", command=save_as_pdf)
save_pdf_button.grid(row=3, column=0, columnspan=4, pady=5)

text_frame = tk.Frame(root)
text_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

input_textbox = tk.Text(text_frame, wrap=tk.WORD, width=40, height=20)
input_textbox.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

output_textbox = tk.Text(text_frame, wrap=tk.WORD, width=40, height=20)
output_textbox.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
