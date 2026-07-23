import os
import json
import re

def extract_title(file_path):
    """Extracts first heading title from markdown file, falls back to clean filename."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if line_str.startswith("#"):
                    return re.sub(r"^#\s*", "", line_str)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    # Fallback to filename
    basename = os.path.basename(file_path)
    return os.path.splitext(basename)[0].replace("_", " ").title()

def update_dir_registry(dir_name, registry_filename):
    dir_path = os.path.join("docs", dir_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
        
    files_list = []
    # Scan directory
    for file in sorted(os.listdir(dir_path)):
        if file.endswith(".md") and not file.endswith(registry_filename):
            file_path = os.path.join(dir_path, file)
            title = extract_title(file_path)
            files_list.append({
                "path": f"docs/{dir_name}/{file}",
                "name": title
            })
            
    registry_path = os.path.join(dir_path, registry_filename)
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(files_list, f, ensure_ascii=False, indent=4)
        
    print(f"Generated registry with {len(files_list)} files at {registry_path}")

def update_all_registries():
    # Update templates registry
    update_dir_registry("templates", "registry.json")
    # Update results registry
    update_dir_registry("results", "registry.json")

if __name__ == "__main__":
    update_all_registries()
