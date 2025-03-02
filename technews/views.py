from django.shortcuts import render
from .models import TechNews
import requests
import os
from datetime import datetime
import logging

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
    
    OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
    
    for topic in topics:
        try:
            logger.info(f"Generating news for category: {topic['category']}")
            
            response = requests.post(
                OLLAMA_ENDPOINT,
                json={
                    "model": "llama2",
                    "prompt": topic['prompt'],
                    "stream": False,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            )
            
            if response.status_code == 200:
                generated_text = response.json().get('response', '')
                lines = generated_text.split('\n')
                title = lines[0].replace('Title:', '').strip()
                content = '\n\n'.join(line for line in lines[2:] if line.strip())
                
                TechNews.objects.create(
                    title=title,
                    content=content,
                    category=topic['category']
                )
                logger.info(f"Successfully generated news for {topic['category']}")
            else:
                logger.error(f"Error from Ollama API: {response.status_code}")
                _create_fallback_article(topic['category'])
                
        except Exception as e:
            logger.error(f"Error generating news for {topic['category']}: {str(e)}")
            _create_fallback_article(topic['category'])

def _create_fallback_article(category):
    """Create a fallback article if LLM generation fails."""
    fallback_content = {
        'AI & Innovation': {
            'title': "AI Breakthrough: Neural Networks Show Human-Like Learning",
            'content': """Researchers have unveiled a groundbreaking neural network architecture that demonstrates unprecedented learning capabilities. The new system shows remarkable ability to adapt and learn from minimal data, similar to human cognitive processes.

The technical innovation lies in a novel approach to neural network design, incorporating principles from neuroscience and cognitive psychology. This hybrid approach has resulted in significantly improved performance across various learning tasks.

Industry experts are already exploring applications in autonomous systems, healthcare diagnostics, and educational technology. Several major tech companies have expressed interest in implementing this technology in their products.

"This represents a significant step forward in our understanding of artificial intelligence," notes Dr. Sarah Chen, lead researcher at the AI Institute. "The system's ability to learn and adapt with minimal training data could revolutionize how we approach AI development."

The implications for various industries are substantial, with potential applications ranging from personalized medicine to adaptive educational systems. Early testing shows promising results in real-world applications."""
        },
        'Tech Industry News': {
            'title': "Major Tech Companies Announce Groundbreaking Collaboration",
            'content': """In a significant development for the technology sector, leading tech giants have announced a collaborative initiative aimed at addressing key industry challenges. The partnership, valued at several billion dollars, focuses on developing shared infrastructure for emerging technologies.

Market analysts project substantial industry-wide impacts from this collaboration. Early estimates suggest the initiative could generate over $50 billion in economic value over the next five years.

The collaboration introduces innovative approaches to long-standing technical challenges, particularly in areas of data security and system interoperability. Industry experts praise the initiative's potential to accelerate technological advancement.

Several major organizations have already committed to adopting the new framework, with implementation plans starting in the coming months. "The response from the industry has been overwhelmingly positive," notes industry analyst Maria Rodriguez.

The global implications of this collaboration are expected to reshape how companies approach technology development and implementation. Regional adaptations are already being planned to ensure worldwide compatibility."""
        },
        'Future Tech Trends': {
            'title': "Emerging Technologies Set to Transform Industries by 2025",
            'content': """A comprehensive analysis of emerging technology trends reveals transformative changes expected to reshape multiple industries within the next year. Experts predict significant advances in quantum computing, biotechnology, and sustainable energy solutions.

Research institutions worldwide report breakthrough developments in quantum computing stability and error correction. These advances are expected to accelerate the practical implementation of quantum systems in various industries.

The biotechnology sector shows particular promise, with new tools for genetic research and personalized medicine leading the way. Industry experts predict these advances will revolutionize healthcare delivery and treatment approaches.

"We're entering a new era of technological capability," explains Dr. James Martinez, technology forecaster. "The convergence of multiple emerging technologies is creating unprecedented opportunities for innovation."

Timeline projections suggest rapid adoption of these technologies across industries, with initial implementations expected within the next 6-12 months. Market analysts predict substantial economic impacts as these technologies mature."""
        }
    }
    
    content = fallback_content.get(category)
    if content:
        TechNews.objects.create(
            title=content['title'],
            content=content['content'],
            category=category
        )
        logger.info(f"Created fallback article for {category}")
    else:
        logger.error(f"No fallback content available for category: {category}")
