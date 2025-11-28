# Deploying to Render

This guide will walk you through deploying your Competitor Analysis API to Render.

## Prerequisites

1. **GitHub Account** - Your code should be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **Environment Variables** - Have your credentials ready:
   - `TENANT_ID`
   - `CLIENT_ID`
   - `CLIENT_SECRET`
   - `DRIVE_ID`
   - `GEMINI_API_KEY`

---

## Deployment Methods

### Method 1: Using render.yaml (Recommended) ⭐

This method uses the `render.yaml` file for automated deployment.

#### Step 1: Push to GitHub

```bash
# If not already initialized
git init
git add .
git commit -m "Initial commit for Render deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

#### Step 2: Connect to Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file
5. Click **"Apply"**

#### Step 3: Configure Environment Variables

Render will prompt you to add the required environment variables:

| Variable Name | Description | Example |
|--------------|-------------|---------|
| `TENANT_ID` | Azure AD Tenant ID | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `CLIENT_ID` | Azure App Client ID | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `CLIENT_SECRET` | Azure App Client Secret | `your-secret-value` |
| `DRIVE_ID` | SharePoint Drive ID | `b!xxxxxxxxxxxxx` |
| `GEMINI_API_KEY` | Google Gemini API Key | `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXX` |

#### Step 4: Deploy

- Click **"Create Web Service"**
- Render will build and deploy your Docker container
- Wait for the build to complete (usually 3-5 minutes)

---

### Method 2: Manual Deployment (Alternative)

If you prefer manual setup:

#### Step 1: Create Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select your repository

#### Step 2: Configure Service

Fill in the following settings:

| Setting | Value |
|---------|-------|
| **Name** | `competitor-analysis-api` |
| **Region** | Singapore (or closest to you) |
| **Branch** | `main` |
| **Runtime** | Docker |
| **Instance Type** | Free |

#### Step 3: Add Environment Variables

In the **Environment** section, add all 5 required variables (see table above).

#### Step 4: Deploy

- Click **"Create Web Service"**
- Render will automatically build from your Dockerfile

---

## Post-Deployment

### 1. Get Your API URL

After deployment, Render will provide a URL like:
```
https://competitor-analysis-api.onrender.com
```

### 2. Test Your API

Test the health endpoint:
```bash
curl https://your-app-name.onrender.com/
```

Expected response:
```json
{
  "status": "online",
  "service": "Competitor Analysis API"
}
```

### 3. Test the Analysis Endpoint

```bash
curl -X POST https://your-app-name.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "copilot_response": "Your copilot response here...",
    "target_company": "Example Corp"
  }'
```

### 4. Check Cache Statistics

```bash
curl https://your-app-name.onrender.com/cache/stats
```

---

## Important Notes

### Free Tier Limitations

- **Spin Down**: Free services spin down after 15 minutes of inactivity
- **Cold Start**: First request after spin down takes 30-60 seconds
- **Build Time**: Limited to 500 build hours/month
- **Memory**: 512 MB RAM

### Handling Cold Starts

The free tier spins down after inactivity. To minimize impact:

1. **Expect delays**: First request after inactivity will be slow
2. **Use caching**: Your app already has 48-hour caching implemented
3. **Upgrade if needed**: Paid plans ($7/month) keep services always running

### Upgrading to Paid Plan

If you need better performance:

1. Go to your service in Render Dashboard
2. Click **"Settings"** → **"Instance Type"**
3. Select **"Starter"** ($7/month) or higher
4. Benefits:
   - Always running (no cold starts)
   - More memory (512 MB → 2 GB)
   - Better CPU performance

---

## Monitoring & Logs

### View Logs

1. Go to your service in Render Dashboard
2. Click **"Logs"** tab
3. View real-time logs of your application

### Health Checks

Render automatically monitors your `/` endpoint. If it fails, Render will restart your service.

---

## Updating Your Deployment

### Automatic Deploys (Recommended)

By default, Render auto-deploys when you push to your main branch:

```bash
git add .
git commit -m "Update API logic"
git push origin main
```

Render will automatically rebuild and deploy.

### Manual Deploys

1. Go to your service in Render Dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

### Disable Auto-Deploy

If you want to control when deployments happen:

1. Go to **Settings** → **Build & Deploy**
2. Toggle off **"Auto-Deploy"**

---

## Troubleshooting

### Build Fails

**Check Dockerfile:**
- Ensure `Dockerfile` is in the root directory
- Verify all dependencies are in `requirements.txt`

**Check Logs:**
- Go to **Logs** tab in Render Dashboard
- Look for error messages during build

### Service Won't Start

**Check Environment Variables:**
- Ensure all 5 variables are set correctly
- No extra spaces or quotes

**Check Port:**
- Your app should listen on `0.0.0.0:8000`
- Render automatically maps this to port 80/443

### API Returns Errors

**Check Logs:**
```bash
# View recent logs in dashboard or use Render CLI
```

**Common Issues:**
- Invalid SharePoint credentials
- Invalid Gemini API key
- Network connectivity issues

### Slow Response Times

**Free Tier Cold Starts:**
- First request after 15 min inactivity is slow
- Consider upgrading to paid plan

**Large File Processing:**
- Excel files take time to process
- Use the caching feature to avoid reprocessing

---

## Security Best Practices

### 1. Never Commit Secrets

Your `.gitignore` should include:
```
.env
*.env
```

### 2. Use Render's Secret Files (Optional)

For additional security:
1. Go to **Environment** → **Secret Files**
2. Add `.env` as a secret file
3. Paste your environment variables

### 3. Rotate Credentials Regularly

Update your API keys and secrets periodically:
1. Update in Azure/Google Cloud
2. Update in Render Dashboard
3. Redeploy service

---

## Cost Optimization

### Free Tier Tips

1. **Use caching**: Your app caches results for 48 hours
2. **Batch requests**: Process multiple analyses together
3. **Monitor usage**: Check Render Dashboard for usage stats

### When to Upgrade

Consider paid plan if:
- You need instant response times
- You have frequent API calls
- You need more than 512 MB RAM
- You process large Excel files

---

## API Documentation

Once deployed, you can access interactive API docs:

- **Swagger UI**: `https://your-app-name.onrender.com/docs`
- **ReDoc**: `https://your-app-name.onrender.com/redoc`

---

## Support & Resources

- **Render Docs**: [docs.render.com](https://docs.render.com)
- **Render Community**: [community.render.com](https://community.render.com)
- **Status Page**: [status.render.com](https://status.render.com)

---

## Quick Reference

### Service URL
```
https://your-app-name.onrender.com
```

### Endpoints
- `GET /` - Health check
- `POST /analyze` - Analyze competitors
- `GET /cache/stats` - Cache statistics
- `GET /docs` - API documentation

### Environment Variables
- `TENANT_ID`
- `CLIENT_ID`
- `CLIENT_SECRET`
- `DRIVE_ID`
- `GEMINI_API_KEY`

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Create Render account
3. ✅ Deploy using Blueprint (render.yaml)
4. ✅ Configure environment variables
5. ✅ Test your API
6. 🎉 You're live!

---

**Need help?** Check the troubleshooting section or Render's documentation.
