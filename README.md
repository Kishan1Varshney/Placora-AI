# 🎓 AI Placement Mentor for College Students

> An Intelligent Career Guidance System using Data Science and Generative AI

---

## 📌 Project Overview

AI Placement Mentor ek intelligent platform hai jo college students ko placement preparation mein help karta hai. Yeh system resume analyze karta hai, skill gaps identify karta hai, placement probability predict karta hai, aur AI-based career guidance deta hai.

---

## 🚀 Modules

| Module | Description | Status |
|--------|-------------|--------|
| Module 1 | Resume Analyzer & ATS Score | ✅ Ready |
| Module 2 | Skill Extraction & Gap Analysis | ✅ Ready |
| Module 3 | Placement Prediction (ML) | 🔄 In Progress |
| Module 4 | Job Recommendation System | 🔄 In Progress |
| Module 5 | Interview Question Generator (Gemini) | 🔄 In Progress |
| Module 6 | Career Roadmap Generator | 🔄 In Progress |
| Module 7 | AI Career Mentor Chatbot | 🔄 In Progress |
| Module 8 | Streamlit Dashboard | 🔄 In Progress |

---

## 🛠️ Tech Stack

- **Language**: Python 3.11+
- **UI**: Streamlit
- **Database**: MySQL
- **ML**: Scikit-learn, XGBoost
- **NLP**: NLTK, SpaCy, Transformers
- **GenAI**: Gemini API, OpenAI API
- **Visualization**: Plotly

---

## ⚡ Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/AI_Placement_Mentor.git
cd AI_Placement_Mentor
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Keys
```bash
# config/.env file edit karo
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
DB_PASSWORD=your_mysql_password
```

### Step 4: Database Setup
```bash
mysql -u root -p < database/placement.sql
```

### Step 5: Run the App
```bash
streamlit run dashboard/streamlit_app.py
```

---

## 📁 Project Structure

```
AI_Placement_Mentor/
│
├── app/
│   ├── resume_parser.py       # Module 1: Resume Analysis
│   ├── skill_extractor.py     # Module 2: Skill Extraction
│   ├── predictor.py           # Module 3: ML Prediction
│   ├── recommender.py         # Module 4: Job Recommendation
│   └── chatbot.py             # Module 7: AI Chatbot
│
├── dashboard/
│   └── streamlit_app.py       # Main Streamlit UI
│
├── database/
│   ├── placement.sql          # Database schema
│   └── db_connection.py       # DB helper functions
│
├── models/                    # Trained ML models
├── data/                      # Datasets
├── config/                    # Configuration files
└── requirements.txt
```

---

## 👨‍💻 Developer

**[Your Name]**  
B.Tech [Branch] | [College Name]  
GitHub: github.com/yourusername

---

## 📄 License

This project is for educational purposes.
