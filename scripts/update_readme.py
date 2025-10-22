#!/usr/bin/env python3
"""
Auto-update script for awesome-robotScientist README.md

This script updates the README.md file with:
- Latest news and developments
- Recent papers from arXiv
- Last updated timestamp
"""

import re
import requests
from datetime import datetime
from typing import List, Dict
import arxiv

def fetch_arxiv_papers(max_results: int = 5) -> List[Dict[str, str]]:
    """
    Fetch recent papers from arXiv related to robot scientists and self-driving labs.
    
    Args:
        max_results: Maximum number of papers to fetch
        
    Returns:
        List of paper dictionaries with title, url, published date, and authors
    """
    search_queries = [
        "self-driving lab OR autonomous laboratory",
        "robot scientist OR laboratory automation",
        "AI for science discovery"
    ]
    
    papers = []
    
    for query in search_queries:
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            for result in search.results():
                paper = {
                    'title': result.title,
                    'url': result.entry_id,
                    'published': result.published.strftime('%Y-%m'),
                    'authors': ', '.join([author.name for author in result.authors[:3]]),
                    'summary': result.summary[:200] + '...' if len(result.summary) > 200 else result.summary
                }
                papers.append(paper)
                if len(papers) >= max_results:
                    break
        except Exception as e:
            print(f"Error fetching papers for query '{query}': {e}")
            continue
        
        if len(papers) >= max_results:
            break
    
    # Remove duplicates based on title
    seen = set()
    unique_papers = []
    for paper in papers:
        if paper['title'] not in seen:
            seen.add(paper['title'])
            unique_papers.append(paper)
    
    return unique_papers[:max_results]


def fetch_recent_news() -> List[Dict[str, str]]:
    """
    Generate recent news items (placeholder for actual news aggregation).
    
    Returns:
        List of news item dictionaries
    """
    # This is a placeholder. In a real implementation, you could:
    # - Scrape news websites
    # - Use news APIs
    # - Monitor specific RSS feeds
    # - Track GitHub repositories for releases
    
    current_date = datetime.now()
    current_month = current_date.strftime('%Y-%m')
    
    news_items = [
        {
            'date': current_month,
            'title': 'Advances in self-driving labs and autonomous research continue'
        },
        {
            'date': current_month,
            'title': 'New AI models for scientific hypothesis generation and testing'
        },
        {
            'date': current_month,
            'title': 'Integration of robotics and machine learning in laboratory automation'
        }
    ]
    
    return news_items


def update_readme_section(content: str, section_start: str, section_end: str, new_content: str) -> str:
    """
    Update a specific section in the README content.
    
    Args:
        content: Full README content
        section_start: Start marker for the section
        section_end: End marker for the section
        new_content: New content to insert between markers
        
    Returns:
        Updated README content
    """
    pattern = f"({re.escape(section_start)})(.*?)({re.escape(section_end)})"
    replacement = f"\\1\n{new_content}\n\\3"
    
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    return updated_content


def format_news_items(news_items: List[Dict[str, str]]) -> str:
    """Format news items for README."""
    formatted = []
    for item in news_items:
        formatted.append(f"- **{item['date']}**: {item['title']}")
    return '\n'.join(formatted)


def format_papers(papers: List[Dict[str, str]]) -> str:
    """Format papers for README."""
    formatted = []
    for paper in papers:
        formatted.append(
            f"- **[{paper['title']}]({paper['url']})** ({paper['published']})\n"
            f"  - {paper['authors']}\n"
            f"  - {paper['summary']}"
        )
    return '\n\n'.join(formatted)


def update_timestamp(content: str) -> str:
    """Update the last updated timestamp in the README."""
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Update the timestamp at the bottom
    pattern = r"\*\*Last Updated\*\*:.*"
    replacement = f"**Last Updated**: {current_date} (Auto-updated weekly via GitHub Actions)"
    
    updated_content = re.sub(pattern, replacement, content)
    
    return updated_content


def main():
    """Main function to update README.md"""
    readme_path = 'README.md'
    
    print("Starting README update...")
    
    # Read current README
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {readme_path} not found")
        return
    
    # Fetch new content
    print("Fetching news items...")
    news_items = fetch_recent_news()
    
    print("Fetching recent papers from arXiv...")
    papers = fetch_arxiv_papers(max_results=5)
    
    # Update news section
    if news_items:
        print(f"Updating news section with {len(news_items)} items...")
        news_content = format_news_items(news_items)
        content = update_readme_section(
            content,
            "<!-- AUTO-GENERATED:NEWS:START -->",
            "<!-- AUTO-GENERATED:NEWS:END -->",
            news_content
        )
    
    # Update papers section
    if papers:
        print(f"Updating papers section with {len(papers)} papers...")
        papers_content = format_papers(papers)
        content = update_readme_section(
            content,
            "<!-- AUTO-GENERATED:PAPERS:START -->",
            "<!-- AUTO-GENERATED:PAPERS:END -->",
            papers_content
        )
    
    # Update timestamp
    print("Updating timestamp...")
    content = update_timestamp(content)
    
    # Write updated README
    try:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("README.md updated successfully!")
    except Exception as e:
        print(f"Error writing to {readme_path}: {e}")


if __name__ == '__main__':
    main()
