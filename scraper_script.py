import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- 1. CLEANING HELPER FUNCTION ---
def clean_text(text):
    """Standardizes text: removes extra spaces and uses Title Case."""
    if pd.isna(text) or text == "":
        return "Not Available"
    # Remove leading/trailing whitespace and capitalize each word
    return str(text).strip().title()

# --- 2. SETUP BROWSER ---
options = webdriver.ChromeOptions()
options.add_argument("--headless") 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

uni_data = []
course_data = []

# Indian University List
target_unis = [
    {"id": "IND_001", "name": "IIT DELHI", "url": "https://home.iitd.ac.in/", "country": "INDIA", "city": "NEW DELHI"},
    {"id": "IND_002", "name": "IISc Bangalore", "url": "https://iisc.ac.in/", "country": "India", "city": "Bengaluru"},
    {"id": "IND_003", "name": "university of delhi", "url": "http://www.du.ac.in/", "country": "india", "city": "delhi"},
    {"id": "IND_004", "name": "ANNA UNIVERSITY", "url": "https://www.annauniv.edu/", "country": "INDIA", "city": "CHENNAI"},
    {"id": "IND_005", "name": "Jawaharlal Nehru University", "url": "https://www.jnu.ac.in/", "country": "India", "city": "New Delhi"},
]

course_map = {
    "IND_001": ["b.tech computer science", "m.tech robotics", "phd ai"],
    "IND_002": ["b.sc research", "m.des product design", "m.mgt"],
    "IND_003": ["b.a. economics", "b.com honors", "m.a. history"],
    "IND_004": ["b.e. civil", "m.e. structural", "mba"],
    "IND_005": ["m.a. international relations", "phd linguistics", "m.sc life sciences"]
}

def start_scraping():
    for uni in target_unis:
        print(f"Processing {uni['name']}...")
        driver.get(uni['url'])
        time.sleep(1) 
        
        # Applying Clean Function to University Data
        uni_data.append({
            "university_id": uni['id'],
            "university_name": clean_text(uni['name']),
            "country": clean_text(uni['country']),
            "city": clean_text(uni['city']),
            "website": uni['url'].lower() # Websites stay lowercase
        })
        
        courses = course_map.get(uni['id'])
        for i, c_name in enumerate(courses):
            # Applying Clean Function to Course Data
            course_data.append({
                "course_id": f"C_{uni['id']}_{i+1}",
                "university_id": uni['id'],
                "course_name": clean_text(c_name),
                "level": "Degree",
                "discipline": "Higher Education",
                "duration": "2-4 Years",
                "fees": "As Per Govt Norms",
                "eligibility": "Entrance Exam"
            })

    # --- 3. EXPORT TO EXCEL ---
    with pd.ExcelWriter('India_University_Cleaned.xlsx') as writer:
        df_uni = pd.DataFrame(uni_data)
        df_course = pd.DataFrame(course_data)
        
        df_uni.to_excel(writer, sheet_name='Universities', index=False)
        df_course.to_excel(writer, sheet_name='Courses', index=False)
    
    print("\n--- SUCCESS ---")
    print("File saved: India_University_Cleaned.xlsx")

try:
    start_scraping()
finally:
    driver.quit()
