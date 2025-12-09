import json
from typing import List, Dict, Any

from fastapi import HTTPException

from .config import settings
from .utils import filter_reference_by_topics

import openai
from openai import OpenAI
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

openai_client = None
if settings.LLM_PROVIDER == "openai" and settings.OPENAI_API_KEY:
    openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

if settings.LLM_PROVIDER == "gemini" and settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)


def build_prompt(
    modules: List[Dict[str, Any]],
    reference_text: str,
    existing_questions: List[str],
    num_sets: int = 3,
) -> str:
    return f"""
You are an assistant that generates university examination question papers.

CONSTRAINTS:
- Use ONLY the given reference content as knowledge.
- NO questions should be outside these syllabus topics and reference content.
- Respect the number of questions and marks for each module.
- Use Bloom's taxonomy levels (Remember, Understand, Apply, Analyze, Evaluate, Create).
- Generate {num_sets} DISTINCT sets of question papers.
- Absolutely NO repetition of any question text across:
  - different sets in this response
  - and this list of previously used questions:
    {json.dumps(existing_questions, ensure_ascii=False)}

MODULES (input specification):
{json.dumps(modules, ensure_ascii=False, indent=2)}

REFERENCE CONTENT (filtered by topics, concatenated syllabus + reference books + reference question papers):
{reference_text[:12000]}

OUTPUT FORMAT:
Return ONLY JSON with this exact structure (no extra text):

{{
  "sets": [
    {{
      "set_number": 1,
      "modules": [
        {{
          "module_number": 1,
          "questions": [
            {{
              "text": "Question text here",
              "marks": 10,
              "blooms_level": "Analyze"
            }}
          ]
        }}
      ]
    }}
  ]
}}
    """


def call_openai(prompt: str) -> Dict[str, Any]:
    """Call OpenAI chat completions API and return parsed JSON.

    Any provider-side errors are converted into HTTPException so the API
    returns a clean 4xx/5xx instead of a raw traceback.
    """
    if not openai_client:
        raise HTTPException(status_code=503, detail="OpenAI client not initialized.")
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You generate exam questions strictly from provided content."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=2400,
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except openai.RateLimitError as e:
        # More user-friendly message when quota is exhausted.
        raise HTTPException(
            status_code=503,
            detail="OpenAI quota exceeded. Please check your OpenAI billing/plan or switch LLM provider.",
        ) from e
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"OpenAI error: {str(e)}") from e


def call_gemini(prompt: str) -> Dict[str, Any]:
    """Call Gemini and return parsed JSON.

    Uses a widely available model name and converts common provider errors
    into HTTPException with clear messages.
    """
    try:
        # Use the requested Gemini model; adjust here if your project uses a different one.
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt)
        text = response.text.strip()
        start = text.find("{")
        end = text.rfind("}")
        json_text = text[start : end + 1]
        return json.loads(json_text)
    except google_exceptions.NotFound as e:
        raise HTTPException(
            status_code=503,
            detail=(
                "Gemini model not available or not enabled for this project. "
                "Check your Google AI Studio configuration or adjust the model name."
            ),
        ) from e
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Gemini error: {str(e)}") from e


def generate_question_sets(
    modules: List[Dict[str, Any]],
    reference_text: str,
    existing_questions: List[str],
    num_sets: int = 3,
) -> Dict[str, Any]:
    merged_topics = "\n".join([m.get("topics", "") for m in modules])
    filtered_ref = filter_reference_by_topics(reference_text, merged_topics)

    prompt = build_prompt(modules, filtered_ref, existing_questions, num_sets=num_sets)
    if settings.LLM_PROVIDER == "gemini":
        return call_gemini(prompt)
    return call_openai(prompt)
