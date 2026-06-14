# ============================================
# PLACORA - Module 5: AI Career Chatbot
# File: app/chatbot.py
# Powered by: OpenAI ChatGPT API
# ============================================

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'config', '.env'))

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def _ask_chatgpt(prompt: str, max_tokens: int = 500) -> str:
    """
    Internal helper — ChatGPT API call karta hai.
    Ek hi jagah API call hoti hai, baaki functions yahi use karte hain.
    """
    if not client:
        return "❌ OpenAI API key config/.env mein set nahi hai. OPENAI_API_KEY daalo."
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are PLACORA, an expert AI placement mentor for Indian engineering college students. Always respond in simple Hinglish (mix of Hindi and English)."},
                {"role": "user",   "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ ChatGPT API error: {str(e)}"


# ============================================
# Function 1: Career Guidance
# ============================================

def get_career_guidance(student_profile: dict, user_question: str) -> str:
    """
    ChatGPT se personalized career guidance leta hai.
    """
    skills_str = ', '.join(student_profile.get('skills', [])) or 'Not mentioned'

    prompt = f"""
Student Profile:
- Name           : {student_profile.get('name', 'Student')}
- CGPA           : {student_profile.get('cgpa', 'N/A')}
- Branch         : {student_profile.get('branch', 'N/A')}
- Skills         : {skills_str}
- Target Role    : {student_profile.get('target_role', 'Not decided')}
- Placement Prob : {student_profile.get('placement_probability', 'N/A')}%
- ATS Score      : {student_profile.get('ats_score', 'N/A')}/100

Student Question: {user_question}

Instructions:
- Practical aur actionable advice do
- Specific resources mention karo (Coursera, LeetCode, GitHub, Internshala, NPTEL)
- 150-200 words mein rakho
- Bullet points use karo jahan helpful ho
- Ek motivational line se end karo
"""
    return _ask_chatgpt(prompt, max_tokens=400)


# ============================================
# Function 2: Interview Questions Generator
# ============================================

def generate_interview_questions(target_role: str, difficulty: str = "Medium") -> dict:
    """
    Target role ke liye interview questions generate karta hai.
    """
    prompt = f"""
Generate interview questions for {target_role} position at {difficulty} difficulty level for Indian fresher/entry-level candidates.

Return in EXACTLY this format:

TECHNICAL:
1. [question]
2. [question]
3. [question]
4. [question]
5. [question]

HR:
1. [question]
2. [question]
3. [question]

TIPS:
- [tip 1]
- [tip 2]
- [tip 3]
"""
    raw_text = _ask_chatgpt(prompt, max_tokens=600)

    # Response parse karo
    questions = {'technical': [], 'hr': [], 'tips': [], 'raw': raw_text}
    current   = None

    for line in raw_text.split('\n'):
        line = line.strip()
        if 'TECHNICAL' in line.upper():
            current = 'technical'
        elif line.upper().startswith('HR'):
            current = 'hr'
        elif 'TIPS' in line.upper():
            current = 'tips'
        elif line and current and (line[0].isdigit() or line.startswith('-')):
            clean = line.lstrip('0123456789.-) ').strip()
            if clean:
                questions[current].append(clean)

    return questions


# ============================================
# Function 3: Learning Roadmap Generator
# ============================================

def generate_learning_roadmap(missing_skills: list, target_role: str, months: int = 3) -> str:
    """
    Missing skills ke liye personalized learning roadmap generate karta hai.
    """
    if not missing_skills:
        return "🎉 Great! Aapke paas sab required skills hain! Ab projects banao aur apply karo."

    skills_str = ', '.join(missing_skills[:8])

    prompt = f"""
Create a {months}-month learning roadmap for an Indian engineering student targeting {target_role} role.
Skills to learn: {skills_str}

Format:
Month 1: [Focus Area] - [Specific Topics] - [Free Resources]
Month 2: [Focus Area] - [Specific Topics] - [Free Resources]
Month 3: [Focus Area] - [Specific Topics] - [Free Resources]

Free Resources: [List 3-4 specific free websites/platforms]
Daily Schedule: [2-3 hour daily study routine suggestion]

Keep it practical and achievable for a college student with 2-3 hours daily.
"""
    return _ask_chatgpt(prompt, max_tokens=500)


# ============================================
# Function 4: AI Resume Feedback
# ============================================

def analyze_resume_with_ai(resume_text: str, target_role: str) -> str:
    """
    ChatGPT se resume ka detailed feedback leta hai.
    """
    prompt = f"""
You are an expert resume reviewer for Indian engineering placements.
Target Role: {target_role}

Resume Content:
{resume_text[:2000]}

Provide structured feedback:

STRENGTHS:
- [strength 1]
- [strength 2]

WEAKNESSES:
- [weakness 1]
- [weakness 2]

IMPROVEMENTS:
- [specific improvement 1]
- [specific improvement 2]
- [specific improvement 3]

ATS TIPS:
- [keyword tip]
- [formatting tip]

Be specific, practical, and encouraging.
"""
    return _ask_chatgpt(prompt, max_tokens=500)


# ============================================
# Test
# ============================================
if __name__ == "__main__":
    print("=" * 50)
    print("   PLACORA - ChatGPT AI Chatbot Test")
    print("=" * 50)
    print(f"OpenAI API Key: {'✅ Set' if OPENAI_API_KEY else '❌ NOT SET - config/.env check karo'}")

    if OPENAI_API_KEY:
        print("\nCareer guidance test kar rahe hain...")
        profile = {
            'name': 'Rahul', 'cgpa': 7.5, 'branch': 'CSE',
            'skills': ['Python', 'SQL', 'Excel'],
            'target_role': 'Data Analyst',
            'placement_probability': 65, 'ats_score': 72
        }
        response = get_career_guidance(profile, "Mujhe Data Analyst banne ke liye kya karna chahiye?")
        print("\nAI Response:")
        print(response)
