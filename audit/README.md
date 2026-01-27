# StudyPug PPC Landing Page Audit Tool

Comprehensive QA tool for auditing StudyPug PPC landing pages using Claude AI. Performs both individual page audits and inter-page consistency checks.

## Features

✅ **Individual Page Audits**
- CTA compliance checking (no "Try Free" language)
- Feature accuracy by grade level
- Regional localization validation
- Copy quality analysis
- UI/UX review (with screenshots)
- Conversion psychology assessment

✅ **Inter-Page Consistency Audits**
- Cross-page CTA consistency
- Social proof number logic validation
- Feature naming consistency
- Testimonial uniqueness checks
- Pricing consistency
- Regional cross-contamination detection

✅ **Batch Processing**
- Audit multiple pages at once
- Automatic consistency checking
- Organized report generation

## Installation

### 1. Clone or Download

Download the audit tool files:
- `studypug_audit_tool.py`
- `StudyPug_Individual_Page_Audit_Prompt_v2_0.txt`
- `StudyPug_InterPage_Consistency_Audit_Prompt_v2_0.txt`

### 2. Install Dependencies

```bash
pip install anthropic
```

### 3. Set API Key

Set your Anthropic API key as an environment variable:

```bash
# Mac/Linux
export ANTHROPIC_API_KEY='your-api-key-here'

# Windows (Command Prompt)
set ANTHROPIC_API_KEY=your-api-key-here

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY='your-api-key-here'
```

## Usage

### Quick Start: Audit a Single Page

```bash
python studypug_audit_tool.py audit \
  --url "https://www.studypug.com/ca/grade-5-math" \
  --region ca \
  --screenshot screenshots/grade5.png \
  --output audit_report.json
```

**Arguments:**
- `--url`: URL of the page being audited (required)
- `--region`: Region code - ca, us, uk, au, nz, ie, sg (required)
- `--screenshot`: Path to screenshot image (optional)
- `--content`: Path to HTML content file (optional)
- `--output`: Output JSON file path (default: audit_report.json)

### Batch Audit Multiple Pages

**Step 1:** Create a batch configuration file (see `batch_config_example.json`):

```json
{
  "audit_batch": "Q4_2024_PPC_Pages",
  "pages": [
    {
      "url": "https://www.studypug.com/ca/grade-5-math",
      "region": "ca",
      "screenshot": "screenshots/ca_grade5.png",
      "content": "content/ca_grade5.html"
    },
    {
      "url": "https://www.studypug.com/us/5th-grade-math",
      "region": "us",
      "screenshot": "screenshots/us_grade5.png"
    }
  ]
}
```

**Step 2:** Run the batch audit:

```bash
python studypug_audit_tool.py batch \
  --config batch_config.json \
  --output-dir audit_reports
```

This will:
1. Audit each page individually
2. Save individual reports in `audit_reports/`
3. Run consistency check across all pages
4. Generate summary report

**Arguments:**
- `--config`: Path to batch config JSON (required)
- `--output-dir`: Output directory for reports (default: audit_reports)
- `--skip-consistency`: Skip the consistency audit

### Run Consistency Check Only

If you already have individual audit reports and want to run consistency checks:

```bash
python studypug_audit_tool.py consistency \
  --reports audit_reports/audit_*.json \
  --output consistency_report.json
```

**Arguments:**
- `--reports`: Paths to individual audit JSON files (required, supports wildcards)
- `--output`: Output file path (default: consistency_audit.json)

## Understanding Reports

### Individual Page Audit Report

```json
{
  "page_audit": {
    "url": "https://www.studypug.com/ca/grade-5-math",
    "audit_date": "2024-12-29T10:30:00",
    "page_context": {
      "region": "ca",
      "grade_level": "4-9",
      "target_audience": "parent"
    },
    "scores": {
      "overall_pass_rate": "85%",
      "by_severity": {
        "critical": 2,
        "high": 1,
        "medium": 3,
        "low": 1
      }
    },
    "issues": [
      {
        "id": "ISSUE-001",
        "category": "cta",
        "severity": "critical",
        "current_text": "Try Free",
        "problem": "Header CTA uses banned phrase 'Try Free'",
        "fix": "Change to 'Get Started'",
        "reference": "Section 2.1 - Banned CTA Phrases"
      }
    ]
  }
}
```

### Consistency Audit Report

