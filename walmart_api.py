from serpapi import GoogleSearch
import json
from typing import Dict, List, Optional
import streamlit as st
import openai
import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class WalmartAPI:
    def __init__(self, api_key: str):
        """
        Initialize the WalmartAPI class with your SerpApi key
        
        Args:
            api_key (str): Your SerpApi API key
        """
        self.api_key = api_key

    def search_products(
        self,
        query: str,
        sort: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        page: int = 1,
        store_id: Optional[str] = None,
    ) -> Dict:
        """
        Search for products on Walmart
        
        Args:
            query (str): Search query
            sort (str, optional): Sorting option (price_low, price_high, best_seller, best_match, rating_high, new)
            min_price (float, optional): Minimum price filter
            max_price (float, optional): Maximum price filter
            page (int, optional): Page number (1-100)
            store_id (str, optional): Specific store ID to search in
            
        Returns:
            Dict: JSON response containing search results
        """
        params = {
            "api_key": self.api_key,
            "engine": "walmart",
            "query": query,
            "page": page
        }

        # Add optional parameters if provided
        if sort:
            params["sort"] = sort
        if min_price is not None:
            params["min_price"] = min_price
        if max_price is not None:
            params["max_price"] = max_price
        if store_id:
            params["store_id"] = store_id

        search = GoogleSearch(params)
        results = search.get_dict()
        
        return results

    def get_product_details(self, product_id: str) -> Dict:
        """
        Get detailed information about a specific product
        
        Args:
            product_id (str): Walmart product ID
            
        Returns:
            Dict: Product details
        """
        params = {
            "api_key": self.api_key,
            "engine": "walmart",
            "product_id": product_id
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        return results

    def get_product_suggestions(self, categories: List[str]) -> str:
        """
        Get product suggestions for given categories using Walmart API
        
        Args:
            categories (List[str]): List of product categories
            
        Returns:
            str: Formatted markdown string with product suggestions
        """
        suggestions = []
        
        for category in categories:
            results = self.search_products(
                query=category,
                sort="rating_high",
                page=1
            )
            
            if "organic_results" in results and results["organic_results"]:
                product = results["organic_results"][0]  # Get the first (highest-rated) product
                
                product_name = product.get('title', 'N/A')
                # Extract the product URL and ensure it's properly formatted
                product_url = product.get('product_page_url', product.get('link', '#'))
                if not product_url.startswith('http'):
                    product_url = f"https://www.walmart.com{product_url}"
                price = product.get('primary_offer', {}).get('offer_price', 'N/A')
                
                suggestion = f"""
Category: {category}

1. **{product_name}** - <a href="{product_url}" target="_blank">Buy Here</a>  
   - Price: ${price}  
   - Store: Walmart
"""
                suggestions.append(suggestion)
            else:
                suggestion = f"""
Category: {category}
No valid products found
"""
                suggestions.append(suggestion)
        
        return "\n".join(suggestions)

def analyze_personality(responses):
    """
    Analyze quiz responses and suggest product categories
    
    Args:
        responses (Dict): Quiz responses
        
    Returns:
        List[str]: List of suggested product categories
    """
    prompt = f"""
    Given these personality traits: {responses},
    suggest 3 relevant product keywords that would return good results on Walmart.

    - Use real, purchasable products.
    - Avoid vague terms like "cool stuff."
    - Provide specific and broad keywords (e.g., "smartwatch", "camping gear", "scented candles").

    Output format: ["Keyword1", "Keyword2", "Keyword3"]
    """

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    categories = response.choices[0].message.content

    try:
        categories = eval(categories)
    except:
        st.error("Error converting response to list. Please try again.")
        return []

    return categories

def get_quiz_responses():
    """Display quiz interface and collect responses"""
    st.title("AI-Powered Gift Recommender ")
    st.write("Answer these questions to get Walmart gift suggestions!")

    responses = {}

    responses['ideal_date'] = st.selectbox(
        "What's your ideal first date?", 
        ["Dinner and a movie", "Outdoor adventure", "Coffee and deep conversation", "Fun activity like bowling or mini-golf"],
        key="quiz_ideal_date"
    )
    
    responses['love_language'] = st.selectbox(
        "What's your love language?", 
        ["Words of Affirmation", "Acts of Service", "Receiving Gifts", "Quality Time", "Physical Touch"],
        key="quiz_love_language"
    )
    
    responses['communication_style'] = st.radio(
        "How do you prefer to communicate in a relationship?", 
        ["Frequent texts and calls", "Quality time in person", "Thoughtful gestures", "Give each other space"],
        key="quiz_communication_style"
    )

    responses['hobbies'] = st.text_area("What are your favorite hobbies and interests?", key="quiz_hobbies")

    responses['gift_preference'] = st.radio(
        "Do you prefer sentimental or practical gifts?", 
        ["Sentimental", "Practical", "A mix of both", "Depends on the occasion"],
        key="quiz_gift_preference"
    )

    if st.button("Submit Responses"):
        st.success("Thank you for completing the quiz! ")
        st.session_state['responses'] = responses
        st.session_state['categories'] = analyze_personality(responses)
        st.session_state['fetch_new_products'] = True
        st.rerun()

def get_gift_suggestions(walmart_api: WalmartAPI):
    """Fetch and display gift suggestions using Walmart API"""
    if 'categories' not in st.session_state or not st.session_state['categories']:
        return

    categories = st.session_state['categories']
    st.subheader(" Suggested Gift Categories")
    for category in categories:
        st.write(f" **{category}**")

    if 'fetch_new_products' in st.session_state and st.session_state['fetch_new_products']:
        with st.spinner("Fetching products from Walmart..."):
            suggestions = walmart_api.get_product_suggestions(categories)
            st.session_state['gift_suggestions'] = suggestions
            st.session_state['fetch_new_products'] = False
        st.rerun()

    if 'gift_suggestions' in st.session_state:
        st.subheader("Walmart Gift Suggestions")
        st.markdown(st.session_state['gift_suggestions'], unsafe_allow_html=True)

        feedback = st.selectbox(
            "Are you satisfied with these suggestions?",
            ["Select an option", "Yes", "No"],
            key="feedback"
        )

        if feedback == "Yes":
            # Clear everything and restart
            st.session_state.clear()
            st.rerun()
        elif feedback == "No":
            # Keep categories but clear suggestions and fetch new ones
            saved_categories = st.session_state['categories']
            st.session_state.clear()
            st.session_state['categories'] = saved_categories
            st.session_state['fetch_new_products'] = True
            st.rerun()

def main():
    # Initialize Walmart API with SerpApi key
    API_KEY = "38c3dcd13eb74956768ba45be7f362a23398fa9d55ead4fd639d4573bd4e39e5"
    walmart_api = WalmartAPI(API_KEY)
    
    get_quiz_responses()
    get_gift_suggestions(walmart_api)

if __name__ == "__main__":
    main()