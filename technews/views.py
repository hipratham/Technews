from django.shortcuts import render
from .models import TechNews
import requests
import os
from datetime import datetime
import logging
import time

logger = logging.getLogger(__name__)

def home(request):
    # Get the three most recent news articles
    news_articles = TechNews.objects.all().order_by('-id')[:3]
    
    # If we don't have 3 articles, generate them
    if len(news_articles) < 3:
        generate_tech_news()
        news_articles = TechNews.objects.all().order_by('-id')[:3]
    
    return render(request, 'technews/home.html', {'news_articles': news_articles})

def generate_tech_news():
    """Generate tech news using Ollama LLM."""
    logger.info("Starting news generation process...")
    
    # Clear existing news
    TechNews.objects.all().delete()
    
    # Define topics for news generation
    topics = [
        {
            'category': 'AI & Innovation',
            'prompt': """You are a technology journalist writing an article about recent AI developments. Write a detailed news article following this format:

Title: [Create an engaging title about recent AI breakthroughs]

[Write 4-5 detailed paragraphs covering:
1. A major recent AI breakthrough or innovation
2. Technical details and methodology
3. Industry impact and real-world applications
4. Expert opinions and future implications

Use specific examples, statistics, and expert quotes. Make it engaging and informative. Focus on factual reporting.]"""
        },
        {
            'category': 'Tech Industry News',
            'prompt': """You are a technology industry analyst writing about recent developments. Write a detailed news article following this format:

Title: [Create an engaging title about tech industry developments]

[Write 4-5 detailed paragraphs covering:
1. Major company announcements or industry trends
2. Market analysis with specific numbers
3. Competition and strategic implications
4. Industry expert insights and future outlook

Include specific data points, market figures, and expert quotes. Keep it factual and analytical.]"""
        },
        {
            'category': 'Future Tech Trends',
            'prompt': """You are a technology futurist writing about emerging trends. Write a detailed news article following this format:

Title: [Create an engaging title about emerging tech trends]

[Write 4-5 detailed paragraphs covering:
1. Emerging technology trends and breakthroughs
2. Research and development progress
3. Potential applications and industry impact
4. Timeline predictions and adoption forecasts

Focus on concrete examples, research findings, and expert insights. Keep it grounded in current developments.]"""
        }
    ]
    
    OLLAMA_ENDPOINT = os.getenv('OLLAMA_ENDPOINT', 'http://localhost:11434/api/generate')
    MAX_RETRIES = 3
    
    for topic in topics:
        retries = 0
        while retries < MAX_RETRIES:
            try:
                logger.info(f"Generating news for category: {topic['category']} (Attempt {retries + 1})")
                
                response = requests.post(
                    OLLAMA_ENDPOINT,
                    json={
                        "model": "llama2",
                        "prompt": topic['prompt'],
                        "stream": False,
                        "temperature": 0.9,
                        "top_p": 0.9
                    }
                )
                
                if response.status_code == 200:
                    generated_text = response.json().get('response', '')
                    lines = generated_text.split('\n')
                    title = lines[0].replace('Title:', '').strip()
                    content = '\n\n'.join(line for line in lines[2:] if line.strip())
                    
                    if title and content:
                        TechNews.objects.create(
                            title=title,
                            content=content,
                            category=topic['category']
                        )
                        logger.info(f"Successfully generated news for {topic['category']}")
                        break
                    else:
                        logger.warning(f"Empty content generated for {topic['category']}, retrying...")
                        retries += 1
                else:
                    logger.error(f"Error from Ollama API: {response.status_code}, retrying...")
                    retries += 1
                
            except Exception as e:
                logger.error(f"Error generating news for {topic['category']}: {str(e)}, retrying...")
                retries += 1
            
            if retries < MAX_RETRIES:
                time.sleep(2)  # Wait 2 seconds before retrying
        
        if retries == MAX_RETRIES:
            logger.error(f"Failed to generate content for {topic['category']} after {MAX_RETRIES} attempts")
            # Generate a new attempt with a different prompt
            try:
                backup_prompt = f"""You are a professional tech journalist. Write a breaking news article about the latest developments in {topic['category']}. 
                Include a title, and make sure to cover recent innovations, market impact, and expert opinions. 
                Be specific and include technical details, statistics, and quotes."""
                
                response = requests.post(
                    OLLAMA_ENDPOINT,
                    json={
                        "model": "llama2",
                        "prompt": backup_prompt,
                        "stream": False,
                        "temperature": 0.9,
                        "top_p": 0.95
                    }
                )
                
                if response.status_code == 200:
                    generated_text = response.json().get('response', '')
                    lines = generated_text.split('\n')
                    title = lines[0].strip()
                    content = '\n\n'.join(line for line in lines[1:] if line.strip())
                    
                    if title and content:
                        TechNews.objects.create(
                            title=title,
                            content=content,
                            category=topic['category']
                        )
                        logger.info(f"Successfully generated news with backup prompt for {topic['category']}")
                
            except Exception as e:
                logger.error(f"Failed to generate content with backup prompt for {topic['category']}: {str(e)}")
