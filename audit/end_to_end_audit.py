#!/usr/bin/env python3
"""
StudyPug End-to-End Audit Workflow
===================================
Complete workflow: Capture screenshots → Audit → Generate reports

Step 1: Take screenshots (FREE - runs locally with Playwright)
Step 2: Audit screenshots (PAID - uses Claude API)
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime


def print_banner(text):
    """Print a formatted banner."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def check_prerequisites():
    """Check if required files and dependencies exist."""
    print_banner("Checking Prerequisites")
    
    errors = []
    warnings = []
    
    # Check for urls.json
    if not Path("urls.json").exists() and not Path("/mnt/user-data/uploads/urls.json").exists():
        errors.append("❌ urls.json not found")
    else:
        print("✅ urls.json found")
    
    # Check for screenshot script
    if not Path("url_screenshot.py").exists():
        errors.append("❌ url_screenshot.py not found")
    else:
        print("✅ url_screenshot.py found")
    
    # Check for audit tool
    if not Path("studypug_audit_tool.py").exists():
        errors.append("❌ studypug_audit_tool.py not found")
    else:
        print("✅ studypug_audit_tool.py found")
    
    # Check for Playwright
    try:
        import playwright
        print("✅ Playwright installed")
    except ImportError:
        warnings.append("⚠️  Playwright not installed (needed for screenshots)")
        warnings.append("   Install: pip install playwright && playwright install")
    
    # Check for Anthropic
    try:
        import anthropic
        print("✅ Anthropic library installed")
    except ImportError:
        warnings.append("⚠️  Anthropic library not installed (needed for audits)")
        warnings.append("   Install: pip install anthropic")
    
    # Check for .env file
    if not Path(".env").exists():
        warnings.append("⚠️  .env file not found (needed for authenticated screenshots)")
        warnings.append("   Create .env with login credentials for parent/student pages")
    else:
        print("✅ .env file found")
    
    if errors:
        print("\n" + "!" * 70)
        for error in errors:
            print(error)
        print("!" * 70)
        return False
    
    if warnings:
        print()
        for warning in warnings:
            print(warning)
    
    return True


def count_urls():
    """Count total URLs from urls.json."""
    urls_path = Path("urls.json") if Path("urls.json").exists() else Path("/mnt/user-data/uploads/urls.json")
    
    if not urls_path.exists():
        return 0
    
    url_data = json.loads(urls_path.read_text())
    
    total = 0
    for region, data in url_data.items():
        if isinstance(data, dict):
            total += len(data.get('guest_urls', []))
            total += len(data.get('parent_urls', []))
            total += len(data.get('student_urls', []))
    
    return total


def run_screenshots():
    """Run the screenshot capture script."""
    print_banner("Step 1: Capturing Screenshots (FREE)")
    
    print("This will use Playwright to capture all pages locally.")
    print("No API costs - everything runs on your computer!")
    print()
    
    total_urls = count_urls()
    print(f"📊 Total URLs to capture: {total_urls}")
    print()
    
    proceed = input("▶️  Proceed with screenshot capture? (y/n) [y]: ").strip().lower()
    
    if proceed not in ['', 'y', 'yes']:
        print("⏭️  Skipped screenshot capture")
        return False
    
    print("\n🚀 Running url_screenshot.py...")
    print("-" * 70)
    
    try:
        result = subprocess.run(
            [sys.executable, "url_screenshot.py"],
            check=True,
            capture_output=False,
            text=True
        )
        print("-" * 70)
        print("✅ Screenshot capture complete!\n")
        return True
    except subprocess.CalledProcessError as e:
        print("-" * 70)
        print(f"❌ Screenshot capture failed with error code {e.returncode}\n")
        return False
    except FileNotFoundError:
        print("❌ url_screenshot.py not found in current directory\n")
        return False


def estimate_audit_cost(num_pages):
    """Estimate audit cost."""
    cost_per_page = 0.15
    return num_pages * cost_per_page


