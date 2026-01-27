#!/usr/bin/env python3
"""
URL Screenshot Tool
Takes screenshots of a list of URLs and saves them as PNG files.
"""

import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
from datetime import datetime
import re
import os  # NEW
from dotenv import load_dotenv  # NEW

# Load .env from the same folder as this script
ENV_PATH = Path(__file__).parent / ".env"  # NEW
load_dotenv(dotenv_path=ENV_PATH)  # NEW

# Role-based auth storage paths
def get_auth_state_path(role: str) -> Path:
    role_key = (role or "default").lower()
    return Path("screenshots") / f"storage_state_{role_key}.json"


def sanitize_filename(url):
    """Convert URL to a safe filename."""
    filename = re.sub(r'^https?://', '', url)
    filename = re.sub(r'[^\w\-.]', '_', filename)
    if filename.startswith('stage.studypug.com_'):
        filename = filename[len('stage.studypug.com_'):]
    if len(filename) > 100:
        filename = filename[:100]
    return filename

def _debug_env(role: str, user_var: str, pass_var: str):
    u = os.getenv(user_var)
    p = os.getenv(pass_var)
    print(
        f"🔎 Env loaded from: {ENV_PATH} | role={role} | {user_var} set: {bool(u)} | {pass_var} set: {bool(p)}"
    )

