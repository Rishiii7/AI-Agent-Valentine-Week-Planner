# AI-Agent Valentine Week Planner 🎁💝

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red.svg)](https://streamlit.io/)
[![Agno](https://img.shields.io/badge/Agno-AI%20Agent-purple.svg)](https://agno.ai/)

## 🌟 Project Overview

The AI-Agent Valentine Week Planner is a sophisticated AI-powered application that creates the perfect Valentine's experience using multiple specialized AI agents built with the Agno Framework. The system combines a Gift Recommender Agent and a Day Planner Agent, to analyze personality traits, recommend personalized gifts, and plan the perfect Valentine's date - all while seamlessly integrating with Google Calendar for scheduling.

## 🚀 Key Features

- **Dual AI Agent System**: 
  - Gift Recommender Agent: Analyzes personality traits using GPT-4o and suggests perfect gifts
  - Day Planner Agent: Creates personalized date plans based on personality analysis
- **Deep Personality Analysis**: Leverages GPT-4o to analyze love languages, MBTI, hobbies, and preferences
- **Smart Gift Matching**: Connects personality insights with Walmart's product catalog via SerpAPI
- **Intelligent Date Planning**: 
  - Suggests optimal date venues and activities based on personality traits
  - Recommends perfect timing and duration
  - Automatically syncs with Google Calendar
- **Interactive Experience**: Streamlit-based interface for seamless user interaction

## 🛠️ Technical Stack

- **Backend**: Python
- **AI/ML**: OpenAI GPT-4o, Agno AI Agent Framework
- **Frontend**: Streamlit
- **APIs**: 
  - OpenAI API for personality analysis
  - SerpAPI for Walmart product integration
  - Google Calendar API for event planning
- **Architecture**: Object-Oriented Design with modular components

## 💡 Implementation Highlights

- **Advanced AI Agent Architecture**:
  1. Personality Analysis Phase:
     - GPT-4o powered agent processes user quiz responses
     - Analyzes love languages, MBTI, hobbies, and preferences
     - Generates personality traits
  
  2. Gift Recommendation Phase:
     - Agent translates personality traits into gift categories
     - Queries Walmart's catalog via SerpAPI
     - Filters products based on personality match
  
  3. Date Planning Phase:
     - Agent uses personality insights to craft perfect date plan
     - Suggests venue, activities, and timing
     - Generates personalized date itinerary
  
  4. Calendar Integration:
     - Automatically syncs date plans with Google Calendar
     - Sends reminders and event details

- **Clean Architecture**: Modular design with clear separation of concerns
- **Type Safety**: Extensive use of Python type hints for better code reliability
- **API Abstraction**: Well-designed class interfaces for external API interactions
- **Error Handling**: Robust error management for API calls and user inputs
- **Environment Management**: Secure handling of API keys using environment variables

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/Rishiii7/AI-Agent-Valentine-Week-Planner.git

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your API keys to .env file

# Run the application
streamlit run main.py
```

## 🎯 Future Enhancements

- Integration with additional e-commerce platforms
- Advanced calendar integration for special occasion reminders
- Mobile application development

---

*Built with ❤️ for the AGI House 'The Romantic Hacker' Hackathon!