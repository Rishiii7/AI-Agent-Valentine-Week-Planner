import streamlit as st
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from serpapi import GoogleSearch
from typing import Dict, List, Optional

# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class GiftRecommender:
    """Generates gift suggestions using both AI Agent and Walmart's product catalog."""

    def __init__(self):
        self.agent = self.initialize_agent()
        self.api_key = "38c3dcd13eb74956768ba45be7f362a23398fa9d55ead4fd639d4573bd4e39e5"  # SerpApi key for Walmart

    def initialize_agent(self):
        """Initialize the Agno agent for personality analysis and category suggestions."""
        return Agent(
            model=OpenAIChat(id="gpt-4o"),
            instructions=[
                f"""
                You are a gift recommendation expert. Your task is to analyze personality traits
                and suggest the most suitable gift categories.

                Based on the provided personality traits:
                - Ideal Date type
                - Love Language
                - Communication Style
                - Hobbies
                - Gift Preference

                Suggest exactly 3 product categories that would make perfect gifts.
                
                Key Guidelines:
                    1. ROMANTIC FOCUS:
                    - Each suggestion must have a romantic or emotional connection
                    - Transform general interests into romantic gift ideas
                    - Example: If they like outdoors, suggest "Couples Camping Hammock" instead of "Survival Kit"
                    
                    2. VALENTINE'S THEMES:
                    - Incorporate elements of romance, love, or shared experiences
                    - Consider items that create romantic moments or memories
                    - Think about gifts that can be enjoyed together
                    
                    3. PERSONALIZATION RULES:
                    - Tailor to the partner's personality traits from the quiz
                    - Use specific terms (e.g., "Personalized Couple's Star Map" not just "Wall Art")
                    - Consider their love language and gift preferences
                    - Focus on items that combine their interests with romantic elements
                    
                    4. GIFT CATEGORIES TO PRIORITIZE:
                    - Suggest real, purchasable products
                    - Use specific terms (e.g., "wireless earbuds" not "electronics")
                    - Personalized/Custom items that tell your love story
                    - Experience gifts to share together
                    - Romantic versions of their hobbies/interests
                    - Sentimental keepsakes
                    - Luxury/special occasion variants of everyday items they love
                    
                    5. AVOID:
                    - Generic utility items without romantic context
                    - Purely practical gifts without emotional significance
                    - Standard hobby equipment without romantic customization

                Output format must be exactly: ["Category1", "Category2", "Category3"]
                This format is crucial as it will be used for product search.
                """
            ]
        )

    def search_walmart_products(self, query: str) -> Dict:
        """Search for products on Walmart using SerpApi."""
        params = {
            "api_key": self.api_key,
            "engine": "walmart",
            "query": query,
            "sort": "rating_high",
            "page": 1
        }

        search = GoogleSearch(params)
        return search.get_dict()

    def get_gift_suggestions(self, quiz_data: Dict) -> str:
        """Get gift suggestions using both AI Agent and Walmart API."""
        try:
            # Use Agno agent to analyze personality and suggest categories
            response = self.agent.run(f"Based on these traits, suggest gift categories: {quiz_data}")
            if not hasattr(response, "content"):
                return "No suggestions available."
            
            try:
                # Extract categories from agent's response
                categories = eval(response.content.strip())
                if not isinstance(categories, list):
                    raise ValueError("Invalid category format")
            except:
                st.error("Error processing agent's response. Using default categories.")
                categories = ["gift set", "electronics", "accessories"]

            # Use Walmart API to find actual products for each category
            suggestions = []
            for category in categories:
                results = self.search_walmart_products(category)
                
                if "organic_results" in results and results["organic_results"]:
                    product = results["organic_results"][0]  # Get the highest-rated product
                    
                    product_name = product.get('title', 'N/A')
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
            
        except Exception as e:
            st.error(f"Error generating gift suggestions: {e}")
            return None

    def render(self, quiz_data: Dict):
        """Displays gift recommendations based on the quiz responses."""
        st.subheader("🎁 Your Personalized Gift Suggestions")
        
        if not st.session_state.get("quiz_submitted"):
            st.warning("Complete the quiz to get personalized gift suggestions!")
            return

        # Generate and display gift suggestions
        with st.spinner("Finding perfect gifts for you..."):
            suggestions = self.get_gift_suggestions(quiz_data)
            if suggestions:
                st.session_state["gift_suggestions"] = suggestions
                st.markdown(suggestions, unsafe_allow_html=True)

                # Add feedback options
                # feedback = st.selectbox(
                #     "Are you satisfied with these suggestions?",
                #     ["Select an option", "Yes", "No"],
                #     key="feedback"
                # )

                # if feedback == "Yes":
                #     st.session_state.clear()
                #     st.rerun()
                # elif feedback == "No":
                #     # Keep quiz data but get new suggestions
                #     quiz_responses = st.session_state.get("responses", {})
                #     st.session_state.clear()
                #     st.session_state["responses"] = quiz_responses
                #     st.session_state["quiz_submitted"] = True
                #     st.rerun()