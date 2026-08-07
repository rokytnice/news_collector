# IT News Aggregator

This project is an IT news aggregator that collects and summarizes IT-related news from various RSS feeds. It uses a Large Language Model (LLM) for relevance filtering and translation, and streams the results into an HTML file.

## Features

- **RSS Feed Collection:** Gathers news from a predefined list of IT news sources.
- **LLM-based Filtering:** Uses Claude via the `claude` CLI (bash) to check the relevance of articles based on defined IT categories.
- **LLM-based Translation:** Translates non-German article titles and summaries into German using Claude.
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
   *(Note: A `requirements.txt` file is assumed. If it doesn't exist, you may need to create one with `requests` and `feedparser`.)*

3. Make sure the Claude CLI is installed and logged in — it is the only LLM this project uses:
   ```bash
   claude --version
   claude -p "ping"
   ```
   No API key is required; the CLI session handles authentication. If `claude` is not on your
   `PATH`, point the script at it:
   ```bash
   export CLAUDE_CLI_PATH=/home/aroc/.local/bin/claude
   ```

## Configuration

Configuration settings are stored in separate Python files.

- [`config.py`](config.py): Contains the default configuration, including news sources, pre-filter keywords, LLM categories, LLM rate limit, and the Claude CLI path/model name.
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



## LLM policy

Claude via the `claude` CLI is the **only** LLM used in this project. Do not add other providers.
Manual smoke test of the same call the script makes:

```bash
echo 'Antworte NUR mit JA oder NEIN: Ist Python eine Programmiersprache?' | \
  claude -p --model sonnet --output-format text --allowedTools "" --strict-mcp-config
```
