import os
import requests

txt_file_path = r'D:\A-Projects\Urban Heat Island\LAADS_query.2024-06-24T11_58_urls.txt'
download_dir = r'D:\A-Projects\Urban Heat Island\Hdf'

# Bearer Token
bearer_token = 'eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6InBhcnJqaTIwMDIiLCJleHAiOjE3MjQyMTAwODAsImlhdCI6MTcxOTAyNjA4MCwiaXNzIjoiRWFydGhkYXRhIExvZ2luIn0.XR0IObSviz1vc1C04Osk1bYJDWcYUQy0UdUQK7MMjcq4HUE_Rw_UshFp3Dab-vjhcoQ-Ny8nDqIxUDyyECVsJH7vkMclLLfMGBifG63S-mrJ0TzmXTMhRUiiYP0X7hQc1LIRmUXM3wzo7fYEfsbCdddvqA7Cvhxi836dCfyR7HB9ek1VtgEI96xetCAy5PoTLVAAFja87jW9UsvJ9WlJPmbNMo3ICwsqLKE4vI5egWqHCKNCe5VpJnInAL0K8AeGEo1r6Z-5W4vZo1fP62NVb1S1YN3gY7kyVxmsSJzyakN8NpHBsdXTMDMu9BFaO9TNuZtdsDW3uR7pcg50k8_8bA'  # 替换为你的Bearer Token

if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# 读取txt文件中的所有URLs
with open(txt_file_path, 'r') as file:
    urls = [line.strip() for line in file if line.strip()]

# 下载每个URL指向的文件
for url in urls:
    try:
        print(f"Downloading {url}...")
        headers = {
            "Authorization": f"Bearer {bearer_token}"
        }
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        file_name = os.path.join(download_dir, url.split('/')[-1])
        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {url} to {file_name}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")
