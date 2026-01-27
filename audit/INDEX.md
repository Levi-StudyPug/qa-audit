# StudyPug PPC Audit Tool - File Index

## 🌟 NEW: FULLY AUTOMATED WORKFLOW

**You have a structured URL mapping!** Use the most powerful audit method:

### ⚡ 2-Command Audit (Recommended!)

```bash
# 1. Generate screenshot naming guide
python generate_screenshot_guide.py

# 2. Run fully automated audit
export ANTHROPIC_API_KEY='your-key'
python auto_audit_screenshots.py
```

✅ **Automatically loads 280+ URLs from urls.json**  
✅ **Auto-maps screenshots to URLs**  
✅ **Audits all regions: CA, US, UK, AU, NZ, IE, SG + shared**  
✅ **Handles guest/parent/student states**  
✅ **Complete consistency analysis**  

📖 **See:** `AUTOMATED_WORKFLOW.md` for complete guide

---

## ⭐ Alternative: Screenshot Directory Workflow

**If screenshots are already in `/screenshot/screenshots/` without URL mapping:**

```bash
# Set API key
export ANTHROPIC_API_KEY='your-key-here'

# Run the specialized script
python quick_audit_screenshots.py
```

✅ **Automatically finds all screenshots**  
✅ **Auto-detects region from filenames**  
✅ **Prompts for URL and region**  

📖 **See:** `SCREENSHOT_WORKFLOW.md` for full guide

---

## 📦 Complete Package Contents

### 🚀 Quick Start Files

1. **AUTOMATED_WORKFLOW.md** 🌟 **NEW! BEST!**
   - **START HERE** for structured URL-based audits
   - Fully automated with urls.json mapping
   - Handles 280+ URLs across all regions
   - 2-command workflow
   - Complete guide

2. **SCREENSHOT_WORKFLOW.md**
   - For screenshots in `/screenshot/screenshots/`
   - Auto-detects region from filenames
   - Interactive URL entry
   - Step-by-step guide

3. **QUICKSTART.md**
   - General quick start guide
   - Common workflows
   - Quick reference

4. **setup.sh** (Mac/Linux)
   - Automated setup script
   - Installs dependencies
   - Creates necessary directories
   - Run: `./setup.sh`

5. **setup.bat** (Windows)
   - Automated setup script for Windows
   - Installs dependencies
   - Creates necessary directories
   - Run: `setup.bat`

### 🔧 Core Tools

4. **studypug_audit_tool.py**
   - Main audit engine
   - CLI interface for auditing
   - Individual page audits
   - Batch processing
   - Consistency checks
   - Can be used programmatically

5. **auto_audit_screenshots.py** 🌟 **NEW! BEST!**
   - Fully automated audit tool
   - Loads URLs from urls.json
   - Auto-maps screenshots to URLs
   - Handles all regions and user states
   - Intelligent URL matching
   - Interactive fallback for unmapped screenshots
   - Run: `python auto_audit_screenshots.py`

6. **generate_screenshot_guide.py** 🌟 **NEW!**
   - Generates screenshot naming guide from urls.json
   - Creates directory structure script
   - Helps ensure proper auto-mapping
   - Run: `python generate_screenshot_guide.py`

7. **quick_audit_screenshots.py**
   - Specialized tool for `/screenshot/screenshots/` directory
   - Auto-finds all screenshots
   - Auto-detects region from filenames
   - Interactive prompts for each screenshot
   - One command to audit everything
   - Run: `python quick_audit_screenshots.py`

8. **audit_helper.py**
   - Interactive helper script
   - User-friendly interface
   - No command line arguments needed
   - Quick screenshot auditing
   - Batch config creation
   - Run: `python audit_helper.py`

### 📋 Audit Rules (AI Prompts)

7. **StudyPug_Individual_Page_Audit_Prompt_v2_0.txt**
   - Comprehensive audit rules for individual pages
   - CTA compliance standards
   - Feature accuracy by grade
   - Regional localization rules
   - Copy quality standards
   - UI/UX requirements
   - Used automatically by the tool

8. **StudyPug_InterPage_Consistency_Audit_Prompt_v2_0.txt**
   - Cross-page consistency rules
   - CTA consistency checking
   - Social proof validation
   - Feature naming standards
   - Testimonial uniqueness
   - Regional cross-contamination detection
   - Used automatically by the tool

