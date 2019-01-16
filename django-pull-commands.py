import os
import sys

path = r'C:\Users\p15144f\Documents\Code\Anaconda\mysite\\'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
