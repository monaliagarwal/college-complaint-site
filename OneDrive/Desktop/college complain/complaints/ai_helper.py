import os
import json
import re
from groq import Groq


def analyze_complaint(title, description):
    try:
        client = Groq(api_key=os.getenv('GEMINI_API_KEY'))

        prompt = f"""You are an assistant for a college complaint management system.
Analyze this complaint and respond ONLY with a JSON object, nothing else. No markdown, no backticks.

Complaint Title: {title}
Complaint Description: {description}

Respond in this exact format:
{{"urgency": "low" or "medium" or "high", "summary": "one sentence summary of the complaint"}}

Rules for urgency:
- high: safety issues, harassment, no electricity/water, health risks, exam disruption
- medium: food quality, broken facilities, wifi problems
- low: suggestions, minor inconveniences, general feedback"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=200
        )

        text = response.choices[0].message.content
        if not text:
            print("AI Error: Empty response from model")
            return 'low', ''

        text = text.strip()
        print(f"AI RAW RESPONSE: {text}")

        match = re.search(r'\{.*?\}', text, re.DOTALL)
        if not match:
            print("AI Error: No JSON found in response")
            return 'low', ''

        result = json.loads(match.group())
        urgency = result.get('urgency', 'low').strip().lower()
        if urgency not in ['low', 'medium', 'high']:
            urgency = 'low'

        summary = result.get('summary', '')
        return urgency, summary

    except Exception as e:
        print(f"AI Error: {e}")
        return 'low', ''
