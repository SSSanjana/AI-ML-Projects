#post_analyzer.py
import re
from llm_helper import generate_response

def extract_section(text, keyword):
    """
    Extracts the section content based on the keyword using a robust pattern.
    """
    # Match section headers even if they vary slightly or include colons
    pattern = rf"{re.escape(keyword)}.*?\n(.*?)(?=\n[🧱🧠🗂️📊🛠️✍️🌐🎯]|$)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else "Not Available"

def analyze_post(post_text,likes=0, comments=0, shares=0, impressions=0):
    """
    Analyzes a LinkedIn post and extracts detailed insights based on predefined criteria.
    """
    prompt = f"""
    Analyze the following LinkedIn post and provide a detailed analysis by filling in each of the following sections:

    🧱 Structure: Breakdown into Hook, Body, CTA  
    🧠 Tone and Emotional Feel  
    🗂️ Post Type (e.g. Story, Tips, Announcement)  
    📊 Performance (based on engagement + structure)  
    🛠️ Suggestions to Improve  
    ✍️ Rewritten (Your Style)  
    🌐 Platforms to Post  
    🎯 Audience it will attract

    Format the response as:
    🧱 Structure:
    <...>

    🧠 Tone and Emotional Feel:
    <...>

    and so on...

    Post:
    {post_text}
    """

    response = generate_response(prompt)

    return {
        "structure": extract_section(response, "🧱 Structure"),
        "tone": extract_section(response, "🧠 Tone and Emotional Feel"),
        "post_type": extract_section(response, "🗂️ Post Type"),
        "performance": extract_section(response, "📊 Performance"),
        "suggestions": extract_section(response, "🛠️ Suggestions to Improve"),
        "rewritten": extract_section(response, "✍️ Rewritten"),
        "platforms": extract_section(response, "🌐 Platforms"),
        "audience": extract_section(response, "🎯 Audience"),
        "summary": response  # Full raw response for debug
    }
