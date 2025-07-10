# CST8917 Assignment 1: Azure Durable Functions Image Processing Pipeline

> **All documentation is included in this file.**

---

## 📋 Project Overview

This assignment implements an Azure Durable Functions pipeline for image metadata processing, combining Lab 1 (Queue and SQL dual output) and Lab 2 (Blob trigger and image processing). The solution processes uploaded images, extracts metadata, stores it in SQL database, sends messages to queues, and generates processing reports.

---

## 🎯 Assignment Requirements Met & Summary

- ✅ **Lab 1 Integration**: Queue output, SQL database storage, dual output system
- ✅ **Lab 2 Integration**: Blob trigger, image processing, metadata extraction
- ✅ **Assignment 1**: Durable Functions pipeline, error handling, local & Azure deployment, comprehensive verification, full English documentation

**Status**: ✅ **READY FOR SUBMISSION**
**Date**: July 10, 2025
**Student**: CST8917 Assignment 1

---

## 🏗️ Architecture

```
Image Upload → Blob Trigger → Metadata Extraction → SQL Storage → Queue Message → Report Generation
```

### Components:
- **Azure Blob Storage**: Input/output containers
- **Azure Function App**: Python-based blob trigger function
- **Azure SQL Database**: Metadata storage
- **Azure Storage Queue**: Processing notifications
- **PIL (Python Imaging Library)**: Image metadata extraction

---

## 📁 Project Structure & File List

```
as1/
├── function_app/
│   ├── __init__.py          # Main function code (English)
│   └── function.json        # Function configuration (English)
├── requirements.txt         # Python dependencies (English)
├── local.settings.json      # Local development settings (English)
├── host.json                # Function app configuration (English)
├── verify_results.py        # Verification script (English)
├── test_azure_upload.py     # Azure testing script (English)
├── final_test.py            # Complete system test (English)
├── README.md                # Comprehensive documentation (English)
```

| File | Purpose |
|------|---------|
| `function_app/__init__.py` | Main function implementation |
| `function_app/function.json` | Function configuration |
| `requirements.txt` | Python dependencies |
| `local.settings.json` | Local development settings |
| `host.json` | Function app configuration |
| `verify_results.py` | Verification script |
| `test_azure_upload.py` | Azure testing script |
| `final_test.py` | Complete system test |
| `README.md` | Main documentation |

---

## 🚀 Setup and Deployment

### Prerequisites
- Azure CLI installed
- Python 3.10+
- Azure Functions Core Tools
- Azure subscription

### 1. Local Development Setup

```bash
pip install -r requirements.txt
# Update local.settings.json with your Azure connection strings
func start
```

### 2. Azure Deployment

```bash
az functionapp create \
  --name cst8917-assignment1-func \
  --resource-group cst8917-assignment1-rg \
  --storage-account cst8917assignment1sa \
  --consumption-plan-location canadacentral \
  --runtime python \
  --runtime-version 3.10 \
  --functions-version 4 \
  --os-type Linux

az functionapp config appsettings set \
  --name cst8917-assignment1-func \
  --resource-group cst8917-assignment1-rg \
  --settings "SqlConnectionString=Driver={ODBC Driver 18 for SQL Server};Server=tcp:cst8917-assignment1-sql.database.windows.net,1433;Database=ImageMetadataDB;Uid=cst8917admin;Pwd=Azure@8917;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

func azure functionapp publish cst8917-assignment1-func
```

---

## 🔧 Configuration

- **Resource Group**: `cst8917-assignment1-rg`
- **Storage Account**: `cst8917assignment1sa`
- **SQL Server**: `cst8917-assignment1-sql`
- **Database**: `ImageMetadataDB`
- **Function App**: `cst8917-assignment1-func`
- **AzureWebJobsStorage**: Storage account connection string
- **SqlConnectionString**: SQL database connection string

---

## 🧪 Testing & Verification

### Python Script Verification
- `python verify_results.py` — Checks local settings, files, SQL, queue, blob storage
- `python test_azure_upload.py` — Uploads test image to Azure, triggers function
- `python final_test.py` — Runs all tests and prints summary

### Azure Portal Verification
- **SQL Database**: Query `ImageMetadata` table for records
- **Storage Account**: Check `images-input` and `output` containers
- **Queue**: Check `image-processing-queue` for messages
- **Function App**: View logs and execution history

### KQL Query Verification (Application Insights)
- Go to Function App → Application Insights → Logs (Analytics)
- Paste and run KQL queries below

---

## 📊 KQL Query Examples

### 1. Basic Log Queries
```kql
// View all Function App logs
traces
| where timestamp > ago(1h)
| where cloud_RoleName == "cst8917-assignment1-func"
| order by timestamp desc

// View function execution logs
traces
| where timestamp > ago(1h)
| where cloud_RoleName == "cst8917-assignment1-func"
| where message contains "function_app"
| order by timestamp desc
```