# NEW: login helpers
async def login_and_save_state(p, auth_url: str, role: str):
    # Choose role-specific env vars (fallback to generic)
    role_l = (role or "").lower()
    if role_l == "parent":
        email_env = "SP_PARENT_USERNAME_STAGE"
        pass_env = "SP_PARENT_PASSWORD_STAGE"
    elif role_l == "student":
        email_env = "SP_STUDENT_USERNAME_STAGE"
        pass_env = "SP_STUDENT_PASSWORD_STAGE"
    else:
        email_env = "SP_USERNAME"
        pass_env = "SP_PASSWORD"

    _debug_env(role_l or "default", email_env, pass_env)
    username = os.getenv(email_env)
    password = os.getenv(pass_env)
    if not username or not password:
        raise RuntimeError(f"Missing credentials: set {email_env} and {pass_env} (env path: {ENV_PATH})")

    browser = await p.chromium.launch(headless=False)  # keep visible while debugging
    context = await browser.new_context()
    page = await context.new_page()

    print(f"🔐 Logging in at: {auth_url}")
    await page.goto(auth_url, wait_until='domcontentloaded', timeout=60000)
    
    # Wait for Material-UI form to render
    await page.wait_for_timeout(500)
    
    # Debug: screenshot the signin page
    await page.screenshot(path="screenshots/signin_form.png", full_page=True)
    print(f"  📸 Debug screenshot saved: screenshots/signin_form.png")
    
    # Inspect page structure to debug
    frames = page.frames
    print(f"🔍 Page frames: {len(frames)} frame(s)")
    for i, frame in enumerate(frames):
        print(f"   Frame {i}: {frame.name or '(unnamed)'}")
    
    # Get all input fields on the page
    all_inputs = await page.locator('input').all()
    print(f"🔍 Total input fields found: {len(all_inputs)}")
    for i, inp in enumerate(all_inputs):
        try:
            input_type = await inp.get_attribute('type')
            input_name = await inp.get_attribute('name')
            input_id = await inp.get_attribute('id')
            input_placeholder = await inp.get_attribute('placeholder')
            print(f"   Input {i}: type={input_type}, name={input_name}, id={input_id}, placeholder={input_placeholder}")
        except:
            pass

    # Fill credentials with concrete selectors
    try:
        # Email - try many selectors
        target = page  # assume top-level form
        email_filled = False
        email_selectors = [
            'input#Email',
            'input[id="Email"]',
            'input[type="email"]',
            'input[placeholder*="someone@email" i]',
            'input[name="email"]',
        ]
        
        for sel in email_selectors:
            if await target.locator(sel).first.count():
                try:
                    await target.fill(sel, username)
                    email_filled = True
                    print(f"  ✓ Filled email via {sel}")
                    break
                except:
                    continue

        # Password
        password_filled = False
        password_selectors = [
            'input#component-outlined2',
            'input[id="component-outlined2"]',
            'input[type="password"]',
            'input[placeholder*="6-40" i]',
            'input[name="password"]',
        ]
        
        for sel in password_selectors:
            count = await target.locator(sel).count()
            if count > 0:
                try:
                    await target.fill(sel, password)
                    password_filled = True
                    print(f"  ✓ Filled password via {sel}")
                    break
                except:
                    continue

        # Submit: look for the yellow "Log in" button
        submitted = False
        submit_selectors = [
            'button:has-text("Log in")',
            'button:has-text("Login")',
            'button[type="submit"]',
            'button:has-text("Sign in")',
            'button[name="login"]',
        ]
        
        for sel in submit_selectors:
            count = await target.locator(sel).count()
            if count > 0:
                print(f"  ✓ Clicking button via: {sel}")
                await target.locator(sel).first.click()
                submitted = True
                break
        
        if not submitted:
            print(f"  ⚠️ Could not find submit button, trying Enter key")
            # Try pressing Enter on password field
            pwd_fields = await target.locator('input[placeholder*="Password" i], input[type="password"]').all()
            if pwd_fields:
                await pwd_fields[0].press('Enter')
            else:
                print(f"  ⚠️ No password field found for Enter key")
    except Exception as e:
        print(f"⚠️ Login interaction failed: {e}")
        try:
            await page.screenshot(path="screenshots/login_error.png", full_page=True)
            print(f"  📸 Error state screenshot saved: screenshots/login_error.png")
        except:
            pass
        await browser.close()
        raise

    # Wait for navigation away from signin and network to settle
    try:
        await page.wait_for_url(re.compile(r'^(?!.*\/signin).*'), timeout=15000)
        print(f"  ✓ URL changed away from /signin")
    except Exception:
        print(f"  ℹ️ URL did not change away from /signin")

    # Give page a moment to stabilize but don't wait for full networkidle
    await page.wait_for_timeout(2000)

    # Debug screenshot to see what page we're actually on
    await page.screenshot(path="screenshots/login_attempt.png", full_page=True)
    print(f"  📸 Debug screenshot saved: screenshots/login_attempt.png")

    # Post-login signal: adjust to your app (avatar/menu/etc.)
    # Example selectors — replace with a reliable one in your UI:
    post_login_ok = False
    for sel in [
        '[data-test="user-menu"]',
        '.UserMenu',
        'nav [aria-label*="Account"]',
        'a[href*="/dashboard"]',
    ]:
        if await page.locator(sel).first.count():
            post_login_ok = True
            break

    url_after = page.url
    cookies = await context.cookies()
    all_cookies = [(c.get("name"), c.get("domain")) for c in cookies]
    has_session = any(
        ("studypug" in c.get("domain", "")) and (
            "session" in c.get("name", "").lower() or "auth" in c.get("name", "").lower()
        ) for c in cookies
    )
    print(f"🔎 Post-login URL: {url_after}")
    print(f"🔎 Cookies: {all_cookies}")
    print(f"🔎 Session cookie found: {has_session}")
    print(f"🔎 Post-login selector found: {post_login_ok}")

    if ("signin" in url_after and not has_session and not post_login_ok):
        print(f"⚠️ Still on sign-in page with no auth indicators. Check screenshots/login_attempt.png")
        await browser.close()
        raise RuntimeError("Login likely failed: still on sign-in with no session and no post-login selector.")

    auth_path = get_auth_state_path(role_l or "default")
    auth_path.parent.mkdir(parents=True, exist_ok=True)
    await context.storage_state(path=str(auth_path))
    print(f"✅ Auth state saved to: {auth_path}")
    await browser.close()


async def create_authenticated_context(p, role: str):
    auth_path = get_auth_state_path((role or "default").lower())
    if not auth_path.exists():
        raise RuntimeError(f"Auth state not found for role '{role}'. Run login first.")
    browser = await p.chromium.launch()
    context = await browser.new_context(storage_state=str(auth_path))
    return browser, context


