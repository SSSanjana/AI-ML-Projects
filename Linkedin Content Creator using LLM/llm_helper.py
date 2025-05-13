# llm_helper.py
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-8b-8192"
)

def invoke_raw_prompt(prompt_text):
    """
    Takes a raw text prompt and returns the plain LLM response string.
    """
    chain = ChatPromptTemplate.from_messages([
        ("system", "You are a professional LinkedIn content strategist."),
        ("user", "{prompt}")
    ]) | llm | StrOutputParser()

    return chain.invoke({"prompt": prompt_text})


def generate_response(prompt):
    """
    Generate a basic response using the LLM given a prompt string.
    Used by post_analyzer.py.
    """
    chain = ChatPromptTemplate.from_messages([
        ("system", "You are a professional LinkedIn content strategist."),
        ("user", "{prompt}")
    ]) | llm | StrOutputParser()

    response = chain.invoke({"prompt": prompt})
    print("🔍 RAW LLM RESPONSE:\n", response)
    return response


def compare_posts_with_llm(brand_post, other_post):
    """
    Compare two LinkedIn posts using the LLM and return analysis.
    """
    comparison_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional LinkedIn content strategist. Given two LinkedIn posts, provide a detailed comparison and evaluation."),
        ("user", """Compare the following two LinkedIn posts:

BrandBoost Post:
{brand_post}

Other AI Tool Post:
{other_post}

1. Structure & Flow Comparison  
2. Hook effectiveness  
3. Emotional engagement  
4. Tone and relevance  
5. Language and readability  
6. Potential engagement impact  

Then conclude with:  
- Why BrandBoost post might perform better  
- Score (0–10) for each post  
- Suggestions to improve the other post  
- Suggest: 'Write something like this in your own style'
""")
    ])

    chain = comparison_prompt | llm | StrOutputParser()

    result = chain.invoke({
        "brand_post": brand_post,
        "other_post": other_post
    })

    return result


if __name__ == "__main__":
    # Test example
    response = generate_response("What's a good LinkedIn hook for a data analyst portfolio?")
    print(response)
