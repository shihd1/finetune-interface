import os
from supabase import create_client

url = 'https://nhanfdvbgpgcxrqcjful.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5oYW5mZHZiZ3BnY3hycWNqZnVsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjE3NTg1OTksImV4cCI6MjAzNzMzNDU5OX0.dkDZKZvw6deIu-i-yC4TYbeK-ASlEX5fMiYyKy1VmWY'
supabase = create_client(url, key)

response = (
    supabase.table("countries")
    .insert({"id": 1, "name": "Denmark"})
    .execute()
)