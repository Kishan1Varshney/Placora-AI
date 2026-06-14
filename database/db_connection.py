# ============================================
# AI Placement Mentor - Database Connection
# File: database/db_connection.py
# ============================================

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# .env file load karo
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'config', '.env'))


def get_connection():
    """
    MySQL database se connection banata hai.
    Returns: connection object ya None
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', '127.0.0.1'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'Placora')
        )
        if connection.is_connected():
            print("✅ MySQL se successfully connect ho gaye!")
            return connection
    except Error as e:
        print(f"❌ Database connection error: {e}")
        return None


def close_connection(connection, cursor=None):
    """
    Database connection band karta hai.
    """
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.close()
        print("🔒 MySQL connection band ho gaya.")


def execute_query(query, params=None, fetch=False):
    """
    SQL query execute karta hai.
    
    Args:
        query  : SQL query string
        params : Query parameters (tuple)
        fetch  : True = SELECT, False = INSERT/UPDATE/DELETE
    
    Returns:
        Results (fetch=True) ya last inserted ID (fetch=False)
    """
    connection = get_connection()
    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())

        if fetch:
            results = cursor.fetchall()
            return results
        else:
            connection.commit()
            return cursor.lastrowid

    except Error as e:
        print(f"❌ Query Error: {e}")
        return None
    finally:
        close_connection(connection, cursor)


# ============================================
# Student Database Functions
# ============================================

def save_student(name, email, cgpa, branch, college, graduation_year):
    """Naya student database mein save karta hai."""
    query = """
        INSERT INTO students (name, email, cgpa, branch, college, graduation_year)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            cgpa = VALUES(cgpa),
            branch = VALUES(branch)
    """
    student_id = execute_query(query, (name, email, cgpa, branch, college, graduation_year))
    return student_id


def get_student_by_email(email):
    """Email se student dhundta hai."""
    query = "SELECT * FROM students WHERE email = %s"
    results = execute_query(query, (email,), fetch=True)
    return results[0] if results else None


def save_resume(student_id, resume_text, file_name):
    """Resume database mein save karta hai."""
    query = """
        INSERT INTO resumes (student_id, resume_text, file_name)
        VALUES (%s, %s, %s)
    """
    return execute_query(query, (student_id, resume_text, file_name))


def save_skills(student_id, skills_list):
    """Student ke skills save karta hai."""
    # Pehle purane skills delete karo
    execute_query("DELETE FROM skills WHERE student_id = %s", (student_id,))
    
    for skill in skills_list:
        query = """
            INSERT INTO skills (student_id, skill_name, skill_type)
            VALUES (%s, %s, %s)
        """
        execute_query(query, (student_id, skill, 'Technical'))


def save_prediction(student_id, ats_score, placement_prob, target_role):
    """Prediction results save karta hai."""
    query = """
        INSERT INTO predictions (student_id, ats_score, placement_probability, target_role)
        VALUES (%s, %s, %s, %s)
    """
    return execute_query(query, (student_id, ats_score, placement_prob, target_role))


def get_student_predictions(student_id):
    """Student ki predictions fetch karta hai."""
    query = """
        SELECT * FROM predictions 
        WHERE student_id = %s 
        ORDER BY predicted_at DESC 
        LIMIT 5
    """
    return execute_query(query, (student_id,), fetch=True)


# ============================================
# Test Connection
# ============================================
if __name__ == "__main__":
    print("🔍 Database connection test kar rahe hain...")
    conn = get_connection()
    if conn:
        print("✅ Connection successful!")
        close_connection(conn)
    else:
        print("❌ Connection failed! .env file check karo.")
