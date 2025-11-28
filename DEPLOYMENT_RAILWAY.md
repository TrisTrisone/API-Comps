# 🚀 Deployment Guide: Railway

This guide will help you deploy your Competitor Analysis API to Railway in under 10 minutes.

---

## 📋 Prerequisites

- [x] GitHub account
- [x] Code tested locally (✅ PASSED)
- [x] Environment variables ready

---

## 🎯 Step-by-Step Deployment

### Step 1: Push Code to GitHub

If you haven't already, push your code to GitHub:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Ready for deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/API-Comps.git
git branch -M main
git push -u origin main
```

---

### Step 2: Sign Up for Railway

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Sign in with GitHub (recommended)

---

### Step 3: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: `API-Comps`
4. Railway will automatically detect it's a Python project

---

### Step 4: Configure Environment Variables

1. In your Railway project, click on your service
2. Go to **"Variables"** tab
3. Add the following variables:

```
TENANT_ID=<your-tenant-id>
CLIENT_ID=<your-client-id>
CLIENT_SECRET=<your-client-secret>
DRIVE_ID=<your-drive-id>
GEMINI_API_KEY=<your-gemini-api-key>
```

**Important:** Copy these from your local `.env` file

---

### Step 5: Configure Build Settings (Optional)

Railway should auto-detect your settings, but verify:

**Build Command:** (Auto-detected from requirements.txt)
```
pip install -r requirements.txt
```

**Start Command:** (Auto-detected from Dockerfile or you can set manually)
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

### Step 6: Deploy!

1. Click **"Deploy"**
2. Wait for build to complete (~2-3 minutes)
3. Railway will provide you with a public URL

Your API will be available at:
```
https://your-app-name.up.railway.app
```

---

### Step 7: Test Your Deployment

Once deployed, test your API:

**Health Check:**
```bash
curl https://your-app-name.up.railway.app/
```

Expected response:
```json
{"status":"online","service":"Competitor Analysis API"}
```

**API Documentation:**
Open in browser:
```
https://your-app-name.up.railway.app/docs
```

**Test Analysis Endpoint:**
Use the interactive docs at `/docs` or send a POST request:

```bash
curl -X POST https://your-app-name.up.railway.app/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "copilot_response": "Full Path: /sites/.../file.xlsx",
    "target_company": "Coca Cola"
  }'
```

---

## 🔧 Railway Configuration Tips

### Custom Domain (Optional)
1. Go to **Settings** → **Domains**
2. Click **"Generate Domain"** for a custom Railway subdomain
3. Or add your own custom domain

### Monitoring
1. Go to **Metrics** tab to see:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

### Logs
1. Go to **Deployments** tab
2. Click on latest deployment
3. View real-time logs

### Auto-Deploy
Railway automatically deploys when you push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push
```
Railway will detect the push and redeploy automatically!

---

## 💰 Pricing

### Free Tier (Hobby Plan)
- **$5 free credits per month**
- **500 hours of execution time**
- **Perfect for testing and low-traffic apps**

### Pro Plan
- **$5/month base**
- **Pay for what you use**
- **No execution time limits**

**Estimated Cost for Your App:**
- Low traffic (< 1000 requests/day): **FREE** or ~$2-5/month
- Medium traffic (1000-10000 requests/day): ~$10-20/month

---

## 🔒 Security Best Practices

### 1. Environment Variables
✅ Already configured - secrets are not in code

### 2. Add Rate Limiting (Optional)
Install slowapi:
```bash
pip install slowapi
```

Update `main.py`:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/analyze")
@limiter.limit("10/minute")  # 10 requests per minute
def analyze_competitors(request: AnalysisRequest):
    # ... existing code
```

### 3. Add API Key Authentication (Optional)
```python
from fastapi import Header, HTTPException

API_KEY = os.getenv("API_KEY")

@app.post("/analyze")
def analyze_competitors(
    request: AnalysisRequest,
    x_api_key: str = Header(...)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    # ... existing code
```

---

## 🐛 Troubleshooting

### Issue: Build Failed
**Solution:** Check Railway logs for specific error. Common issues:
- Missing dependencies in `requirements.txt`
- Python version mismatch

### Issue: App Crashes on Startup
**Solution:** 
- Verify all environment variables are set
- Check logs for specific error messages

### Issue: Timeout Errors
**Solution:**
- Railway has no timeout limits (unlike Vercel)
- If still timing out, check SharePoint connectivity

### Issue: File Download Fails
**Solution:**
- Verify SharePoint credentials are correct
- Check DRIVE_ID is accurate
- Ensure files exist at specified paths

---

## 📊 Monitoring Your App

### View Logs
```bash
# Install Railway CLI (optional)
npm i -g @railway/cli

# Login
railway login

# View logs
railway logs
```

### Set Up Alerts
1. Go to Railway dashboard
2. Settings → Notifications
3. Add email or Slack webhook for deployment notifications

---

## 🔄 Updating Your App

### Method 1: Git Push (Recommended)
```bash
# Make changes to your code
git add .
git commit -m "Your update message"
git push

# Railway auto-deploys!
```

### Method 2: Manual Redeploy
1. Go to Railway dashboard
2. Click **"Redeploy"**

---

## ✅ Post-Deployment Checklist

- [ ] API is accessible at public URL
- [ ] Health endpoint returns 200 OK
- [ ] `/docs` page loads correctly
- [ ] Test analysis with sample data
- [ ] Environment variables are set
- [ ] Logs show no errors
- [ ] Set up monitoring/alerts
- [ ] Document your API URL
- [ ] Share with team

---

## 🎉 You're Live!

Your Competitor Analysis API is now deployed and accessible worldwide!

**Next Steps:**
1. Share the API URL with your team
2. Integrate with your applications
3. Monitor usage and performance
4. Scale as needed

---

## 📞 Support

**Railway Documentation:** https://docs.railway.app  
**Railway Discord:** https://discord.gg/railway  
**Your Test Results:** See `TEST_RESULTS.md`

---

**Deployment Time:** ~10 minutes  
**Difficulty:** ⭐⭐☆☆☆ (Easy)  
**Recommended:** ✅ YES
