# Quick Setup Guide

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Google Cloud Firestore

1. **Create/Select a Google Cloud Project**
   - Visit: https://console.cloud.google.com/
   - Create a new project or select existing one

2. **Enable Firestore API**
   - Go to: APIs & Services > Library
   - Search: "Cloud Firestore API"
   - Click: Enable

3. **⚠️ IMPORTANT: Create/Initialize Firestore Database**
   - Go to: https://console.cloud.google.com/firestore
   - Or visit: https://console.cloud.google.com/datastore/setup?project=YOUR_PROJECT_ID
   - Click: "Create Database" or "Select Native Mode"
   - Choose your location (e.g., us-central, europe-west, etc.)
   - Click: "Create"
   - **This step is REQUIRED** - the database must exist before you can use it!

4. **Create Service Account**
   - Go to: IAM & Admin > Service Accounts
   - Click: Create Service Account
   - Name: `firestore-service` (or any name)
   - Role: **Cloud Datastore User** or **Firestore User**
   - Click: Create Key > JSON > Download

5. **Set Environment Variable**

   **Windows PowerShell:**
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\service-account-key.json"
   ```

   **Windows CMD:**
   ```cmd
   set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service-account-key.json
   ```

   **Linux/Mac:**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
   ```

## Step 4: Run the Application

```bash
python app.py
```

Open your browser and go to: **http://localhost:5000**

## Step 5: Test the Application

1. Click "Add New Customer" to create your first customer
2. Try searching for customers by name or email
3. Edit a customer by clicking the "Edit" button
4. Delete a customer by clicking the "Delete" button

## Troubleshooting

**"Could not automatically determine credentials"**
- Make sure `GOOGLE_APPLICATION_CREDENTIALS` is set correctly
- Verify the path to your service account key file is correct

**"Permission denied"**
- Check that your service account has Firestore permissions
- Ensure the Firestore API is enabled in your project

**"Project not found"**
- Verify your Google Cloud project ID is correct
- Make sure Firestore is enabled for your project

**"The database (default) does not exist"**
- ⚠️ **This is the most common error!**
- You must CREATE the Firestore database first
- Visit: https://console.cloud.google.com/firestore
- Or use the direct link from the error message
- Click "Create Database" and follow the setup wizard
- Choose Native Mode (not Datastore Mode)
- Select a location and click "Create"

## Next Steps

- Read the full `README.md` for detailed documentation
- Explore the API endpoints for programmatic access
- Customize the templates in the `templates/` folder

