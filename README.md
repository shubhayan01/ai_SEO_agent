AI Overview Content Gap Agent

An automated SEO analysis agent that monitors Google AI Overviews, compares competitor pages against a client article, and generates a structured content gap report. The agent extracts structural signals from competitor content, runs LLM analysis, and produces actionable recommendations for improving the client article.

Outputs

Structured Word report (.docx) for writers
Machine-readable JSON output for automation pipelines
Overview

SEO teams often need to manually analyze several competitor pages to understand what their content is missing.
This tool automates that workflow.

The agent will:
Identify sources cited in Google AI Overviews
Scrape competitor pages
Analyze the client article
Compare structural coverage
Generate a content gap report with improvement suggestions
Instead of manually reading 5–10 pages, the agent performs the analysis automatically.

Features
AI Overview Source Extraction
Fetches URLs cited in Google AI Overviews using:
SerpAPI (recommended)
Serper.dev (fallback)
Competitor Page Analysis
Each competitor page is analyzed for structural signals such as:
Word count
Headings (H1–H3)
FAQ sections
Tables
Lists
Paragraph distribution
Client Article Analysis
The client page is analyzed using the same metrics to ensure a fair comparison.

LLM Gap Analysis
The agent sends competitor and client signals to an LLM to detect:
Missing topics
Structural gaps
Content weaknesses
SEO improvement opportunities
Dual Output

Two outputs are generated:

File	Purpose
gap_report.docx	Human-readable report for writers and SEO teams
gap_report.json	Structured data for automation
Example Workflow
Keyword
   ↓
Google AI Overview sources
   ↓
Competitor pages scraped
   ↓
Client article scraped
   ↓
Structural comparison
   ↓
LLM analysis
   ↓
Gap report generated

Project Structure
ai-overview-agent
│
├── agent.py
├── requirements.txt
├── README.md
├── .env.example
│
├── mock_html
│   ├── competitor_1.html
│   ├── competitor_2.html
│   └── client.html
│
├── sample_output.json
└── gap_report_sample.pdf

Prerequisites
Python
Python 3.10+
Search API

Choose one.

SerpAPI
https://serpapi.com

Free tier: 100 searches/month

Serper.dev
https://serper.dev

Free tier: 2500 searches/month

LLM API Choose one.

Anthropic Claude (recommended)
https://console.anthropic.com

OpenAI
https://platform.openai.com

Installation
Install dependencies.
pip install -r requirements.txt
Create environment file.
cp .env.example .env

Add your API keys.

SERPAPI_KEY=your_key
ANTHROPIC_API_KEY=your_key
Running the Agent
Live Mode

Normal usage with live SERP and scraping.

python agent.py \
  --keyword "best term insurance plan India" \
  --client-url "https://www.example.com/term-insurance-guide" \
  --output report.docx
Mock Mode (Offline / Demo)

Mock mode runs the agent without HTTP requests.

Useful when:
pages block scraping
pages require login
running demos without API costs
Step 1 — Save pages as HTML

Example using curl.

curl -L -A "Mozilla/5.0" -o mock_html/competitor_1.html https://site.com/article
curl -L -A "Mozilla/5.0" -o mock_html/competitor_2.html https://site.com/article
curl -L -A "Mozilla/5.0" -o mock_html/client.html https://client-site.com/article

You can also use:

Browser → File → Save Page As → HTML
Save the files inside:
mock_html/

File naming rules:
competitor_1.html
competitor_2.html
client.html
Step 2 — Run mock mode
python agent.py \
  --keyword "best term insurance plan India" \
  --client-url "https://www.policybazaar.com/term-insurance/" \
  --mock-html-dir mock_html/ \
  --output gap_report.docx

The agent will:
skip SERP calls
skip HTTP scraping
analyze saved HTML files instead

CLI Arguments
Argument	Required	Description
--keyword	Yes	Target keyword
--client-url	Yes	Client article URL
--output	No	Output file path
--mock-html-dir	No	Directory containing saved HTML files
Design Decisions
Why SerpAPI

SerpAPI exposes a dedicated field:
ai_overview.sources
This makes extracting AI Overview URLs reliable.

Why BeautifulSoup
Most SEO pages are static HTML.

BeautifulSoup provides:

fast parsing
minimal dependencies
reliable heading extraction
JS-rendered pages can be handled using mock mode.

Why a Single Python File

Frameworks like:
LangChain
CrewAI
Autogen
were intentionally avoided.

This workflow is sequential, so plain Python provides:
simpler debugging
easier deployment
faster execution
Token Cost Control
Each page is truncated to: 3000 words

This keeps LLM cost extremely low while preserving the signals needed for analysis.
Typical run cost:
< $0.01
Geography Configuration

The agent sets: gl=in

AI Overviews appear more frequently in Indian search results.
If AI Overviews do not appear for a keyword: try a VPN set to India

test alternative keywords
Trial Limit
The agent includes a 3-run free trial per machine.
After three runs a licence key is required.

Add the key to .env:

LICENCE_KEY=your_key

Future Improvements
Possible enhancements:
automated SERP clustering
competitor topic extraction
internal link recommendations
automated article outline generation
CMS integrations