### 📖 Documentation

9. **README.md**
   - Complete documentation
   - Installation instructions
   - Usage examples
   - API reference
   - Standards reference
   - Troubleshooting guide

10. **urls.json** 🌟 **NEW!**
    - Your URL structure mapping
    - 280+ URLs across all regions
    - Guest/parent/student states
    - Used by auto_audit_screenshots.py
    - Can be edited to add/remove URLs

11. **batch_config_example.json**
    - Example batch configuration file
    - Shows proper JSON structure
    - Template for your own batches
    - Edit and use for batch audits

12. **batch_config_screenshot_dir.json**
    - Config example with `/screenshot/screenshots/` paths
    - Shows correct path format
    - Includes naming convention tips
    - Auto-detection examples

13. **requirements.txt**
    - Python dependencies
    - Used by setup scripts
    - Manual install: `pip install -r requirements.txt`

---

## 🎯 Which Files Do I Need?

### For Automated URL-Based Workflow (🌟 BEST!)
```
✅ AUTOMATED_WORKFLOW.md      (read this first!)
✅ urls.json                  (your URL structure)
✅ auto_audit_screenshots.py  (automated audit tool)
✅ generate_screenshot_guide.py (naming guide generator)
✅ studypug_audit_tool.py     (main engine)
✅ Both prompt .txt files     (audit rules)
✅ requirements.txt           (dependencies)
```

### For Screenshot Directory (Alternative)
```
✅ SCREENSHOT_WORKFLOW.md   (read this first!)
✅ quick_audit_screenshots.py (specialized tool)
✅ studypug_audit_tool.py   (main engine)
✅ Both prompt .txt files   (audit rules)
✅ requirements.txt         (dependencies)
```

### For Quick Start (Basic Method)
```
✅ QUICKSTART.md          (read first)
✅ studypug_audit_tool.py (main tool)
✅ audit_helper.py        (interactive mode)
✅ Both prompt .txt files (audit rules)
✅ requirements.txt       (dependencies)
✅ setup.sh or setup.bat  (automated setup)
```

### For Advanced Use
```
✅ All above files
✅ README.md              (full documentation)
✅ batch_config_*.json    (batch templates)
✅ QUICK_REFERENCE.txt    (cheat sheet)
```

---

## 🏁 Getting Started

### 🌟 Method 1: Automated URL-Based (BEST!)

**For structured screenshot organization with URL mapping**

```bash
# Install
pip install anthropic

# Set API key
export ANTHROPIC_API_KEY='your-key'

# Generate naming guide (first time only)
python generate_screenshot_guide.py

# Run automated audit
python auto_audit_screenshots.py
```

**Best for:** Organized teams, multiple regions, large-scale audits

### 🎯 Method 2: Screenshot Directory

**For existing screenshots in `/screenshot/screenshots/`**

```bash
# Install + API key (same as above)

# Run specialized tool
python quick_audit_screenshots.py
```

**Best for:** Quick audits, smaller batches, ad-hoc testing

### ⚙️ Method 3: Interactive Helper

**For guided step-by-step workflow**

```bash
# Mac/Linux
./setup.sh
python audit_helper.py

# Windows
setup.bat
python audit_helper.py
```

**Best for:** First-time users, learning the tool

---

## 📁 Directory Structure After Setup

```
studypug-audit-tool/
├── studypug_audit_tool.py          ← Main tool
├── audit_helper.py                 ← Interactive helper
├── StudyPug_Individual_*.txt       ← Audit rules
├── StudyPug_InterPage_*.txt        ← Consistency rules
├── README.md                       ← Full docs
├── QUICKSTART.md                   ← Quick guide
├── requirements.txt                ← Dependencies
├── setup.sh / setup.bat            ← Setup scripts
├── batch_config_example.json       ← Config template
├── screenshots/                    ← Your screenshots here
├── content/                        ← HTML content here
└── audit_reports/                  ← Reports saved here
    ├── audit_001_ca_*.json
    ├── audit_002_us_*.json
    ├── consistency_audit.json
    └── batch_audit_summary.json
```

---

## 🎨 Usage Patterns

