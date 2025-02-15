from agno.agent import Agent
from agno.models.openai import OpenAIChat

def format_categories(categories):
    """Converts a list of categories into a formatted string for prompt embedding."""
    return ", ".join(f'"{category}"' for category in categories)

def generate_product_prompt(categories):
    """Generates a structured prompt for the AI agent to retrieve product recommendations."""
    categories_str = format_categories(categories)
    
    prompt = f"""
    I have a list of categories: [{categories_str}].

    **Your Task:**  
    For each category, find **exactly one relevant product** from Amazon that match the following strict criteria:

    1. **Relevance:** The product must clearly align with the specified category [{categories_str}].  
    2. **Availability:** The product must be in stock and available for immediate purchase.  
    3. **Link Validity:** Provide a verified, functional, and directly accessible product link. Ensure the link leads to the correct product and does not redirect to unrelated pages.  
    4. **Product Quality:** Prioritize products with high ratings (4 stars or above) and multiple verified customer reviews to ensure quality.  
    5. **Category Adherence:** Do not deviate from the listed categories [{categories_str}] or add additional products beyond the specified one per category.  

    Your response should be structured as follows:

    Category: <Category Name>  
    1. **Product Name** - [Buy Here](Product Link)  
       - Price: $XX.XX  
       - Store: <Amazon/Walmart/Target/Best Buy>

    **Important:**  
    - Double-check all links for validity and relevance before submission.  
    - If a valid product cannot be found for a category, state "**No valid products found**" and provide no substitutes.  
    - Strictly adhere to the categories provided. Avoid any extraneous or off-topic suggestions.  
    """
    
    return prompt.strip()

# Initialize agent
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="You are a product recommendation expert specializing in finding the best available items from major retailers.",
    markdown=True
)