```json
{
  "consistency_audit": {
    "pages_analyzed": 4,
    "overall_consistency_score": "92%",
    "deployment_recommendation": "fix_critical_first",
    "consistency_issues": [
      {
        "id": "CONSIST-001",
        "category": "cta",
        "severity": "critical",
        "title": "Inconsistent header CTAs",
        "pages_affected": [
          {
            "url": "page1.com",
            "value_found": "Get Started"
          },
          {
            "url": "page2.com",
            "value_found": "Try Free"
          }
        ],
        "recommended_canonical": "Get Started",
        "fix_action": "Update page2 header CTA to 'Get Started'"
      }
    ]
  }
}
```

## Python API Usage

You can also use the tool programmatically:

```python
from studypug_audit_tool import StudyPugAuditor

# Initialize
auditor = StudyPugAuditor(api_key="your-api-key")

# Audit single page
report = auditor.audit_individual_page(
    page_url="https://www.studypug.com/ca/grade-5-math",
    region_code="ca",
    screenshot_path="screenshot.png",
    output_file="report.json"
)

# Batch audit
result = auditor.batch_audit(
    pages=[
        {"url": "url1", "region": "ca", "screenshot": "shot1.png"},
        {"url": "url2", "region": "us", "screenshot": "shot2.png"}
    ],
    output_dir="reports",
    run_consistency=True
)

# Consistency check
consistency = auditor.audit_consistency(
    audit_reports=["report1.json", "report2.json"],
    output_file="consistency.json"
)
```

## Audit Standards Reference

### Critical Issues (Must Fix Before Launch)

- ❌ **Banned CTA phrases**: "Try Free", "Free Trial"
- ❌ **Wrong features for grade**: Video lessons on K-3 pages
- ❌ **Regional cross-contamination**: "State standards" on Canadian pages
- ❌ **Price inconsistencies**: Different prices across pages

### High Issues (Should Fix)

- ⚠️ **Social proof contradictions**: Subregion > parent region numbers
- ⚠️ **Feature naming inconsistencies**: "Quick Assessment" vs "Diagnostic Assessment"
- ⚠️ **Incorrect localization**: Wrong grade format for region

### Medium Issues (Nice to Fix)

- 📝 **Copy quality**: Grammar, readability, tone
- 📝 **Testimonial issues**: Duplicates, audience mismatches
- 📝 **UI/UX patterns**: Inconsistent button styles

## Regional Standards Quick Reference

| Region | Math Spelling | Grade Format | Curriculum Term |
|--------|---------------|--------------|-----------------|
| CA | Math | Grade X | Provincial curriculum |
| US | Math | Xth grade | State standards |
| UK | Maths | Year X | National Curriculum |
| AU | Maths | Year X | Australian Curriculum |
| NZ | Maths | Year X | NZ Curriculum |
| IE | Maths | Year/Class | Irish Curriculum |
| SG | Maths | Primary/Secondary X | MOE Syllabus |

## CTA Standards by Audience

| Page Type | Header CTA (logged out) | Body CTA |
|-----------|-------------------------|----------|
| All pages | "Get Started" | (varies below) |
| Parent K-9 | "Get Started" | "Get Started" |
| Student 10-12 | "Get Started" | "Start Learning" |
| Homeschool | "Get Started" | "Start Today" |
| Test Prep | "Get Started" | "Start Now" |

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
Set your API key as an environment variable or pass it to the constructor.

### "Prompt file not found"
Make sure the prompt files are in the same directory as the tool or in `/mnt/user-data/uploads/`.

### JSON parsing errors
The tool automatically handles markdown code blocks. If errors persist, check the raw output in the report.

### Image format not supported
Supported formats: JPG, JPEG, PNG, GIF, WEBP

## Cost Estimation

Each page audit uses approximately:
- **Individual audit**: ~10,000-15,000 tokens
- **Consistency audit**: ~5,000-10,000 tokens per page analyzed

With Claude Sonnet 4:
- Individual audit: ~$0.15 per page
- Consistency audit: ~$0.30 for 10 pages

## Support

For issues or questions:
1. Check the audit prompts for detailed rules
2. Review example batch config
3. Check Claude API documentation

## Version

- **Tool Version**: 1.0
- **Prompt Version**: 2.0
- **Compatible Models**: Claude Sonnet 4, Claude Opus 4

## License

Internal tool for StudyPug QA team.
