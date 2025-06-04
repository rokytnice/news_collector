# IT News Aggregator

This project is an IT news aggregator that collects and summarizes IT-related news from various RSS feeds. It uses a Large Language Model (LLM) for relevance filtering and translation, and streams the results into an HTML file.

## Features

- **RSS Feed Collection:** Gathers news from a predefined list of IT news sources.
- **LLM-based Filtering:** Uses a Gemini LLM via REST API to check the relevance of articles based on defined IT categories.
- **LLM-based Translation:** Translates non-German article titles and summaries into German using a Gemini LLM.
- **HTML Output:** Streams the processed news articles into a single HTML file for easy viewing.
- **Configurable Sources and Keywords:** Allows defining news sources, pre-filter keywords, and LLM categories in separate configuration files.
- **Command-line Configuration:** Supports specifying the configuration file to use via a command-line argument.

## Setup

### Prerequisites

- Python 3.6 or higher
- `pip` package installer

### Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd news_collector
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: A `requirements.txt` file is assumed. If it doesn't exist, you may need to create one with `requests`, `feedparser`, and potentially `google-generativeai` if using the client library instead of REST API directly)*

3. Set your Gemini API key as an environment variable:
   ```bash
   export GEMINI_API_KEY='YOUR_API_KEY'
   ```
   Replace `'YOUR_API_KEY'` with your actual Gemini API key.

## Configuration

Configuration settings are stored in separate Python files.

- [`config.py`](config.py): Contains the default configuration, including news sources, pre-filter keywords, LLM categories, LLM rate limit, and Gemini API endpoint/model name.
- [`config_it.py`](config_it.py): Contains an alternative set of news sources, keywords, and translations, specifically tailored for IT news.

You can create your own configuration files following the same structure.

## Usage

Run the `news.py` script from the terminal.

To use the default configuration (`config.py`):

```bash
python news.py
```

Or explicitly specify the default configuration:

```bash
python news.py --config config
```

To use an alternative configuration, for example, `config_it.py`:

```bash
python news.py --config config_it
```

Replace `config_it` with the name of your desired configuration file (without the `.py` extension).

The script will generate an HTML file in the same directory containing the aggregated news.

## File Structure

```
.
├── news.py             # Main script to run the aggregator
├── config.py           # Default configuration settings
├── config_it.py        # Alternative IT-specific configuration
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

*(Note: Other files like `news_coding.py` and `news_it.py` might exist but `news.py` is the primary entry point with configurable options)*
