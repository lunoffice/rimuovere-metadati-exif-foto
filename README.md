# Rimuovere i metadati EXIF dalle foto (locale)

Script Python **offline** che rimuove i metadati EXIF (coordinate GPS, data di scatto, modello del dispositivo) da un'immagine con [`Pillow`](https://pypi.org/project/pillow/), salvando una copia pulita senza toccare l'originale.

Allineato alla guida Lab di ai riparo:

**[Rimuovere i metadati EXIF dalle foto prima di inviarle](https://airiparo.it/lab/rimuovere-metadati-exif-foto/)**

## Caratteristiche

- Pulizia locale: dopo l'installazione di `Pillow` lo script **non** apre connessioni di rete
- Crea una copia con prefisso `pulita_` accanto all'originale, che resta intatto
- Applica l'orientamento EXIF ai pixel prima di scartare i metadati (le foto verticali restano dritte)
- Rimuove EXIF e XMP
- Formati: `.jpg`, `.jpeg`, `.png`, `.webp`, `.tif`, `.tiff`
- Licenza **MIT**

## Requisiti

- Python **3.9+**
- Dipendenza: `Pillow` (nel `venv` del progetto)
- Windows, macOS o Linux

## Installazione

### Opzione 1 — Clona il repository

```bash
git clone https://github.com/lunoffice/rimuovere-metadati-exif-foto.git
cd rimuovere-metadati-exif-foto
python3 -m venv .venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\activate.bat
python -m pip install Pillow
```

### Opzione 2 — Solo lo script

Scarica `pulisci_exif.py` dalla [release/pagina del repo](https://github.com/lunoffice/rimuovere-metadati-exif-foto) oppure dalla scheda download su ai riparo (stesso SHA-256):

[Download verificato su ai riparo](https://airiparo.it/lab/rimuovere-metadati-exif-foto/)

## Uso

```bash
python pulisci_exif.py foto.jpg

# percorsi con spazi: usa le virgolette
python pulisci_exif.py "C:\Users\Tu\Foto estate\foto.jpg"
python3 pulisci_exif.py "/Users/tu/Foto estate/foto.jpg"
```

### Esempio di output

```text
Lettura: foto.jpg
Fatto. Immagine senza metadati salvata in: …/pulita_foto.jpg
```

## Opzioni della CLI

| Argomento | Effetto | Default |
| --- | --- | --- |
| `immagine` (posizionale) | File immagine da pulire | obbligatorio |
| `--version` | Mostra la versione dello script | — |
| `-h` / `--help` | Aiuto nativo | — |

## Note di privacy e sicurezza

- Molte app di messaggistica ricomprimono le foto, ma non tutte rimuovono i metadati in ogni modalità di invio (per esempio «come file»).
- Lo script lavora solo sul file che indichi: non carica nulla online.
- I JPEG vengono salvati di nuovo con qualità 95: la copia può differire di poco dall'originale.

## Checksum

Lo SHA-256 di `pulisci_exif.py` è pubblicato nella scheda download della guida Lab (deve coincidere con il file di questo repository).

## Licenza

MIT — Copyright (c) 2026 Alex Lunalbi (ai riparo)
