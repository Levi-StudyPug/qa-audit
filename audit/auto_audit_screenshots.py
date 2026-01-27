#!/usr/bin/env python3
"""
StudyPug Automated Screenshot Audit
====================================
Automatically audits all screenshots using the URL structure from urls.json

Directory structure:
- /screenshot/screenshots/ca/guest/*.png
- /screenshot/screenshots/ca/parent/*.png
- /screenshot/screenshots/ca/student/*.png
- /screenshot/screenshots/us/guest/*.png
- ... etc
- /screenshot/screenshots/shared/guest/*.png
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Optional
from studypug_audit_tool import StudyPugAuditor


def load_url_structure(urls_file: str = "urls.json") -> Dict:
    """Load the URL structure from urls.json."""
    urls_path = Path(urls_file)
    
    # Try multiple locations
    possible_paths = [
        urls_path,
        Path("/mnt/user-data/uploads") / urls_file,
        Path(".") / urls_file
    ]
    
    for path in possible_paths:
        if path.exists():
            return json.loads(path.read_text())
    
    raise FileNotFoundError(f"Could not find {urls_file} in any expected location")


def find_screenshots_in_directory(directory: Path) -> List[Path]:
    """Find all screenshot files in a directory."""
    screenshots = []
    for ext in ['*.png', '*.jpg', '*.jpeg', '*.webp']:
        screenshots.extend(directory.glob(ext))
    return sorted(screenshots)


def match_screenshot_to_url(screenshot_name: str, urls: List[str]) -> Optional[str]:
    """
    Try to match a screenshot filename to a URL.
    
    Matching strategies:
    1. Exact match: "grade1.png" → "/grade1/"
    2. Partial match: "ca_grade1_main.png" → "/grade1/"
    3. Slugified match: "parents_ca.png" → "/parents/ca/"
    """
    # Remove extension and normalize
    name_normalized = screenshot_name.lower().replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
    
    # Try to find best matching URL
    best_match = None
    best_score = 0
    
    for url in urls:
        url_parts = [p for p in url.split('/') if p and p not in ['https:', '', 'dev.studypug.com']]
        
        # Calculate match score
        score = 0
        for part in url_parts:
            if part.lower() in name_normalized:
                score += len(part)
        
        if score > best_score:
            best_score = score
            best_match = url
    
    return best_match


def scan_screenshots(base_path: Path = Path("/screenshot/screenshots")) -> Dict:
    """
    Scan the screenshot directory structure and return organized data.
    
    Returns dict with structure:
    {
        'ca': {
            'guest': [{'path': Path, 'url': str}, ...],
            'parent': [...],
            'student': [...]
        },
        ...
    }
    """
    if not base_path.exists():
        raise FileNotFoundError(f"Screenshot base path not found: {base_path}")
    
    results = {}
    
    # Scan each region
    regions = ['ca', 'us', 'uk', 'au', 'nz', 'ie', 'sg', 'shared']
    
    for region in regions:
        region_path = base_path / region
        if not region_path.exists():
            continue
        
        results[region] = {}
        
        # Scan each user state
        states = ['guest', 'parent', 'student'] if region != 'shared' else ['guest']
        
        for state in states:
            state_path = region_path / state
            if not state_path.exists():
                continue
            
            screenshots = find_screenshots_in_directory(state_path)
            if screenshots:
                results[region][state] = [{'path': s, 'url': None} for s in screenshots]
    
    return results


def map_urls_to_screenshots(screenshot_data: Dict, url_structure: Dict) -> Dict:
    """Map URLs from urls.json to screenshots."""
    
    for region, states in screenshot_data.items():
        if region == 'shared':
            # Handle shared region
            urls = url_structure.get('shared', {}).get('guest_urls', [])
            if 'guest' in states:
                for screenshot in states['guest']:
                    matched_url = match_screenshot_to_url(screenshot['path'].name, urls)
                    screenshot['url'] = matched_url or "NEEDS_MANUAL_URL"
        else:
            # Handle regional pages
            region_urls = url_structure.get(region, {})
            
            for state, screenshots in states.items():
                if state == 'guest':
                    urls = region_urls.get('guest_urls', [])
                elif state == 'parent':
                    urls = region_urls.get('parent_urls', [])
                elif state == 'student':
                    urls = region_urls.get('student_urls', [])
                else:
                    urls = []
                
                for screenshot in screenshots:
                    matched_url = match_screenshot_to_url(screenshot['path'].name, urls)
                    screenshot['url'] = matched_url or "NEEDS_MANUAL_URL"
    
    return screenshot_data


def generate_batch_config(screenshot_data: Dict) -> List[Dict]:
    """Generate batch configuration from screenshot data."""
    pages = []
    
    for region, states in screenshot_data.items():
        region_code = region if region != 'shared' else 'ca'  # Default shared to 'ca' for audit purposes
        
        for state, screenshots in states.items():
            for screenshot in screenshots:
                pages.append({
                    'url': screenshot['url'],
                    'region': region_code,
                    'screenshot': str(screenshot['path']),
                    'user_state': state,
                    'notes': f"{region.upper()} - {state} - {screenshot['path'].name}"
                })
    
    return pages


def interactive_url_review(pages: List[Dict]) -> List[Dict]:
    """Allow user to review and update URLs that need manual mapping."""
    needs_review = [p for p in pages if p['url'] == "NEEDS_MANUAL_URL"]
    
    if not needs_review:
        return pages
    
    print("\n" + "=" * 70)
    print(f"  📝 {len(needs_review)} screenshots need URL mapping")
    print("=" * 70)
    print("\nPlease provide URLs for the following screenshots:")
    print("(Press Enter to skip)\n")
    
    for page in needs_review:
        print(f"\n📸 {Path(page['screenshot']).name}")
        print(f"   Region: {page['region'].upper()} | State: {page['user_state']}")
        url = input("   URL: ").strip()
        
        if url:
            page['url'] = url
            print("   ✅ Updated")
        else:
            print("   ⏭️  Skipped (will be excluded from audit)")
    
    # Remove pages that still don't have URLs
    pages = [p for p in pages if p['url'] != "NEEDS_MANUAL_URL"]
    
    return pages


def main():
    """Main function."""
    print("=" * 70)
    print("  StudyPug Automated Screenshot Audit")
    print("=" * 70)
    print()
    
    # Step 1: Load URL structure
    print("📋 Step 1: Loading URL structure...")
    try:
        url_structure = load_url_structure()
        total_urls = sum(
            len(region_data.get('guest_urls', [])) + 
            len(region_data.get('parent_urls', [])) + 
            len(region_data.get('student_urls', []))
            for region_data in url_structure.values()
            if isinstance(region_data, dict)
        )
        print(f"   ✅ Loaded {total_urls} URLs from urls.json")
    except Exception as e:
        print(f"   ❌ Error loading URLs: {e}")
        return 1
    
    # Step 2: Scan screenshots
    print("\n📸 Step 2: Scanning screenshot directories...")
    try:
        screenshot_data = scan_screenshots()
        total_screenshots = sum(
            len(screenshots)
            for states in screenshot_data.values()
            for screenshots in states.values()
        )
        print(f"   ✅ Found {total_screenshots} screenshots")
        
        # Show breakdown
        for region, states in screenshot_data.items():
            for state, screenshots in states.items():
                print(f"      • {region}/{state}: {len(screenshots)} screenshots")
    except Exception as e:
        print(f"   ❌ Error scanning screenshots: {e}")
        return 1
    
    # Step 3: Map URLs to screenshots
    print("\n🔗 Step 3: Mapping URLs to screenshots...")
    screenshot_data = map_urls_to_screenshots(screenshot_data, url_structure)
    
    # Generate batch config
    pages = generate_batch_config(screenshot_data)
    
    # Count successful mappings
    auto_mapped = len([p for p in pages if p['url'] != "NEEDS_MANUAL_URL"])
    needs_manual = len([p for p in pages if p['url'] == "NEEDS_MANUAL_URL"])
    
    print(f"   ✅ Auto-mapped: {auto_mapped} URLs")
    if needs_manual > 0:
        print(f"   ⚠️  Need manual mapping: {needs_manual} URLs")
    
    # Step 4: Interactive review if needed
    if needs_manual > 0:
        review = input("\n🤔 Review and provide missing URLs? (y/n) [y]: ").strip().lower()
        if review in ['', 'y', 'yes']:
            pages = interactive_url_review(pages)
    else:
        pages = [p for p in pages if p['url'] != "NEEDS_MANUAL_URL"]
    
    if not pages:
        print("\n❌ No pages to audit after mapping")
        return 1
    
    # Step 5: Save config
    print(f"\n💾 Step 4: Saving configuration...")
    config = {
        "audit_batch": "Automated_Screenshot_Audit",
        "description": f"Automated audit of {len(pages)} screenshots",
        "pages": pages
    }
    
    config_path = Path("automated_audit_config.json")
    config_path.write_text(json.dumps(config, indent=2))
    print(f"   ✅ Config saved: {config_path}")
    
    # Step 6: Run audit
    print("\n" + "=" * 70)
    print(f"  Ready to audit {len(pages)} pages")
    print("=" * 70)
    
    run_now = input("\n🚀 Run audit now? (y/n) [y]: ").strip().lower()
    
    if run_now in ['', 'y', 'yes']:
        print("\n" + "=" * 70)
        print("  Starting Audit")
        print("=" * 70)
        print()
        
        try:
            auditor = StudyPugAuditor()
            result = auditor.batch_audit(
                pages=pages,
                output_dir="audit_reports",
                run_consistency=len(pages) > 1
            )
            
            print("\n" + "=" * 70)
            print("  ✅ Audit Complete!")
            print("=" * 70)
            print()
            print("📁 Reports saved in: audit_reports/")
            print("📊 Summary: audit_reports/batch_audit_summary.json")
            
            if len(pages) > 1:
                print("🔄 Consistency: audit_reports/consistency_audit.json")
            
            # Show summary
            batch_data = result.get('batch_audit', {})
            print(f"\n📈 Results:")
            print(f"   • Pages audited: {batch_data.get('pages_audited', 0)}")
            print(f"   • Pages failed: {batch_data.get('pages_failed', 0)}")
            
        except Exception as e:
            print("\n" + "=" * 70)
            print("  ❌ Audit Failed")
            print("=" * 70)
            print(f"\nError: {e}")
            print("\nPlease check:")
            print("1. ANTHROPIC_API_KEY is set")
            print("2. Prompt files are in the correct location")
            return 1
    else:
        print("\n✅ Config saved. Run audit later with:")
        print(f"   python studypug_audit_tool.py batch --config {config_path}")
    
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
