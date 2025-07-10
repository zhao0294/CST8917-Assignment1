#!/usr/bin/env python3
"""
测试 Azure Function App 的脚本
上传图片到 Azure Blob 容器，触发函数执行
"""

import os
from azure.storage.blob import BlobServiceClient
import json

def upload_test_image():
    """Upload test image to Azure Blob container"""
    
    # Read connection string from local.settings.json
    try:
        with open('local.settings.json', 'r') as f:
            settings = json.load(f)
            connection_string = settings['Values']['AzureWebJobsStorage']
    except Exception as e:
        print(f"❌ Failed to read connection string: {e}")
        return
    
    # Create BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    # Get container client
    container_name = "images-input"
    container_client = blob_service_client.get_container_client(container_name)
    
    # Test image path
    test_image_path = "apple.png"
    
    if not os.path.exists(test_image_path):
        print(f"❌ Test image not found: {test_image_path}")
        return
    
    # Upload image
    blob_name = f"test_azure_{os.path.basename(test_image_path)}"
    
    try:
        with open(test_image_path, "rb") as data:
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.upload_blob(data, overwrite=True)
            print(f"✅ Successfully uploaded image to Azure: {blob_name}")
            print(f"🌐 This will trigger Azure Function App: https://cst8917-assignment1-func.azurewebsites.net")
            print(f"📊 View logs: https://portal.azure.com/#resource/subscriptions/83fb8d4d-37ec-4e26-9d37-e6c0e026f658/resourceGroups/cst8917-assignment1-rg/providers/Microsoft.Web/sites/cst8917-assignment1-func/logs")
            
    except Exception as e:
        print(f"❌ Upload failed: {e}")

if __name__ == "__main__":
    print("🚀 Testing Azure Function App")
    print("=" * 50)
    upload_test_image() 