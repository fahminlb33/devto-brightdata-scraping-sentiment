# Bright Data Hackathon: Trading Signal using Sentiment Analysis

This repo contains the source code for my submission for [Bright Data Web Scraping Hackathon at DEV.to](https://dev.to/devteam/join-us-for-the-bright-data-web-scraping-challenge-3000-in-prizes-3mg2?bb=196803).

## Setup

Use `uv` to install dependencies. Clone this repo and run `uv sync` to install the packages.

## Running the Project

Trigger data collection API to scrape the news from multiple sources.

```bash
python scripts/scrape_api.py --api-key YOUR_API_KEY discover --output-file ./data/snapshot-bbc.jsonl --keywords 'apple,facebook meta,microsoft,nvidia' --engine bbc
python scripts/scrape_api.py --api-key YOUR_API_KEY discover --output-file ./data/snapshot-cnn.jsonl --keywords 'apple,facebook meta,microsoft,nvidia' --engine cnn
python scripts/scrape_api.py --api-key YOUR_API_KEY discover --output-file ./data/snapshot-reuters.jsonl --keywords 'apple,facebook meta,microsoft,nvidia' --engine reuters
```

Copy the contents of all 3 snapshot files into one, then download the scraped data.

```bash
python scripts/scrape_api.py --api-key YOUR_API_KEY download --snapshots-file ./data/snapshot-all.jsonl --output-path ./data/scraped
```

Then, run these notebooks in order:

1. [merge.ipynb](./notebooks/merge.ipynb)
2. [eda-stock-data.ipynb](./notebooks/eda-stock-data.ipynb)
3. [eda-llm-extraction.ipynb](./notebooks/eda-llm-extraction.ipynb)
4. [eval.ipynb](./notebooks/eval.ipynb)

Note: You will also need Ollama with Llama 3.1 to run the LLM extraction notebook.
