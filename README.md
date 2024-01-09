# Where You Read Me?
This project is in it's early stage, it is more like an idea for now.

## Overview
"Where You Read Me?" is an innovative project designed to trace the path of news stories across different websites based on their embedding vectors. This unique approach involves comparing the vectorized representation of news articles to determine similarities and track how a particular news story evolves and gets represented in various forms on different news platforms. Users can set a similarity threshold to find articles similar to a chosen piece across sites. Additionally, the project features a dashboard to compare news based on later discovered features and their embeddings.

## Project Structure
### Database
- **EdgeDB**: Used for storing and managing the data efficiently.

### Scraper
- Located in the `scraper` folder.
- A Scrapy scraper that currently extracts news from three Hungarian websites: `index.hu`, `telex.hu`, `mandiner.hu`.
- The scraping component is complete.

### Postprocessor
- Found in the `postprocessor` folder.
- Processes the scraped news, extracts relevant information, and converts the title, description, and content text into vectors.
- Utilizes `bert-multilingual` for vectorizing due to its high performance in embeddings and because its free. Longer texts are stored in chunks due to the small context window of the model.
- The postprocessor is complete.

### Frontend
- Will be developed using `SvelteKit`.
- Currently, only the basic skeleton of the frontend is completed.

### Backend
- Implemented using `FastAPI`.
- The basic template of the backend is in place.

## Installation
(Include detailed steps to set up the project locally. For example:)
1. Clone the repository: `git clone [repository URL]`
2. Navigate to the project directory: `cd [project directory]`
3. Install required dependencies: `pip install -r requirements.txt`
4. (Additional installation steps)

## Usage
Not yet.

## Future Plans
- Enhance the vectorizing process by integrating OpenAI embeddings.
- Complete the development of the SvelteKit frontend.
- Further backend development to support advanced features.

