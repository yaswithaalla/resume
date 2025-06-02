import streamlit as st
from fpdf import FPDF
import os
import tempfile
from datetime import date

st.set_page_config(page_title="Resume Builder", layout="centered")

def sanitize_text(text):
    return text.replace("–", "-").replace("’", "'").replace("“", '"').replace("”", '"') if text else ""

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 16)
        self.cell(0, 10, self.title, ln=True, align="C")

    def add_section_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, sanitize_text(title), ln=True)

    def add_text(self, text):
        self.set_font("Arial", "", 11)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 8, sanitize_text(text))
        self.ln(2)

# Streamlit UI
st.title("📄 Resume Builder")

with st.form("resume_form"):
    st.subheader("🔹 Personal Info")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    linkedin = st.text_input("LinkedIn URL")
    github = st.text_input("GitHub URL")

    st.subheader("🔹 Summary & Education")
    summary = st.text_area("Professional Summary")
    degree = st.text_input("Degree and Branch")
    college = st.text_input("College Name")
    edu_duration = st.text_input("Duration (e.g. 2021 - 2025)")
    cgpa = st.text_input("CGPA / Percentage")
    courses = st.text_input("Relevant Coursework")

    st.subheader("🔹 Skills & Projects")
    skills = st.text_area("Skills (comma separated)")
    project_title = st.text_input("Project Title")
    project_tech = st.text_input("Technologies Used")
    project_desc = st.text_area("Project Description")

    st.subheader("🔹 Experience & Certifications")
    exp_title = st.text_input("Experience Title")
    exp_company = st.text_input("Company Name")
    exp_desc = st.text_area("Experience Description")
    cert1 = st.text_input("Certification 1")
    cert2 = st.text_input("Certification 2")

    st.subheader("🔹 Extras")
    achievements = st.text_area("Achievements / Extracurriculars")
    languages = st.text_input("Languages Known")
    place = st.text_input("Place")
    today = date.today().strftime("%B %d, %Y")

    submitted = st.form_submit_button("📄 Generate Resume")

if submitted:
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.title = sanitize_text(name)
    pdf.add_page()

    # Header Info
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, sanitize_text(name), ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"{sanitize_text(email)} | {sanitize_text(phone)}", ln=True)
    pdf.cell(0, 8, f"LinkedIn: {sanitize_text(linkedin)} | GitHub: {sanitize_text(github)}", ln=True)
    pdf.ln(5)

    # Sections
    pdf.add_section_title("Professional Summary")
    pdf.add_text(summary)

    pdf.add_section_title("Education")
    pdf.add_text(f"{degree}, {college}\n{edu_duration} | {cgpa}\nCourses: {courses}")

    pdf.add_section_title("Technical Skills")
    pdf.add_text(skills)

    pdf.add_section_title("Project")
    pdf.add_text(f"{project_title} - {project_tech}\n{project_desc}")

    pdf.add_section_title("Experience")
    pdf.add_text(f"{exp_title} at {exp_company}\n{exp_desc}")

    pdf.add_section_title("Certifications")
    cert_text = "\n".join(filter(None, [cert1, cert2]))
    pdf.add_text(cert_text)

    pdf.add_section_title("Achievements & Extracurriculars")
    pdf.add_text(achievements)

    pdf.add_section_title("Languages")
    pdf.add_text(languages)

    # Declaration
    pdf.ln(10)
    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(0, 8, sanitize_text(f"I hereby declare that the above information is true.\nDate: {today}\nPlace: {place}"))

    # Save PDF to temporary file and provide download
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        tmp.seek(0)
        st.success("✅ Resume generated successfully!")
        st.download_button("📥 Download Resume PDF", tmp, file_name="My_Resume.pdf", mime="application/pdf")


