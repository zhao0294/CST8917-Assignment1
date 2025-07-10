#!/usr/bin/env python3
"""
Assignment 1 Result Verification Script
Verify all Azure resources are working properly
"""

import json
import os
from datetime import datetime

def print_header(title):
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print(f"{'='*50}")

def verify_local_settings():
    """Verify local settings"""
    print_header("Local Settings Verification")
    
    try:
        with open('local.settings.json', 'r') as f:
            settings = json.load(f)
        
        required_settings = [
            'AzureWebJobsStorage',
            'SqlConnectionString'
        ]
        
        for setting in required_settings:
            if setting in settings['Values']:
                print(f"✅ {setting}: Configured")
            else:
                print(f"❌ {setting}: Not configured")
                
    except Exception as e:
        print(f"❌ Failed to read local.settings.json: {e}")

def verify_sql_database():
    """Verify SQL database"""
    print_header("SQL Database Verification")
    
    try:
        import pyodbc
        
        # Read connection string
        with open('local.settings.json', 'r') as f:
            settings = json.load(f)
            connection_string = settings['Values']['SqlConnectionString']
        
        # Connect to database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT COUNT(*) FROM ImageMetadata")
        count = cursor.fetchone()[0]
        print(f"✅ ImageMetadata table exists with {count} records")
        
        # Show latest records
        cursor.execute("""
            SELECT TOP 5 Id, FileName, Format, Width, Height, FileSizeKB, CreatedAt
            FROM ImageMetadata 
            ORDER BY CreatedAt DESC
        """)
        
        records = cursor.fetchall()
        if records:
            print("\n📊 Latest records:")
            for record in records:
                print(f"  - {record[1]} ({record[2]}, {record[3]}x{record[4]}, {record[5]:.2f}KB)")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ SQL database verification failed: {e}")

def verify_storage_queue():
    """Verify storage queue"""
    print_header("Storage Queue Verification")
    
    try:
        from azure.storage.queue import QueueClient
        
        # Read connection string
        with open('local.settings.json', 'r') as f:
            settings = json.load(f)
            connection_string = settings['Values']['AzureWebJobsStorage']
        
        # Connect to queue
        queue_client = QueueClient.from_connection_string(
            connection_string, 
            queue_name="image-processing-queue"
        )
        
        # Get queue properties
        properties = queue_client.get_queue_properties()
        print(f"✅ Queue exists with {properties.approximate_message_count} messages")
        
    except Exception as e:
        print(f"❌ Storage queue verification failed: {e}")

def verify_blob_storage():
    """Verify Blob storage"""
    print_header("Blob Storage Verification")
    
    try:
        from azure.storage.blob import BlobServiceClient
        
        # Read connection string
        with open('local.settings.json', 'r') as f:
            settings = json.load(f)
            connection_string = settings['Values']['AzureWebJobsStorage']
        
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Check input container
        input_container = blob_service_client.get_container_client("images-input")
        input_blobs = list(input_container.list_blobs())
        print(f"✅ images-input container: {len(input_blobs)} files")
        
        # Check output container
        output_container = blob_service_client.get_container_client("output")
        output_blobs = list(output_container.list_blobs())
        print(f"✅ output container: {len(output_blobs)} files")
        
        if output_blobs:
            print("\n📄 Output files:")
            for blob in output_blobs:
                print(f"  - {blob.name}")
        
    except Exception as e:
        print(f"❌ Blob storage verification failed: {e}")

def verify_function_app():
    """Verify function app"""
    print_header("Function App Verification")
    
    # Check function files
    function_files = [
        'function_app/__init__.py',
        'function_app/function.json',
        'host.json',
        'local.settings.json'
    ]
    
    for file_path in function_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}: Exists")
        else:
            print(f"❌ {file_path}: Missing")
    
    # Check dependencies
    try:
        import azure.functions
        import pyodbc
        from azure.storage.blob import BlobServiceClient
        from azure.storage.queue import QueueClient
        from PIL import Image
        
        print("✅ All dependencies installed")
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")

def main():
    """Main verification function"""
    print("🚀 Assignment 1 Result Verification")
    print(f"Verification time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    verify_local_settings()
    verify_function_app()
    verify_sql_database()
    verify_storage_queue()
    verify_blob_storage()
    
    print_header("Verification Complete")
    print("✅ If all items show ✅, Assignment 1 has been successfully completed!")

if __name__ == "__main__":
    main() 