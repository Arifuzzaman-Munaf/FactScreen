# Deploying FactScreen API to Render (Free Tier)

This is a quick guide to deploy your FactScreen API to Render's **free tier**.

## Prerequisites

1. ✅ A [Render account](https://dashboard.render.com/register) (free account works)
2. ✅ Your code pushed to a GitHub, GitLab, or Bitbucket repository
3. ✅ Your API keys ready:
   - `GOOGLE_API_KEY` (Google Fact Check API)
   - `FACT_CHECKER_API_KEY` (RapidAPI Fact Checker)
   - `GEMINI_API_KEY` (Google Gemini API)

## Quick Deploy Steps

### Step 1: Push Your Code to Git

Make sure your code (including `render.yaml`) is pushed to your repository:

```bash
git add .
git commit -m "Configure for Render free tier deployment"
git push origin main
```

### Step 2: Connect Repository to Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New > Blueprint** (or **New > Web Service**)
3. Connect your GitHub/GitLab/Bitbucket repository
4. Render will automatically detect `render.yaml` and configure the service

### Step 3: Configure Environment Variables

**Important:** Add these environment variables in Render Dashboard:

1. Go to your service settings
2. Navigate to **Environment** section
3. Add these variables:
   ```
   GOOGLE_API_KEY=your-google-factcheck-key
   FACT_CHECKER_API_KEY=your-rapidapi-key
   GEMINI_API_KEY=your-gemini-key
   ```
   **⚠️ Do NOT set PORT manually** - Render sets this automatically

### Step 4: Deploy

Render will automatically:
- Build your application
- Install dependencies
- Start the server
- Make it available at `https://your-service-name.onrender.com`

## Verify Deployment

Once deployed, test your API:

```bash
# Health check
curl https://your-service-name.onrender.com/v1/health

# Test validation endpoint
curl -X POST "https://your-service-name.onrender.com/v1/validate" \
  -H "Content-Type: application/json" \
  -d '{"text": "The Eiffel Tower will be demolished next year"}'
```

## Access Your API

- **API Base URL**: `https://your-service-name.onrender.com`
- **API Documentation**: `https://your-service-name.onrender.com/docs`
- **ReDoc**: `https://your-service-name.onrender.com/redoc`
- **Health Check**: `https://your-service-name.onrender.com/v1/health`

## Free Tier Limitations

⚠️ **Important Free Tier Limitations:**

1. **512MB RAM limit** - May cause memory issues with large ML models
2. **Spins down after 15 minutes** of inactivity
3. **First request after spin-down** may take 30-60 seconds (cold start)
4. **750 hours/month** limit (about 31 days of continuous uptime)
5. **No persistent disk** - logs are ephemeral

### If You Encounter Memory Issues

If you get "Out of memory" errors:
- The free tier has 512MB RAM limit
- Consider upgrading to **Starter plan** ($7/month) for production
- Or optimize your dependencies/models

## Troubleshooting

### Service Won't Start

- ✅ Check that all environment variables are set
- ✅ Verify `entrypoint/server.py` exists
- ✅ Review logs in Render Dashboard
- ✅ Ensure health check endpoint `/v1/health` is accessible

### Port Binding Issues

- ✅ The server automatically detects Render environment
- ✅ It binds to `0.0.0.0` and uses `PORT` env var
- ✅ Check logs to see if server started successfully

### Build Fails

- ✅ Check that `requirements-dev.txt` is in repository
- ✅ Verify Python version (should be 3.10+)
- ✅ Review build logs in Render Dashboard

### Slow First Request

- ✅ This is normal on free tier (cold start after spin-down)
- ✅ Subsequent requests will be faster
- ✅ Consider upgrading to Starter plan to avoid spin-downs

## Updating Your Deployment

Render automatically redeploys when you push to your connected branch.

To manually redeploy:
1. Go to your service in Render Dashboard
2. Click **Manual Deploy > Deploy latest commit**

## Configuration Details

The `render.yaml` file is already configured for free tier:

```yaml
services:
  - type: web
    name: factscreen-api
    env: python
    plan: free  # Free tier
    buildCommand: pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements-dev.txt
    startCommand: python entrypoint/server.py
    healthCheckPath: /v1/health
```

The server automatically:
- Detects Render environment (checks for `PORT` env var)
- Binds to `0.0.0.0` (required by Render)
- Uses `PORT` environment variable (set by Render)
- Runs in production mode (no auto-reload)

## Next Steps

1. ✅ Test your deployed API
2. ✅ Share the API URL with your team
3. ✅ Monitor usage in Render Dashboard
4. ✅ Consider upgrading to Starter plan if you need:
   - No spin-downs
   - More reliable performance
   - Better for production use

## Need Help?

- Check [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed instructions
- Review [Render Documentation](https://render.com/docs)
- Check service logs in Render Dashboard