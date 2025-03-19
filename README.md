# प्रथम Times - AI-Powered Tech News Website

A Django-based tech news website that automatically generates and displays technology news articles using AI (Ollama LLM).

## Features

- Automated news generation every day at 3 AM
- Three distinct news categories:
  - Innovation and AI 
  - Tech Industry News
  - Future Tech Trends
- Beautiful newspaper-style layout
- Fallback content system for reliability
- Comprehensive logging system

## Tech Stack

- Django 5.0.2
- Python 3.x
- Ollama LLM API
- APScheduler for automated tasks

## Setup

1. Clone the repository:
```bash
git clone https://github.com/hipratham/Technews.git
cd Technews
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to view the website.

## Configuration

- News articles are automatically generated at 3 AM daily
- Logs are stored in technews.log
- Make sure Ollama API is running locally on port 11434

## Contributing

Feel free to open issues and pull requests!
