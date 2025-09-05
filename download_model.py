import gdown
import os

FILE_ID = "1O0SheM_jLssJSRJFWp1O0pdTes7svgGA"
URL = f"https://drive.google.com/uc?id={FILE_ID}"
OUTPUT = "similarity.pkl"

if not os.path.exists(OUTPUT):
    print("Downloading similarity.pkl from Google Drive…")
    gdown.download(URL, OUTPUT, quiet=False)
else:
    print("similarity.pkl already exists.")
