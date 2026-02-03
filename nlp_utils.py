import spacy
import re
import pdfplumber
from docx import Document

nlp = spacy.load("en_core_web_sm")


def extract_text(file):
    name = file.name.lower()

    if name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            return "\n".join([p.extract_text() or "" for p in pdf.pages])

    if name.endswith(".docx"):
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

    return file.read().decode("utf-8")


def split_clauses(text):
    clauses = re.split(r"\n\d+\.|\n[a-zA-Z]\)", text)
    return [c.strip() for c in clauses if len(c.strip()) > 40]


def extract_entities(text):
    doc = nlp(text)
    result = []

    for ent in doc.ents:
        if ent.label_ in ["ORG", "PERSON", "DATE", "MONEY", "GPE"]:
            result.append({
                "text": ent.text,
                "label": ent.label_
            })

    return result
