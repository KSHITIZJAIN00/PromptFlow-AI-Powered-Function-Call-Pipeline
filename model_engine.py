# ai_pipeline_project/model_engine.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import json
import re

MODEL_NAME = "declare-lab/flan-alpaca-large"

class ModelEngine:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        self.pipe = pipeline("text2text-generation", model=self.model, tokenizer=self.tokenizer)

    def plan_sequence(self, user_query: str) -> str:
        prompt = f"""
You are an assistant that transforms user queries into a JSON sequence of function calls.

Available Functions:
- get_invoices(month: str)
- summarize_invoices(invoices)
- send_email(to: str, subject: str, body: str)
- create_calendar_event(title: str, date: str, time: str)
- write_summary_to_file(content: str, filename: str)

Respond ONLY with a valid JSON array like this:

[
  {{
    "function": "get_invoices",
    "args": {{"month": "March"}}
  }},
  {{
    "function": "summarize_invoices",
    "args": {{"invoices": "<output_of_get_invoices>"}}
  }},
  {{
    "function": "send_email",
    "args": {{
      "to": "me@example.com",
      "subject": "Invoice Summary",
      "body": "<output_of_summarize_invoices>"
    }}
  }}
]

Only output the JSON array. No explanation text.

User query: "{user_query}"
"""
        output = self.pipe(prompt, max_new_tokens=512)[0]["generated_text"]
        print("\n=== Raw Model Output ===\n", output)

        try:
            json_match = re.search(r"\[\s*{.*?}\s*\]", output, re.DOTALL)
            if not json_match:
                raise ValueError("No valid JSON array found in model output.")

            json_block = json_match.group(0)
            parsed = json.loads(json_block)
            return json.dumps(parsed, indent=2)

        except Exception as e:
            print(f"[Error] JSON parsing failed:\n{e}")
            print("[Warning] Using enhanced fallback parser due to malformed JSON.")

            steps = []

            # Extract month if present
            month_match = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b', user_query, re.IGNORECASE)
            month = month_match.group(0).capitalize() if month_match else "March"

            # Detect common intents
            if "invoice" in user_query.lower():
                steps.append({
                    "function": "get_invoices",
                    "args": {"month": month}
                })
                steps.append({
                    "function": "summarize_invoices",
                    "args": {"invoices": "<output_of_get_invoices>"}
                })

            if "email" in user_query.lower():
                steps.append({
                    "function": "send_email",
                    "args": {
                        "to": "me@example.com",
                        "subject": "Invoice Summary",
                        "body": "<output_of_summarize_invoices>"
                    }
                })

            if "save" in user_query.lower() or "write" in user_query.lower():
                steps.append({
                    "function": "write_summary_to_file",
                    "args": {
                        "content": "<output_of_summarize_invoices>",
                        "filename": "summary.txt"
                    }
                })

            if "calendar" in user_query.lower() or "meeting" in user_query.lower() or "event" in user_query.lower():
                date_match = re.search(r"\d{4}-\d{2}-\d{2}", user_query)
                time_match = re.search(r"\d{2}:\d{2}", user_query)
                title_match = re.search(r"called\s+'([^']+)'", user_query) or re.search(r'titled\s+"([^"]+)"', user_query)

                steps.append({
                    "function": "create_calendar_event",
                    "args": {
                        "title": title_match.group(1) if title_match else "Meeting",
                        "date": date_match.group(0) if date_match else "2025-07-01",
                        "time": time_match.group(0) if time_match else "09:00"
                    }
                })

            if not steps:
                raise ValueError("No recognizable functions found for fallback.")

            return json.dumps(steps, indent=2)
