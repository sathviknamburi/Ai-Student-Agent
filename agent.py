import os
import time

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found.\n"
        "Please create a .env file and add:\n"
        "GROQ_API_KEY=your_groq_api_key_here"
    )


# ============================================================
# CREATE GROQ CLIENT
# ============================================================

client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# GROQ MODEL
# ============================================================

MODEL_NAME = "openai/gpt-oss-120b"


# ============================================================
# CREATE STUDY PLAN
# ============================================================

def create_study_plan(
    name,
    goal,
    current_level,
    subjects,
    hours_per_day,
    days
):
    """
    Generate a personalized study plan using Groq.
    """

    # ========================================================
    # PROMPT
    # ========================================================

    prompt = f"""
You are an expert AI study planner.

Create a practical, realistic and personalized study plan
for a student.

STUDENT INFORMATION
-------------------
Name: {name}
Goal: {goal}
Current Level: {current_level}
Subjects / Topics: {subjects}
Available Study Hours Per Day: {hours_per_day}
Number of Days: {days}

REQUIREMENTS
------------

1. Create a day-by-day study plan.

2. Clearly mention the topics to study each day.

3. Divide the available study hours intelligently.

4. Include learning time.

5. Include practice time.

6. Include revision sessions.

7. Include practice questions or problems where appropriate.

8. Include progress checkpoints.

9. Keep the workload realistic.

10. Do not overload the student.

11. Include short breaks where appropriate.

12. Give practical tips for consistency.

13. Adapt the difficulty according to the student's current level.

14. Make the plan actionable rather than giving generic advice.

OUTPUT FORMAT
-------------

Use Markdown.

Start with:

# Personalized Study Plan

Then include:

## Student Overview

## Overall Strategy

## Day-by-Day Plan

Use a table where appropriate.

For every day include:

- Topics
- Learning activities
- Practice
- Revision
- Expected outcome

Finally include:

## Progress Checkpoints

## Tips for Success

Return ONLY the final study plan.
"""

    # ========================================================
    # RETRY CONFIGURATION
    # ========================================================

    max_retries = 3

    # ========================================================
    # GROQ REQUEST
    # ========================================================

    for attempt in range(max_retries):

        try:

            response = client.chat.completions.create(
                model=MODEL_NAME,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert AI study planner. "
                            "Create practical and personalized "
                            "study plans for students."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.7,

                max_completion_tokens=8192
            )

            # =================================================
            # GET RESPONSE
            # =================================================

            if not response:
                return "Groq returned no response. Please try again."

            if not response.choices:
                return "Groq returned no choices. Please try again."

            content = response.choices[0].message.content

            if not content:
                return "Groq returned an empty response. Please try again."

            return content

        # ====================================================
        # RATE LIMIT / TEMPORARY ERROR
        # ====================================================

        except Exception as e:

            error_message = str(e)

            print(
                f"Groq error "
                f"(attempt {attempt + 1}/{max_retries}): "
                f"{error_message}"
            )

            # Retry temporary/rate-limit errors
            if (
                "429" in error_message
                or "rate limit" in error_message.lower()
                or "timeout" in error_message.lower()
                or "503" in error_message
                or "502" in error_message
            ):

                if attempt < max_retries - 1:

                    wait_time = 2 ** attempt

                    time.sleep(wait_time)

                    continue

            # Other errors should be shown immediately
            return (
                "❌ Groq API Error:\n\n"
                f"{error_message}"
            )

    # ========================================================
    # FINAL FALLBACK
    # ========================================================

    return (
        "Unable to generate the study plan. "
        "Please try again."
    )