### 2. Function Execution Details
```kql
// View function execution success/failure
traces
| where timestamp > ago(1h)
| where cloud_RoleName == "cst8917-assignment1-func"
| where message contains "Executed" or message contains "Failed"
| project timestamp, message, severityLevel
| order by timestamp desc

// View Blob Trigger execution
traces
| where timestamp > ago(1h)
| where cloud_RoleName == "cst8917-assignment1-func"
| where message contains "blobTrigger" or message contains "Image uploaded"
| project timestamp, message
| order by timestamp desc
```

### 3. Error and Exception Queries
```kql
// View error logs
traces
| where timestamp > ago(1h)
| where cloud_RoleName == "cst8917-assignment1-func"
| where severityLevel == 3
| project timestamp, message, customDimensions
| order by timestamp desc

// View exceptions
exceptions
| where timestamp > ago(1h)
| where cloud_RoleName == "cst8917-assignment1-func"
| project timestamp, type, message, operation_Name
| order by timestamp desc
```

### 4. Performance Monitoring
```kql
// View function execution time
traces
| where timestamp > ago(1h)
| where cloud_RoleName == "cst8917-assignment1-func"
| where message contains "Duration"
| project timestamp, message
| order by timestamp desc

// View memory usage
performanceCounters
| where timestamp > ago(1h)
| where cloud_RoleName == "cst8917-assignment1-func"
| where name contains "Memory"
| project timestamp, name, value
| order by timestamp desc
```

### 5. Custom Queries - Assignment 1 Specific
```kql
// View image processing workflow
traces
| where timestamp > ago(1h)
| where cloud_RoleName == "cst8917-assignment1-func"
| where message contains "Image uploaded" or 
      message contains "Metadata extracted" or
      message contains "SQL Database Save" or
      message contains "Queue Send" or
      message contains "Processing report"
| project timestamp, message, severityLevel
| order by timestamp desc

// View SQL database operations
traces
| where timestamp > ago(1h)
| where cloud_RoleName == "cst8917-assignment1-func"
| where message contains "SQL" or message contains "database"
| project timestamp, message
| order by timestamp desc

// View queue operations
traces
| where timestamp > ago(1h)
| where cloud_RoleName == "cst8917-assignment1-func"
| where message contains "Queue" or message contains "queue"
| project timestamp, message
| order by timestamp desc
```

### 6. Real-time Monitoring Queries
```kql
// Real-time function execution monitoring
traces
| where timestamp > ago(10m)
| where cloud_RoleName == "cst8917-assignment1-func"
| where message contains "Executing" or message contains "Executed"
| project timestamp, message
| order by timestamp desc

// View recent errors
traces
| where timestamp > ago(30m)
| where cloud_RoleName == "cst8917-assignment1-func"
| where severityLevel >= 2
| project timestamp, message, severityLevel
| order by timestamp desc
```

#### How to Use in Azure Portal
1. Go to Function App → Application Insights → Logs (Analytics)
2. Paste the above KQL queries in the query editor
3. Click "Run" to execute the query
4. Save queries or create dashboards as needed

---

## 📈 Expected Results & Checklist

### Successful Processing Flow:
1. **Image Upload**: `test_azure_apple.png` uploaded to blob container
2. **Blob Trigger**: Function automatically triggered
3. **Metadata Extraction**: Image properties extracted (2400x1889, PNG, 560.28KB)
4. **SQL Storage**: Metadata saved to `ImageMetadata` table
5. **Queue Message**: Processing notification sent to queue
6. **Report Generation**: Processing report saved to output container

### Verification Checklist:
- ✅ Function App deployed and running
- ✅ Blob trigger automatically triggered
- ✅ Metadata correctly extracted
- ✅ SQL database operations successful
- ✅ Queue messages sent
- ✅ Processing reports generated
- ✅ Error handling working
- ✅ Logging comprehensive

---

## 🔍 Troubleshooting & Support

### Common Issues
- ODBC Driver Issues: `brew install msodbcsql18`
- Connection String Issues: Check format, firewall, credentials
- Function App Deployment Issues: Check Azure CLI login, resource group, Python version

### Debug Commands
```bash
az account show
az functionapp list --resource-group cst8917-assignment1-rg
az functionapp logs tail --name cst8917-assignment1-func --resource-group cst8917-assignment1-rg
```

For issues or questions:
- Check troubleshooting section
- Review Azure Portal logs
- Verify configuration settings
- Test with provided verification scripts

---

## 🎉 Final Status

- ✅ All files are English only
- ✅ All files are assignment related
- ✅ All requirements and features implemented
- ✅ Comprehensive documentation and verification
- ✅ Ready for submission 