# Update Scripts

This directory contains scripts for automating updates to the awesome-robotScientist repository.

## update_readme.py

Python script that automatically updates the README.md file with:

- Latest news and developments in robot science and self-driving labs
- Recent papers from arXiv related to autonomous laboratories
- Current timestamp

### Usage

```bash
python scripts/update_readme.py
```

### Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```

### Auto-update Markers

The script updates content between special markers in README.md:

- `<!-- AUTO-GENERATED:NEWS:START -->` ... `<!-- AUTO-GENERATED:NEWS:END -->` - News section
- `<!-- AUTO-GENERATED:PAPERS:START -->` ... `<!-- AUTO-GENERATED:PAPERS:END -->` - Papers section

### Customization

You can customize the update behavior by modifying:

- `fetch_arxiv_papers()` - Change search queries or number of papers
- `fetch_recent_news()` - Integrate with news APIs or RSS feeds
- Update markers in README.md to control what sections get auto-updated

## GitHub Actions Integration

The script is automatically run weekly by the GitHub Actions workflow defined in `.github/workflows/auto-update.yml`.

The workflow:
- Runs every Monday at 9:00 AM UTC
- Can be manually triggered via workflow_dispatch
- Commits and pushes changes if updates are found
- Creates an issue if the update fails
