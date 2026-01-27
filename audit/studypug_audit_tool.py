#!/usr/bin/env env python3
"""
StudyPug PPC Landing Page Audit Tool
=====================================
Comprehensive QA tool for auditing StudyPug PPC landing pages using Claude API.

Features:
- Individual page audits (screenshot + content analysis)
- Inter-page consistency audits
- Batch processing
- JSON report generation
"""

import os
import json
import base64
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Union
from datetime import datetime
import asyncio
import anthropic


class StudyPugAuditor:
    """Main auditor class for StudyPug landing pages."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the auditor with Claude API."""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Set it as environment variable or pass to constructor."
            )
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
        # Load audit prompts
        self.individual_prompt = self._load_prompt("individual")
        self.consistency_prompt = self._load_prompt("consistency")
    
    def _load_prompt(self, prompt_type: str) -> str:
        """Load audit prompt from file."""
        prompt_files = {
            "individual": "StudyPug_Individual_Page_Audit_Prompt_v2_0.txt",
            "consistency": "StudyPug_InterPage_Consistency_Audit_Prompt_v2_0.txt"
        }
        
        prompt_file = prompt_files.get(prompt_type)
        if not prompt_file:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
        
        # Try to load from /mnt/user-data/uploads first
        upload_path = Path("/mnt/user-data/uploads") / prompt_file
        if upload_path.exists():
            return upload_path.read_text()
        
        # Try current directory
        local_path = Path(prompt_file)
        if local_path.exists():
            return local_path.read_text()
        
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
    
    def _encode_image(self, image_path: str) -> tuple[str, str]:
        """Encode image to base64 and detect media type."""
        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode("utf-8")
        
        # Detect media type
        suffix = Path(image_path).suffix.lower()
        media_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }
        media_type = media_types.get(suffix, "image/jpeg")
        
        return image_data, media_type
    
    def audit_individual_page(
        self,
        page_url: str,
        region_code: str,
        screenshot_path: Optional[str] = None,
        page_content: Optional[str] = None,
        output_file: Optional[str] = None
    ) -> Dict:
        """
        Audit a single landing page.
        
        Args:
            page_url: URL of the page being audited
            region_code: Region code (ca, us, uk, au, nz, ie, sg)
            screenshot_path: Path to screenshot image (optional)
            page_content: HTML or text content of the page (optional)
            output_file: Path to save JSON report (optional)
        
        Returns:
            Dict containing the audit report
        """
        print(f"\n🔍 Auditing: {page_url}")
        print(f"   Region: {region_code}")
        
        # Prepare the prompt
        prompt = self.individual_prompt
        prompt = prompt.replace("{{PAGE_URL}}", page_url)
        prompt = prompt.replace("{{REGION_CODE}}", region_code.upper())
        
        if page_content:
            prompt = prompt.replace("{{PAGE_CONTENT}}", page_content)
        else:
            prompt = prompt.replace("{{PAGE_CONTENT}}", "[No content provided]")
        
        # Build message content
        message_content = []
        
        # Add screenshot if provided
        if screenshot_path:
            print(f"   Screenshot: {screenshot_path}")
            image_data, media_type = self._encode_image(screenshot_path)
            message_content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": image_data
                }
            })
            prompt = prompt.replace("{{SCREENSHOT_OR_NOT_PROVIDED}}", "[Screenshot provided above]")
        else:
            prompt = prompt.replace("{{SCREENSHOT_OR_NOT_PROVIDED}}", "[No screenshot provided]")
        
        # Add the prompt text
        message_content.append({
            "type": "text",
            "text": prompt
        })
        
        # Call Claude API
        print("   Analyzing with Claude...")
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=16000,
            temperature=0,
            messages=[{
                "role": "user",
                "content": message_content
            }]
        )
        
        # Extract JSON from response
        response_text = response.content[0].text
        audit_result = self._extract_json(response_text)
        
        # Save to file if requested
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(audit_result, indent=2))
            print(f"   ✅ Report saved: {output_file}")
        
        return audit_result
    
    def audit_consistency(
        self,
        audit_reports: List[Union[str, Dict]],
        output_file: Optional[str] = None
    ) -> Dict:
        """
        Run inter-page consistency audit across multiple page audits.
        
        Args:
            audit_reports: List of audit report dicts or paths to JSON files
            output_file: Path to save consistency report (optional)
        
        Returns:
            Dict containing the consistency audit report
        """
        print(f"\n🔄 Running consistency audit across {len(audit_reports)} pages...")
        
        # Load audit reports if paths provided
        reports = []
        for report in audit_reports:
            if isinstance(report, str):
                reports.append(json.loads(Path(report).read_text()))
            else:
                reports.append(report)
        
        # Prepare the consistency prompt
        prompt = self.consistency_prompt
        reports_json = json.dumps(reports, indent=2)
        prompt = prompt.replace("{{INDIVIDUAL_AUDIT_REPORTS_JSON}}", reports_json)
        
        # Call Claude API
        print("   Analyzing consistency with Claude...")
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=16000,
            temperature=0,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Extract JSON from response
        response_text = response.content[0].text
        consistency_result = self._extract_json(response_text)
        
        # Save to file if requested
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(consistency_result, indent=2))
            print(f"   ✅ Consistency report saved: {output_file}")
        
        return consistency_result
    
    def batch_audit(
        self,
        pages: List[Dict[str, str]],
        output_dir: str = "audit_reports",
        run_consistency: bool = True
    ) -> Dict:
        """
        Audit multiple pages in batch.
        
        Args:
            pages: List of dicts with keys: url, region, screenshot (optional), content (optional)
            output_dir: Directory to save reports
            run_consistency: Whether to run consistency audit after individual audits
        
        Returns:
            Dict with individual reports and consistency report (if run)
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📊 Starting batch audit of {len(pages)} pages...")
        print(f"   Output directory: {output_dir}")
        
        individual_reports = []
        
        # Audit each page
        for i, page in enumerate(pages, 1):
            print(f"\n--- Page {i}/{len(pages)} ---")
            
            report_filename = f"audit_{i:03d}_{page['region']}_{self._sanitize_filename(page['url'])}.json"
            report_path = output_path / report_filename
            
            try:
                report = self.audit_individual_page(
                    page_url=page['url'],
                    region_code=page['region'],
                    screenshot_path=page.get('screenshot'),
                    page_content=page.get('content'),
                    output_file=str(report_path)
                )
                individual_reports.append(report)
            except Exception as e:
                print(f"   ❌ Error auditing page: {e}")
                continue
        
        result = {
            "batch_audit": {
                "audit_date": datetime.now().isoformat(),
                "pages_audited": len(individual_reports),
                "pages_failed": len(pages) - len(individual_reports),
                "individual_reports": individual_reports
            }
        }
        
        # Run consistency audit if requested
        if run_consistency and len(individual_reports) > 1:
            consistency_report_path = output_path / "consistency_audit.json"
            consistency_report = self.audit_consistency(
                individual_reports,
                output_file=str(consistency_report_path)
            )
            result["consistency_audit"] = consistency_report
        
        # Save batch summary
        summary_path = output_path / "batch_audit_summary.json"
        summary_path.write_text(json.dumps(result, indent=2))
        print(f"\n✅ Batch audit complete! Summary saved: {summary_path}")
        
        return result
    
    def _extract_json(self, text: str) -> Dict:
        """Extract JSON from Claude's response (handles markdown code blocks)."""
        # Try to find JSON in markdown code block
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            json_text = text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            json_text = text[start:end].strip()
        else:
            json_text = text.strip()
        
        try:
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse JSON: {e}")
            print("Returning raw text instead.")
            return {"raw_response": text}
    
    def _sanitize_filename(self, url: str) -> str:
        """Convert URL to safe filename."""
        return url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_")[:50]


