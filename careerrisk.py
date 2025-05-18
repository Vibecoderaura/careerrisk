import streamlit as st
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup
import time
from PyPDF2 import PdfReader
import docx2txt

# ----------- Google Sheets setup -----------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    r"C:\Users\Frank\Downloads\frank (1)\eternal-unity-460214-p7-0c0081c14763.json",
    scope)
client = gspread.authorize(creds)
sheet = client.open("Career Risk Scores").sheet1

# ----------- Questionnaire -----------
questions = [
    # Job Security
    "Has your company announced any recent layoffs or restructuring?",
    "Have any colleagues in your team been let go recently?",
    "Has your department’s budget been cut?",
    "Has there been a reduction in your workload?",
    "Have your responsibilities been reassigned to others or automated?",
    "Are you hearing more rumors than usual about organizational changes?",
    # Manager & Team Behaviour
    "Has your manager stopped giving you feedback or coaching?",
    "Have you been left out of important meetings or communications?",
    "Are you receiving fewer new projects or responsibilities than before?",
    "Has your performance been questioned recently (formally or informally)?",
    "Do you feel your work is being overly scrutinized or micromanaged?",
    "Do you sense tension or awkwardness when you interact with your manager?",
    # Career Growth & Motivation
    "Have you been passed over for a promotion or raise you were expecting?",
    "Do you feel like you’re no longer growing or learning in your role?",
    "Have you lost interest in your work?",
    "Are you working in the same role for more than 3 years with no progression?",
    "Have you recently considered studying or switching industries?",
    # Mental & Emotional Health
    "Do you feel anxious or stressed most days before starting work?",
    "Do you feel physically or emotionally exhausted after work?",
    "Have you felt dread about going to work for several weeks?",
    "Do you feel disconnected or unmotivated at work?",
    # Personal Readiness to Leave
    "Have you updated your CV in the last 3 months?",
    "Are you currently applying for other jobs or thinking about it often?",
    "Do you have savings or a financial cushion to survive a few months without work?",
    "Have you spoken to a recruiter or mentor about changing roles recently?",
    # Optional Bonus
    "Do you feel your job could be done by AI or automation within 2 years?"
]

# ----------- Helper functions -----------

def scrape_indeed_jobs(job_titles):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    base_url = "https://uk.indeed.com/jobs?q="
    job_descs = {}
    for title in job_titles:
        desc_list = []
        search_url = base_url + requests.utils.quote(title)
        resp = requests.get(search_url, headers=headers)
        if resp.status_code != 200:
            job_descs[title] = []
            continue
        soup = BeautifulSoup(resp.text, "html.parser")
        job_cards = soup.find_all("div", class_="job_seen_beacon")
        for card in job_cards[:10]:
            summary = card.find("div", class_="job-snippet")
            if summary:
                desc_text = summary.get_text(separator=" ").strip()
                desc_list.append(desc_text)
        job_descs[title] = desc_list
        time.sleep(1)  # polite delay
    return job_descs

def extract_text_from_cv(uploaded_file):
    if uploaded_file.type == "application/pdf":
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.lower()
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = docx2txt.process(uploaded_file)
        return text.lower()
    else:
        return ""

def match_cv_to_jobs(cv_text, job_descs):
    results = {}
    for title, desc_list in job_descs.items():
        combined_desc = " ".join(desc_list).lower()
        job_words = set(combined_desc.split())
        cv_words = set(cv_text.split())
        if not job_words:
            match_pct = 0
        else:
            matched_words = job_words.intersection(cv_words)
            match_pct = len(matched_words) / len(job_words) * 100
        results[title] = round(match_pct, 2)
    return results

# ----------- Streamlit UI -----------

st.title("Career Risk & Exit Readiness Check")

st.write("Rate each question from 1 (No risk / Strong No) to 10 (High risk / Strong Yes).")

total_score = 0
responses = []

for q in questions:
    score = st.slider(q, 1, 10, 5)
    responses.append(score)
    total_score += score

average_score = total_score / len(questions)

st.markdown(f"### Your Average Risk Score: **{average_score:.2f} / 10**")

if average_score < 4:
    risk_level = "LOW"
    st.success("✅ Your job appears stable and you seem fairly content.")

else:
    if 4 <= average_score < 7:
        risk_level = "MODERATE"
        st.warning("⚠️ There are warning signs. Monitor closely and consider exploring new options.")
    else:
        risk_level = "HIGH"
        st.error("🚨 You’re likely at risk or already disengaged. Time to prepare your exit strategy.")

    # Extra services for MODERATE and HIGH risk
    st.markdown("---")
    st.subheader("🔧 Career Support Options")

    st.markdown("### 🎓 Recommended Career Courses")
    st.markdown("[➡️ Python for Beginners (Udemy)](https://www.udemy.com/course/pythonforbeginners/?ref=your_affiliate_code)")
    st.markdown("[➡️ Project Management Certification (Coursera)](https://www.coursera.org/professional-certificates/project-management?ref=your_affiliate_code)")
    st.markdown("[➡️ Data Analysis Bootcamp (Skillshare)](https://www.skillshare.com/browse/data-analysis?ref=your_affiliate_code)")

    st.markdown("### 🛡 Citizens Advice & Worker Protection")
    st.markdown("If you believe you're being unfairly targeted or at risk of dismissal, consider speaking with:")
    st.markdown("- [Citizens Advice Employment Rights](https://www.citizensadvice.org.uk/work/)")
    st.markdown("- [ACAS - Advisory, Conciliation and Arbitration Service](https://www.acas.org.uk/your-rights-at-work)")

    st.markdown("### 🤖 CV Matching Subscription (£4.99/month)")
    wants_service = st.checkbox("Yes, match my CV to current job openings")

    if wants_service:
        email = st.text_input("📧 Enter your email address")
        job_titles = st.text_input("💼 Job titles you're interested in (comma-separated)")
        cv_file = st.file_uploader("📄 Upload your CV (PDF or DOCX)", type=["pdf", "docx"])
        confirmed = st.checkbox("I understand I will be charged £4.99 per month")

        if st.button("Submit"):
            if email and job_titles and cv_file and confirmed:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sheet.append_row([timestamp, email, round(average_score, 2), risk_level, job_titles])

                job_title_list = [j.strip() for j in job_titles.split(",") if j.strip()]
                job_descriptions = scrape_indeed_jobs(job_title_list)
                cv_text = extract_text_from_cv(cv_file)
                match_results = match_cv_to_jobs(cv_text, job_descriptions)

                st.success("✅ Submitted! Your CV has been matched with current openings.")
                st.write("### Match Scores by Job Title:")
                for jt, score in match_results.items():
                    st.write(f"- **{jt}**: {score}% match")
            else:
                st.warning("Please fill in all fields and agree to the subscription to continue.")

