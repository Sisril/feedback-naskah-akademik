import docx
from pdfminer.high_level import extract_text as extract_pdf_text
import openai
import re
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text(file):
    if file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    elif file.name.endswith(".pdf"):
        return extract_pdf_text(file)
    else:
        return "Format file tidak didukung"

def extract_bab1(text):
   match = re.search(r'(?i)\bBAB\s*[I1]\b(.*?)(?=\bBAB\s*[II2]\b|DAFTAR PUSTAKA|$)', text, re.DOTALL)
    return match.group(1) if match else "Bab I tidak ditemukan"

def analyze_bab1(bab1_text):
    prompt = f"""
Evaluasilah Bab I berikut berdasarkan kriteria:
1. Latar belakang: apakah menjelaskan topik secara umum, relevan, berbasis data, dan merujuk kajian terbaru?
2. Rumusan masalah: apakah dalam bentuk 'bagaimana' atau 'mengapa', dan sesuai dengan latar belakang?
3. Tujuan penelitian: apakah sejalan dengan rumusan masalah?
4. Manfaat penelitian: apakah dijelaskan secara teoritis dan praktis?

Teks Bab I:
{bab1_text}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=800
    )
    return response['choices'][0]['message']['content']
