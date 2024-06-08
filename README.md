# Text Übersetzer

Ein einfacher Textübersetzer, der eine grafische Benutzeroberfläche (GUI) bietet, um Text- und PDF-Dateien zu übersetzen. Der Übersetzer verwendet das MarianMT-Modell und bietet Unterstützung für mehrere Sprachen.

## Funktionen

- Laden von Text- und PDF-Dateien zur Übersetzung
- Übersetzung zwischen verschiedenen Sprachen
- Einfügen von Text aus der Zwischenablage
- Speichern des übersetzten Textes als PDF-Datei

## Unterstützte Sprachen

- Deutsch (de)
- Englisch (en)
- Französisch (fr)
- Spanisch (es)
- Italienisch (it)
- Niederländisch (nl)
- Portugiesisch (pt)
- Russisch (ru)
- Chinesisch (zh)

## Installation

1. **Klonen Sie das Repository**

    ```bash
    git clone https://github.com/IhrBenutzername/Text-Übersetzer.git
    cd Text-Übersetzer
    ```

2. **Erstellen Sie eine virtuelle Umgebung und aktivieren Sie sie**

    ```bash
    python -m venv env
    source env/bin/activate  # Auf Windows: env\Scripts\activate
    ```

3. **Installieren Sie die erforderlichen Bibliotheken**

    ```bash
    pip install -r requirements.txt
    ```

## Abhängigkeiten

- tkinter
- transformers
- PyPDF2
- reportlab

Installieren Sie die Abhängigkeiten mit:

```bash
pip install tkinter transformers PyPDF2 reportlab
```

## Nutzung

Führen Sie das Skript `translator_gui.py` aus:

```bash
python translator_gui.py
```

### Benutzeranleitung

1. **Quell- und Zielsprache auswählen**: Wählen Sie die Sprachen aus den Dropdown-Menüs aus.
2. **Datei öffnen**: Klicken Sie auf den Button "Datei öffnen", um eine Text- oder PDF-Datei auszuwählen.
3. **Text aus Zwischenablage einfügen**: Klicken Sie auf den Button "Aus Zwischenablage einfügen", um Text aus der Zwischenablage in die Eingabetextbox einzufügen.
4. **Übersetzen**: Klicken Sie auf den Button "Übersetzen", um den Text in der Eingabetextbox zu übersetzen. Der übersetzte Text wird in der Ausgabetextbox angezeigt.
5. **Als PDF speichern**: Klicken Sie auf den Button "Als PDF speichern", um den übersetzten Text als PDF-Datei zu speichern.

## Screenshots


![Hauptfenster](https://github.com/kruemmel-python/Text--bersetzer/assets/169469747/e18542a1-36cb-4849-af85-6452ff34cec5)


## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Weitere Informationen finden Sie in der `LICENSE`-Datei.

## Beitrag

Beiträge sind willkommen! Bitte öffnen Sie ein Issue oder senden Sie einen Pull-Request.

## Autoren

- [Ralf Krümmel]([(https://github.com/kruemmel-python))

## Danksagungen

- Vielen Dank an die Entwickler der Bibliotheken `transformers`, `PyPDF2` und `reportlab`.


