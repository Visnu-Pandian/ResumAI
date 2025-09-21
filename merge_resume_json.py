
import json
import os
import time
import logging
from google import genai
from google.genai import types

# set logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# initialize Gemini API client
client = genai.Client(api_key="AIzaSyCC7PnYgOd8CAxv8jdVDKNw4gMML53-bPM")

# json files directory(adjustable)
json_dir = '.'  # current directory

def load_json_files():
    """Read all JSON files and sort them by time (new files take priority)"""
    json_files = sorted(
        [f for f in os.listdir(json_dir) if f.endswith('.json') and (f.startswith('text_response_') or f.startswith('pdf_response_'))],
        key=lambda f: os.path.getmtime(os.path.join(json_dir, f))
    )
    
    print("List of read JSON files (in the order of generation, from old to new) :")
    all_data = []
    for file in json_files:
        file_path = os.path.join(json_dir, file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_data.append(data)
                print(f"\n内容 of {file}:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON file: {file}")
            print(f"Error: Failed to parse {file}. Skipping.")
    
    return json_files, all_data

def merge_json_with_gemini(all_data):
    """Merging JSON Data using Gemini API"""
    prompt = f"""
You are a JSON merger expert. Merge the following JSON data list into a single unique JSON object.

Rules:
- The data is in chronological order (oldest first, newest last).
- Prioritize newer information to override older ones in case of conflicts (e.g., if a key like "research" has updated details in later JSON, use the newest).
- Handle conflicts intelligently: For fields like "keywords" or "resume_section", combine them without duplication, favoring newer additions.
- For arrays (e.g., keywords, questions), merge uniquely, removing duplicates, and prefer newer entries if conflicting.
- Generate a clean, comprehensive JSON with all sections (contact, education, research, skills, honors, projects, coursework).
- Output ONLY the merged JSON object, no other text.

JSON Data List:
{json.dumps(all_data, indent=2)}
"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are a JSON merger expert. Output only valid JSON.",
                response_mime_type="application/json",
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            )
        )
        return response.text.strip()
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        print(f"Error: Failed to merge JSON with Gemini API: {e}")
        return None

def main():
    print("JSON Merger: Combine session history into a single resume JSON.")
    
    # load json files
    json_files, all_data = load_json_files()
    if not all_data:
        print("No valid JSON files found. Please run the resume assistant first.")
        return
    
    # merge JSON
    merged_json_str = merge_json_with_gemini(all_data)
    if not merged_json_str:
        print("Failed to merge JSON. Check API key or input data.")
        return
    
    #resolve and save the merged result
    try:
        merged_data = json.loads(merged_json_str)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        new_file = f"merged_resume_{timestamp}.json"
        with open(new_file, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, indent=2, ensure_ascii=False)
        print(f"\n生成的唯一新 JSON 文件: {new_file}")
        print("合并结果:")
        print(json.dumps(merged_data, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        logger.error("Gemini response is not valid JSON.")
        print("Error: Gemini response is not valid JSON.")
        print("Raw Gemini output:")
        print(merged_json_str)

if __name__ == "__main__":
    main()
