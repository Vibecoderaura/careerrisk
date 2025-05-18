import streamlit as st



# Define the list of questions

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



# Streamlit UI setup

st.set_page_config(page_title="Career Risk Score", layout="centered")

st.title("Career Risk / Exit Readiness Assessment")

st.markdown("Rate each question from **1 (Strong No / No Risk)** to **10 (Strong Yes / High Risk)**.")



# Collect scores from sliders

scores = []

for question in questions:

    score = st.slider(question, min_value=1, max_value=10, value=5)

    scores.append(score)



# Submit button

if st.button("Submit"):

    average_score = sum(scores) / len(questions)

    st.markdown(f"### Your Average Risk Score: **{average_score:.2f} / 10**")



    # Risk feedback & email pitch

    if average_score < 4:

        st.success("**Risk Level: LOW** — Your job appears stable and you seem fairly content.")

        pitch = "Want to stay ahead of future risks? Get a free monthly newsletter with job trends and alerts."

    elif 4 <= average_score < 7:

        st.warning("**Risk Level: MODERATE** — There are warning signs. Monitor closely and explore your options.")

        pitch = "Get 3 expert tips to protect your job, course suggestions, and new job alerts. Enter your email:"

    else:

        st.error("**Risk Level: HIGH** — You’re likely at risk or disengaged. Start preparing your exit strategy now.")

        pitch = "We'll help match your CV to real jobs, recommend retraining options, or suggest union support. Enter your email below:"



    # Email collection section

    st.markdown("### Next Step")

    st.info(pitch)

    email = st.text_input("Enter your email to receive support")



    if st.button("Send"):

        if email and "@" in email:

            st.success(f"Thanks! We'll be in touch at **{email}**.")

            # Optional: Save this email or send it to a service

        else:

            st.error("Please enter a valid email address.")