# -*- coding: utf-8 -*-

import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML



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
    create_pdf_resume()
    