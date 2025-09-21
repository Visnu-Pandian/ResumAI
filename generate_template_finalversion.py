# -*- coding: utf-8 -*-

import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

MODEL_NAME = "gemini-2.5-flash"
# Here is the input of merged json file. 
INPUT_JSON_PATH = "converted_resume.json"
OUTPUT_HTML_PATH = "resume_template.html"

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


CSS_TEMPLATES = {
    "classic_single_column": """
body {
    font-family: 'Source Sans Pro', sans-serif;
    margin: 0;
    padding: 1in;
    line-height: 1.2;
    color: #000;
    background: #fff;
  }

  a {
    text-decoration: underline;
    color: inherit;
  }

  h1, h2, h3 {
    margin: 0;
  }

  /* ---------- Heading ---------- /
  .header {
    text-align: center;
    margin-bottom: 1em;
  }

  .header h1 {
    font-size: 2.5em;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .header .contact {
    font-size: 0.85em;
  }

  / ---------- Sections ---------- /
  section {
    margin-bottom: 1em;
  }

  section h2 {
    font-size: 1.2em;
    text-transform: uppercase;
    border-bottom: 1px solid #000;
    padding-bottom: 2px;
    margin-bottom: 0.5em;
  }

  / ---------- Subheadings ---------- /
  .subheading {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.1em;
    font-weight: bold;
  }

  .subheading .subinfo {
    font-style: italic;
    font-weight: normal;
    font-size: 0.85em;
  }

  / ---------- Lists ---------- /
  ul {
    margin: 0 0 0.8em 0.15in;
    padding-left: 0;
    list-style-type: disc;
  }

  li {
    margin-bottom: 0.2em;
    font-size: 0.9em;
  }

  / ---------- Projects ---------- /
  .project-title {
    display: flex;
    justify-content: space-between;
    font-weight: bold;
  }

  .project-subtitle {
    font-style: italic;
    font-size: 0.85em;
  }

  / ---------- Technical Skills ---------- */
  .skills {
    margin-left: 0.15in;
    font-size: 0.9em;
  }

  .skills b {
    display: inline-block;
    width: 130px;
  }
    """
}



def create_resume_template(style_name="modern_two_column"):
    """
    Generates an HTML resume template using the Gemini API.
    The CSS is pulled from the internal CSS_TEMPLATES dictionary.
    """
    try:  
        # 1. Read the input JSON file
        json_content = Path(INPUT_JSON_PATH).read_text()
        print(f"✅ Read JSON data. Using '{style_name}' template.")

        # <-- CHANGED: Get the CSS from the dictionary.
        # Use .get() for safety, with a default fallback.
        css_guide = CSS_TEMPLATES.get(style_name, list(CSS_TEMPLATES.values())[0])

        # 2. Construct the detailed prompt for the AI
        prompt = f"""
        Your task is to generate a single, self-contained HTML file to be used as a resume template.
        The template must be a Jinja2 template, using `{{{{ item.key }}}}` for variables and `{{% for item in list %}} ... {{% endfor %}}` for loops.

        Here is the JSON data structure that will be used to populate the template:
        ---JSON STRUCTURE AND DATA---
        {json_content}
        ---END JSON---

        Here is the CSS style guide. The class names in the generated HTML MUST match the selectors in this CSS. The CSS must be placed inside a `<style>` tag in the HTML `<head>`.
        ---CSS STYLE GUIDE---
        {css_guide}
        ---END CSS---

        Instructions:
        1. Create a complete HTML5 document.
        2. The HTML should be semantically structured.
        3. The CSS from the style guide must be included in a `<style>` tag in the document's `<head>`.
        4. The body of the HTML should be a Jinja2 template that correctly iterates through the JSON data.
        5. Produce ONLY the complete HTML code. Do not include any other text or markdown formatting.
        6. page boarder and margin should both be 0; titel font-weight shoule be "normal"; and Overall font-size should be smaller.
        """

        # 3. Initialize the Gemini client and make the API call
        print("🤖 Calling the Gemini API to generate the template...")
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are an expert web developer specializing in creating clean, semantic HTML and CSS for professional resumes.",
                temperature=0.0
            )
        )

        # 4. Save the generated HTML to a file
        generated_html = response.text.strip()
        # Create a unique filename for the output based on the style
        output_filename = f"resume_template_{style_name}.html"
        Path(output_filename).write_text(generated_html)
        print(f"🎉 Success! Your new resume template has been saved to: {output_filename}")

    except FileNotFoundError as e:
        print(f"❌ Error: Could not find a required file. Make sure '{e.filename}' exists.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")



def create_pdf_resume():

    try:
        # set paths

        # 1. your merged json resume file
        json_filename = "converted_resume.json"
        
        # 2. The html template we provide
        template_filename = "resume_template_modern_two_column.html" 
        
        # 3. the final output PDF file name
        output_filename = "my_final_resume.pdf"

  

        # step1: Load your real JSON data 
        print(f"loading data from {json_filename} ...")
        with open(json_filename, 'r', encoding='utf-8') as f:
            resume_data = json.load(f)
        print("✅ data successfully loaded.")

        # Step 2: Set up the Jinja2 template environment and load your HTML template
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template(template_filename)
        print(f"✅ Sucessfully load template from {template_filename} ")
        
        
        # Step 3: Render the template. This is the most crucial step. Jinja2 will find all the {{... }} Placeholder 
        # Replace them with the real data in the 'resume_data' dictionary.        

        html_out = template.render(resume_data)
        print("✅ Successfully filled your data into the template")

        # Step 4: Use the WeasyPrint library to convert the final filled HTML string to a PDF 
        # base_url='.' helps WeasyPrint find local files (such as images, although this template does not have them)
        print(f"Generating PDF file...")
        HTML(string=html_out, base_url='.').write_pdf(output_filename)

        print("\n" + "="*40)
        print(f"🎉🎉🎉 Success! Your final resume has been saved as: {output_filename}")
        print("="*40)

    except FileNotFoundError as e:
        print(f"❌ Error: File not found. Please make sure '{e.filename}' has the same path as this script.")
    except Exception as e:
        print(f"❌ Unexpected error happened: {e}")



if __name__ == "__main__":
    create_resume_template(style_name="modern_two_column")
    create_pdf_resume()
    
# %%
