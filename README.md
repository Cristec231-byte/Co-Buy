# Co-Buy API

A FastAPI application for managing shared purchasing.

## Local Development

1. Install dependencies:
```bash
pip install -r app/requirements.txt
```

2. Set up your local database and update the DATABASE_URL in `app/database.py`

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## Railway Deployment

This application is configured for deployment on Railway.

### Prerequisites
- A Railway account
- A GitHub repository with this code

### Deployment Steps

1. **Connect Repository to Railway:**
   - Go to [railway.app](https://railway.app)
   - Create a new project
   - Connect your GitHub repository

2. **Add a PostgreSQL Database:**
   - In your Railway project dashboard
   - Click "New Service" → "Database" → "PostgreSQL"
   - Railway will automatically provide a `DATABASE_URL` environment variable

3. **Deploy the Application:**
   - Railway will automatically detect this is a Python application
   - It will use the `railway.json` configuration and `Procfile`
   - The app will be available at your Railway-provided URL

### Environment Variables

The following environment variables are automatically provided by Railway:
- `DATABASE_URL` - PostgreSQL connection string
- `PORT` - Port number for the application

### API Endpoints

- `GET /` - Health check
- `POST /items/` - Create a new item
- `GET /items/` - Get all items
- `GET /items/{item_id}` - Get a specific item
- `PUT /items/{item_id}` - Update an item
- `DELETE /items/{item_id}` - Delete an item

## Project Structure

```
Co-Buy/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # Database operations
│   ├── database.py      # Database configuration
│   └── requirements.txt # Python dependencies
├── Procfile            # Railway process configuration
├── railway.json        # Railway deployment configuration
└── README.md          # This file
```
