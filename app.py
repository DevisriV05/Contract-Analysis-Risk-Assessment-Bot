import streamlit as st
from nlp_utils import extract_text, split_clauses, extract_entities
from risk_engine import score_clause, contract_score
from llm_utils import explain_clause
from audit import save_audit
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="GenAI Legal Assistant")

st.title("🧑‍⚖️ SME Contract Analyzer")

uploaded = st.file_uploader("Upload Contract", type=["pdf", "docx", "txt"])

if uploaded:
    text = extract_text(uploaded)

    clauses = split_clauses(text)
    entities = extract_entities(text)

    results = []
    scores = []

    for c in clauses:
        r = score_clause(c)
        scores.append(r)

        results.append({
            "clause": c,
            "risk": r,
            "explanation": explain_clause(c)
        })

    overall = contract_score(scores)

    st.subheader("📊 Contract Risk Level")
    st.write(overall)

    st.subheader("📌 Key Entities")
    st.json(entities)

    st.subheader("📄 Clause Analysis")

    for i, r in enumerate(results):
        with st.expander(f"Clause {i+1} – Risk: {r['risk']}"):
            st.write(r["clause"])
            st.info(r["explanation"])

    if st.button("Save Audit"):
        audit_id = save_audit({
            "entities": entities,
            "results": results,
            "overall_risk": overall
        })
        st.success(f"Audit saved: {audit_id}")

    if st.button("Export PDF"):
        styles = getSampleStyleSheet()
        doc = SimpleDocTemplate("report.pdf", pagesize=A4)

        flow = [Paragraph(f"<b>Overall Risk:</b> {overall}", styles["Normal"])]

        for r in results:
            flow.append(Paragraph(f"<b>Risk:</b> {r['risk']}", styles["Normal"]))
            flow.append(Paragraph(r["explanation"], styles["Normal"]))

        doc.build(flow)
        st.success("PDF generated as report.pdf")
