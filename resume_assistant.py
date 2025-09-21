

from google import genai
from google.genai import types
import pathlib
import json
import os
import time
import logging
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Setting logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# initial client
client = genai.Client(api_key=API_KEY)
# create chatting session
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=(
            "You are a Resume Coach. Inspire ideas, capture key words from user's input exactly without exaggeration, ask guiding questions for unclear parts, and summarize professionally. "
            "Remember all user-provided information strictly and do not add unconfirmed details. "
            "Structure responses with sections: [Key Points Captured], [Questions for Clarification], [Suggested Resume Section]. "
            "Always ask for more details if information is insufficient to make resume sentence strong. "
            "For PDF inputs, extract key resume details and present in the same structured format."
        ),
        response_mime_type="text/plain",
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_MEDIUM_AND_ABOVE"),
        ],
        thinking_config=types.ThinkingConfig(thinking_budget=0),
    ),
    history=[],
)

# function: process PDF file (Inline Data or File API)
def process_pdf(file_path):
    logger.info(f"Attempting to process PDF: {file_path}")
    file_path = pathlib.Path(file_path)
    if not file_path.exists():
        logger.error(f"File {file_path} does not exist.")
        print(f"Error: File {file_path} does not exist. Please check the path.")
        return None
    if not file_path.is_file():
        logger.error(f"Path {file_path} is not a file.")
        print(f"Error: {file_path} is not a valid file.")
        return None
    
    try:
        file_size = file_path.stat().st_size / (1024 * 1024)  # MB
        logger.info(f"File size: {file_size:.2f} MB")
        
        if file_size <= 20:  # Inline Data for <20MB
            logger.info("Using Inline Data for PDF upload (size <= 20MB).")
            return types.Part.from_bytes(
                data=file_path.read_bytes(),
                mime_type='application/pdf'
            )
        else:  # File API for >20MB
            logger.info("Using File API for PDF upload (size > 20MB).")
            sample_file = client.files.upload(
                file=file_path,
                config=dict(mime_type='application/pdf')
            )
            file_info = client.files.get(name=sample_file.name)
            while file_info.state == "PROCESSING":
                logger.info("Processing PDF... Please wait.")
                print("Processing PDF... Please wait.")
                time.sleep(5)
                file_info = client.files.get(name=sample_file.name)
            if file_info.state == "FAILED":
                logger.error("PDF processing failed.")
                print("Error: PDF processing failed.")
                return None
            logger.info(f"PDF processed successfully: {sample_file.uri}")
            return types.Part.from_file_data(
                file_uri=sample_file.uri,
                mime_type=sample_file.mime_type
            )
    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        print(f"Error processing PDF: {e}")
        return None

# function: save response to JSON log
def save_json_response(response_text, filename_prefix="response"):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.json"
    try:
        data = {"response_text": response_text, "timestamp": timestamp}
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Response saved to {filename}")
        session_file = "session_history.json"
        session_data = {}
        if os.path.exists(session_file):
            with open(session_file, "r", encoding="utf-8") as f:
                session_data = json.load(f)
        session_data[f"response_{timestamp}"] = data
        with open(session_file, "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Merged to {session_file}")
    except Exception as e:
        logger.error(f"Failed to save JSON: {e}")
        with open(filename, "w") as f:
            f.write(response_text)
        logger.info(f"Raw saved to {filename}")

# main loop
def main():
    logger.info("Starting Resume Assistant")
    print("Welcome to the Resume Assistant! Enter info, 'upload <file_path>' or 'open <file_path>' for PDF, 'save' to save response, or 'exit'.")
    
    while True:
        user_input = input("\nYour input: ").strip()
        
        if user_input.lower() == "exit":
            logger.info("Exiting Resume Assistant")
            print("Exiting.")
            break
        if user_input.lower() == "save":
            print("Latest response saved (if available).")
            continue
        
        # handle PDF upload
        file_path = None
        if user_input.lower().startswith("upload "):
            file_path = user_input[7:].strip().strip('<>').strip()
        elif user_input.lower().startswith("can you open this: ") or user_input.lower().startswith("open "):
            if user_input.lower().startswith("can you open this: "):
                file_path = user_input[18:].strip().strip('<>').strip()
            else:
                file_path = user_input[5:].strip().strip('<>').strip()
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)
                logger.info(f"Converted to absolute path: {file_path}")
        
        if file_path:
            pdf_part = process_pdf(file_path)
            if pdf_part:
                response = chat.send_message(
                    message=[
                        types.Part(text="Summarize the key information from this PDF for a resume in the format: [Key Points Captured], [Questions for Clarification], [Suggested Resume Section]."),
                        pdf_part
                    ]
                )
                print("\nAssistant Response:")
                print(response.text)
                save_json_response(response.text, "pdf_response")
                if response.usage_metadata:
                    print("\nToken Usage:")
                    print(f"Prompt Tokens: {response.usage_metadata.prompt_token_count}")
                    print(f"Candidates Tokens: {response.usage_metadata.candidates_token_count}")
                    print(f"Total Tokens: {response.usage_metadata.total_token_count}")
            continue
        
        #  handle text input
        response = chat.send_message(message=user_input)
        print("\nAssistant Response:")
        print(response.text)
        save_json_response(response.text, "text_response")
        if response.usage_metadata:
            print("\nToken Usage:")
            print(f"Prompt Tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Candidates Tokens: {response.usage_metadata.candidates_token_count}")
            print(f"Total Tokens: {response.usage_metadata.total_token_count}")
        
        # history record (for debugging)
        # print("\nChat History:")
        # for content in chat.get_history():
        #     print(f"Role: {content.role}, Text: {content.parts[0].text}")

if __name__ == "__main__":
    main()
    
    
    
    
    
# %%
