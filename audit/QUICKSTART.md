# 🚀 QUICKSTART GUIDE

Get up and running with the StudyPug PPC Audit Tool in 5 minutes!

## Step 1: Setup (2 minutes)

```bash
# Install dependency
pip install anthropic

# Set your API key
export ANTHROPIC_API_KEY='your-api-key-here'
```

## Step 2: Choose Your Method

### 🎯 Method A: Interactive Helper (Easiest!)

```bash
python audit_helper.py
```

Then follow the prompts to:
- Audit from screenshots directory
- Create batch configs
- Check consistency
- View summaries

### 📸 Method B: Single Page Audit

```bash
python studypug_audit_tool.py audit \
  --url "https://www.studypug.com/ca/grade-5-math" \
  --region ca \
  --screenshot screenshot.png \
  --output report.json
```

### 📦 Method C: Batch Audit

Create `my_batch.json`:
```json
{
  "pages": [
    {
      "url": "https://www.studypug.com/ca/grade-5-math",
      "region": "ca",
      "screenshot": "screenshots/grade5.png"
    }
  ]
}
```

Run:
```bash
python studypug_audit_tool.py batch --config my_batch.json
```

## Step 3: Review Results

Reports are saved as JSON files containing:
- ✅ Pass/fail status
- 🔴 Critical issues (must fix)
- 🟡 High priority issues
- 🟢 Medium priority issues
- 📊 Consistency analysis (batch only)

## Common Workflows

### Workflow 1: Quick Screenshot Audit
1. Put all screenshots in `./screenshots/` folder
2. Run: `python audit_helper.py`
3. Choose option 1
4. Enter URL and region for each screenshot
5. Get reports in `quick_audit_reports/`

### Workflow 2: Consistency Check
1. Run individual audits (save to `audit_reports/`)
2. Run: `python audit_helper.py`
3. Choose option 3
4. Get `consistency_audit.json`

### Workflow 3: Monitor Changes
1. Audit pages before changes
2. Make updates
3. Audit pages after changes
4. Compare reports

## What Gets Checked?

### ❌ CRITICAL (Must Fix)
- "Try Free" or "Free Trial" CTAs
- Wrong features for grade (e.g., video on K-3)
- Regional cross-contamination
- Price inconsistencies

### ⚠️ HIGH (Should Fix)
- Social proof contradictions
- Feature naming inconsistencies
- Localization errors

### 📝 MEDIUM (Nice to Fix)
- Copy quality issues
- Duplicate testimonials
- UI/UX patterns

## Report Structure

```
audit_reports/
├── audit_001_ca_page1.json          # Individual audits
├── audit_002_us_page2.json
├── audit_003_uk_page3.json
├── consistency_audit.json           # Consistency check
└── batch_audit_summary.json         # Overall summary
```

## Quick Reference

### Region Codes
- `ca` - Canada
- `us` - United States
- `uk` - United Kingdom
- `au` - Australia
- `nz` - New Zealand
- `ie` - Ireland
- `sg` - Singapore

### Required Header CTA
**All pages (logged out):** "Get Started"

### Required Body CTAs
- Parent pages (K-9): "Get Started"
- Student pages (10-12): "Start Learning"
- Homeschool: "Start Today"
- Test Prep: "Start Now"

### Banned Phrases
❌ NEVER use:
- "Try Free"
- "Free Trial"
- "Start Free Trial"
- "Try for Free"

## Troubleshooting

**Problem:** "ANTHROPIC_API_KEY not found"
**Solution:** Set the environment variable: `export ANTHROPIC_API_KEY='key'`

**Problem:** "Prompt file not found"
**Solution:** Make sure prompt .txt files are in the same directory

**Problem:** Report has parsing errors
**Solution:** Tool auto-handles this - check `raw_response` field

## Cost Estimate

- Single page audit: ~$0.15
- 10-page batch with consistency: ~$1.80

## Need Help?

1. Check `README.md` for detailed documentation
2. Review `batch_config_example.json` for examples
3. Use `audit_helper.py` for interactive guidance

## Pro Tips

💡 **Tip 1:** Run audits before and after changes to track improvements

💡 **Tip 2:** Use batch mode for efficiency when auditing multiple pages

💡 **Tip 3:** Check consistency report for cross-page issues

💡 **Tip 4:** Fix CRITICAL issues first - they block deployment

💡 **Tip 5:** Keep screenshots named clearly: `ca_grade5.png`, `us_grade6.png`

---

Ready to start? Run: `python audit_helper.py`
