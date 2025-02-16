import streamlit as st
import openai
from serpapi import GoogleSearch
from typing import Dict, List, Optional

class GiftRecommender:
    """Generates gift suggestions using Walmart's product catalog."""

    def __init__(self):
        # Initialize with SerpApi key for Walmart API
        self.api_key = "38c3dcd13eb74956768ba45be7f362a23398fa9d55ead4fd639d4573bd4e39e5"

    def analyze_personality(self, quiz_data: Dict) -> List[str]:
        """Analyze quiz responses and suggest product categories."""
        prompt = f"""
        You are a romantic gift curator specializing in Valentine's Day presents. Based on these personality traits from the quiz: {quiz_data},
        suggest 3 thoughtful, romantic product categories that would make perfect Valentine's Day gifts.


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
           - Tailor to the partner's personality traits from the quiz: {quiz_data}
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
        
        Output format: ["Category1", "Category2", "Category3"]
        Each category should be specific and romantically oriented.
        """

        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a romantic gift curator who specializes in transforming personal interests into thoughtful, romantic Valentine's Day gifts."},
                {"role": "user", "content": prompt}
            ]
        )

        try:
            categories = eval(response.choices[0].message.content)
            return categories
        except:
            st.error("Error processing gift categories. Please try again.")
            return []

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
        """Get gift suggestions based on quiz responses."""
        try:
            # Get product categories based on personality
            categories = self.analyze_personality(quiz_data)
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
        """Displays gift recommendations based on the stored quiz responses."""
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
                feedback = st.selectbox(
                    "Are you satisfied with these suggestions?",
                    ["Select an option", "Yes", "No"],
                    key="feedback"
                )

                if feedback == "Yes":
                    st.session_state.clear()
                    st.rerun()
                elif feedback == "No":
                    # Keep quiz data but get new suggestions
                    quiz_responses = st.session_state.get("responses", {})
                    st.session_state.clear()
                    st.session_state["responses"] = quiz_responses
                    st.session_state["quiz_submitted"] = True
                    st.rerun()
