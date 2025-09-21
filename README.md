# - AI Resume Architect

## Elevator Pitch

An intelligent, conversational AI coach that helps you build and refine your professional resume. Simply chat with the AI or upload an existing resume, and get a polished, professionally formatted PDF in minutes.

---
## 🌟 Features

* **🚀 Start Your Way:** Begin a conversation from scratch or upload an existing PDF resume to get instant, actionable feedback.
* **🤖 Guided AI Coaching:** Engage with an AI coach trained to ask insightful questions, helping you uncover key achievements and quantify your impact effectively.
* **💾 Accurate Data Capture:** Your professional details (dates, roles, tasks) are accurately captured and iteratively saved. You have full control to confirm or correct the AI's summaries throughout the conversation.
* **📄 One-Click PDF Generation:** Generate a beautifully formatted PDF resume at any point in the process with a single click.


---


## Inspiration

Many job seekers struggle with what to include in their resumes and how to format them effectively. We were inspired to create a tool that not only automates the formatting but also acts as a **supportive coach**. Our goal is to help users articulate their experiences powerfully and tailor their resumes for any job, boosting their confidence and success rate in the job market.

---

## 🎬 Demo


## Demo

(paste the link of video, gif, or image here)

---

## Teck Stack

**Front end**:


* **Backend:** **Python, Jinja2, WeasyPrint**
* **AI:** **Google Gemini API (gemini-2.5-flash)**
* **Deployment:**
* **Version Control:** **Git**


## Getting Started

Follow these instructions to set up and run the backend services locally.


1. Preerquisites

- Python 3.10
- An active Google Gemini API Key.


3. ⬇️ Installation

```bash
# 1. Clone the Repository
git clone []()

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

5. Reunning the Application

The backend operates in a three-stage pipeline. Run the scripts in this order:

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

    - Solution: We developed a more robust, hybrid architecture. We use the LLM for its core strength: understanding and structuring data (JSON merging, HTML templating). Then, we hand off the final rendering to deterministic tools like Jinja2 for data injection and WeasyPrint for reliable HTML/CSS to PDF conversion. This approach significantly increases the reliability of the final output.

- Problem: Handling Conflicting User Inputs. Users might correct themselves or provide updated information in later parts of the conversation.

    - Solution: We built a "smart merge" script that leverages the Gemini API. It feeds all session JSON files to the model with a specific prompt, instructing it to intelligently consolidate the data, prioritize newer information to resolve conflicts, and de-duplicate list items. This ensures the final JSON is always clean and up-to-date.

### Front End


## ☀️ What's Next

  - UI for Template Customization: Allow users to fine-tune spacing, fonts, and colors directly in the UI.

  - More Resume Themes: Introduce a library of different visual templates (e.g., Modern, Creative, Academic).

  - Mock Interview Feature: After generating a resume, offer users a mock interview session based on their new resume content.

## 🔥 Team Members

- Irisin - Back end - [github.com/Irisiiin](github.com/Irisiiin)

