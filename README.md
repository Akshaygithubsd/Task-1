# Flask + Firestore Customer Management System

This is a complete Flask application that demonstrates CRUD (Create, Read, Update, Delete) operations with Google Cloud Firestore.

## Features

- ✅ **Create**: Add new customer entries with name, email and phone number
- ✅ **Read**: View all customers or search by name/email
- ✅ **Update**: Modify existing customer details
- ✅ **Delete**: Remove customer entries from the collection

## Prerequisites

1. **Python 3.7+** should be installed on your system
2. **Google Cloud Project** with Firestore enabled
3. **Service Account Key** with Firestore permissions

## Setup Instructions

### 1. Install Dependencies

```
pip install -r requirements.txt
```

### 2. Set Up Google Cloud Firestore

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Cloud Firestore API**:
   - Navigate to APIs & Services > Library
   - Search for Cloud Firestore API
   - Click "Enable"

4.  Create/Initialize Firestore Database
   - Navigate to: https://console.cloud.google.com/firestore
   - Or visit: https://console.cloud.google.com/datastore/setup?project=YOUR_PROJECT_ID
   - Click Create Database
   - Choose Native Mode
   - Select a location (e.g. us-central)
   - Click "Create"
   -the database instance must be created before use!

5. Create a Service Account:
   - Go to IAM & Admin > Service Accounts
   - Click Create Service Account
   - Give it a name (e.g., "firestore-service")
   - Grant it the role: Cloud Datastore User or Firestore User
   - Click Create Key and download the JSON key file

### 4. Configure Authentication

**Option A: Environment Variable (Recommended)**
```bash
# Windows PowerShell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\service-account-key.json"

# Windows CMD
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service-account-key.json

# Linux/Mac
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
```

**Option B: Modify app.py**
You can also modify the `app.py` file to directly specify the path:
```python
from google.cloud import firestore
import os

# Option 1: Use environment variable (recommended)
db = firestore.Client()

# Option 2: Specify credentials directly
# from google.oauth2 import service_account
# credentials = service_account.Credentials.from_service_account_file(
#     "path/to/service-account-key.json"
# )
# db = firestore.Client(credentials=credentials, project="your-project-id")
```

### 5. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and set your secret key:
   ```
   SECRET_KEY=your-random-secret-key-here
   ```

### 6. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`


#### Get All Customers
```bash
GET /api/customers
```


## Firestore Database Structure

The application uses a collection named **"Customer"** with the following structure:

```
Customer (Collection)
├── {document_id}
    ├── name: string
    ├── email: string
    └── phone: string (optional)
```

## Project Structure

```
Task 2/
├── app.py                 # Main Flask app
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables 
├── README.md             # This file
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Customer list page
    ├── add_customer.html # Add customer form
    └── edit_customer.html # Edit customer form
```


