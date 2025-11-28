from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import os
import hashlib
from dotenv import load_dotenv
from cachetools import TTLCache
from extractor import CopilotResponseProcessor, GeminiCompanyExtractor, get_graph_token, download_file_from_sharepoint

# Load environment variables
load_dotenv()

app = FastAPI(title="Competitor Analysis API")

# Initialize in-memory cache with 48-hour TTL (172800 seconds)
# Max 100 entries to prevent memory issues
analysis_cache = TTLCache(maxsize=100, ttl=172800)

# Configuration
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
DRIVE_ID = os.getenv("DRIVE_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class AnalysisRequest(BaseModel):
    copilot_response: str
    target_company: str

class AnalysisResponse(BaseModel):
    target_company: str
    verified_competitors: list
    to_crosscheck: list
    verified_count: int
    crosscheck_count: int
    reasoning: str
    files_processed: int
    total_files_found: int
    failed_files: list
    cached: bool = False  # Indicates if result came from cache

def get_cache_key(target_company: str, file_paths: list) -> str:
    """
    Generate a unique cache key based on target company and file paths.
    This ensures different file sets get different cache entries.
    """
    # Sort file paths to ensure consistent hashing
    paths_str = "".join(sorted(file_paths))
    paths_hash = hashlib.md5(paths_str.encode()).hexdigest()[:8]
    company_key = target_company.lower().replace(' ', '_').replace('-', '_')
    return f"{company_key}_{paths_hash}"

@app.get("/")
def read_root():
    return {"status": "online", "service": "Competitor Analysis API"}

@app.get("/cache/stats")
def get_cache_stats():
    """Get cache statistics"""
    return {
        "cache_size": len(analysis_cache),
        "max_size": analysis_cache.maxsize,
        "ttl_hours": analysis_cache.ttl / 3600,
        "entries": list(analysis_cache.keys())
    }

@app.post("/analyze", response_model=AnalysisResponse)
def analyze_competitors(request: AnalysisRequest):
    if not all([TENANT_ID, CLIENT_ID, CLIENT_SECRET, DRIVE_ID, GEMINI_API_KEY]):
        raise HTTPException(status_code=500, detail="Server configuration error: Missing environment variables.")

    try:
        # 1. Initialize Processor
        processor = CopilotResponseProcessor(
            copilot_response=request.copilot_response,
            target_company=request.target_company,
            api_key=GEMINI_API_KEY
        )

        # 2. Extract File Paths
        file_paths, relative_paths = processor.extract_file_paths()
        
        if not file_paths:
            return AnalysisResponse(
                target_company=request.target_company,
                verified_competitors=[],
                to_crosscheck=[],
                verified_count=0,
                crosscheck_count=0,
                reasoning="No file paths found in Copilot response.",
                files_processed=0,
                total_files_found=0,
                failed_files=[],
                cached=False
            )

        # 3. Check Cache
        cache_key = get_cache_key(request.target_company, file_paths)
        if cache_key in analysis_cache:
            print(f"✅ Cache hit for {request.target_company} (key: {cache_key})")
            cached_result = analysis_cache[cache_key]
            cached_result.cached = True
            return cached_result
        
        print(f"🔄 Cache miss for {request.target_company} (key: {cache_key}). Processing...")

        # 3. Authenticate with SharePoint
        try:
            access_token = get_graph_token(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"SharePoint Authentication failed: {str(e)}")

        # 4. Process Files
        all_competitors_set = set()
        failed_files = []
        processed_count = 0

        for rel_path, full_path in zip(relative_paths, file_paths):
            try:
                # Download file
                file_stream = download_file_from_sharepoint(access_token, DRIVE_ID, rel_path)
                
                # Extract companies
                extractor = GeminiCompanyExtractor(
                    source=file_stream, 
                    api_key=GEMINI_API_KEY,
                    target_company=request.target_company
                )
                
                results = extractor.extract_with_gemini()
                
                if results and results.get("all_companies"):
                    companies = results["all_companies"]
                    processor.file_wise_companies[full_path] = list(companies)
                    all_competitors_set.update(companies)
                    processed_count += 1
                else:
                    failed_files.append({"path": rel_path, "error": "No companies extracted"})
                    
            except Exception as e:
                failed_files.append({"path": rel_path, "error": str(e)})
                continue

        # 5. Classify Competitors
        classification_result = processor.classify_competitors_with_gemini(list(all_competitors_set))
        
        result = AnalysisResponse(
            target_company=request.target_company,
            verified_competitors=classification_result.get("verified_competitors", []),
            to_crosscheck=classification_result.get("to_crosscheck", []),
            verified_count=len(classification_result.get("verified_competitors", [])),
            crosscheck_count=len(classification_result.get("to_crosscheck", [])),
            reasoning=classification_result.get("reasoning", ""),
            files_processed=processed_count,
            total_files_found=len(file_paths),
            failed_files=failed_files,
            cached=False
        )
        
        # 6. Store in cache
        analysis_cache[cache_key] = result
        print(f"💾 Cached result for {request.target_company} (key: {cache_key})")
        
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
