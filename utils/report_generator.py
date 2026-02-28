"""
Aegis - HTML Report Generator
Generates detailed accessibility test reports.
"""

import os
import json
from datetime import datetime


def generate_html_report(all_results, output_path=None):
    """
    Generate an HTML accessibility report from axe results.
    
    Args:
        all_results: dict mapping page_name -> axe_results
        output_path: where to save the report (default: reports/a11y_report.html)
    """
    if output_path is None:
        reports_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
        os.makedirs(reports_dir, exist_ok=True)
        output_path = os.path.join(reports_dir, "a11y_report.html")

    total_violations = 0
    total_passes = 0
    total_incomplete = 0
    page_summaries = []

    for page_name, results in all_results.items():
        violations = results.get("violations", [])
        passes = results.get("passes", [])
        incomplete = results.get("incomplete", [])
        total_violations += len(violations)
        total_passes += len(passes)
        total_incomplete += len(incomplete)
        page_summaries.append({
            "name": page_name,
            "violations": violations,
            "passes": len(passes),
            "incomplete": incomplete,
        })

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aegis Accessibility Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: #f5f5f5; color: #333; line-height: 1.6; }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 24px; }}
        h1 {{ font-size: 2rem; margin-bottom: 8px; color: #1a73e8; }}
        .meta {{ color: #666; margin-bottom: 32px; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 32px; }}
        .summary-card {{ background: #fff; border-radius: 8px; padding: 20px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .summary-card .number {{ font-size: 2.5rem; font-weight: 700; }}
        .summary-card .label {{ color: #666; font-size: 0.9rem; }}
        .violations-num {{ color: #d93025; }}
        .passes-num {{ color: #1e8e3e; }}
        .incomplete-num {{ color: #f9ab00; }}
        .page-section {{ background: #fff; border-radius: 8px; padding: 24px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .page-section h2 {{ font-size: 1.4rem; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #1a73e8; }}
        .violation {{ border-left: 4px solid #d93025; padding: 12px 16px; margin-bottom: 12px; background: #fce8e6; border-radius: 0 4px 4px 0; }}
        .violation.serious {{ border-left-color: #e37400; background: #fef7e0; }}
        .violation.moderate {{ border-left-color: #f9ab00; background: #fffde7; }}
        .violation.minor {{ border-left-color: #1a73e8; background: #e8f0fe; }}
        .violation h3 {{ font-size: 1rem; margin-bottom: 4px; }}
        .violation .impact {{ display: inline-block; padding: 1px 8px; border-radius: 10px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #fff; }}
        .impact-critical {{ background: #d93025; }}
        .impact-serious {{ background: #e37400; }}
        .impact-moderate {{ background: #f9ab00; color: #333; }}
        .impact-minor {{ background: #1a73e8; }}
        .violation code {{ background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-size: 0.85rem; word-break: break-all; }}
        .violation a {{ color: #1a73e8; }}
        .nodes {{ margin-top: 8px; }}
        .node {{ background: #fff; padding: 8px; border-radius: 4px; margin-top: 4px; font-size: 0.85rem; }}
        .no-issues {{ color: #1e8e3e; font-weight: 600; padding: 16px; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Aegis Accessibility Report</h1>
        <p class="meta">Generated: {timestamp}</p>

        <div class="summary-grid">
            <div class="summary-card">
                <div class="number violations-num">{total_violations}</div>
                <div class="label">Violations</div>
            </div>
            <div class="summary-card">
                <div class="number passes-num">{total_passes}</div>
                <div class="label">Rules Passed</div>
            </div>
            <div class="summary-card">
                <div class="number incomplete-num">{total_incomplete}</div>
                <div class="label">Needs Review</div>
            </div>
        </div>
"""

    for page in page_summaries:
        html += f"""
        <div class="page-section">
            <h2>{page['name']}</h2>
            <p style="margin-bottom:12px;">
                <strong>{len(page['violations'])}</strong> violations |
                <strong>{page['passes']}</strong> passed |
                <strong>{len(page['incomplete'])}</strong> needs review
            </p>
"""
        if not page['violations']:
            html += '            <p class="no-issues">No violations found!</p>\n'
        else:
            for v in page['violations']:
                impact = v.get('impact', 'unknown')
                impact_class = f"impact-{impact}"
                css_class = impact if impact in ('serious', 'moderate', 'minor') else ''
                help_url = v.get('helpUrl', '#')
                nodes = v.get('nodes', [])

                html += f"""
            <div class="violation {css_class}">
                <h3>
                    <span class="impact {impact_class}">{impact}</span>
                    {v.get('id', 'unknown')}
                </h3>
                <p>{v.get('description', '')}</p>
                <p><a href="{help_url}" target="_blank">Learn more &rarr;</a></p>
                <div class="nodes">
"""
                for node in nodes[:5]:
                    target = ", ".join(node.get("target", []))
                    html_snippet = node.get("html", "")[:200]
                    html += f'                    <div class="node"><strong>Element:</strong> <code>{target}</code><br><code>{_escape_html(html_snippet)}</code></div>\n'

                if len(nodes) > 5:
                    html += f'                    <p style="margin-top:8px;color:#666;">...and {len(nodes) - 5} more elements</p>\n'

                html += """                </div>
            </div>
"""

        html += "        </div>\n"

    html += """
    </div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[Aegis] Report saved to: {output_path}")
    return output_path


def _escape_html(text):
    """Escape HTML special characters."""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))
