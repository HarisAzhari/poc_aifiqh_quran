from flask import Flask, request, Response, stream_with_context, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
from google.genai.types import Tool, GoogleSearch
import os
from datetime import datetime
import pytz


class Config:
    """Configuration class for the application"""
    GEMINI_API_KEY = "AIzaSyAX9VE23i84xK20B5RlTi80wR1VxrLuoZ4"
    MODEL = "gemini-2.0-flash-exp"

def get_malaysia_time():
    """Get current time in Malaysia timezone"""
    malaysia_tz = pytz.timezone('Asia/Kuala_Lumpur')
    return datetime.now(malaysia_tz)

def get_malaysia_time_str():
    """Get formatted Malaysia time string"""
    return get_malaysia_time().strftime('%Y-%m-%d %H:%M:%S %Z')

def get_general_response(query):
    """Handle general queries using Google Search"""
    try:
        print(f"🔍 Performing Google Search for: {query}")
        
        search_client = genai.Client(api_key=Config.GEMINI_API_KEY)
        google_search_tool = Tool(google_search=GoogleSearch())
        search_config = types.GenerateContentConfig(
            tools=[google_search_tool],
            response_modalities=["TEXT"],
            temperature=0.3,
            max_output_tokens=8000
        )
        
        response = search_client.models.generate_content(
            model=Config.MODEL,
            contents=query,
            config=search_config,
        )
        
        return {
            "success": True,
            "response": response.text,
            "query": query,
            "search_enhanced": True
        }
        
    except Exception as e:
        print(f"❌ Google Search Error: {str(e)}")
        return {
            "success": False,
            "error": f"Search failed: {str(e)}",
            "query": query
        }

def get_quran_response(query):
    """Handle Quran-related queries using specialized search on quran.com with detailed Islamic guidance"""
    try:
        print(f"📖 Performing Quran search for: {query}")
        
        # Enhance query to specifically search quran.com and request comprehensive Islamic response
        enhanced_query = f"""
        Search site:quran.com for information about: {query}
        
        Provide Islamic response with:
        - Arabic verse first, then English translation
        - Quran.com URL links
        - Brief explanation from Islamic perspective
        
        Format: **Arabic:** [text] **Translation:** [text] **Link:** [quran.com URL]
        """
        
        search_client = genai.Client(api_key=Config.GEMINI_API_KEY)
        google_search_tool = Tool(google_search=GoogleSearch())
        search_config = types.GenerateContentConfig(
            tools=[google_search_tool],
            response_modalities=["TEXT"],
            temperature=0.2,  # Lower temperature for more focused religious content
            max_output_tokens=8000
        )
        
        response = search_client.models.generate_content(
            model=Config.MODEL,
            contents=enhanced_query,
            config=search_config,
        )
        
        # Format the response to ensure it includes required elements
        formatted_response = f"🕌 **Islamic Guidance on: {query}**\n\n"
        formatted_response += response.text
        formatted_response += f"\n\n📚 **Source**: Quran.com search results"
        formatted_response += f"\n🔗 **For more details, visit**: https://quran.com"
        
        return {
            "success": True,
            "response": formatted_response,
            "query": query,
            "search_source": "quran.com",
            "search_enhanced": True,
            "content_type": "Islamic/Quranic guidance",
            "note": "Comprehensive Islamic response with Quranic verses, reasoning, and links to quran.com"
        }
        
    except Exception as e:
        print(f"❌ Quran Search Error: {str(e)}")
        return {
            "success": False,
            "error": f"Quran search failed: {str(e)}",
            "query": query,
            "search_source": "quran.com"
        }

def get_function_tools():
    """Get all available function tools for Gemini"""
    
    # General search function
    general_response_function = {
        "name": "get_general_response",
        "description": f"This function is used to get a general response to a question or any topic using Google Search. It provides current, up-to-date information from the web. Use this for general knowledge, current events, technology questions, or any non-Islamic topics. Today's date is {get_malaysia_time_str()}.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "query": {
                    "type": "STRING",
                    "description": "The question or topic to search for using Google Search"
                }
            },
            "required": ["query"]
        }
    }
    
    # Quran search function
    quran_response_function = {
        "name": "get_quran_response",
        "description": f"Handle Quran-related queries using specialized search on quran.com. This function provides comprehensive Islamic guidance with Quranic verses, reasoning, proper citations, and links to quran.com. Use this ONLY when users ask about Islam, Quran, Islamic teachings, Sunnah, Islamic guidance, religious questions, Islamic law, Islamic ethics, Islamic history, Prophet Muhammad (PBUH), Islamic practices (prayer, fasting, hajj, zakat), Islamic beliefs, or anything related to Islamic knowledge. This will search specifically on quran.com and provide verses with proper Surah:Ayah citations, interpretations, and direct links. Today's date is {get_malaysia_time_str()}.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "query": {
                    "type": "STRING",
                    "description": "The Islamic/Quranic question or topic to search for (e.g., 'What does Quran say about patience?', 'Islamic guidance on charity', 'Ayat about forgiveness', 'Prayer in Islam', 'Islamic concept of justice')"
                }
            },
            "required": ["query"]
        }
    }
    
    return [general_response_function, quran_response_function]

