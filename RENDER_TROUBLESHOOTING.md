# Render Deployment Troubleshooting: "No Open Ports Detected"

## Problem
Render shows error: **"Port scan timeout reached, no open ports detected"**

This means Render cannot detect that your application is listening on a port.

## Solution 1: Use render_start.py (Recommended)

I've created a dedicated startup script for Render. Make sure:

1. ✅ `render_start.py` is in your repository root
2. ✅ `render.yaml` uses: `startCommand: python render_start.py`
3. ✅ Push both files to your repository

## Solution 2: Check Your Logs

In Render Dashboard:
1. Go to your service
2. Click on **Logs** tab
3. Look for errors during startup

Common issues to check:
- ❌ Import errors (missing dependencies)
- ❌ Port binding errors
- ❌ Application crashes before binding to port
- ❌ Environment variable issues

## Solution 3: Verify Start Command

Your `render.yaml` should have:

```yaml
startCommand: python render_start.py
```

**Alternative commands to try** (if render_start.py doesn't work):

**Option A: Direct uvicorn with shell expansion**
```yaml
startCommand: sh -c "uvicorn src.app.main:app --host 0.0.0.0 --port ${PORT:-10000}"
```

**Option B: Python one-liner**
```yaml
startCommand: python -c "import os; import uvicorn; uvicorn.run('src.app.main:app', host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))"
```

**Option C: Direct uvicorn (if PORT is set correctly)**
```yaml
startCommand: uvicorn src.app.main:app --host 0.0.0.0 --port $PORT
```

## Solution 4: Verify Requirements

Make sure your `requirements-dev.txt` includes:
- ✅ `uvicorn[standard]>=0.32.0`
- ✅ `fastapi>=0.115.0`
- ✅ All other dependencies

## Solution 5: Check Environment Variables

In Render Dashboard → Environment section, verify:
- ✅ `GOOGLE_API_KEY` is set
- ✅ `FACT_CHECKER_API_KEY` is set
- ✅ `GEMINI_API_KEY` is set
- ❌ **DO NOT** set `PORT` manually (Render sets this automatically)

## Solution 6: Test Locally First

Before deploying, test that the app starts correctly:

```bash
# Set PORT environment variable (simulating Render)
export PORT=10000

# Test the startup script
python render_start.py
```

The server should start and you should see:
```
Starting FactScreen API on Render...
Host: 0.0.0.0
Port: 10000
```

## Solution 7: Check Application Code

Make sure `src/app/main.py` exists and the FastAPI app is named `app`:

```python
from fastapi import FastAPI
app = FastAPI(...)  # Must be named 'app'
```

## Solution 8: Memory Issues (Free Tier)

If you're on free tier and getting memory errors:
- The app might crash before binding to port
- Check logs for "Out of memory" errors
- Consider upgrading to Starter plan ($7/month)

## Solution 9: Health Check Configuration

Make sure your health check path exists:

```yaml
healthCheckPath: /v1/health
```

And that your API has this endpoint:
```python
@app.get("/v1/health")
async def health():
    return {"status": "healthy"}
```

## Debugging Steps

1. **Check Build Logs**: Look for errors during `pip install`
2. **Check Runtime Logs**: Look for errors when starting the app
3. **Verify PORT is Set**: Add this to your startup script temporarily:
   ```python
   print(f"PORT env var: {os.environ.get('PORT')}")
   ```
4. **Test Import**: Make sure all imports work:
   ```python
   python -c "from src.app.main import app; print('Import successful')"
   ```

## Common Causes

1. **Process exits too quickly**: App crashes before binding to port
2. **Wrong host binding**: Not binding to `0.0.0.0` (must be `0.0.0.0`, not `127.0.0.1`)
3. **Port not read correctly**: PORT environment variable not being read
4. **Missing dependencies**: Import errors cause app to crash
5. **Memory issues**: App runs out of memory on free tier

## Still Not Working?

1. **Check Render Status Page**: https://status.render.com
2. **Review Render Docs**: https://render.com/docs/web-services
3. **Check Service Logs**: Look for any error messages
4. **Try Manual Deploy**: In Render Dashboard → Manual Deploy → Deploy latest commit

## Quick Fix Checklist

- [ ] `render_start.py` exists in repository root
- [ ] `render.yaml` has correct `startCommand`
- [ ] All environment variables are set (except PORT)
- [ ] `requirements-dev.txt` includes uvicorn
- [ ] `src/app/main.py` exists with `app = FastAPI(...)`
- [ ] Health check endpoint `/v1/health` exists
- [ ] Code is pushed to repository
- [ ] Service is redeployed after changes

## Test Your Fix

After making changes:

1. Push to repository
2. Wait for Render to redeploy
3. Check logs for "Starting FactScreen API on Render..."
4. Check logs for "Uvicorn running on http://0.0.0.0:XXXX"
5. Test health endpoint: `curl https://your-service.onrender.com/v1/health`

If you see the uvicorn startup message in logs, the port should be detected!

