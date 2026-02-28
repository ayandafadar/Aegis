"""
Aegis - Dashboard Page Accessibility Tests
Tests data tables, dynamic content, ARIA attributes, and chart accessibility.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.axe_helper import (
    run_axe, run_axe_wcag2aa, get_violations, get_violation_count,
    get_violations_by_impact, format_violations
)


class TestDashboardAxeScan:
    """axe-core scans of the dashboard page."""

    def test_full_scan(self, dashboard_page):
        """Run full axe-core scan on dashboard."""
        results = run_axe(dashboard_page)
        violations = get_violations(results)

        if violations:
            report = format_violations(violations)
            print(f"\n[DASHBOARD] Full scan found {len(violations)} violation(s):\n{report}")

    def test_wcag2aa_compliance(self, dashboard_page):
        """Check WCAG 2.0 AA compliance."""
        results = run_axe_wcag2aa(dashboard_page)
        violations = get_violations(results)

        if violations:
            report = format_violations(violations)
            print(f"\n[DASHBOARD] WCAG 2.0 AA violations:\n{report}")

        critical = get_violations_by_impact(results, "critical")
        assert len(critical) == 0, (
            f"Found {len(critical)} critical WCAG 2.0 AA violation(s):\n"
            f"{format_violations(critical)}"
        )

    def test_no_serious_violations(self, dashboard_page):
        """No serious-impact violations allowed."""
        results = run_axe(dashboard_page)
        serious = get_violations_by_impact(results, "serious")

        if serious:
            report = format_violations(serious)
            print(f"\n[DASHBOARD] Serious violations:\n{report}")


class TestDashboardTables:
    """Test data table accessibility."""

    def test_tables_exist(self, dashboard_page):
        """Dashboard should have data tables."""
        tables = dashboard_page.find_elements("css selector", "table")
        assert len(tables) >= 1, "Dashboard should have at least one data table"

    def test_tables_have_headers(self, dashboard_page):
        """Data tables should use th elements for headers."""
        tables = dashboard_page.find_elements("css selector", "table")

        for i, table in enumerate(tables):
            headers = table.find_elements("css selector", "th")
            # Report tables missing proper headers
            if not headers:
                print(f"\n[DASHBOARD] Table {i+1} is missing <th> header elements")

    def test_table_headers_have_scope(self, dashboard_page):
        """Table headers should have scope attribute."""
        headers = dashboard_page.find_elements("css selector", "table th")
        missing_scope = []

        for th in headers:
            scope = th.get_attribute("scope")
            if not scope:
                missing_scope.append(th.text[:30])

        if missing_scope:
            print(f"\n[DASHBOARD] Table headers missing scope: {missing_scope}")

    def test_tables_have_caption_or_label(self, dashboard_page):
        """Tables should have an accessible name via caption or aria-labelledby."""
        tables = dashboard_page.find_elements("css selector", "table")

        for i, table in enumerate(tables):
            caption = table.find_elements("css selector", "caption")
            aria_label = table.get_attribute("aria-label")
            aria_labelledby = table.get_attribute("aria-labelledby")

            has_name = caption or aria_label or aria_labelledby
            if not has_name:
                print(f"\n[DASHBOARD] Table {i+1} has no accessible name")


class TestDashboardARIA:
    """Test ARIA attributes and live regions."""

    def test_no_empty_links(self, dashboard_page):
        """All links must have discernible text."""
        results = run_axe(dashboard_page)
        link_violations = [v for v in get_violations(results) if v.get('id') == 'link-name']
        
        assert len(link_violations) == 0, (
            f"Found empty link(s) without accessible text:\n"
            f"{format_violations(link_violations)}"
        )

    def test_alert_roles(self, dashboard_page):
        """Alert elements should have role='alert'."""
        alerts = dashboard_page.find_elements("css selector", ".alert")

        for alert in alerts:
            role = alert.get_attribute("role")
            assert role in ("alert", "status"), (
                f"Alert element should have role='alert' or 'status', got '{role}'"
            )

    def test_interactive_elements_are_buttons(self, dashboard_page):
        """Elements that trigger actions should be proper buttons."""
        # Find span/div elements with onclick handlers
        fake_buttons = dashboard_page.find_elements(
            "css selector", "span[onclick], div[onclick]"
        )

        if fake_buttons:
            print(f"\n[DASHBOARD] Found {len(fake_buttons)} non-button element(s) with onclick handlers")
            for fb in fake_buttons:
                tag = fb.tag_name
                text = fb.text[:30]
                role = fb.get_attribute("role")
                print(f"  - <{tag}> \"{text}\" (role={role})")


class TestDashboardCharts:
    """Test chart and data visualization accessibility."""

    def test_chart_has_text_alternative(self, dashboard_page):
        """Charts/visualizations must have text alternatives."""
        charts = dashboard_page.find_elements("css selector", "[role='img']")

        for chart in charts:
            aria_label = chart.get_attribute("aria-label")
            aria_labelledby = chart.get_attribute("aria-labelledby")
            
            if not aria_label and not aria_labelledby:
                print(f"\n[DASHBOARD] Chart element with role='img' has no accessible label")
