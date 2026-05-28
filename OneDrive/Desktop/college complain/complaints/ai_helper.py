import os
import json
from google import genai


def analyze_complaint(title, description):
    try:
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

        prompt = f"""
You are an assistant for a college complaint management system.
Analyze this complaint and respond ONLY with a JSON object, nothing else.

Complaint Title: {title}
Complaint Description: {description}

Respond in this exact format:
{{
  "urgency": "low" or "medium" or "high",
  "summary": "one sentence summary of the complaint"
}}

Rules for urgency:
- high: safety issues, harassment, no electricity/water, health risks, exam disruption
- medium: food quality, broken facilities, wifi problems
- low: suggestions, minor inconveniences, general feedback
"""
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )

        text = response.text.strip()
        print(f"AI RAW RESPONSE: {text}")

        if text.startswith('```'):
            text = text.split('```')[1]
            if text.startswith('json'):
                text = text[4:]

        result = json.loads(text)
        urgency = result.get('urgency', 'low')
        if urgency not in ['low', 'medium', 'high']:
            urgency = 'low'

        summary = result.get('summary', '')
        return urgency, summary

    except Exception as e:
        print(f"AI Error: {e}")
        return 'low', ''