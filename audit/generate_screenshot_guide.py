#!/usr/bin/env python3
"""
Screenshot Naming Guide Generator
==================================
Generates a guide for naming screenshots based on the URL structure.
This helps ensure auto-mapping works correctly.
"""

import json
from pathlib import Path
from typing import Dict


def slugify(text: str) -> str:
    """Convert text to a safe filename."""
    return text.replace('/', '_').replace('?', '_').replace('=', '_').replace(':', '').replace('https_', '').replace('http_', '')


def generate_screenshot_names(url_structure: Dict) -> Dict:
    """Generate suggested screenshot names for each URL."""
    suggestions = {}
    
    for region, data in url_structure.items():
        if not isinstance(data, dict):
            continue
        
        if region == 'shared':
            suggestions['shared'] = {'guest': []}
            
            for url in data.get('guest_urls', []):
                # Extract meaningful part of URL
                parts = [p for p in url.split('/') if p and p not in ['https:', '', 'dev.studypug.com', 'studypug.com']]
                suggested_name = '_'.join(parts) + '.png'
                
                suggestions['shared']['guest'].append({
                    'url': url,
                    'suggested_name': suggested_name,
                    'path': f'/screenshot/screenshots/shared/guest/{suggested_name}'
                })
        else:
            suggestions[region] = {'guest': [], 'parent': [], 'student': []}
            
            # Guest URLs
            for url in data.get('guest_urls', []):
                parts = [p for p in url.split('/') if p and p not in ['https:', '', 'dev.studypug.com', 'studypug.com', region]]
                suggested_name = '_'.join(parts) + '.png'
                
                suggestions[region]['guest'].append({
                    'url': url,
                    'suggested_name': suggested_name,
                    'path': f'/screenshot/screenshots/{region}/guest/{suggested_name}'
                })
            
            # Parent URLs
            for url in data.get('parent_urls', []):
                parts = [p for p in url.split('/') if p and p not in ['https:', '', 'dev.studypug.com', 'studypug.com', region]]
                suggested_name = '_'.join(parts) + '.png'
                
                suggestions[region]['parent'].append({
                    'url': url,
                    'suggested_name': suggested_name,
                    'path': f'/screenshot/screenshots/{region}/parent/{suggested_name}'
                })
            
            # Student URLs
            for url in data.get('student_urls', []):
                parts = [p for p in url.split('/') if p and p not in ['https:', '', 'dev.studypug.com', 'studypug.com', region]]
                suggested_name = '_'.join(parts) + '.png'
                
                suggestions[region]['student'].append({
                    'url': url,
                    'suggested_name': suggested_name,
                    'path': f'/screenshot/screenshots/{region}/student/{suggested_name}'
                })
    
    return suggestions


def save_naming_guide(suggestions: Dict):
    """Save naming guide as JSON and human-readable text."""
    
    # Save JSON
    json_path = Path("screenshot_naming_guide.json")
    json_path.write_text(json.dumps(suggestions, indent=2))
    print(f"✅ JSON guide saved: {json_path}")
    
    # Save human-readable
    text_path = Path("screenshot_naming_guide.txt")
    lines = []
    lines.append("=" * 80)
    lines.append("StudyPug Screenshot Naming Guide")
    lines.append("=" * 80)
    lines.append("")
    lines.append("This guide shows suggested screenshot names for each URL.")
    lines.append("Name your screenshots according to this guide for auto-mapping to work.")
    lines.append("")
    
    for region, states in suggestions.items():
        lines.append("")
        lines.append("=" * 80)
        lines.append(f"REGION: {region.upper()}")
        lines.append("=" * 80)
        
        for state, urls in states.items():
            lines.append("")
            lines.append(f"--- {state.upper()} ({len(urls)} URLs) ---")
            lines.append("")
            
            for item in urls:
                lines.append(f"URL: {item['url']}")
                lines.append(f"Screenshot: {item['suggested_name']}")
                lines.append(f"Full path: {item['path']}")
                lines.append("")
    
    text_path.write_text('\n'.join(lines))
    print(f"✅ Text guide saved: {text_path}")


def save_directory_structure(suggestions: Dict):
    """Save a shell script to create the directory structure."""
    
    script_lines = [
        "#!/bin/bash",
        "# Create screenshot directory structure",
        "",
        "BASE=/screenshot/screenshots",
        "",
        "echo 'Creating screenshot directory structure...'",
        ""
    ]
    
    regions = set()
    states_by_region = {}
    
    for region, states in suggestions.items():
        regions.add(region)
        states_by_region[region] = list(states.keys())
    
    script_lines.append("# Create base directory")
    script_lines.append("mkdir -p $BASE")
    script_lines.append("")
    
    for region in sorted(regions):
        script_lines.append(f"# {region.upper()}")
        for state in states_by_region[region]:
            script_lines.append(f"mkdir -p $BASE/{region}/{state}")
        script_lines.append("")
    
    script_lines.append("echo '✅ Directory structure created!'")
    script_lines.append("echo ''")
    script_lines.append("echo 'Directory tree:'")
    script_lines.append("tree -L 3 $BASE || ls -R $BASE")
    
    script_path = Path("create_screenshot_dirs.sh")
    script_path.write_text('\n'.join(script_lines))
    script_path.chmod(0o755)
    print(f"✅ Directory script saved: {script_path}")
    print(f"   Run: ./create_screenshot_dirs.sh")


def main():
    """Main function."""
    print("\n" + "=" * 80)
    print("Screenshot Naming Guide Generator")
    print("=" * 80)
    print()
    
    # Load URL structure
    print("📋 Loading URL structure from urls.json...")
    
    urls_path = None
    possible_paths = [
        Path("urls.json"),
        Path("/mnt/user-data/uploads/urls.json"),
        Path("./urls.json")
    ]
    
    for path in possible_paths:
        if path.exists():
            urls_path = path
            break
    
    if not urls_path:
        print("❌ Could not find urls.json")
        print("\nPlease ensure urls.json is in:")
        print("  • Current directory")
        print("  • /mnt/user-data/uploads/")
        return 1
    
    url_structure = json.loads(urls_path.read_text())
    
    # Count URLs
    total_urls = sum(
        len(region_data.get('guest_urls', [])) + 
        len(region_data.get('parent_urls', [])) + 
        len(region_data.get('student_urls', []))
        for region_data in url_structure.values()
        if isinstance(region_data, dict)
    )
    
    print(f"✅ Loaded {total_urls} URLs")
    print()
    
    # Generate suggestions
    print("📝 Generating naming suggestions...")
    suggestions = generate_screenshot_names(url_structure)
    print("✅ Done")
    print()
    
    # Save guides
    print("💾 Saving guides...")
    save_naming_guide(suggestions)
    save_directory_structure(suggestions)
    print()
    
    print("=" * 80)
    print("✅ Complete!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Run: ./create_screenshot_dirs.sh (to create directory structure)")
    print("2. Take screenshots and name them according to screenshot_naming_guide.txt")
    print("3. Run: python auto_audit_screenshots.py (to auto-audit)")
    print()


if __name__ == "__main__":
    main()
