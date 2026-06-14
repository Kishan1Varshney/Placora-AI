# ============================================
# AI Placement Mentor - Module 2
# Skill Extraction from Resume
# File: app/skill_extractor.py
# ============================================

import re

# ============================================
# Master Skills Database
# Yahan sab popular skills defined hain
# ============================================

SKILLS_DATABASE = {

    # === Programming Languages ===
    'programming_languages': [
        'python', 'java', 'javascript', 'c', 'c++', 'c#', 'r', 'golang', 'go',
        'ruby', 'php', 'swift', 'kotlin', 'typescript', 'scala', 'perl',
        'rust', 'matlab', 'vba', 'bash', 'shell', 'dart', 'objective-c'
    ],

    # === Web Development ===
    'web_development': [
        'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'node.js',
        'express', 'django', 'flask', 'fastapi', 'spring', 'laravel',
        'bootstrap', 'tailwind', 'jquery', 'redux', 'graphql', 'rest api',
        'restful', 'asp.net', 'next.js', 'nuxt', 'webpack', 'sass', 'less'
    ],

    # === Data Science & ML ===
    'data_science_ml': [
        'machine learning', 'deep learning', 'artificial intelligence', 'ai',
        'ml', 'data science', 'data analysis', 'data analytics',
        'neural network', 'nlp', 'natural language processing',
        'computer vision', 'reinforcement learning', 'supervised learning',
        'unsupervised learning', 'regression', 'classification', 'clustering',
        'tensorflow', 'keras', 'pytorch', 'scikit-learn', 'sklearn',
        'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly',
        'statistics', 'statistical analysis', 'hypothesis testing',
        'feature engineering', 'model deployment', 'mlops'
    ],

    # === Databases ===
    'databases': [
        'sql', 'mysql', 'postgresql', 'mongodb', 'sqlite', 'oracle',
        'ms sql', 'sql server', 'redis', 'cassandra', 'elasticsearch',
        'firebase', 'dynamodb', 'nosql', 'database design', 'er diagram'
    ],

    # === Cloud & DevOps ===
    'cloud_devops': [
        'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes',
        'jenkins', 'ci/cd', 'git', 'github', 'gitlab', 'bitbucket',
        'terraform', 'ansible', 'linux', 'unix', 'devops', 'cloud computing',
        'microservices', 'serverless', 'lambda', 'ec2', 's3'
    ],

    # === Data Visualization & BI ===
    'visualization_bi': [
        'power bi', 'tableau', 'excel', 'google sheets', 'data studio',
        'looker', 'qlik', 'superset', 'grafana', 'kibana',
        'advanced excel', 'pivot table', 'vlookup'
    ],

    # === Mobile Development ===
    'mobile': [
        'android', 'ios', 'flutter', 'react native', 'xamarin',
        'kotlin', 'swift', 'mobile development', 'app development'
    ],

    # === Cybersecurity ===
    'cybersecurity': [
        'cybersecurity', 'network security', 'ethical hacking', 'penetration testing',
        'kali linux', 'wireshark', 'metasploit', 'owasp', 'firewall',
        'encryption', 'ssl', 'vulnerability assessment'
    ],

    # === Soft Skills ===
    'soft_skills': [
        'communication', 'leadership', 'teamwork', 'problem solving',
        'critical thinking', 'time management', 'adaptability',
        'presentation', 'project management', 'agile', 'scrum',
        'jira', 'trello', 'microsoft office'
    ]
}


# ============================================
# Job Role ke liye Required Skills
# ============================================

JOB_REQUIRED_SKILLS = {
    'Data Scientist': [
        'python', 'machine learning', 'deep learning', 'statistics',
        'sql', 'pandas', 'numpy', 'scikit-learn', 'tensorflow',
        'data analysis', 'feature engineering', 'nlp'
    ],
    'Data Analyst': [
        'python', 'sql', 'excel', 'power bi', 'tableau',
        'data analysis', 'statistics', 'pandas', 'matplotlib',
        'data visualization', 'reporting'
    ],
    'Web Developer': [
        'html', 'css', 'javascript', 'react', 'nodejs',
        'sql', 'git', 'rest api', 'bootstrap'
    ],
    'Software Engineer': [
        'python', 'java', 'c++', 'data structures', 'algorithms',
        'sql', 'git', 'object oriented programming', 'system design'
    ],
    'ML Engineer': [
        'python', 'machine learning', 'deep learning', 'tensorflow',
        'pytorch', 'mlops', 'docker', 'aws', 'model deployment',
        'sql', 'feature engineering'
    ],
    'AI Engineer': [
        'python', 'deep learning', 'nlp', 'computer vision',
        'tensorflow', 'pytorch', 'transformers', 'llm',
        'generative ai', 'api integration'
    ],
    'Backend Developer': [
        'python', 'java', 'nodejs', 'sql', 'mongodb',
        'rest api', 'docker', 'git', 'django', 'flask'
    ],
    'Frontend Developer': [
        'html', 'css', 'javascript', 'react', 'vue',
        'typescript', 'bootstrap', 'responsive design', 'git'
    ],
    'DevOps Engineer': [
        'linux', 'docker', 'kubernetes', 'aws', 'ci/cd',
        'jenkins', 'git', 'terraform', 'ansible', 'python'
    ],
    'Business Analyst': [
        'sql', 'excel', 'power bi', 'tableau', 'data analysis',
        'requirements gathering', 'communication', 'presentation',
        'project management'
    ]
}