def get_function_config():
    """Get the function calling configuration for Gemini"""
    function_tools = get_function_tools()
    tools = types.Tool(function_declarations=function_tools)
    config = types.GenerateContentConfig(
        tools=[tools],
        temperature=0.3,
        max_output_tokens=8000
    )
    return config

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    CORS(app)

    # Initialize Gemini client
    client = genai.Client(api_key=Config.GEMINI_API_KEY)

    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'timestamp': get_malaysia_time_str(),
            'service': 'AI Assistant with Islamic Knowledge'
        })

    @app.route('/generate', methods=['POST'])
    def generate():
        """Main generation endpoint with intelligent function calling"""
        data = request.json
        question = data.get('question', '')
        chat_history = data.get('chat_history', [])
        
        # Limit chat history to latest 10 messages
        if len(chat_history) > 10:
            chat_history = chat_history[-10:]
        
        def generate_response():
            try:
                # Build conversation context
                conversation_context = ""
                if chat_history:
                    conversation_context = "\n\nPrevious conversation context:\n"
                    for chat in chat_history:
                        role = chat.get('role', 'UNKNOWN')
                        message = chat.get('message', '')
                        conversation_context += f"{role}: {message}\n"
                    conversation_context += "\n"
                
                # Create the main prompt with intelligent routing instructions
                main_prompt = f"""
You are a helpful AI assistant with specialized knowledge capabilities.

📅 Today's Date: {get_malaysia_time_str()}
📅 Current Time: {get_malaysia_time().strftime('%H:%M:%S %Z')}

{conversation_context}

IMPORTANT FUNCTION CALLING RULES:

🔍 **For GENERAL topics** (technology, science, current events, general knowledge, non-religious topics):
- Use the "get_general_response" function to get up-to-date information from Google Search
- This includes: news, weather, technology updates, general facts, non-Islamic topics

📖 **For ISLAMIC/RELIGIOUS topics** (Islam, Quran, Islamic teachings, religious guidance):
- Use the "get_quran_response" function to get specialized Islamic guidance from quran.com
- This includes: Quranic verses, Islamic teachings, Sunnah, Islamic law, religious practices, Islamic ethics, Prophet Muhammad (PBUH), prayer, fasting, hajj, zakat, Islamic beliefs, Islamic history

🗣️ **For SIMPLE conversations** (greetings, personal questions, casual chat):
- Respond directly without using any functions
- Keep it natural and conversational

CONVERSATION STYLE:
- Be warm, helpful, and respectful
- Use light-hearted tone when appropriate 😊
- For Islamic topics, maintain reverence and respect
- Provide clear, well-formatted responses
- Use emojis tastefully to enhance readability

FORMATTING RULES:
- Use proper markdown formatting: **bold**, *italic*, `code`
- Use headers (#, ##), bullet points (-), and tables when helpful
- Add blank lines between sections for readability
- Use emojis to make responses more engaging

CRITICAL: Analyze the user's question carefully and determine if it's:
1. Islamic/Religious → use get_quran_response
2. General knowledge/search needed → use get_general_response  
3. Simple conversation → respond directly

User Question: {question}
"""
                
                # Get function tools and config
                function_config = get_function_config()
                
                # First, get the response with potential function calls
                response = client.models.generate_content(
                    model=Config.MODEL,
                    contents=main_prompt,
                    config=function_config
                )
                
                # Check for function calls
                function_calls_made = []
                function_results = []
                
                if hasattr(response, 'candidates') and response.candidates:
                    for candidate in response.candidates:
                        if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                            for part in candidate.content.parts:
                                if hasattr(part, 'function_call') and part.function_call:
                                    function_call = part.function_call
                                    function_calls_made.append(function_call)
                                    
                                    # Execute function calls
                                    if function_call.name == "get_general_response":
                                        yield "🔍 Searching for current information...\n\n"
                                        result = get_general_response(**function_call.args)
                                        function_results.append({
                                            "name": function_call.name,
                                            "result": result
                                        })
                                        
                                    elif function_call.name == "get_quran_response":
                                        yield "📖 Searching for Islamic guidance from Quran...\n\n"
                                        result = get_quran_response(**function_call.args)
                                        function_results.append({
                                            "name": function_call.name,
                                            "result": result
                                        })
                
                # Generate final response
                if function_calls_made:
                    yield "💭 Processing information and generating response...\n\n"
                    
                    # Include function results in final prompt
                    results_text = ""
                    for func_result in function_results:
                        results_text += f"\n\nFunction {func_result['name']} returned:\n{str(func_result['result'])}"
                    
                    final_prompt = main_prompt + results_text + "\n\nNow provide your comprehensive, well-formatted response based on the above data. Be warm, helpful, and use appropriate emojis!"
                    
                    # Stream final response
                    final_response_stream = client.models.generate_content_stream(
                        model=Config.MODEL,
                        contents=final_prompt,
                        config=types.GenerateContentConfig(
                            temperature=0.3,
                            max_output_tokens=8000
                        )
                    )
                    
                    # Stream the final response
                    for chunk in final_response_stream:
                        try:
                            if hasattr(chunk, 'text') and chunk.text:
                                yield chunk.text
                            elif hasattr(chunk, 'parts') and chunk.parts:
                                for part in chunk.parts:
                                    if hasattr(part, 'text') and part.text:
                                        yield part.text
                        except Exception as inner_e:
                            yield f"Chunk error: {str(inner_e)}"
                else:
                    # No function calls, stream original response
                    if hasattr(response, 'text'):
                        yield response.text
                    elif hasattr(response, 'parts'):
                        for part in response.parts:
                            if hasattr(part, 'text'):
                                yield part.text
                
                yield "\n\n✨ [Response Complete]"
                
            except Exception as e:
                yield f"❌ Error: {str(e)}"
        
        return Response(stream_with_context(generate_response()), mimetype='text/plain')

    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Starting AI Assistant with Islamic Knowledge...")
    print(f"🕒 Current time: {get_malaysia_time_str()}")
    print("📖 Islamic queries will be routed to Quran.com search")
    print("🔍 General queries will use Google Search")
    print("💬 Ready for conversations!")
    app.run(debug=True, host='0.0.0.0', port=4040)
