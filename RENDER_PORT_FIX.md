# Fixing "No Open Ports Detected" on Render

Based on [Render's documentation](https://render.com/docs/web-services#port-binding), your app must:
1. ✅ Bind to `0.0.0.0` (not `127.0.0.1`)
2. ✅ Use the `PORT` environment variable (default: 10000)
3. ✅ Keep the process running in the foreground

## Current Configuration

I've updated your `render.yaml` with the most reliable approach per Render docs:

```yaml
startCommand: python -c "import os; import uvicorn; port = int(os.environ.get('PORT', 10000)); uvicorn.run('src.app.main:app', host='0.0.0.0', port=port)"
```

## What to Check in Render Logs

After deploying, check your Render Dashboard → Logs. You should see:

### ✅ Success Indicators:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000 (Press CTRL+C to quit)
```

### ❌ Failure Indicators:
- Import errors (missing dependencies)
- Configuration errors (missing config files)
- Memory errors (Out of memory)
- Port binding errors

## Alternative Start Commands to Try

If the current command doesn't work, try these in order:

### Option 1: Current (Python one-liner)
```yaml
startCommand: python -c "import os; import uvicorn; port = int(os.environ.get('PORT', 10000)); uvicorn.run('src.app.main:app', host='0.0.0.0', port=port)"
```

### Option 2: Using render_start.py
```yaml
startCommand: python render_start.py
```

### Option 3: Direct uvicorn (if PORT expands)
```yaml
startCommand: uvicorn src.app.main:app --host 0.0.0.0 --port $PORT
```

### Option 4: Shell expansion
```yaml
startCommand: sh -c "uvicorn src.app.main:app --host 0.0.0.0 --port ${PORT:-10000}"
```

## Common Causes & Solutions

### 1. App Crashes During Import
**Symptom**: Logs show import errors or tracebacks

**Solution**: 
- Check that all dependencies are in `requirements-dev.txt`
- Verify config files exist (`config/local.yaml`)
- Check for missing environment variables

### 2. App Crashes During Startup
**Symptom**: Logs show errors after "Application startup"

**Solution**:
- Check for missing API keys in environment variables
- Verify config file structure
- Check for ML model loading issues (memory problems)

### 3. Port Not Binding
**Symptom**: No "Uvicorn running on..." message

**Solution**:
- Ensure host is `0.0.0.0` (not `127.0.0.1`)
- Verify PORT is being read correctly
- Check that uvicorn is installed

### 4. Memory Issues (Free Tier)
**Symptom**: "Out of memory" errors

**Solution**:
- Free tier has 512MB limit
- Consider upgrading to Starter plan ($7/month)
- Or optimize model loading (lazy loading)

## Debugging Steps

1. **Check Build Logs**: Look for errors during `pip install`
2. **Check Runtime Logs**: Look for errors when starting the app
3. **Verify Environment Variables**: All API keys must be set
4. **Test Import Locally**:
   ```bash
   python -c "from src.app.main import app; print('Import successful')"
   ```
5. **Test Startup Locally**:
   ```bash
   export PORT=10000
   python render_start.py
   ```

## Quick Checklist

Before deploying:
- [ ] `render.yaml` has correct `startCommand`
- [ ] All environment variables are set in Render Dashboard
- [ ] `requirements-dev.txt` includes `uvicorn[standard]`
- [ ] `src/app/main.py` exists with `app = FastAPI(...)`
- [ ] Code is pushed to repository
- [ ] Service is set to redeploy

After deploying:
- [ ] Check logs for "Uvicorn running on..."
- [ ] Check logs for any error messages
- [ ] Test health endpoint: `curl https://your-service.onrender.com/v1/health`

## If Still Not Working

1. **Share your Render logs** - Look for the exact error message
2. **Check the Events tab** - See if build or deploy failed
3. **Try manual deploy** - Render Dashboard → Manual Deploy
4. **Verify service type** - Must be "Web Service" not "Background Worker"

## Reference

- [Render Web Services Docs](https://render.com/docs/web-services)
- [Render Port Binding](https://render.com/docs/web-services#port-binding)
- [Render Troubleshooting](https://render.com/docs/troubleshooting-deploys)

