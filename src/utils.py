from PyPDF2 import PdfReader
import docx
from PIL import Image
import pytesseract

def ler_pdf(caminho):
    try:
        texto = ""
        pdf = PdfReader(caminho)
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n"
        return texto
    except:
        return ""

def ler_docx(caminho):
    try:
        doc = docx.Document(caminho)
        return "\n".join([p.text for p in doc.paragraphs])
    except:
        return ""

def ler_imagem(caminho):
    try:
        img = Image.open(caminho)
        return pytesseract.image_to_string(img, lang='por')
    except:
        return ""
