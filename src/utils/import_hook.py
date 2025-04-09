import sys
import importlib.abc
import time

class ImportLogger(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        print(f"[{time.strftime('%H:%M:%S')}] Module loaded: {fullname}")
        return None  # Allows normal import to proceed

# Insert our custom finder at the beginning of sys.meta_path
sys.meta_path.insert(0, ImportLogger())
