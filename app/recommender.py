# ============================================
# PLACORA - Module 4: Job Recommendation
# File: app/recommender.py
# ============================================

from app.skill_extractor import JOB_REQUIRED_SKILLS

JOB_DETAILS = {
    'Data Scientist':    {'avg_salary': '8-18 LPA',  'companies': ['Google','Amazon','Flipkart','Zomato'],    'growth': 'High',      'difficulty': 'Hard'},
    'Data Analyst':      {'avg_salary': '4-10 LPA',  'companies': ['Deloitte','Accenture','Infosys','TCS'],   'growth': 'High',      'difficulty': 'Medium'},
    'Web Developer':     {'avg_salary': '4-12 LPA',  'companies': ['TCS','Infosys','Wipro','HCL'],            'growth': 'Medium',    'difficulty': 'Medium'},
    'Software Engineer': {'avg_salary': '6-20 LPA',  'companies': ['Microsoft','Google','Amazon','Infosys'],  'growth': 'High',      'difficulty': 'Hard'},
    'ML Engineer':       {'avg_salary': '10-25 LPA', 'companies': ['Google','Microsoft','Amazon','Nvidia'],   'growth': 'Very High', 'difficulty': 'Hard'},
    'AI Engineer':       {'avg_salary': '12-30 LPA', 'companies': ['Google','OpenAI','Microsoft','Meta'],     'growth': 'Very High', 'difficulty': 'Very Hard'},
    'Backend Developer': {'avg_salary': '5-15 LPA',  'companies': ['Zomato','Swiggy','Razorpay','CRED'],      'growth': 'High',      'difficulty': 'Medium'},
    'Frontend Developer':{'avg_salary': '4-12 LPA',  'companies': ['Zoho','Freshworks','UrbanClap'],          'growth': 'Medium',    'difficulty': 'Medium'},
    'DevOps Engineer':   {'avg_salary': '8-20 LPA',  'companies': ['Amazon AWS','Microsoft Azure','IBM'],     'growth': 'Very High', 'difficulty': 'Hard'},
    'Business Analyst':  {'avg_salary': '5-12 LPA',  'companies': ['Deloitte','KPMG','Accenture','TCS'],      'growth': 'Medium',    'difficulty': 'Easy'},
}


def recommend_jobs(student_skills_flat, top_n=5):
    student_lower = [s.lower() for s in student_skills_flat]
    recommendations = []
    for role, required_skills in JOB_REQUIRED_SKILLS.items():
        matched = [s for s in required_skills if s.lower() in student_lower]
        missing = [s for s in required_skills if s.lower() not in student_lower]
        match_score = round((len(matched) / len(required_skills)) * 100, 1) if required_skills else 0
        details = JOB_DETAILS.get(role, {})
        recommendations.append({
            'role': role,
            'match_score': match_score,
            'matched_skills': matched,
            'missing_skills': missing,
            'avg_salary': details.get('avg_salary', 'N/A'),
            'companies': details.get('companies', []),
            'growth': details.get('growth', 'Medium'),
            'difficulty': details.get('difficulty', 'Medium'),
        })
    recommendations.sort(key=lambda x: x['match_score'], reverse=True)
    return recommendations[:top_n]


def get_career_path(current_role):
    paths = {
        'Data Analyst':      {'next': 'Data Scientist',             'steps': ['Machine Learning seekho','ML projects banao','Kaggle competitions karo','Portfolio GitHub pe daalo']},
        'Web Developer':     {'next': 'Full Stack Developer',       'steps': ['Backend (Node.js/Django) seekho','REST API banao','Docker basics seekho','Full stack projects banao']},
        'Software Engineer': {'next': 'Senior Software Engineer',   'steps': ['System Design seekho','DSA practice karo','Cloud certification lo','Open source contribute karo']},
        'Data Scientist':    {'next': 'ML Engineer / AI Engineer',  'steps': ['MLOps seekho','Model deployment sikho','LLM/GenAI explore karo','Research papers padho']},
    }
    return paths.get(current_role, {'next': 'Senior ' + current_role, 'steps': ['Current skills deepen karo','Certifications lo','2+ years experience gain karo','Network build karo']})


if __name__ == "__main__":
    print("=" * 50)
    print("   PLACORA - Job Recommendation System")
    print("=" * 50)
    skills = ['Python', 'SQL', 'Pandas', 'Machine Learning', 'Power BI', 'Excel', 'Data Analysis', 'Git']
    print(f"\nSkills: {', '.join(skills)}")
    recs = recommend_jobs(skills, top_n=5)
    for i, job in enumerate(recs, 1):
        print(f"\n{i}. {job['role']}  |  {job['match_score']}%  |  {job['avg_salary']}  |  Growth: {job['growth']}")
        if job['missing_skills']:
            print(f"   Missing: {', '.join(job['missing_skills'][:3])}")
