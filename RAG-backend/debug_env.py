import os
from dotenv import dotenv_values

# Load using dotenv_values to see raw values
config = dotenv_values(".env")
print("Raw values from dotenv_values:")
for key, value in config.items():
    print(f"{key}: {repr(value)}")

print("\n" + "="*50 + "\n")

# Also try manual parsing
with open('.env', 'r') as f:
    lines = f.readlines()

print("Raw lines from .env file:")
for i, line in enumerate(lines, 1):
    print(f"{i:2d}: {repr(line)}")