async def take_screenshot(
    url,
    output_dir="screenshots",
    viewport_width=1920,
    viewport_height=1080,
    use_auth=False,
    auth_url="https://stage.studypug.com/signin/ca/?role=student",
    role: str | None = None
):
    """
    Take a screenshot of a single URL.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    filename = sanitize_filename(url) + '.png'
    filepath = Path(output_dir) / filename

    async with async_playwright() as p:
        # Prepare browser/context
        if use_auth:
            if not role:
                raise RuntimeError("use_auth=True requires a role ('parent' or 'student')")
            auth_path = get_auth_state_path(role)
            if not auth_path.exists():
                print(f"ℹ️ No auth state found for role '{role}'. Performing login...")
                await login_and_save_state(p, auth_url, role)
            else:
                print(f"ℹ️ Using existing auth state at {auth_path}")
            browser, context = await create_authenticated_context(p, role)
        else:
            browser = await p.chromium.launch()
            context = await browser.new_context()

        page = await context.new_page()
        await page.set_viewport_size({'width': viewport_width, 'height': viewport_height})

        try:
            print(f"📸 Capturing: {url}")
            await page.goto(url, wait_until='networkidle', timeout=30000)
            await page.wait_for_timeout(1000)
            await page.screenshot(path=str(filepath), full_page=True)
            print(f"✅ Saved: {filepath}")
        except Exception as e:
            print(f"❌ Error capturing {url}: {str(e)}")
        finally:
            await page.close()
            await browser.close()


async def take_screenshots_batch(
    urls,
    output_dir="screenshots",
    viewport_width=1920,
    viewport_height=1080,
    use_auth=False,
    auth_url="https://stage.studypug.com/signin/ca/?role=student",
    role: str | None = None
):
    """
    Take screenshots of multiple URLs efficiently.
    """
    print(f"📋 take_screenshots_batch called with use_auth={use_auth}")
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        # Prepare browser/context
        if use_auth:
            if not role:
                raise RuntimeError("use_auth=True requires a role ('parent' or 'student')")
            print(f"🔐 Auth mode enabled for role '{role}'")
            auth_path = get_auth_state_path(role)
            if not auth_path.exists():
                print(f"ℹ️ No auth state found at {auth_path}. Performing login...")
                await login_and_save_state(p, auth_url, role)
            else:
                print(f"ℹ️ Using existing auth state at {auth_path}")
            browser, context = await create_authenticated_context(p, role)
        else:
            browser = await p.chromium.launch()
            context = await browser.new_context()

        for url in urls:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            filename = sanitize_filename(url)

            # replace signin with start for auth-related pages
            if use_auth and "signin" in filename:
                filename = filename.replace('signin', 'start')

            filename += '.png'
            filepath = Path(output_dir) / filename

            page = await context.new_page()
            await page.set_viewport_size({'width': viewport_width, 'height': viewport_height})

            try:
                print(f"📸 Capturing: {url}")
                await page.goto(url, wait_until='networkidle', timeout=60000)
                await page.wait_for_timeout(1000)
                await page.screenshot(path=str(filepath), full_page=True)
                print(f"✅ Saved: {filepath}")
            except Exception as e:
                print(f"❌ Error capturing {url}: {str(e)}")
            finally:
                await page.close()

        await browser.close()


async def main():
    """Main function with separate guest, parent, and student screenshot batches."""
    
    # Guest URLs (no login required)
    guest_urls = [       
        # // Lander page
        'https://stage.studypug.com/parents/us/',
        'https://stage.studypug.com/students/us/',
        'https://stage.studypug.com/homeschoolers/us/',
        'https://stage.studypug.com/teachers/us/',
        
        # // course pages
        'https://stage.studypug.com/us/math-1/',
        'https://stage.studypug.com/us/math-1/practice-test',
        
         # // course pages
        'https://stage.studypug.com/us/us-ela-grade-1/',
        'https://stage.studypug.com/us/us-ela-grade-9/',
                
        # // Auth pages
        'https://stage.studypug.com/signin/us/?role=parent',
        'https://stage.studypug.com/signin/us/?role=student',
        'https://stage.studypug.com/signup/us/?role=parent',
        'https://stage.studypug.com/signup/us/?role=student',
        
        # // Worksheet pages
        'https://stage.studypug.com/worksheets/us/grade/2/', 
        'https://stage.studypug.com/worksheets/us/', 
        'https://stage.studypug.com/worksheets/us/foundation/addition/',
        
        # // Curriculum pages
        'https://stage.studypug.com/curriculum/us/',
        'https://stage.studypug.com/curriculum/us/ca/math/',
        'https://stage.studypug.com/curriculum/us/ca/math/grade3/',
        
        # // Try-free pages
        'https://stage.studypug.com/try-free/curriculum/us/ca/math/grade3/',
        'https://stage.studypug.com/try-free/curriculum/us/ca/math/homeschool/',
        'https://stage.studypug.com/try-free/curriculum/us/ca/math/',
        
        # // Support pages
        'https://stage.studypug.com/support/us/how-it-works/?role=student',
        'https://stage.studypug.com/support/us/how-it-works/?role=parent',
        'https://stage.studypug.com/support/us/how-it-works/?role=testprep',
        'https://stage.studypug.com/support/us/why-choose-studypug?role=student',
        'https://stage.studypug.com/support/us/why-choose-studypug?role=parent',
        'https://stage.studypug.com/support/us/why-choose-studypug?role=testprep',
        'https://stage.studypug.com/support/us/pricing/?role=student',
        'https://stage.studypug.com/support/us/pricing/?role=parent',
        'https://stage.studypug.com/support/about-us/',
        'https://stage.studypug.com/support/faq/',
        'https://stage.studypug.com/support/testimonials/',
        'https://stage.studypug.com/support/contact-us/',
        'https://stage.studypug.com/support/us/pricing/?role=parent',
        'https://stage.studypug.com/support/us/pricing/?role=student',
        
        # // Help pages
        'https://stage.studypug.com/basic-math-help/',
        'https://stage.studypug.com/algebra-help/',
        'https://stage.studypug.com/geometry-help/',
        'https://stage.studypug.com/trigonometry-help/',
        'https://stage.studypug.com/calculus-help/',
        'https://stage.studypug.com/chemistry-help/',
        'https://stage.studypug.com/physics-help/',
        'https://stage.studypug.com/statistics-help/',
        'https://stage.studypug.com/differential-equations-help/',
        'https://stage.studypug.com/linear-algebra-help/',
        'https://stage.studypug.com/micro-econ-help/',
        'https://stage.studypug.com/orgchem-help/',
        
        # // Tutor pages
        'https://stage.studypug.com/basic-math-tutor/',
        'https://stage.studypug.com/algebra-tutor/',
        'https://stage.studypug.com/geometry-tutor/',
        'https://stage.studypug.com/trigonometry-tutor/',
        'https://stage.studypug.com/calculus-tutor/',
        'https://stage.studypug.com/chemistry-tutor/',
        'https://stage.studypug.com/physics-tutor/',
        'https://stage.studypug.com/statistics-tutor/',
        'https://stage.studypug.com/differential-equations-tutor/',
        'https://stage.studypug.com/linear-algebra-tutor/',
        'https://stage.studypug.com/micro-econ-tutor/',
        'https://stage.studypug.com/orgchem-tutor/'
    ]
    
    # Parent-authenticated URLs (requires parent login)
    parent_urls = [
        'https://stage.studypug.com/payment/us/?role=parent',
        'https://stage.studypug.com/signin/us/?role=parent'

    ]

    # Student-authenticated URLs (requires student login)
    student_urls = [
        # Add student-only/protected URLs here
        # Example:
        'https://stage.studypug.com/payment/us/?role=student',
        'https://stage.studypug.com/signin/us/?role=student'
 
    ]

    print(f"🚀 Starting screenshot capture")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Take guest screenshots
    if guest_urls:
        print(f"📸 Guest Screenshots: {len(guest_urls)} URLs (no authentication)")
        print("=" * 60)
        await take_screenshots_batch(
            urls=guest_urls,
            output_dir="screenshots/guest",
            viewport_width=1920,
            viewport_height=1080,
            use_auth=False
        )
        print()

    # Take parent authenticated screenshots
    if parent_urls:
        print(f"🔐 Parent Screenshots: {len(parent_urls)} URLs (requires parent login)")
        print("=" * 60)
        await take_screenshots_batch(
            urls=parent_urls,
            output_dir="screenshots/parent",
            viewport_width=1920,
            viewport_height=1080,
            use_auth=True,
            auth_url="https://stage.studypug.com/signin/ca/?role=parent",
            role="parent",
        )
        print()

    # Take student authenticated screenshots
    if student_urls:
        print(f"🔐 Student Screenshots: {len(student_urls)} URLs (requires student login)")
        print("=" * 60)
        await take_screenshots_batch(
            urls=student_urls,
            output_dir="screenshots/student",
            viewport_width=1920,
            viewport_height=1080,
            use_auth=True,
            auth_url="https://stage.studypug.com/signin/ca/?role=student",
            role="student",
        )
        print()

    print(f"✨ Done! Screenshots saved to 'screenshots' directory")
    print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    asyncio.run(main())