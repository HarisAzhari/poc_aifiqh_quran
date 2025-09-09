# 🤖 AI Assistant with Intelligent Islamic Knowledge Routing

An intelligent AI assistant powered by Google's Gemini AI that can automatically detect and route questions to the appropriate knowledge source:

- **📖 Islamic/Quran Questions** → Specialized search on Quran.com 
- **🔍 General Questions** → Google Search for current information
- **💬 Casual Conversation** → Direct AI responses

## ✨ Features

### 🧠 Intelligent Query Routing
The system automatically analyzes incoming questions and determines:
1. **Islamic Topics**: Triggers `get_quran_response()` for Islamic guidance with Quranic verses
2. **General Topics**: Triggers `get_general_response()` for current information via Google Search  
3. **Simple Chat**: Responds directly for casual conversation

### 📖 Islamic Knowledge Capabilities
- Searches specifically on **quran.com** for authentic Islamic content
- Provides comprehensive responses with:
  - 🕌 Quranic verses with proper Surah:Ayah citations
  - 📚 Islamic reasoning and explanations
  - 🔗 Direct links to quran.com pages
  - 🎓 Scholarly interpretations and context

### 🔍 General Knowledge Capabilities  
- Uses **Google Search** for up-to-date information
- Covers current events, technology, science, and general knowledge
- Real-time information access

### 💬 Natural Conversation
- Warm, respectful, and engaging communication style
- Light-hearted tone with appropriate emojis 😊
- Well-formatted markdown responses
- Maintains conversation context

## 🚀 Quick Start

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### API Usage
```bash
# Health check
curl http://localhost:5000/health

# Ask a general question
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"question": "What is artificial intelligence?"}'

# Ask an Islamic question  
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"question": "What does the Quran say about patience?"}'

# Casual conversation
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello, how are you?"}'
```

## 🎯 How It Works

### 1. Question Analysis
The AI analyzes each question to determine its category:

```python
# Islamic questions trigger get_quran_response()
"What does Quran say about charity?" → 📖 Islamic Knowledge
"Prayer times in Islam" → 📖 Islamic Knowledge  
"Islamic concept of justice" → 📖 Islamic Knowledge

# General questions trigger get_general_response()
"Latest news about AI" → 🔍 Google Search
"Weather in Kuala Lumpur" → 🔍 Google Search
"How does blockchain work?" → 🔍 Google Search

# Simple conversations get direct responses
"Hello!" → 💬 Direct Response
"How are you?" → 💬 Direct Response
"Thank you" → 💬 Direct Response
```

### 2. Function Execution
Based on the analysis, the appropriate function is called:

#### Islamic Function (`get_quran_response`)
- Searches `site:quran.com` for the query
- Returns comprehensive Islamic guidance
- Includes Quranic verses with proper citations
- Provides context and scholarly interpretation

#### General Function (`get_general_response`)  
- Uses Google Search for current information
- Returns up-to-date, relevant information
- Covers technology, news, science, etc.

#### Direct Response
- No function calls needed
- Natural conversational responses
- Maintains warm, engaging tone

### 3. Response Generation
The system generates well-formatted responses with:
- **Markdown formatting** for readability
- **Emojis** for visual appeal
- **Clear structure** with headers and bullet points
- **Respectful tone** appropriate for the content type

## 🛠️ Configuration

### API Configuration
The system uses Google's Gemini AI API:
```python
class Config:
    GEMINI_API_KEY = "AIzaSyAX9VE23i84xK20B5RlTi80wR1VxrLuoZ4"
    MODEL = "gemini-2.0-flash-exp"
```

### Function Tools
Two main functions are available:

1. **get_general_response**: For general knowledge and current information
2. **get_quran_response**: For Islamic knowledge and Quranic guidance

## 📝 Example Interactions

### Islamic Question
**Input**: "What does Islam say about helping others?"
**Output**: 
```
📖 Searching for Islamic guidance from Quran...

🕌 **Islamic Guidance on: What does Islam say about helping others?**

[Detailed response with Quranic verses, citations, and Islamic reasoning]

📚 **Source**: Quran.com search results
🔗 **For more details, visit**: https://quran.com
```

### General Question  
**Input**: "What's the latest in AI technology?"
**Output**:
```
🔍 Searching for current information...

[Up-to-date information about AI technology from Google Search]
```

### Casual Conversation
**Input**: "Hello, how are you today?"
**Output**: 
```
Hello there! 😊 I'm doing wonderfully, thank you for asking! I'm here and ready to help you with anything you need - whether it's Islamic knowledge, general questions, or just a friendly chat. How are you doing today? Is there anything specific I can assist you with? ✨
```

## 🌟 Key Benefits

1. **🎯 Intelligent Routing**: Automatically determines the best knowledge source
2. **📖 Authentic Islamic Content**: Direct access to Quran.com for religious guidance  
3. **🔍 Current Information**: Real-time access to Google Search for general topics
4. **💬 Natural Conversation**: Warm, engaging communication style
5. **🎨 Beautiful Formatting**: Well-structured, readable responses with emojis
6. **🔄 Streaming Responses**: Real-time response generation with progress indicators

## 📚 Technical Details

- **Framework**: Flask with CORS support
- **AI Model**: Google Gemini 2.0 Flash Exp  
- **Function Calling**: Intelligent routing based on query analysis
- **Search Integration**: Google Search + Quran.com specialized search
- **Response Format**: Streaming JSON responses
- **Time Zone**: Malaysia timezone support

## 🎉 Perfect For

- Islamic education and guidance
- General knowledge inquiries  
- Current events and news
- Technology and science questions
- Casual conversation and chat
- Multi-topic discussions with intelligent routing

This system bridges the gap between general AI knowledge and specialized Islamic expertise, providing users with accurate, respectful, and comprehensive responses regardless of their query type! 🌟 