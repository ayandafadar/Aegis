"""
Aegis - axe-core Integration Helper
Injects and runs axe-core accessibility engine via Selenium WebDriver.
"""

import json
import os
import urllib.request

AXE_CDN_URL = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.1/axe.min.js"
AXE_LOCAL_PATH = os.path.join(os.path.dirname(__file__), "..", ".axe-cache", "axe.min.js")


def _get_axe_script():
    """Get axe-core script content — download and cache if needed."""
    os.makedirs(os.path.dirname(AXE_LOCAL_PATH), exist_ok=True)
    if not os.path.exists(AXE_LOCAL_PATH):
        print("[Aegis] Downloading axe-core from CDN...")
        urllib.request.urlretrieve(AXE_CDN_URL, AXE_LOCAL_PATH)
        print("[Aegis] axe-core cached locally.")
    with open(AXE_LOCAL_PATH, "r", encoding="utf-8") as f:
        return f.read()


def inject_axe(driver):
    """Inject axe-core into the current page."""
    axe_script = _get_axe_script()
    driver.execute_script(axe_script)


def run_axe(driver, options=None):
    """
    Run axe-core analysis on the current page.

    Args:
        driver: Selenium WebDriver instance
        options: Optional dict of axe.run() options, e.g.:
            {
                "runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa"]},
                "resultTypes": ["violations", "incomplete"]
            }

    Returns:
        dict with keys: violations, passes, incomplete, inapplicable
    """
    inject_axe(driver)

    if options:
        opts_json = json.dumps(options)
        script = f"return await axe.run(document, {opts_json});"
    else:
        script = "return await axe.run(document);"

    # Use execute_async_script for the Promise-based axe.run
    # Wrap in a callback-based approach for compatibility
    callback_script = f"""
    var callback = arguments[arguments.length - 1];
    axe.run(document{', ' + json.dumps(options) if options else ''})
        .then(function(results) {{ callback(results); }})
        .catch(function(err) {{ callback({{"error": err.message}}); }});
    """
    results = driver.execute_async_script(callback_script)

    if isinstance(results, dict) and "error" in results:
        raise RuntimeError(f"axe-core error: {results['error']}")

    return results


def run_axe_wcag2a(driver):
    """Run axe-core checking only WCAG 2.0 Level A rules."""
    return run_axe(driver, {
        "runOnly": {"type": "tag", "values": ["wcag2a"]}
    })


def run_axe_wcag2aa(driver):
    """Run axe-core checking WCAG 2.0 Level A and AA rules."""
    return run_axe(driver, {
        "runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa"]}
    })


def run_axe_wcag21aa(driver):
    """Run axe-core checking WCAG 2.1 Level AA (includes 2.0)."""
    return run_axe(driver, {
        "runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]}
    })


def run_axe_section508(driver):
    """Run axe-core checking Section 508 rules."""
    return run_axe(driver, {
        "runOnly": {"type": "tag", "values": ["section508"]}
    })


def run_axe_best_practices(driver):
    """Run axe-core checking best practice rules."""
    return run_axe(driver, {
        "runOnly": {"type": "tag", "values": ["best-practice"]}
    })


def get_violations(results):
    """Extract violations from axe results."""
    return results.get("violations", [])


def get_violation_count(results):
    """Get total number of violations."""
    return len(results.get("violations", []))


def get_violations_by_impact(results, impact="critical"):
    """Filter violations by impact level: critical, serious, moderate, minor."""
    return [v for v in results.get("violations", [])
            if v.get("impact") == impact]


def format_violations(violations):
    """Format violations into human-readable strings."""
    lines = []
    for v in violations:
        nodes_count = len(v.get("nodes", []))
        tags = ", ".join(v.get("tags", []))
        lines.append(
            f"  [{v.get('impact', '?').upper()}] {v.get('id')}: {v.get('description')}\n"
            f"    Help: {v.get('helpUrl', 'N/A')}\n"
            f"    Elements affected: {nodes_count}\n"
            f"    Tags: {tags}"
        )
    return "\n\n".join(lines)