# ============================================
# MAIN FUNCTION: Skills Extract karna
# ============================================

def extract_skills(text):
    """
    Resume text se skills extract karta hai.
    
    Args:
        text: Resume ka clean text
    
    Returns:
        Dictionary with categorized skills
    """
    text_lower = text.lower()
    found_skills = {}

    for category, skills in SKILLS_DATABASE.items():
        found = []
        for skill in skills:
            # Word boundary check for accurate matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found.append(skill.title())  # Capitalize karo

        if found:
            found_skills[category] = found

    return found_skills


def get_all_skills_flat(skills_dict):
    """
    Categorized skills ko flat list mein convert karta hai.
    
    Args:
        skills_dict: extract_skills() ka output
    
    Returns:
        Simple list of all skills
    """
    all_skills = []
    for category, skills in skills_dict.items():
        all_skills.extend(skills)
    return list(set(all_skills))  # Duplicates remove


# ============================================
# Skill Gap Analysis
# ============================================

def analyze_skill_gap(student_skills_flat, target_role):
    """
    Student ke skills aur target role ke required skills ka comparison karta hai.
    
    Args:
        student_skills_flat : Student ki skills (flat list)
        target_role         : Target job role (string)
    
    Returns:
        present_skills, missing_skills, match_percentage
    """
    if target_role not in JOB_REQUIRED_SKILLS:
        return [], [], 0

    required = JOB_REQUIRED_SKILLS[target_role]
    student_lower = [s.lower() for s in student_skills_flat]

    present_skills = []
    missing_skills = []

    for skill in required:
        if skill.lower() in student_lower:
            present_skills.append(skill)
        else:
            missing_skills.append(skill)

    if len(required) > 0:
        match_percentage = round((len(present_skills) / len(required)) * 100, 1)
    else:
        match_percentage = 0

    return present_skills, missing_skills, match_percentage


# ============================================
# Resume-Job Description Matching
# ============================================

def match_resume_with_jd(resume_text, job_description):
    """
    Resume ko Job Description ke saath match karta hai.
    
    Args:
        resume_text     : Resume ka text
        job_description : Job description text
    
    Returns:
        match_score, missing_keywords
    """
    # JD se keywords extract karo
    jd_skills = extract_skills(job_description)
    jd_keywords = get_all_skills_flat(jd_skills)

    # Resume se skills extract karo
    resume_skills = extract_skills(resume_text)
    resume_keywords = get_all_skills_flat(resume_skills)

    resume_lower = [s.lower() for s in resume_keywords]
    jd_lower = [s.lower() for s in jd_keywords]

    if not jd_lower:
        return 0, []

    matched = [kw for kw in jd_lower if kw in resume_lower]
    missing = [kw for kw in jd_lower if kw not in resume_lower]

    match_score = round((len(matched) / len(jd_lower)) * 100, 1)

    return match_score, missing


# ============================================
# Skill Statistics
# ============================================

def get_skill_stats(skills_dict):
    """
    Skills ka summary statistics return karta hai.
    
    Returns:
        Dictionary with total skills and category counts
    """
    stats = {
        'total_skills': 0,
        'categories_found': len(skills_dict),
        'category_breakdown': {}
    }

    for category, skills in skills_dict.items():
        stats['category_breakdown'][category] = len(skills)
        stats['total_skills'] += len(skills)

    return stats


# ============================================
# Test
# ============================================
if __name__ == "__main__":
    print("=" * 50)
    print("   Skill Extractor Test")
    print("=" * 50)

    sample_resume = """
    Skills:
    Python, SQL, Machine Learning, Pandas, NumPy, Power BI,
    HTML, CSS, JavaScript, Git, MySQL, Data Analysis, Tableau
    
    Projects:
    - Built a machine learning model using Scikit-learn
    - Created data dashboards using Power BI and Excel
    - Developed REST API using Flask
    """

    # Skills extract karo
    skills_dict = extract_skills(sample_resume)
    flat_skills = get_all_skills_flat(skills_dict)
    stats = get_skill_stats(skills_dict)

    print(f"\n📊 Total Skills Found: {stats['total_skills']}")
    print(f"📁 Categories: {stats['categories_found']}")
    print(f"\n🔧 Skills by Category:")
    for cat, skills in skills_dict.items():
        print(f"   {cat}: {', '.join(skills)}")

    # Skill Gap Analysis
    print("\n" + "=" * 50)
    print("   Skill Gap Analysis (Target: Data Scientist)")
    print("=" * 50)

    present, missing, match_pct = analyze_skill_gap(flat_skills, 'Data Scientist')
    print(f"\n✅ Present Skills ({len(present)}): {', '.join(present)}")
    print(f"❌ Missing Skills ({len(missing)}): {', '.join(missing)}")
    print(f"📈 Match Percentage: {match_pct}%")
