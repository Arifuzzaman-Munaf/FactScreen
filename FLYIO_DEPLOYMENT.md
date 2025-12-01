# Deploying FactScreen API to Fly.io (Free Tier)

This guide will help you deploy your FactScreen API backend to Fly.io's free tier.

## Prerequisites

1. A [Fly.io account](https://fly.io/app/sign-up) (free)
2. Your code pushed to a Git repository (GitHub recommended)
3. Your API keys ready:
   - `GOOGLE_API_KEY` (Google Fact Check API)
   - `FACT_CHECKER_API_KEY` (RapidAPI Fact Checker)
   - `GEMINI_API_KEY` (Google Gemini API)

## Quick Deploy Steps

### Step 1: Install Fly CLI

**macOS/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

**Or using Homebrew (macOS):**
```bash
brew install flyctl
```

### Step 2: Login to Fly.io

```bash
fly auth login
```

This will open your browser to authenticate. If you don't have an account, you can sign up during this process.

### Step 3: Initialize Your App

Navigate to your project directory and run:

```bash
fly launch
```

This command will:
- Detect your Dockerfile
- Ask for an app name (or use the default)
- Ask for a region (choose closest to your users)
- Ask if you want to set up a Postgres database (optional - say no for now)
- Ask if you want to deploy now (say yes)

### Step 4: Set Environment Variables

After the initial deployment, set your API keys:

```bash
fly secrets set GOOGLE_API_KEY=your-google-factcheck-key
fly secrets set FACT_CHECKER_API_KEY=your-rapidapi-key
fly secrets set GEMINI_API_KEY=your-gemini-key
```

**Or set them all at once:**
```bash
fly secrets set \
  GOOGLE_API_KEY=your-google-factcheck-key \
  FACT_CHECKER_API_KEY=your-rapidapi-key \
  GEMINI_API_KEY=your-gemini-key
```

### Step 5: Deploy

If you didn't deploy during `fly launch`, deploy now:

```bash
fly deploy
```

Fly.io will:
- Build your Docker image
- Push it to Fly.io
- Deploy your app
- Show you the URL

## Access Your Deployed API

Once deployed, your API will be available at:
- **API Base URL**: `https://factscreen-api.fly.dev` (or your custom app name)
- **API Documentation**: `https://factscreen-api.fly.dev/docs`
- **ReDoc**: `https://factscreen-api.fly.dev/redoc`
- **Health Check**: `https://factscreen-api.fly.dev/v1/health`

## Verify Deployment

Test your deployed API:

```bash
# Health check
curl https://factscreen-api.fly.dev/v1/health

# Test validation endpoint
curl -X POST "https://factscreen-api.fly.dev/v1/validate" \
  -H "Content-Type: application/json" \
  -d '{"text": "The Eiffel Tower will be demolished next year"}'
```

## Configuration Files

Your project includes:

- **`fly.toml`** - Fly.io configuration (app name, region, ports, etc.)
- **`Dockerfile`** - Docker image configuration
- **`.dockerignore`** - Files to exclude from Docker build

### Customizing fly.toml

You can edit `fly.toml` to:
- Change app name
- Change region
- Adjust memory/CPU limits
- Configure auto-scaling

**Important:** After changing `fly.toml`, run:
```bash
fly deploy
```

## Fly.io Free Tier

**Free tier includes:**
- **3 shared-cpu-1x VMs** (256MB RAM each)
- **3GB persistent volume storage**
- **160GB outbound data transfer**
- **No credit card required** for free tier

**Limitations:**
- Apps may spin down after inactivity (auto-start on request)
- Shared CPU (not dedicated)
- Limited to 3 VMs

## Managing Your Deployment

### View Logs

```bash
# Real-time logs
fly logs

# Follow logs
fly logs -a factscreen-api
```

### Check App Status

```bash
fly status
```

### Open App in Browser

```bash
fly open
```

### SSH into Your App

```bash
fly ssh console
```

### Scale Your App

```bash
# Scale to 2 instances
fly scale count 2

# Scale memory
fly scale memory 512
```

## Updating Your Deployment

### Automatic Updates

Fly.io doesn't auto-deploy from Git. You need to manually deploy:

```bash
fly deploy
```

### Update Environment Variables

```bash
# Set new secret
fly secrets set NEW_VAR=value

# List all secrets
fly secrets list

# Remove a secret
fly secrets unset VAR_NAME
```

## Troubleshooting

### Build Fails

**Check Dockerfile:**
- Ensure `requirements-dev.txt` exists
- Verify Python version (3.10+)
- Check build logs: `fly logs`

**Common issues:**
- Missing dependencies in requirements-dev.txt
- Docker build context issues
- Memory limits during build

### App Won't Start

**Check logs:**
```bash
fly logs
```

**Common issues:**
- Missing environment variables
- Port binding issues (should bind to 0.0.0.0:8000)
- Import errors

### Memory Issues

**Check memory usage:**
```bash
fly status
```

**Increase memory:**
```bash
fly scale memory 512
```

**Note:** Free tier has limited memory. Consider:
- Optimizing dependencies
- Removing unused packages
- Using smaller ML models

### Health Check Fails

**Verify health endpoint:**
```bash
curl https://factscreen-api.fly.dev/v1/health
```

**Check fly.toml:**
- Ensure `http_checks` path is `/v1/health`
- Verify `internal_port` matches your app (8000)

## Custom Domain

To add a custom domain:

1. **Add domain:**
   ```bash
   fly certs add yourdomain.com
   ```

2. **Follow DNS instructions** shown by Fly.io

3. **Verify:**
   ```bash
   fly certs show yourdomain.com
   ```

## Monitoring

### View Metrics

```bash
fly metrics
```

### View Dashboard

```bash
fly dashboard
```

Or visit: https://fly.io/dashboard

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/fly-deploy.yml`:

```yaml
name: Fly Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    name: Deploy app
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

Get your Fly API token:
```bash
fly auth token
```

Add it to GitHub Secrets as `FLY_API_TOKEN`.

## Cost Management

**Free tier limits:**
- 3 VMs max
- Shared CPU
- 160GB outbound data

**To stay within free tier:**
- Use auto-stop/auto-start (already configured)
- Monitor usage: `fly dashboard`
- Scale down when not needed: `fly scale count 1`

## Additional Resources

- [Fly.io Documentation](https://fly.io/docs)
- [Fly.io Pricing](https://fly.io/docs/about/pricing/)
- [Fly.io Examples](https://fly.io/docs/languages-and-frameworks/)
- [Fly.io Community](https://community.fly.io)

## Quick Reference Commands

```bash
# Deploy
fly deploy

# View logs
fly logs

# Check status
fly status

# Open app
fly open

# Set secrets
fly secrets set KEY=value

# Scale
fly scale count 2

# SSH
fly ssh console

# Dashboard
fly dashboard
```

## Next Steps

1. ✅ Deploy your API to Fly.io
2. ✅ Test all endpoints
3. ✅ Set up custom domain (optional)
4. ✅ Configure CI/CD (optional)
5. ✅ Monitor usage and scale as needed

Your FactScreen API is now live on Fly.io! 🚀

