# 🚀 Deploy to Vercel - Step by Step Guide

## ✅ Code Changes Complete!

All necessary code changes have been made for Vercel deployment. Here's what was configured:

### Files Created/Modified:
- ✅ `vercel.json` - Vercel deployment configuration
- ✅ `build.sh` - Build script for static files
- ✅ `sih_prototype/wsgi.py` - Updated for serverless deployment
- ✅ `sih_prototype/settings.py` - Added Vercel-specific settings
- ✅ All dependencies already in `requirements.txt`

---

## 📋 Deployment Steps

### Step 1: Push Code to GitHub

Make sure all your latest changes are on GitHub:

```powershell
# Check status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Configure for Vercel deployment with PostgreSQL"

# Push to GitHub
git push origin master
```

---

### Step 2: Sign Up for Vercel

1. Go to https://vercel.com
2. Click **"Sign Up"**
3. Choose **"Continue with GitHub"**
4. Authorize Vercel to access your GitHub account

---

### Step 3: Import Your Project

1. After logging in, click **"Add New..."** → **"Project"**
2. You'll see a list of your GitHub repositories
3. Find **"sih-project"** and click **"Import"**

---

### Step 4: Configure Project Settings

On the import page, you'll see configuration options:

#### Framework Preset:
- Select: **"Other"** (since it's Django)

#### Root Directory:
- Leave as: **"."** (root)

#### Build Command:
- Leave as default or enter: `chmod +x build.sh && ./build.sh`

#### Output Directory:
- Leave blank

#### Install Command:
- Leave as default: `pip install -r requirements.txt`

---

### Step 5: Add Environment Variables

This is **CRITICAL**! Click **"Environment Variables"** section and add:

#### Required Variables:

| Name | Value |
|------|-------|
| `DATABASE_URL` | Your Neon.tech PostgreSQL connection string |
| `SECRET_KEY` | `django-insecure-9s6fa3z#71al1p%rv7yn0yopn-3xj*4xpxz+sb3o6em%7dhw!d` |
| `DEBUG` | `False` |
| `STREAM_API_KEY` | `ygzv4mky4dz3` |
| `STREAM_API_SECRET` | `h4yq4uqqmahp48zvxs6b4dxbq4x3q9ute79uqkdsauwy2ky5z4durtv73g8v5ssq` |

**Your DATABASE_URL should look like:**
```
postgresql://username:password@ep-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

⚠️ **Important**: Make sure to select **"Production"** for all environment variables!

---

### Step 6: Deploy

1. After adding environment variables, click **"Deploy"**
2. Vercel will start building your project (takes 2-5 minutes)
3. Watch the build logs - you'll see:
   - Installing dependencies
   - Collecting static files
   - Deploying to serverless functions

---

### Step 7: Run Migrations (First Time Only)

After the first deployment succeeds:

1. Click on your project in Vercel dashboard
2. Go to **"Settings"** → **"Functions"**
3. Or use Vercel CLI to run migrations:

```powershell
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Link to your project
vercel link

# Run migrations remotely (use your local terminal)
```

**Easier method**: Run migrations locally against your Neon database:

```powershell
# Make sure your .env has the DATABASE_URL
python manage.py migrate
python manage.py createsuperuser
```

Since both local and Vercel use the same Neon.tech database, migrations will apply to both!

---

### Step 8: Visit Your Live Site! 🎉

1. After deployment completes, you'll see: **"Your project has been deployed"**
2. Click on the **"Visit"** button or copy the URL
3. Your site will be live at: `https://your-project-name.vercel.app`

Example: `https://sih-project.vercel.app`

---

## 🧪 Testing Your Deployment

Test these features:

- ✅ Homepage loads
- ✅ Sign up / Login works
- ✅ Database queries work (journal entries, appointments, etc.)
- ✅ Stream Chat peer messaging works
- ✅ Admin panel: `https://your-app.vercel.app/admin`

---

## 🔧 Troubleshooting

### Issue: "Application error"

**Solution**: Check deployment logs in Vercel dashboard
- Go to your project → Deployments → Click on latest deployment → View logs

### Issue: "Database connection error"

**Solution**: Verify environment variables
- Go to Settings → Environment Variables
- Make sure `DATABASE_URL` is correct
- Must include `?sslmode=require` at the end

### Issue: "Static files not loading"

**Solution**: 
```powershell
# Locally run
python manage.py collectstatic --noinput

# Commit and push
git add staticfiles/
git commit -m "Add collected static files"
git push
```

### Issue: "CSRF verification failed"

**Solution**: Check that your Vercel domain is in `CSRF_TRUSTED_ORIGINS`
- Should be automatic with `https://*.vercel.app` in settings

---

## 🔄 Updating Your Site

Every time you push to GitHub, Vercel automatically redeploys:

```powershell
git add .
git commit -m "Update feature X"
git push origin master
```

Vercel detects the push and redeploys automatically! 🚀

---

## 💡 Tips

### Custom Domain (Optional):
1. Go to project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

### View Logs:
- Real-time logs available in Vercel dashboard
- Useful for debugging production issues

### Environment Variables Updates:
- If you change env vars, trigger a redeployment
- Go to Deployments → Click "..." → Redeploy

---

## 📊 What You Get with Vercel Free Tier:

✅ **Unlimited deployments**  
✅ **Automatic HTTPS**  
✅ **Global CDN**  
✅ **Automatic scaling**  
✅ **Preview deployments** (for PRs)  
✅ **100GB bandwidth/month**  
✅ **Great for portfolios and demos**

---

## 🎯 Next Steps After Successful Deployment:

1. ✅ Create superuser account (if not done already)
2. ✅ Test all features on live site
3. ✅ Share your Vercel URL in your SIH submission
4. ✅ Monitor usage in Vercel dashboard
5. ✅ Add custom domain (optional)

---

## 📞 Need Help?

If you encounter issues during deployment:

1. Check Vercel build logs
2. Verify all environment variables are set
3. Make sure DATABASE_URL is correct
4. Test database connection locally first

---

## ✨ Your Site Will Be Live At:

```
https://sih-project-[random-id].vercel.app
```

**Good luck with your deployment!** 🚀

---

### Quick Command Reference:

```powershell
# Push to GitHub
git add .
git commit -m "Deploy to Vercel"
git push origin master

# Run migrations locally (applies to Neon.tech DB)
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```
