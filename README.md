# Slack Knowledge Archive MVP

## Overview

This project is a minimal system that permanently preserves useful technical resources shared in the club Slack workspace and allows members to search them later.

## Features

- Import Slack export data (ZIP/JSON)
- Store all messages permanently
- Extract and archive shared URLs
- Scrape the content of supported resources
- Generate a short AI summary for each resource
- Allow users to search archived resources

## Installation

1. Clone the repository:

```bash

```

2. Create a Python 3.11 virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment:

- On Windows:

```bash
.venv\Scripts\activate
```

- On macOS/Linux:

```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Set up environment variables:

Create a `.env` file in the root directory and add the following variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/slack_archive
AI_API_KEY=your_openai_api_key
AI_API_BASE=https://api.openai.com/v1
```

6. Set up the database:

```bash
psql -U user -d slack_archive -f database/schema.sql
```

7. Start the services using Docker Compose:

```bash
docker-compose -f docker/docker-compose.yml up -d
```

## Usage

1. Import a Slack export:

```bash
python scripts/ingest_export.py --file exports/club_export.zip
```

2. Search for resources:

```bash
curl "http://localhost:8000/search?q=your_query"
```

## Project Structure

```text
slack_archive/
│
├── api/
├── config/
├── database/
├── ingestion/
├── parsing/
├── scraping/
├── ai/
├── search/
├── models/
├── scripts/
├── tests/
└── docker/
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Standards

- Use Python type hints for all functions and variables.
- Use Pydantic models for data transfer objects (DTOs) and environment variable validation.
- Separate business logic from API routes.
- Do not write raw SQL outside the `database/` layer.
- Keep modules independent.
- Every public function must include a docstring.
- Configuration values must come from environment variables.
- Never commit API keys, secrets, or sensitive data.
- Log high-level errors only.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your fork.
5. Create a pull request to the main repository.

## License

This project is licensed under the MIT License.