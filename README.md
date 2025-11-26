# Flask + Firestore Customer Management System

A complete Flask application that demonstrates CRUD (Create, Read, Update, Delete) operations with Google Cloud Firestore.

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

## Usage

### Web Interface

1. **View All Customers**: Navigate to the home page (`/`)
2. **Add Customer**: Click "Add New Customer" button
3. **Search Customers**: Use the search bar to filter by name or email
4. **Edit Customer**: Click "Edit" button next to any customer
5. **Delete Customer**: Click "Delete" button (with confirmation)

### API Endpoints

The application also provides REST API endpoints:

#### Get All Customers
```bash
GET /api/customers
```

#### Create Customer
```bash
POST /api/customers
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890"
}
```

#### Update Customer
```bash
PUT /api/customers/{customer_id}
Content-Type: application/json

{
  "name": "John Doe Updated",
  "email": "john.updated@example.com",
  "phone": "+1234567890"
}
```

#### Delete Customer
```bash
DELETE /api/customers/{customer_id}
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

## Troubleshooting

### Error: "Could not automatically determine credentials"

**Solution**: Make sure you've set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your service account key file.

### Error: "Permission denied"

**Solution**: Ensure your service account has the necessary Firestore permissions (Cloud Datastore User or Firestore User role).

### Error: "Project not found"

**Solution**: Verify that your Google Cloud project ID is correct and Firestore is enabled for that project.

### Error: "The database (default) does not exist"

**Solution**: This is a common error! You need to **create the Firestore database instance** first:
1. Visit: https://console.cloud.google.com/firestore
2. Or use the direct link from the error message (e.g., `https://console.cloud.google.com/datastore/setup?project=task-479419`)
3. Click "Create Database"
4. Select **Native Mode** (not Datastore Mode)
5. Choose a location
6. Click "Create"
7. Wait for the database to be created (usually takes 1-2 minutes)
8. Then restart your Flask application

## Security Notes

- Never commit your service account key file to version control
- Use environment variables for sensitive configuration
- Change the `SECRET_KEY` in production
- Consider using Firestore security rules for production deployments

