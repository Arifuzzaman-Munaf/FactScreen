# Deploying FactScreen API to Render

This guide will help you deploy the FactScreen API backend to Render.

## Prerequisites

1. A [Render account](https://dashboard.render.com/register)
2. Your code pushed to a GitHub, GitLab, or Bitbucket repository
3. Your API keys ready (Google Fact Check, RapidAPI Fact Checker, Gemini)

## Quick Deploy

### Option 1: Using render.yaml (Recommended)

1. **Push your code** to your Git repository (make sure `render.yaml` is in the root)

2. **Connect your repository to Render:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click **New > Blueprint**
   - Connect your repository
   - Render will automatically detect `render.yaml` and create the service

3. **Add Environment Variables:**
   - Go to your service settings
   - Navigate to **Environment** section
   - Add the following environment variables:
     ```
     GOOGLE_API_KEY=your-google-factcheck-key
     FACT_CHECKER_API_KEY=your-rapidapi-key
     GEMINI_API_KEY=your-gemini-key
     ```
     **Important:** Do NOT set PORT manually. Render sets this automatically.

4. **Deploy:** Render will automatically build and deploy your service

### Option 2: Manual Setup

1. **Go to Render Dashboard:**
   - Click **New > Web Service**
   - Choose **Build and deploy from a Git repository**

2. **Connect your repository:**
   - Select your GitHub/GitLab/Bitbucket repository
   - Click **Connect**

3. **Configure the service:**
   - **Name**: `factscreen-api` (or your preferred name)
   - **Region**: Choose your preferred region
   - **Branch**: `main` (or your default branch)
   - **Language**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements-dev.txt
     ```
   - **Start Command**: 
     ```bash
     python entrypoint/server.py
     ```

4. **Set Environment Variables:**
   - Go to **Environment** section
   - Add:
     ```
     GOOGLE_API_KEY=your-google-factcheck-key
     FACT_CHECKER_API_KEY=your-rapidapi-key
     GEMINI_API_KEY=your-gemini-key
     ```
     **Note:** Do NOT set PORT manually. Render automatically sets the PORT environment variable.

5. **Configure Health Check:**
   - **Health Check Path**: `/v1/health`

6. **Choose Instance Type:**
   - **Free**: For testing (512MB RAM limit, spins down after inactivity)
   - **Starter**: Recommended for production (512MB RAM, $7/month)
   - **Standard**: For high-traffic production (2GB RAM, $25/month)
   
   **Important:** The free tier has a 512MB memory limit. If you get "Out of memory" errors, upgrade to Starter or Standard plan.

7. **Click "Create Web Service"**

## Port Configuration

The application is automatically configured to work with Render's port requirements:

- **Binds to**: `0.0.0.0` (required by Render) - automatically set in production mode
- **Port**: Uses `PORT` environment variable (Render sets this automatically, default: 10000)
- **Host**: Automatically set to `0.0.0.0` in production mode

The server automatically detects when running on Render (by checking for PORT env var) and:
- Uses the `PORT` environment variable
- Binds to `0.0.0.0` instead of `127.0.0.1`
- Disables auto-reload (production mode)

## Environment Variables

Required environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google Fact Check Tools API key | Yes |
| `FACT_CHECKER_API_KEY` | RapidAPI Fact Checker API key | Yes |
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `PORT` | Server port (auto-set by Render) | No - **Do NOT set manually** |

## Accessing Your Deployed API

Once deployed, your API will be available at:

- **API Base URL**: `https://your-service-name.onrender.com`
- **API Documentation**: `https://your-service-name.onrender.com/docs`
- **ReDoc**: `https://your-service-name.onrender.com/redoc`
- **Health Check**: `https://your-service-name.onrender.com/v1/health`

## Testing the Deployment

After deployment, test your API:

```bash
# Health check
curl https://your-service-name.onrender.com/v1/health

# Test validation endpoint
curl -X POST "https://your-service-name.onrender.com/v1/validate" \
  -H "Content-Type: application/json" \
  -d '{"text": "The Eiffel Tower will be demolished next year"}'
```

## Troubleshooting

### Port Binding Issues

If you see "Port scan timeout reached, no open ports detected":

- **Verify start command**: Make sure it's `python entrypoint/server.py`
- **Check logs**: Look for errors in Render Dashboard logs
- **Verify PORT env var**: Render sets this automatically - do NOT set it manually
- **Check server output**: The server should print "Starting FactScreen API server in production mode..."

**Solution:** The server automatically detects Render environment and binds correctly. Check the logs to see if the server started successfully.

### Memory Issues

If you encounter "Out of memory (used over 512Mi)" errors:

1. **Upgrade to Starter plan** ($7/month) - Recommended minimum for ML workloads
2. **Optimize dependencies**: The build command uses `--no-cache-dir` to reduce memory during build
3. **Reduce model loading**: Consider lazy loading models or using smaller models
4. **Monitor memory usage**: Check Render dashboard metrics

**For production with ML models, Starter plan or higher is strongly recommended.**

### Build Fails

- Check that `requirements-dev.txt` is in the repository
- Verify Python version (should be 3.10+)
- Check build logs in Render Dashboard for specific errors

### Service Won't Start

- Verify all environment variables are set
- Check that `entrypoint/server.py` exists and is executable
- Review service logs in Render Dashboard
- Verify the health check endpoint `/v1/health` exists

### Health Check Fails

- Verify `/v1/health` endpoint exists
- Check that the service is actually running
- Review logs for errors
- Ensure the server bound to the correct port

## Updating Your Deployment

Render automatically redeploys when you push to your connected branch. To manually redeploy:

1. Go to your service in Render Dashboard
2. Click **Manual Deploy > Deploy latest commit**

## Custom Domain

To add a custom domain:

1. Go to your service settings
2. Navigate to **Custom Domains**
3. Add your domain
4. Follow DNS configuration instructions

## Monitoring

- **Logs**: Available in real-time in Render Dashboard
- **Metrics**: View CPU, memory, and request metrics
- **Alerts**: Set up alerts for service downtime

## Free Tier Limitations

If using the free tier:

- **512MB RAM limit** - May cause "Out of memory" errors with ML models
- Service spins down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- Limited to 750 hours/month
- No persistent disk (logs are ephemeral)

**For production with ML models, Starter plan or higher is strongly recommended.**

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [Render Web Services Guide](https://render.com/docs/web-services)
- [Render Port Binding](https://render.com/docs/web-services#port-binding)

