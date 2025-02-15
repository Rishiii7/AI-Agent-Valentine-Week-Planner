import streamlit as st
from agno.agent import Agent
from agno.models.openai import OpenAIChat

class GiftRecommender:
    """Generates gift suggestions based on stored quiz responses."""

    def __init__(self):
        self.agent = self.intialize_agent()
    
    def intialize_agent(self):
        return Agent(
            model=OpenAIChat(id="gpt-4o"),
            instructions=[
                f"""
                Based on the following dating personality traits, suggest 3 product categories that would make the best gifts.

                I have the following list of dating personality traits:
                Ideal Date type, Love Language, Communication Style, Hobbies,  Gift Preference

                **Your Task:**  
                For each category, find **exactly one relevant product** from Amazon that match the following strict criteria:

                1. **Relevance:** The product must clearly align with the specified personality traits.  
                2. **Availability:** The product must be in stock and available for immediate purchase.  
                3. **Link Validity:** Provide a verified, functional, and directly accessible product link. Ensure the link leads to the correct product and does not redirect to unrelated pages.  
                4. **Product Quality:** Prioritize products with high ratings (4 stars or above) and multiple verified customer reviews to ensure quality.  
                5. **Category Adherence:** Do not deviate from the listed personality traits or add additional products beyond the specified one per category.  

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
            ]
        )

    def get_gift_suggestions(self, quiz_data):
        try:
            response = self.agent.run(f"Suggest 3 Amazon product categories that would make the best gifts based on: {quiz_data}")
            return response.content.strip() if hasattr(response, "content") else "No suggestions available."
        except Exception as e:
            st.error(f"Error generating gift suggestions: {e}")
            return None

    def render(self, quiz_data):
        """Displays gift recommendations based on the stored quiz responses."""
        st.subheader("🎁 Your Personalized Gift Suggestions")
        
        if not st.session_state.get("quiz_submitted"):
            st.warning("Complete the quiz to get personalized gift suggestions!")
            return

        # Generate and display gift suggestions
        with st.spinner("Generating gift suggestions..."):
            suggestions = self.get_gift_suggestions(quiz_data)
            if suggestions:
                st.session_state["gift_suggestions"] = suggestions
                st.markdown(suggestions)
