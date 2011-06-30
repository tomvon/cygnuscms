import os
import sys

for path, dir, files in os.walk('addons'):
	sys.path.append(os.path.join(os.path.dirname(__file__), path))