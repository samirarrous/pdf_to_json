"""
Module for extracting text and tables from PDF documents using pdfplumber and EasyOCR.
"""
import pdfplumber
import easyocr
import cv2
import numpy as np
from PIL import Image

# Initialisation unique du reader (coûteux à charger)
reader = easyocr.Reader(["fr", "en"], gpu=False)


def clean_image(pil_image: Image.Image) -> np.ndarray:
    """Prétraitement image pour améliorer la qualité OCR."""
    img = np.array(pil_image)

    # Conversion correcte selon les canaux
    if img.ndim == 2:
        gray = img
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Upscaling si résolution trop faible
    h, w = gray.shape[:2]
    if w < 2000:
        scale = 2000 / w
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # Amélioration contraste
    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Réduction bruit
    gray = cv2.medianBlur(gray, 3)

    return gray  # EasyOCR accepte directement un numpy array


def ocr_image(img_array: np.ndarray) -> str:
    """Lance EasyOCR sur un numpy array et retourne le texte."""
    results = reader.readtext(img_array, detail=0, paragraph=True)
    return "\n".join(results)


def extract_text(file_path: str, poppler_path: str = None) -> str:
    """
    Extrait le texte d'un PDF.
    - Texte natif via pdfplumber si disponible
    - Fallback EasyOCR sur les pages avec images

    Args:
        file_path (str): Chemin vers le fichier PDF.
        poppler_path (str): Chemin vers Poppler sur Windows
                            ex: r"C:\\poppler\\Library\\bin"
    """
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

            if page.images:
                # Utilise PyMuPDF (fitz) pour convertir la page en image (sans dépendance à Poppler)
                import fitz
                doc = fitz.open(file_path)
                fitz_page = doc.load_page(i)
                pix = fitz_page.get_pixmap(dpi=300)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                images = [img]
                

    return text


def extract_tables(file_path: str) -> list:
    """
    Extrait les tableaux structurels d'un PDF via pdfplumber.

    Args:
        file_path (str): Chemin vers le fichier PDF.

    Returns:
        list: Liste de tableaux (liste de lignes, chaque ligne est une liste de cellules).
    """
    with pdfplumber.open(file_path) as pdf:
        tables = []
        for page in pdf.pages:
            tables.extend(page.extract_tables())
        return tables