### Pattern 0a: Automated URL-Based Audit (🌟 BEST!)
```bash
# First time: Generate naming guide
python generate_screenshot_guide.py

# Any time: Run automated audit
python auto_audit_screenshots.py

# The tool will:
# 1. Load 280+ URLs from urls.json
# 2. Scan all screenshot directories
# 3. Auto-map screenshots to URLs
# 4. Prompt for any unmapped URLs
# 5. Run complete audit + consistency
# 6. Generate all reports
```

### Pattern 0b: Screenshots in `/screenshot/screenshots/`
```bash
# Just run this one command!
python quick_audit_screenshots.py

# The tool will:
# 1. Find all screenshots automatically
# 2. Auto-detect region from filenames
# 3. Ask for URL and region
# 4. Run audit + consistency check
# 5. Generate all reports
```

### Pattern 1: Quick Screenshot Audit (Interactive)
```bash
# 1. Put screenshots in screenshots/ folder
# 2. Run helper
python audit_helper.py
# 3. Choose option 1
# 4. Enter URL + region for each screenshot
```

### Pattern 2: Single Page Audit
```bash
python studypug_audit_tool.py audit \
  --url "https://www.studypug.com/ca/grade-5-math" \
  --region ca \
  --screenshot /screenshot/screenshots/grade5.png
```

### Pattern 3: Batch Audit
```bash
# 1. Create config (use batch_config_screenshot_dir.json as template)
# 2. Run batch audit
python studypug_audit_tool.py batch --config my_batch.json
```

### Pattern 4: Consistency Check Only
```bash
python studypug_audit_tool.py consistency \
  --reports audit_reports/audit_*.json
```

---

## 🔑 API Key Setup

The tool requires an Anthropic API key. Get one at: https://console.anthropic.com/

**Set as environment variable:**

Mac/Linux:
```bash
export ANTHROPIC_API_KEY='sk-ant-...'
```

Windows (PowerShell):
```powershell
$env:ANTHROPIC_API_KEY='sk-ant-...'
```

Windows (Command Prompt):
```cmd
set ANTHROPIC_API_KEY=sk-ant-...
```

**Or pass directly in Python:**
```python
auditor = StudyPugAuditor(api_key="sk-ant-...")
```

---

## 💰 Cost Estimation

Using Claude Sonnet 4:
- Single page audit: ~$0.15
- 10-page batch: ~$1.80 (including consistency check)
- 50-page batch: ~$8.00

---

## 🆘 Support

1. **Quick questions:** Check QUICKSTART.md
2. **Detailed info:** Read README.md
3. **Examples:** See batch_config_example.json
4. **Interactive help:** Run `python audit_helper.py`

---

## 📊 What Gets Audited?

### Individual Page Audit
✅ CTA compliance (no "Try Free")
✅ Feature accuracy by grade level
✅ Regional localization (terms, spelling)
✅ Copy quality (grammar, readability)
✅ UI/UX (with screenshots)
✅ Social proof numbers
✅ Testimonials
✅ Conversion psychology

### Consistency Audit (Across Pages)
✅ CTA consistency
✅ Social proof logic
✅ Feature naming
✅ Testimonial uniqueness
✅ Pricing consistency
✅ Regional cross-contamination

---

## 🏆 Best Practices

1. ✅ Always audit BEFORE launching new pages
2. ✅ Run consistency checks when updating multiple pages
3. ✅ Fix CRITICAL issues before deployment
4. ✅ Keep screenshots organized by region/grade
5. ✅ Use batch mode for efficiency
6. ✅ Review consistency report for cross-page issues

---

## 🚀 Ready to Start?

### 🌟 Recommended: Automated URL-Based Workflow
```bash
# Generate naming guide (first time)
python generate_screenshot_guide.py

# Run automated audit
python auto_audit_screenshots.py
```

### Alternative Workflows
```bash
# For /screenshot/screenshots/
python quick_audit_screenshots.py

# For interactive guidance
./setup.sh  # or setup.bat on Windows
python audit_helper.py
```

For more details, see:
- **AUTOMATED_WORKFLOW.md** - For URL-based automated audits (🌟 BEST!)
- **SCREENSHOT_WORKFLOW.md** - For `/screenshot/screenshots/` directory
- **QUICKSTART.md** - For general usage
- **README.md** - For complete documentation
