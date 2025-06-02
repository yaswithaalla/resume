import streamlit as st
from jinja2 import Template
from xhtml2pdf import pisa
import tempfile
import re

# Streamlit App Config
st.set_page_config(page_title="Resume Generator", layout="centered")
st.title("📄 BTech Fresher Resume Generator")

# Session State Initialization
if "education" not in st.session_state:
    st.session_state.education = []
if "projects" not in st.session_state:
    st.session_state.projects = []

# User Info
name = st.text_input("Full Name").strip()
email = st.text_input("Email").strip()
phone = st.text_input("Phone").strip()
linkedin = st.text_input("LinkedIn URL").strip()
github = st.text_input("GitHub URL").strip()
objective = st.text_area("Career Objective", height=80).strip()

# Education Section
st.subheader("🎓 Education")
with st.form("education_form", clear_on_submit=True):
    degree = st.text_input("Degree")
    college = st.text_input("College")
    year = st.text_input("Year")
    cgpa = st.text_input("CGPA")
    if st.form_submit_button("Add Education"):
        if degree and college and year and cgpa:
            st.session_state.education.append({
                "degree": degree.strip(), "college": college.strip(),
                "year": year.strip(), "cgpa": cgpa.strip()
            })

for edu in st.session_state.education:
    st.write(f"• {edu['degree']}, {edu['college']} ({edu['year']}) — CGPA: {edu['cgpa']}")

# Projects Section
st.subheader("🚀 Projects")
with st.form("project_form", clear_on_submit=True):
    proj_title = st.text_input("Project Title")
    proj_desc = st.text_area("Project Description")
    proj_tech = st.text_input("Tech Stack")
    if st.form_submit_button("Add Project"):
        if proj_title and proj_desc:
            st.session_state.projects.append({
                "title": proj_title.strip(),
                "desc": proj_desc.strip(),
                "tech": proj_tech.strip()
            })

for proj in st.session_state.projects:
    st.write(f"• *{proj['title']}* | {proj['tech']}")
    st.write(proj['desc'])

# Other Sections
skills = st.text_area("Technical Skills (comma-separated)").strip()
achievements = st.text_area("Achievements (one per line)").strip()
certifications = st.text_area("Certifications (one per line)").strip()
internships = st.text_area("Internships (Company - Role - Duration - Description)").strip()
workshops = st.text_area("Workshops/Seminars Attended").strip()
extras = st.text_area("Extra-curricular / Leadership Roles").strip()
languages_known = st.text_input("Languages Known (comma-separated)").strip()

# Resume Template (HTML)
html_template = """
<!DOCTYPE html>
<html>
<head>
<style>
body { font-family: Arial, sans-serif; font-size: 13px; margin: 30px; color: #000; }
h1 { font-size: 24px; color: #2c3e50; }
h2 { font-size: 18px; margin-top: 20px; border-bottom: 1px solid #aaa; padding-bottom: 4px; color: #2c3e50; }
ul { padding-left: 20px; }
.section { margin-bottom: 15px; }
</style>
</head>
<body>
<h1>{{ name }}</h1>
<p><strong>Email:</strong> {{ email }} | <strong>Phone:</strong> {{ phone }}</p>
<p><strong>LinkedIn:</strong> {{ linkedin }} | <strong>GitHub:</strong> {{ github }}</p>

<div class="section">
<h2>Career Objective</h2>
<p>{{ objective }}</p>
</div>

<div class="section">
<h2>Education</h2>
<ul>
{% for edu in education %}
<li><strong>{{ edu.degree }}</strong>, {{ edu.college }} ({{ edu.year }}) — CGPA: {{ edu.cgpa }}</li>
{% endfor %}
</ul>
</div>

<div class="section">
<h2>Projects</h2>
<ul>
{% for proj in projects %}
<li><strong>{{ proj.title }}</strong> | <em>{{ proj.tech }}</em><br>{{ proj.desc }}</li>
{% endfor %}
</ul>
</div>

<div class="section">
<h2>Technical Skills</h2>
<p>{{ skills }}</p>
</div>

<div class="section">
<h2>Internships</h2>
<p>{{ internships.replace('\\n', '<br>') }}</p>
</div>

<div class="section">
<h2>Certifications</h2>
<p>{{ certifications.replace('\\n', '<br>') }}</p>
</div>

<div class="section">
<h2>Achievements</h2>
<p>{{ achievements.replace('\\n', '<br>') }}</p>
</div>

<div class="section">
<h2>Workshops / Seminars</h2>
<p>{{ workshops.replace('\\n', '<br>') }}</p>
</div>

<div class="section">
<h2>Extra-curricular / Leadership</h2>
<p>{{ extras.replace('\\n', '<br>') }}</p>
</div>

<div class="section">
<h2>Languages Known</h2>
<p>{{ languages_known }}</p>
</div>

</body>
</html>
"""

# PDF Generation Function
def generate_pdf(html_code, path):
    with open(path, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(html_code, dest=result_file)
    return pisa_status.err

# Button to Generate PDF
if st.button("📄 Generate Resume PDF"):
    if not name or not email or not phone:
        st.warning("Please fill in your name, email, and phone number.")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.warning("Please enter a valid email address.")
    else:
        html = Template(html_template).render(
            name=name, email=email, phone=phone,
            linkedin=linkedin, github=github, objective=objective,
            education=st.session_state.education,
            projects=st.session_state.projects,
            skills=skills, internships=internships,
            certifications=certifications,
            achievements=achievements,
            workshops=workshops,
            extras=extras,
            languages_known=languages_known
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            if generate_pdf(html, tmp.name) == 0:
                st.success("✅ Resume generated successfully!")
                with open(tmp.name, "rb") as f:
                    st.download_button("📥 Download Resume", f, file_name="Resume.pdf", mime="application/pdf")
            else:
                st.error("❌ Failed to generate PDF. Please check your inputs or try again.")
