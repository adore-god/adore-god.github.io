import os
import re

# Root folder (where manifest.json lives)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Regex to match any favicon link and capture the href path
favicon_pattern = re.compile(
    r'(<link[^>]*rel=["\']icon["\'][^>]*href=["\'])([^"\']*favicon\.png)(["\'][^>]*>)',
    re.IGNORECASE
)

# Regex to detect any existing manifest link
manifest_pattern = re.compile(r'<link[^>]*rel=["\']manifest["\'][^>]*>', re.IGNORECASE)

for root, _, files in os.walk(base_dir):
    for file in files:
        if file.lower().endswith(".html"):
            file_path = os.path.join(root, file)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Calculate the correct relative path to manifest.json
            rel_manifest = os.path.relpath(os.path.join(base_dir, "manifest.json"), start=root)
            rel_manifest = rel_manifest.replace("\\", "/")

            def repl(m):
                """Replace favicon line and append/update manifest"""
                # Remove existing manifest if present
                content_without_manifest = re.sub(manifest_pattern, '', content)

                # Insert manifest after the favicon line
                return f'{m.group(1)}{m.group(2)}{m.group(3)}\n<link rel="manifest" href="{rel_manifest}">'

            # Replace favicon + manifest
            new_content, count = re.subn(favicon_pattern, repl, content)

            if count > 0:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {file_path} -> favicon: preserved, manifest: {rel_manifest}")
            else:
                # If no favicon line found, optionally insert one at the top of <head>
                head_tag = re.search(r'<head[^>]*>', content, re.IGNORECASE)
                if head_tag:
                    insert_pos = head_tag.end()
                    new_content = (content[:insert_pos] +
                                   f'\n<link rel="icon" href="favicon.png" type="image/png">\n<link rel="manifest" href="{rel_manifest}">' +
                                   content[insert_pos:])
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Inserted favicon + manifest in {file_path} -> manifest: {rel_manifest}")
                else:
                    print(f"No <head> tag found in {file_path}, skipped.")