def main():
    """CLI interface for the audit tool."""
    parser = argparse.ArgumentParser(
        description="StudyPug PPC Landing Page Audit Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Audit a single page
  python studypug_audit_tool.py audit --url "https://studypug.com/ca/grade-5-math" --region ca --screenshot screenshot.png
  
  # Audit from batch file
  python studypug_audit_tool.py batch --config batch_config.json
  
  # Run consistency check on existing reports
  python studypug_audit_tool.py consistency --reports audit_reports/*.json
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Single page audit command
    audit_parser = subparsers.add_parser("audit", help="Audit a single page")
    audit_parser.add_argument("--url", required=True, help="Page URL")
    audit_parser.add_argument("--region", required=True, choices=["ca", "us", "uk", "au", "nz", "ie", "sg"], help="Region code")
    audit_parser.add_argument("--screenshot", help="Path to screenshot")
    audit_parser.add_argument("--content", help="Path to HTML content file")
    audit_parser.add_argument("--output", default="audit_report.json", help="Output file path")
    
    # Batch audit command
    batch_parser = subparsers.add_parser("batch", help="Audit multiple pages from config")
    batch_parser.add_argument("--config", required=True, help="Path to batch config JSON file")
    batch_parser.add_argument("--output-dir", default="audit_reports", help="Output directory")
    batch_parser.add_argument("--skip-consistency", action="store_true", help="Skip consistency audit")
    
    # Consistency audit command
    consistency_parser = subparsers.add_parser("consistency", help="Run consistency audit on existing reports")
    consistency_parser.add_argument("--reports", nargs="+", required=True, help="Paths to individual audit JSON reports")
    consistency_parser.add_argument("--output", default="consistency_audit.json", help="Output file path")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize auditor
    auditor = StudyPugAuditor()
    
    if args.command == "audit":
        # Load content if provided
        content = None
        if args.content:
            content = Path(args.content).read_text()
        
        auditor.audit_individual_page(
            page_url=args.url,
            region_code=args.region,
            screenshot_path=args.screenshot,
            page_content=content,
            output_file=args.output
        )
    
    elif args.command == "batch":
        # Load batch config
        config = json.loads(Path(args.config).read_text())
        
        auditor.batch_audit(
            pages=config.get("pages", []),
            output_dir=args.output_dir,
            run_consistency=not args.skip_consistency
        )
    
    elif args.command == "consistency":
        auditor.audit_consistency(
            audit_reports=args.reports,
            output_file=args.output
        )


if __name__ == "__main__":
    main()
