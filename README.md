# AI PowerPoint Generator

An AI-powered application that generates professional PowerPoint presentations with AI-generated content and images.

## Features

- **AI-Generated Content**: Uses Google Gemini to create structured slide content
- **AI-Generated Images**: Uses HuggingFace Inference API (FLUX.1) to create relevant images for each slide
- **Simple UI**: Clean Streamlit interface for easy interaction
- **FastAPI Backend**: Robust backend API for processing requests

## Project Structure

```
power point gen/
├── backend/
│   ├── __init__.py
│   ├── main.py           # FastAPI entry point
│   ├── llm_utils.py      # LLM content generation
│   ├── image_utils.py    # Image generation utilities
│   └── ppt_utils.py      # PowerPoint assembly
├── frontend/
│   └── ui.py             # Streamlit UI
├── .env                  # Environment variables (API keys)
├── requirements.txt      # Python dependencies
└── README.md
```

## Setup

1. **Clone the repository** (or download the files)

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory with:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   HF_TOKEN=your_huggingface_token_here
   ```

## Running the Application

### Step 1: Start the Backend (FastAPI)

Open a terminal and run:
```bash
cd "e:\Langchain\power point gen"
python -m backend.main
```

The API will start at `http://127.0.0.1:8000`

### Step 2: Start the Frontend (Streamlit)

Open another terminal and run:
```bash
cd "e:\Langchain\power point gen"
streamlit run frontend/ui.py
```

The UI will open in your browser at `http://localhost:8501`

## Usage

1. Enter a **topic** for your presentation (e.g., "The Future of Artificial Intelligence")
2. Select the **number of slides** (1-10)
3. Click **Generate Presentation**
4. Wait for the AI to generate content and images
5. Download the generated PowerPoint file

## API Endpoint

### POST `/generate_ppt`

**Request Body**:
```json
{
  "topic": "Your Topic Here",
  "slide_count": 5
}
```

**Response**: PowerPoint file (`.pptx`)

## Technologies Used

- **Backend**: FastAPI, Python
- **Frontend**: Streamlit
- **LLM**: Google Gemini 2.5 Flash
- **Image Generation**: HuggingFace FLUX.1-schnell
- **PPT Generation**: python-pptx

## Notes

- Image generation may take time depending on HuggingFace API availability
- Make sure both backend and frontend are running simultaneously
- Generated presentations are saved in `backend/generated/`
