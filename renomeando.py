import os
import re
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract

# Configuração do pytesseract (ajuste o caminho se necessário)
# Exemplo no Windows:
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\ccastro\Downloads\AUTOMAÇÂO\ORGANIZADOR DE CT"

# Caminho da pasta onde estão os PDFs
pasta = r"C:\Users\ccastro\Downloads\AUTOMAÇÂO\ORGANIZADOR DE CT\arquivos"

# Caminho da pasta 'bin' do Poppler (não precisa adicionar ao PATH)
poppler_path = r"C:\Users\ccastro\Downloads\AUTOMAÇÂO\ORGANIZADOR DE CT\poppler-25.07.0\Library\bin"

def extrair_texto_pdf(caminho_pdf):
    """Tenta extrair texto diretamente do PDF com PyPDF2"""
    try:
        with open(caminho_pdf, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text and "QUADRO RESUMO" in page_text.upper():
                    return page_text
    except Exception as e:
        print(f"Erro ao abrir PDF com PyPDF2: {caminho_pdf} → {e}")
    return None

def extrair_texto_ocr(caminho_pdf):
    """Extrai texto do PDF usando OCR com pdf2image + pytesseract"""
    try:
        imagens = convert_from_path(caminho_pdf, dpi=300, poppler_path=poppler_path)
        for img in imagens:
            page_text = pytesseract.image_to_string(img, lang='por')
            if "QUADRO RESUMO" in page_text.upper():
                return page_text
    except Exception as e:
        print(f"Erro no OCR: {caminho_pdf} → {e}")
    return None

def extrair_dados(caminho_pdf):
    # Primeiro tenta PyPDF2
    texto = extrair_texto_pdf(caminho_pdf)

    unidade, bloco, torre, sufixo = None, "", "", ""

    if texto:
        texto = re.sub(r"\s+", " ", texto).upper()
        unidade_match = re.search(r"UNIDADE AUT[ÔO]NOMA[:\s]*([0-9]{2,5})", texto, re.I)
        unidade = unidade_match.group(1) if unidade_match else None
        bloco_match = re.search(r"\bBLOCO\s+([A-Z])\b", texto, re.I)
        bloco = bloco_match.group(1) if bloco_match else ""
        torre_match = re.search(r"\bTORRE\s+(?!ÚNICA)([A-Z])\b", texto, re.I)
        torre = torre_match.group(1) if torre_match else ""
        sufixo = bloco or torre

    # Se falhou em extrair Unidade, força OCR
    if not unidade:
        print(f"📌 Tentando OCR em {os.path.basename(caminho_pdf)}")
        texto_ocr = extrair_texto_ocr(caminho_pdf)
        if texto_ocr:
            texto_ocr = re.sub(r"\s+", " ", texto_ocr).upper()
            unidade_match = re.search(r"UNIDADE AUT[ÔO]NOMA[:\s]*([0-9]{2,5})", texto_ocr, re.I)
            unidade = unidade_match.group(1) if unidade_match else None
            bloco_match = re.search(r"\bBLOCO\s+([A-Z])\b", texto_ocr, re.I)
            bloco = bloco_match.group(1) if bloco_match else ""
            torre_match = re.search(r"\bTORRE\s+(?!ÚNICA)([A-Z])\b", texto_ocr, re.I)
            torre = torre_match.group(1) if torre_match else ""
            sufixo = bloco or torre

    # Debug
    print(f"🔎 {os.path.basename(caminho_pdf)} → Unidade: {unidade}, Bloco: {bloco}, Torre: {torre}, Sufixo: {sufixo}")
    return unidade, sufixo

def renomear_pdfs(pasta):
    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith(".pdf"):
            caminho_pdf = os.path.join(pasta, arquivo)
            unidade, sufixo = extrair_dados(caminho_pdf)

            if unidade:
                novo_nome = f"{unidade} {sufixo}".strip() + ".pdf"
                novo_caminho = os.path.join(pasta, novo_nome)

                if not os.path.exists(novo_caminho):
                    try:
                        os.rename(caminho_pdf, novo_caminho)
                        print(f"✅ Renomeado: {arquivo} → {novo_nome}")
                    except PermissionError:
                        print(f"❌ Arquivo em uso, não foi possível renomear: {arquivo}")
                else:
                    print(f"⚠️ Arquivo já existe: {novo_nome} — pulando...")
            else:
                print(f"❌ Não foi possível extrair dados de {arquivo}")

# ==== EXECUÇÃO ====
renomear_pdfs(pasta)