def run_audit():
    """Run the automated audit."""
    print_banner("Step 2: Auditing Screenshots (PAID - Uses Claude API)")
    
    # Count screenshots
    screenshots_dir = Path("screenshots")
    if not screenshots_dir.exists():
        print("❌ screenshots/ directory not found")
        print("   Run screenshot capture first!\n")
        return False
    
    # Count total screenshots
    total_screenshots = sum(1 for _ in screenshots_dir.rglob("*.png"))
    
    if total_screenshots == 0:
        print("❌ No screenshots found in screenshots/ directory")
        print("   Run screenshot capture first!\n")
        return False
    
    print(f"📊 Found {total_screenshots} screenshots")
    
    estimated_cost = estimate_audit_cost(total_screenshots)
    print(f"💰 Estimated cost: ${estimated_cost:.2f}")
    print()
    
    print("This will use Claude's API to analyze each screenshot.")
    print("You need an ANTHROPIC_API_KEY set in your environment.")
    print()
    
    # Check for API key
    import os
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not set!")
        print()
        print("Set it with:")
        print("  export ANTHROPIC_API_KEY='sk-ant-your-key-here'")
        print()
        return False
    
    print("✅ ANTHROPIC_API_KEY is set")
    print()
    
    proceed = input("▶️  Proceed with audit? (y/n) [y]: ").strip().lower()
    
    if proceed not in ['', 'y', 'yes']:
        print("⏭️  Skipped audit")
        return False
    
    print("\n🚀 Running auto_audit_screenshots.py...")
    print("-" * 70)
    
    try:
        result = subprocess.run(
            [sys.executable, "auto_audit_screenshots.py"],
            check=True,
            capture_output=False,
            text=True
        )
        print("-" * 70)
        print("✅ Audit complete!\n")
        return True
    except subprocess.CalledProcessError as e:
        print("-" * 70)
        print(f"❌ Audit failed with error code {e.returncode}\n")
        return False
    except FileNotFoundError:
        print("❌ auto_audit_screenshots.py not found in current directory\n")
        return False


def show_summary():
    """Show summary of results."""
    print_banner("Summary")
    
    # Check for reports
    reports_dir = Path("audit_reports")
    if not reports_dir.exists():
        print("⚠️  No audit reports found")
        return
    
    summary_file = reports_dir / "batch_audit_summary.json"
    if summary_file.exists():
        summary = json.loads(summary_file.read_text())
        batch = summary.get("batch_audit", {})
        consistency = summary.get("consistency_audit", {}).get("consistency_audit", {})
        
        print(f"📅 Audit completed: {batch.get('audit_date', 'N/A')}")
        print(f"📄 Pages audited: {batch.get('pages_audited', 0)}")
        print(f"❌ Pages failed: {batch.get('pages_failed', 0)}")
        
        if consistency:
            print(f"\n🔄 Consistency Score: {consistency.get('overall_consistency_score', 'N/A')}")
            print(f"📋 Deployment Recommendation: {consistency.get('deployment_recommendation', 'N/A')}")
            
            summary_counts = consistency.get('summary_counts', {})
            print(f"\n🔴 Critical Issues: {summary_counts.get('critical_issues', 0)}")
            print(f"🟡 High Issues: {summary_counts.get('high_issues', 0)}")
            print(f"🟢 Medium Issues: {summary_counts.get('medium_issues', 0)}")
            print(f"⚪ Low Issues: {summary_counts.get('low_issues', 0)}")
            
            print(f"\n✅ Pages Clean: {summary_counts.get('pages_clean', 0)}")
            print(f"⚠️  Pages with Issues: {summary_counts.get('pages_with_issues', 0)}")
        
        print(f"\n📁 Reports location: audit_reports/")
        print(f"📊 View summary: cat audit_reports/batch_audit_summary.json")
    else:
        print("⚠️  Summary file not found")


def main():
    """Main workflow."""
    print("\n" + "=" * 70)
    print("  StudyPug End-to-End Audit Workflow")
    print("  Screenshot Capture → Audit → Reports")
    print("=" * 70)
    
    print(f"\n⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed. Please fix the errors above.")
        return 1
    
    # Show workflow options
    print_banner("Workflow Options")
    print("1. Complete workflow (capture + audit)")
    print("2. Capture screenshots only (FREE)")
    print("3. Audit existing screenshots only (PAID)")
    print("4. Exit")
    print()
    
    choice = input("Select option (1-4) [1]: ").strip() or "1"
    
    if choice == "1":
        # Complete workflow
        print()
        screenshots_success = run_screenshots()
        
        if screenshots_success:
            print("✅ Screenshots captured successfully!")
            print()
            input("Press Enter to continue to audit...")
            audit_success = run_audit()
            
            if audit_success:
                show_summary()
        else:
            print("❌ Screenshot capture failed. Audit skipped.")
            return 1
    
    elif choice == "2":
        # Screenshot only
        print()
        screenshots_success = run_screenshots()
        
        if screenshots_success:
            print("✅ Screenshots captured!")
            print()
            print("💡 Next step: Run this script again and choose option 3 to audit.")
        else:
            return 1
    
    elif choice == "3":
        # Audit only
        print()
        audit_success = run_audit()
        
        if audit_success:
            show_summary()
        else:
            return 1
    
    elif choice == "4":
        print("\n👋 Goodbye!")
        return 0
    
    else:
        print("\n❌ Invalid option")
        return 1
    
    print(f"\n⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "=" * 70)
    print("  ✅ Workflow Complete!")
    print("=" * 70 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
