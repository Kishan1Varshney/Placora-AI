# ============================================
# AI Placement Mentor - Module 1
# Resume Parser & ATS Score Calculator
# File: app/resume_parser.py
# ============================================

import pdfplumber
import re
import string
import os

# ============================================
# STEP 1: PDF se Text Extract karna
# ============================================

def extract_text_from_pdf(pdf_path):
    """
    PDF file se text extract karta hai.
    
    Args:
        pdf_path: PDF file ka path
    Returns:
        Extracted text (string)
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        print(f"✅ PDF se {len(text)} characters extract hue.")
    except Exception as e:
        print(f"❌ PDF read error: {e}")
    return text


def extract_text_from_uploaded_file(uploaded_file):
    """
    Streamlit uploaded file se text extract karta hai.
    
    Args:
        uploaded_file: Streamlit file uploader object
    Returns:
        Extracted text (string)
    """
    import tempfile
    text = ""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        text = extract_text_from_pdf(tmp_path)
        os.unlink(tmp_path)  # temp file delete karo
    except Exception as e:
        print(f"❌ File read error: {e}")
    return text


# ============================================
# STEP 2: Text Clean karna
# ============================================

def clean_resume_text(text):
    """
    Resume text ko clean karta hai.
    
    Args:
        text: Raw text
    Returns:
        Clean text
    """
    if not text:
        return ""

    # Extra whitespace hataao
    text = re.sub(r'\s+', ' ', text)

    # Special characters hataao (lekin important ones rakh lo)
    text = re.sub(r'[^\w\s@.\-+/|,]', ' ', text)

    # Multiple spaces hataao
    text = re.sub(r' +', ' ', text)

    return text.strip()


# ============================================
# STEP 3: Resume Sections Identify karna
# ============================================

def extract_sections(text):
    """
    Resume ke alag alag sections identify karta hai.
    
    Returns:
        Dictionary with sections
    """
    sections = {
        'education': '',
        'experience': '',
        'skills': '',
        'projects': '',
        'certifications': '',
        'contact': ''
    }

    section_keywords = {
        'education': ['education', 'academic', 'qualification', 'degree', 'university', 'college'],
        'experience': ['experience', 'work', 'internship', 'employment', 'job', 'position'],
        'skills': ['skills', 'technical skills', 'technologies', 'tools', 'languages'],
        'projects': ['projects', 'project work', 'academic projects', 'personal projects'],
        'certifications': ['certifications', 'certificates', 'achievements', 'awards', 'courses'],
        'contact': ['contact', 'email', 'phone', 'linkedin', 'github', 'address']
    }

    text_lower = text.lower()
    lines = text.split('\n')

    current_section = 'contact'
    for line in lines:
        line_lower = line.lower().strip()

        # Check karo ye line kaunsa section hai
        for section, keywords in section_keywords.items():
            if any(keyword in line_lower for keyword in keywords):
                current_section = section
                break

        sections[current_section] += line + '\n'

    return sections


# ============================================
# STEP 4: Contact Info Extract karna
# ============================================

def extract_contact_info(text):
    """
    Resume se contact information nikalta hai.
    
    Returns:
        Dictionary with email, phone, linkedin, github
    """
    contact = {
        'email': None,
        'phone': None,
        'linkedin': None,
        'github': None,
        'name': None
    }

    # Email extract
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.findall(email_pattern, text)
    if email_match:
        contact['email'] = email_match[0]

    # Phone extract
    phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
    phone_match = re.findall(phone_pattern, text)
    if phone_match:
        contact['phone'] = phone_match[0]

    # LinkedIn extract
    linkedin_pattern = r'linkedin\.com/in/[\w\-]+'
    linkedin_match = re.findall(linkedin_pattern, text, re.IGNORECASE)
    if linkedin_match:
        contact['linkedin'] = linkedin_match[0]

    # GitHub extract
    github_pattern = r'github\.com/[\w\-]+'
    github_match = re.findall(github_pattern, text, re.IGNORECASE)
    if github_match:
        contact['github'] = github_match[0]

    return contact


# ============================================
# STEP 5: ATS Score Calculate karna
# ============================================

def calculate_ats_score(text, sections):
    """
    Resume ka ATS (Applicant Tracking System) score calculate karta hai.
    
    Scoring Criteria:
    - Contact Info    : 10 points
    - Skills Section  : 20 points
    - Experience      : 20 points
    - Education       : 15 points
    - Projects        : 15 points
    - Certifications  : 10 points
    - Resume Length   : 10 points
    
    Total: 100 points
    
    Returns:
        score (int), breakdown (dict), feedback (list)
    """
    score = 0
    breakdown = {}
    feedback = []
    strengths = []
    weaknesses = []

    # --- Contact Info (10 points) ---
    contact = extract_contact_info(text)
    contact_score = 0
    if contact['email']:
        contact_score += 4
    else:
        weaknesses.append("❌ Email address nahi mila resume mein.")

    if contact['phone']:
        contact_score += 3
    else:
        weaknesses.append("❌ Phone number missing hai.")

    if contact['linkedin']:
        contact_score += 2
        strengths.append("✅ LinkedIn profile present hai.")
    else:
        weaknesses.append("⚠️ LinkedIn profile add karo.")

    if contact['github']:
        contact_score += 1
        strengths.append("✅ GitHub profile present hai.")

    breakdown['contact_info'] = contact_score
    score += contact_score

    # --- Skills Section (20 points) ---
    skills_text = sections.get('skills', '').lower()
    skill_score = 0
    if len(skills_text) > 50:
        skill_score += 15
        strengths.append("✅ Skills section clearly mentioned hai.")
    elif len(skills_text) > 20:
        skill_score += 8
        weaknesses.append("⚠️ Skills section aur detailed ho sakta hai.")
    else:
        weaknesses.append("❌ Skills section bahut weak hai ya missing hai.")

    # Technical keywords check
    tech_keywords = ['python', 'java', 'sql', 'javascript', 'machine learning',
                     'data', 'html', 'css', 'git', 'aws', 'excel', 'power bi']
    tech_found = [kw for kw in tech_keywords if kw in skills_text or kw in text.lower()]
    if len(tech_found) >= 5:
        skill_score += 5
        strengths.append(f"✅ {len(tech_found)} technical skills found.")
    elif len(tech_found) >= 2:
        skill_score += 3

    breakdown['skills'] = skill_score
    score += skill_score

    # --- Experience / Internship (20 points) ---
    exp_text = sections.get('experience', '').lower()
    exp_score = 0
    if len(exp_text) > 100:
        exp_score += 20
        strengths.append("✅ Work/Internship experience hai.")
    elif len(exp_text) > 30:
        exp_score += 10
        weaknesses.append("⚠️ Experience section aur elaborate karo.")
    else:
        exp_score += 5
        weaknesses.append("❌ Work experience ya internship add karo.")

    breakdown['experience'] = exp_score
    score += exp_score

    # --- Education (15 points) ---
    edu_text = sections.get('education', '').lower()
    edu_score = 0
    if len(edu_text) > 50:
        edu_score += 15
        strengths.append("✅ Education section present hai.")
    elif len(edu_text) > 20:
        edu_score += 8
    else:
        weaknesses.append("❌ Education details add karo (college, CGPA, year).")

    breakdown['education'] = edu_score
    score += edu_score

    # --- Projects (15 points) ---
    proj_text = sections.get('projects', '').lower()
    proj_score = 0
    if len(proj_text) > 150:
        proj_score += 15
        strengths.append("✅ Projects section well-described hai.")
    elif len(proj_text) > 50:
        proj_score += 8
        weaknesses.append("⚠️ Projects mein technologies aur impact add karo.")
    else:
        weaknesses.append("❌ Projects section missing ya bahut weak hai.")

    breakdown['projects'] = proj_score
    score += proj_score

    # --- Certifications (10 points) ---
    cert_text = sections.get('certifications', '').lower()
    cert_score = 0
    if len(cert_text) > 30:
        cert_score += 10
        strengths.append("✅ Certifications mentioned hain.")
    else:
        cert_score += 2
        weaknesses.append("⚠️ Relevant certifications add karo (Coursera, Google, etc).")

    breakdown['certifications'] = cert_score
    score += cert_score

    # --- Resume Length (10 points) ---
    word_count = len(text.split())
    length_score = 0
    if 300 <= word_count <= 800:
        length_score = 10
        strengths.append(f"✅ Resume length bilkul sahi hai ({word_count} words).")
    elif word_count < 300:
        length_score = 4
        weaknesses.append(f"❌ Resume bahut chhota hai ({word_count} words). Expand karo.")
    else:
        length_score = 6
        weaknesses.append(f"⚠️ Resume thoda lamba hai ({word_count} words). 1 page rakho.")

    breakdown['length'] = length_score
    score += length_score

    return score, breakdown, strengths, weaknesses


# ============================================
# STEP 6: Main Resume Analysis Function
# ============================================

def analyze_resume(pdf_path=None, uploaded_file=None):
    """
    Complete resume analysis karta hai.
    
    Args:
        pdf_path: PDF ka direct path
        uploaded_file: Streamlit uploaded file
    
    Returns:
        Complete analysis dictionary
    """
    # Text extract karo
    if uploaded_file:
        raw_text = extract_text_from_uploaded_file(uploaded_file)
    elif pdf_path:
        raw_text = extract_text_from_pdf(pdf_path)
    else:
        return {"error": "Koi file provide nahi ki!"}

    if not raw_text:
        return {"error": "PDF se text extract nahi ho saka. PDF sahi format mein hai?"}

    # Text clean karo
    clean_text = clean_resume_text(raw_text)

    # Sections extract karo
    sections = extract_sections(clean_text)

    # Contact info nikalo
    contact = extract_contact_info(clean_text)

    # ATS Score calculate karo
    ats_score, breakdown, strengths, weaknesses = calculate_ats_score(clean_text, sections)

    # Result dictionary
    result = {
        'raw_text': raw_text,
        'clean_text': clean_text,
        'sections': sections,
        'contact_info': contact,
        'ats_score': ats_score,
        'score_breakdown': breakdown,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'word_count': len(clean_text.split()),
        'char_count': len(clean_text)
    }

    return result


# ============================================
# Test (Direct run karo test ke liye)
# ============================================
if __name__ == "__main__":
    print("=" * 50)
    print("   Resume Parser Test")
    print("=" * 50)

    # Sample text se test karo
    sample_text = """
    Rahul Sharma
    rahul.sharma@gmail.com | +91-9876543210
    LinkedIn: linkedin.com/in/rahulsharma | GitHub: github.com/rahulsharma
    
    EDUCATION
    B.Tech Computer Science - ABC Engineering College
    CGPA: 8.5/10 | 2021-2025
    
    SKILLS
    Python, SQL, Machine Learning, Data Analysis, Power BI, 
    Pandas, NumPy, Scikit-learn, Git, HTML, CSS
    
    PROJECTS
    1. Sales Data Analysis - Used Python and Pandas to analyze 10,000+ records
    2. Student Grade Predictor - Built ML model with 85% accuracy
    
    INTERNSHIP
    Data Analyst Intern at XYZ Company (June 2024 - Aug 2024)
    Worked on data cleaning and visualization dashboards.
    """

    sections = extract_sections(sample_text)
    contact = extract_contact_info(sample_text)
    score, breakdown, strengths, weaknesses = calculate_ats_score(sample_text, sections)

    print(f"\n📊 ATS Score: {score}/100")
    print(f"\n✅ Strengths ({len(strengths)}):")
    for s in strengths:
        print(f"   {s}")
    print(f"\n❌ Weaknesses ({len(weaknesses)}):")
    for w in weaknesses:
        print(f"   {w}")
    print(f"\n📋 Score Breakdown: {breakdown}")
    print(f"\n📧 Contact Info: {contact}")
