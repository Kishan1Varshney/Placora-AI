create database Placora;
use Placora;


-- ============================================
-- Table 1: Students
-- ============================================
CREATE TABLE IF NOT EXISTS students (
    student_id   INT PRIMARY KEY AUTO_INCREMENT,
    name         VARCHAR(100) NOT NULL,
    email        VARCHAR(100) UNIQUE NOT NULL,
    cgpa         FLOAT,
    branch       VARCHAR(50),
    college      VARCHAR(100),
    graduation_year INT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Table 2: Resumes
-- ============================================
CREATE TABLE IF NOT EXISTS resumes (
    resume_id    INT PRIMARY KEY AUTO_INCREMENT,
    student_id   INT NOT NULL,
    resume_text  LONGTEXT,
    file_name    VARCHAR(200),
    uploaded_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- ============================================
-- Table 3: Skills
-- ============================================
CREATE TABLE IF NOT EXISTS skills (
    skill_id     INT PRIMARY KEY AUTO_INCREMENT,
    student_id   INT NOT NULL,
    skill_name   VARCHAR(100) NOT NULL,
    skill_type   VARCHAR(50),  -- Technical / Soft / Tool
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- ============================================
-- Table 4: Predictions
-- ============================================
CREATE TABLE IF NOT EXISTS predictions (
    prediction_id        INT PRIMARY KEY AUTO_INCREMENT,
    student_id           INT NOT NULL,
    ats_score            FLOAT,
    placement_probability FLOAT,
    target_role          VARCHAR(100),
    predicted_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- ============================================
-- Table 5: Job Recommendations
-- ============================================
CREATE TABLE IF NOT EXISTS job_recommendations (
    job_id       INT PRIMARY KEY AUTO_INCREMENT,
    student_id   INT NOT NULL,
    job_role     VARCHAR(100),
    match_score  FLOAT,
    recommended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- ============================================
-- Sample Data (Testing ke liye)
-- ============================================
INSERT INTO students (name, email, cgpa, branch, college, graduation_year) VALUES
('Rahul Sharma', 'rahul@test.com', 8.5, 'CSE', 'ABC Engineering College', 2025),
('Priya Singh', 'priya@test.com', 7.8, 'IT', 'XYZ Institute', 2025),
('Amit Kumar', 'amit@test.com', 6.5, 'ECE', 'PQR College', 2024);

-- Verify tables
SHOW TABLES;
SELECT 'Database Setup Complete!' AS Status;
