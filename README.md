# - AI Resume Architect

## Elevator Pitch

An intelligent, conversational AI coach that helps you build and refine your professional resume. Simply chat with the AI or upload an existing resume, and get a polished, professionally formatted PDF in minutes.

---
## 🌟 Features

* **🚀 Start Your Way:** Begin a conversation from scratch or upload an existing PDF/DOCX resume to get instant, actionable feedback.
* **🤖 Guided AI Coaching:** Engage with an AI coach trained to ask insightful questions, helping you uncover key achievements and quantify your impact effectively.
* **💾 Accurate Data Capture:** Your professional details (dates, roles, tasks) are accurately captured from uploaded resumes. You have full control to confirm or correct the AI's summaries throughout the conversation.
* **📄 One-Click LaTeX Generation:** Generate a beautifully formatted, overleaf-friendly LaTeX resume by using data from a PDF or DOCX file with a single click.

---

## Inspiration

Many job seekers struggle with what to include in their resumes and how to format them effectively, including students at career fairs! We were inspired to create a tool that not only automates the formatting but also acts as a **supportive coach**. Our goal is to help users articulate their experiences powerfully and tailor their resumes for any job, boosting their confidence and success rate in the job market.

---

## 🎬 Demo




## Demo

// Youtube link yet to be posted.

---

## Teck Stack

* **Front end**: **HTML, CSS, JavaScript**
* **Backend:** **Python, Flask, Jinja2, WeasyPrint**
* **AI:** **Google Gemini API (gemini-2.5-pro)**
* **Deployment:** **Github**
* **Version Control:** **Git**


## Getting Started

Follow these instructions to set up and run the backend services locally.


1. Pre-erquisites

- Python 3.10
- An active Google Gemini API Key.


3. ⬇️ Installation

```bash
# 1. Clone the Repository
git clone https://github.com/Visnu-Pandian/ResumAI

# 2. Enter project path
cd ResumAI

# 3. Install back end dependencies
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# 4. Install required packages
pip install -r requirements.txt
```

4. Environment Variables

Create a file named `.env` in the root of the project and add your own Google Gemini API key
The application will read this key to authenticate with the Google API. The `.env` file is included in `.gitignore` to ensure your key remains private.

5. Running the Application

The program operates via a single file (app.py)

- Step 1: clone the repository

```bash
git clone https://github.com/Visnu-Pandian/ResumAI
```

- Step 2: cd into the project

```bash
cd ResumAI
```

- Step 3: Run the main app.py file

```bash
python app.py
```

The project's webpage should open in your default web browser if you have all the requirements installed.

The alt-backend operates in a three-stage pipeline. Run the scripts in this order:

- Step 1: Start the conversation with the AI coach to generate session JSON files
`python resume_assistant.py`

- Step 2: Merge the conversation files into a single, clean resume JSON
`python merge_jsons.py`

- Step 3: Generate the final PDF from the merged JSON data
`python generate_resume.py`

## 💥 Challenges we ran into

### Back End

- Problem: Ensuring AI Accuracy and Persona. An LLM can be forgetful or overly creative. We needed our AI to be a focused, reliable coach.

    - Solution: We engineered a detailed system prompt to establish the AI's persona. To guarantee data integrity, we designed a pipeline where each conversational turn is summarized and saved to a versioned JSON file. This prevents the AI from "hallucinating" and keeps the user's data persistent and accurate.

- Problem: Unreliable Direct PDF Generation. Directly asking an LLM to generate complex formats like LaTeX or styled HTML/CSS often results in syntax errors.

    - Solution: We developed a more robust, hybrid architecture. We use the LLM for its core strength: understanding and structuring data (LaTeX generation, JSON merging, HTML templating). Then, we hand off the final rendering to websites like Overleaf or deterministic tools like Jinja2 for data injection and WeasyPrint for reliable HTML/CSS to PDF conversion. This approach significantly increases the reliability of the final output.

- Problem: Handling Conflicting User Inputs. Users might correct themselves or provide updated information in later parts of the conversation.

    - Solution: We built a "smart merge" script that leverages the Gemini API. It feeds all session JSON files to the model with a specific prompt, instructing it to intelligently consolidate the data, prioritize newer information to resolve conflicts, and de-duplicate list items. This ensures the final JSON is always clean and up-to-date. For LaTeX generation, users can prompt their Gemini terminal to explain their needs to it and get the best Overleaf formatting they want.

### Front End

 - Problem: Prompting from outside the terminal. Providing a terminal to the user without giving the AI a way to initiate the conversation led to vagueness and ways for the model to go astray.

    - Solution: We used the user's input resume as part of the prompt and let the AI follow a guided path to deliver a neater resume in an easily editable LaTeX format (via the Overleaf website).

- Problem: Gemini API had a lack of context caching due to each message being individual API calls. 

    - Solution: The user is provided LaTeX output in the chat terminal which they can copy-paste to give full context on what they are talking about.

- Problem: Compile errors prevented code from executing for a large majority of the hackathon. Gemini API's multiple available implementation routes made optimal coding decisions not obvious, leading to large time sinks.

    - Solution: Completing a draft of the hack without any involvement from Gemini API and then integrating it once all feasible and essential features had been added.

## ☀️ What's Next

  - UI for Template Customization: Allow users to fine-tune spacing, fonts, and colors directly in the UI.

  - More Resume Themes: Introduce a library of different visual templates (e.g., Modern, Creative, Academic).

  - PDF Generation: Similar to LaTeX generation, users can get single-click PDF downloads of their custom-formatted resumes.

  - Mock Interview Feature: After generating a resume, offer users a mock interview session based on their new resume content.

## 🔥 Team Members

- Visnu Pandian - Full stack [github.com/Visnu-Pandian](github.com/Visnu-Pandian)
- Irisin - Back end - [github.com/Irisiiin](github.com/Irisiiin)
- Ben Burris - Front end [github.com/bmburris05](github.com/bmburris05)
- Lexus Workman - Front end [github.com/cranberrymatchafrog](github.com/cranberrymatchafrog)
