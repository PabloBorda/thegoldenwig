import requests
import base64
import json

class WordPress:
    def __init__(self, site_url, username, app_password):
        self.site_url = site_url
        self.username = username
        self.app_password = app_password
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {base64.b64encode(f'{username}:{app_password}'.encode('utf-8')).decode('utf-8')}"
        }

    def post_news(self, news):
        post_data = {
            "title": news.title,
            "content": news.body,
            "status": "publish"
        }

        if news.picture:
            media_id = self.upload_media(news.picture)
            if media_id:
                post_data['featured_media'] = media_id

        response = requests.post(f"{self.site_url}/wp-json/wp/v2/posts", headers=self.headers, json=post_data)
        return response

    def upload_media(self, file_path):
        with open(file_path, 'rb') as media:
            media_data = media.read()
        media_headers = self.headers.copy()
        media_headers['Content-Disposition'] = f'attachment; filename={file_path}'
        media_headers['Content-Type'] = 'image/jpeg'  # Change if not JPEG

        response = requests.post(f"{self.site_url}/wp-json/wp/v2/media", headers=media_headers, data=media_data)
        if response.status_code == 201:
            return response.json().get('id')
        return None

    def deploy_to_lightsail(self, instance_name, blueprint_id, bundle_id):

        # Example usage
        aws_access_key = 'YOUR_AWS_ACCESS_KEY'
        aws_secret_key = 'YOUR_AWS_SECRET_KEY'
        region = 'us-west-2'
        wordpress_instance = Wordpress(aws_access_key, aws_secret_key, region)

        instance_name = 'MyWordPressSite'
        blueprint_id = 'wordpress'
        bundle_id = 'nano_2_0'

        response = wordpress_instance.deploy_to_lightsail(instance_name, blueprint_id, bundle_id)
        print(response)
        
        self.client = boto3.client(
            'lightsail',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
        try:
            response = self.client.create_instances(
                instanceNames=[instance_name],
                availabilityZone=f'{self.region}a',  # Modify as needed
                blueprintId=blueprint_id,
                bundleId=bundle_id,
                userData='''#!/bin/bash
                            # Initialization script (optional)
                         '''
            )
            return response
        except Exception as e:
            print(f"Error creating Lightsail instance: {e}")
            return None