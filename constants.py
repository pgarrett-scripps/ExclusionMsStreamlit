import os
import sys

try:
    EXCLUSION_MS_API_IP = f'http://{os.environ["EXCLUSION_MS_API_IP"]}'
except:
    EXCLUSION_MS_API_IP = f'http://{sys.argv[1]}'

print(EXCLUSION_MS_API_IP)

