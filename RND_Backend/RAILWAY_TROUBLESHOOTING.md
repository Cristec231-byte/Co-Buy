# Railway Database Connection Troubleshooting Guide

## Common Issues and Solutions

### 1. **DATABASE_URL Not Set**
**Problem**: Railway not automatically setting DATABASE_URL environment variable
**Solution**: 
- Check Railway dashboard > Variables tab
- Manually add DATABASE_URL if missing
- Use format: `postgresql://user:password@host:port/database`

### 2. **Database Service Not Connected**
**Problem**: Database service not linked to backend service
**Solution**:
- Go to Railway dashboard
- Click on your backend service
- Go to "Variables" tab
- Click "New Variable" > "Add Reference"
- Select your PostgreSQL database service
- This should automatically create DATABASE_URL

### 3. **Wrong Database Credentials**
**Problem**: Hardcoded credentials are outdated
**Solution**:
- Check your PostgreSQL service in Railway dashboard
- Go to "Connect" tab
- Copy the latest connection string
- Update your environment variables

### 4. **SSL Configuration Issues**
**Problem**: SSL mismatch between Railway and local
**Solution**: Our code now handles this automatically
- Railway internal: `sslmode=disable`
- External connections: `sslmode=require`

### 5. **Network Connectivity Issues**
**Problem**: Services can't reach each other
**Solution**:
- Use Railway's internal networking: `postgres.railway.internal:5432`
- Make sure both services are in the same project
- Check Railway's service networking documentation

## Debugging Steps

1. **Check Environment Variables**:
   ```
   GET /debug
   ```

2. **Test Database Connection**:
   ```
   GET /test-db
   ```

3. **Check Railway Logs**:
   - Go to Railway dashboard
   - Click on your service
   - Check "Deployments" tab for logs

4. **Verify Database Service**:
   - Ensure PostgreSQL service is running
   - Check connection details in Railway dashboard

## Railway Setup Checklist

- [ ] PostgreSQL service created
- [ ] Backend service created  
- [ ] DATABASE_URL environment variable set
- [ ] Services are in the same Railway project
- [ ] Latest deployment is successful
- [ ] Database credentials are current

## Manual Database Connection Setup

If automatic setup fails, manually set these variables in Railway:

```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@postgres.railway.internal:5432/railway
PORT=8000
RAILWAY_ENVIRONMENT=production
```

Replace `YOUR_PASSWORD` with your actual PostgreSQL password from Railway dashboard.
