import streamlit as st
from jinja2 import Template
import pdfkit
import tempfile
import os

st.set_page_config(page_title="Resume Generator", layout="centered")
st.title("📄 BTech Fresher Resume Generator")

if "education" not in st.session_state:
    st.session_state.education = []
if "projects" not in st.session_state:
    st.session_state.projects = []

name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
linkedin = st.text_input("LinkedIn URL")
github = st.text_input("GitHub URL")
objective = st.text_area("Career Objective", height=80)

st.subheader("🎓 Education")
with st.form("education_form", clear_on_submit=True):
    degree = st.text_input("Degree")
    college = st.text_input("College")
    year = st.text_input("Year")
    cgpa = st.text_input("CGPA")
    if st.form_submit_button("Add Education"):
        st.session_state.education.append({
            "degree": degree, "college": college, "year": year, "cgpa": cgpa
        })

for edu in st.session_state.education:
    st.write(f"• {edu['degree']}, {edu['college']} ({edu['year']}) — CGPA: {edu['cgpa']}")

st.subheader("🚀 Projects")
with st.form("project_form", clear_on_submit=True):
    proj_title = st.text_input("Project Title")
    proj_desc = st.text_area("Project Description")
    proj_tech = st.text_input("Tech Stack")
    if st.form_submit_button("Add Project"):
        st.session_state.projects.append({
            "title": proj_title, "desc": proj_desc, "tech": proj_tech
        })

for proj in st.session_state.projects:
    st.write(f"• *{proj['title']}* | {proj['tech']}")
    st.write(proj['desc'])

skills = st.text_area("Technical Skills (comma-separated)")
achievements = st.text_area("Achievements (one per line)")
certifications = st.text_area("Certifications (one per line)")
internships = st.text_area("Internships (Company - Role - Duration - Description)")
workshops = st.text_area("Workshops/Seminars Attended")
extras = st.text_area("Extra-curricular / Leadership Roles")
languages_known = st.text_input("Languages Known (comma-separated)")

html_template = """
<!DOCTYPE html>
<html>
<head>
<style>
body { font-family: Arial, sans-serif; font-size: 14px; margin: 20px; color: #000; }
h1 { font-size: 28px; margin-bottom: 8px; color: #2c3e50; }
h2 { font-size: 20px; margin-top: 22px; border-bottom: 1px solid #ccc; padding-bottom: 4px; color: #2c3e50; }
p, li { margin: 4px 0; }
ul { padding-left: 20px; margin: 0; }
</style>
</head>
<body>
<h1>{{ name }}</h1>
<p><strong>Email:</strong> {{ email }} | <strong>Phone:</strong> {{ phone }}</p>
<p><strong>LinkedIn:</strong> {{ linkedin }} | <strong>GitHub:</strong> {{ github }}</p>

<h2>Career Objective</h2>
<p>{{ objective }}</p>

<h2>Education</h2>
<ul>
{% for edu in education %}
<li><strong>{{ edu.degree }}</strong>, {{ edu.college }} ({{ edu.year }}) — CGPA: {{ edu.cgpa }}</li>
{% endfor %}
</ul>

<h2>Projects</h2>
<ul>
{% for proj in projects %}
<li><strong>{{ proj.title }}</strong> | <em>{{ proj.tech }}</em><br>{{ proj.desc }}</li>
{% endfor %}
</ul>

<h2>Technical Skills</h2>
<p>{{ skills }}</p>

<h2>Internships</h2>
<p>{{ internships.replace('\\n', '<br>') }}</p>

<h2>Certifications</h2>
<p>{{ certifications.replace('\\n', '<br>') }}</p>

<h2>Achievements</h2>
<p>{{ achievements.replace('\\n', '<br>') }}</p>

<h2>Workshops / Seminars</h2>
<p>{{ workshops.replace('\\n', '<br>') }}</p>

<h2>Extra-curricular / Leadership</h2>
<p>{{ extras.replace('\\n', '<br>') }}</p>

<h2>Languages Known</h2>
<p>{{ languages_known }}</p>
</body>
</html>
"""

def generate_pdf(html_content):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")  # Update path if needed
        pdfkit.from_string(html_content, tmpfile.name, configuration=config)
        return tmpfile.name

if st.button("📄 Generate Resume PDF"):
    html = Template(html_template).render(
        name=name,
        email=email,
        phone=phone,
        linkedin=linkedin,
        github=github,
        objective=objective,
        education=st.session_state.education,
        projects=st.session_state.projects,
        skills=skills,
        internships=internships,
        certifications=certifications,
        achievements=achievements,
        workshops=workshops,
        extras=extras,
        languages_known=languages_known
    )

    try:
        pdf_path = generate_pdf(html)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download Resume", f, file_name="Resume.pdf", mime="application/pdf")
        st.success("✅ Resume generated successfully!")
    except Exception as e:
        st.error(f"❌ Failed to generate PDF: {e}")

