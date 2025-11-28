# Competitor Analysis API

AI-powered competitor analysis service that extracts and classifies companies from Excel files using Google Gemini AI.

## Features

- 🤖 **AI-Powered Extraction**: Uses Gemini 2.5 Flash to extract company names from Excel files
- 🎯 **Smart Classification**: Automatically classifies competitors with confidence scores (0-100)
- 💾 **48-Hour Caching**: In-memory cache for faster repeated queries
- 📊 **Large File Support**: Processes files with 50,000+ rows using 80% of Gemini's 1M token capacity
- 🔍 **Smart Sheet Detection**: Automatically finds "comps" sheets in Excel files
- ☁️ **SharePoint Integration**: Downloads files directly from SharePoint

## Quick Start

### Prerequisites

- Python 3.9+
- SharePoint credentials (Tenant ID, Client ID, Client Secret, Drive ID)
- Google Gemini API key

### Installation

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file with:

```env
TENANT_ID=your_tenant_id
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
DRIVE_ID=your_drive_id
GEMINI_API_KEY=your_gemini_api_key
```

### Run Locally

```bash
uvicorn main:app --reload --port 8000
```

API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /
```

### Cache Statistics
```
GET /cache/stats
```

### Analyze Competitors
```
POST /analyze
```

**Request Body:**
```json
{
  "copilot_response": "Full Path: /sites/.../file.xlsx",
  "target_company": "Coca Cola"
}
```

**Response:**
```json
{
  "target_company": "Coca Cola",
  "verified_competitors": [
    {"name": "PepsiCo", "score": 95, "reason": "Direct competitor"}
  ],
  "to_crosscheck": [
    {"name": "Nestle", "score": 65, "reason": "Broader food/beverage"}
  ],
  "verified_count": 8,
  "crosscheck_count": 12,
  "reasoning": "Industry analysis...",
  "files_processed": 3,
  "total_files_found": 5,
  "failed_files": [],
  "cached": false
}
```

## Deployment

See [DEPLOYMENT_RAILWAY.md](DEPLOYMENT_RAILWAY.md) for detailed deployment instructions.

### Quick Deploy to Railway

1. Push code to GitHub
2. Connect Railway to your repository
3. Add environment variables
4. Deploy!

## Technical Details

- **Framework**: FastAPI
- **AI Model**: Google Gemini 2.5 Flash
- **Token Capacity**: 80% (800K tokens)
- **Cache**: In-memory TTL cache (48 hours)
- **Max Companies**: 2,000 per analysis
- **Max File Size**: 3.2M characters (~800K tokens)

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License

Proprietary - Tristone Strategic Partners LLP