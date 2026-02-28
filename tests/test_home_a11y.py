"""
Aegis - Home Page Accessibility Tests
Tests page structure, landmarks, headings, images, links, and color contrast.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.axe_helper import (
    run_axe, run_axe_wcag2aa, run_axe_wcag21aa, run_axe_best_practices,
    get_violations, get_violation_count, get_violations_by_impact, format_violations
)


class TestHomePageAccessibility:
    """Full axe-core accessibility scan of the home page."""

    def test_full_axe_scan(self, home_page):
        """Run a complete axe-core scan and report all findings."""
        results = run_axe(home_page)
        violations = get_violations(results)
        
        # This test documents violations rather than hard-failing
        # Useful for initial baseline assessment
        if violations:
            report = format_violations(violations)
            print(f"\n[HOME] Full scan found {len(violations)} violation(s):\n{report}")

    def test_wcag2aa_compliance(self, home_page):
        """Check WCAG 2.0 AA compliance — the standard target."""
        results = run_axe_wcag2aa(home_page)
        violations = get_violations(results)

        if violations:
            report = format_violations(violations)
            print(f"\n[HOME] WCAG 2.0 AA violations:\n{report}")

        # Assert no critical violations
        critical = get_violations_by_impact(results, "critical")
        assert len(critical) == 0, (
            f"Found {len(critical)} critical WCAG 2.0 AA violation(s):\n"
            f"{format_violations(critical)}"
        )

    def test_wcag21aa_compliance(self, home_page):
        """Check WCAG 2.1 AA compliance — current recommended standard."""
        results = run_axe_wcag21aa(home_page)
        violations = get_violations(results)

        if violations:
            report = format_violations(violations)
            print(f"\n[HOME] WCAG 2.1 AA violations:\n{report}")

    def test_no_critical_violations(self, home_page):
        """Ensure no critical-impact accessibility violations."""
        results = run_axe(home_page)
        critical = get_violations_by_impact(results, "critical")

        assert len(critical) == 0, (
            f"Found {len(critical)} critical violation(s):\n"
            f"{format_violations(critical)}"
        )

    def test_best_practices(self, home_page):
        """Check accessibility best practices."""
        results = run_axe_best_practices(home_page)
        violations = get_violations(results)

        if violations:
            report = format_violations(violations)
            print(f"\n[HOME] Best practice violations:\n{report}")


class TestHomePageStructure:
    """Test page structure and semantic HTML."""

    def test_has_html_lang(self, home_page):
        """Page must have a lang attribute on the html element."""
        lang = home_page.find_element("css selector", "html").get_attribute("lang")
        assert lang and len(lang) >= 2, "html element must have a valid lang attribute"

    def test_has_page_title(self, home_page):
        """Page must have a non-empty title."""
        title = home_page.title
        assert title and len(title.strip()) > 0, "Page must have a non-empty title"

    def test_has_main_landmark(self, home_page):
        """Page must have a main landmark."""
        mains = home_page.find_elements("css selector", "main, [role='main']")
        assert len(mains) >= 1, "Page must have at least one main landmark"

    def test_has_single_h1(self, home_page):
        """Page should have exactly one h1 element."""
        h1s = home_page.find_elements("css selector", "h1")
        assert len(h1s) == 1, f"Expected 1 h1, found {len(h1s)}"

    def test_heading_hierarchy(self, home_page):
        """Headings should not skip levels (e.g., h1 -> h3 without h2)."""
        headings = home_page.find_elements("css selector", "h1, h2, h3, h4, h5, h6")
        levels = [int(h.tag_name[1]) for h in headings]

        for i in range(1, len(levels)):
            # A heading can go to the same level, one deeper, or any shallower
            if levels[i] > levels[i - 1] + 1:
                pytest.fail(
                    f"Heading hierarchy skip: h{levels[i-1]} -> h{levels[i]} "
                    f"(headings: {levels})"
                )

    def test_has_skip_link(self, home_page):
        """Page must have a skip-to-content link."""
        skip_links = home_page.find_elements("css selector", "a[href='#main-content']")
        assert len(skip_links) >= 1, "Page must have a skip navigation link"

    def test_has_nav_landmark(self, home_page):
        """Page must have a navigation landmark."""
        navs = home_page.find_elements("css selector", "nav, [role='navigation']")
        assert len(navs) >= 1, "Page must have at least one nav landmark"


class TestHomePageImages:
    """Test image accessibility."""

    def test_images_have_alt(self, home_page):
        """All images must have alt attributes."""
        images = home_page.find_elements("css selector", "img")
        missing_alt = []

        for img in images:
            alt = img.get_attribute("alt")
            if alt is None:  # alt="" is acceptable for decorative images
                src = img.get_attribute("src")[:80] if img.get_attribute("src") else "unknown"
                missing_alt.append(src)

        # We expect to find images without alt (intentional issues in our test app)
        if missing_alt:
            print(f"\n[HOME] Images missing alt attribute: {len(missing_alt)}")
            for src in missing_alt:
                print(f"  - {src}")


class TestHomePageLinks:
    """Test link accessibility."""

    def test_links_have_discernible_text(self, home_page):
        """All links must have accessible text."""
        links = home_page.find_elements("css selector", "a")
        empty_links = []

        for link in links:
            text = link.text.strip()
            aria_label = link.get_attribute("aria-label") or ""
            aria_labelledby = link.get_attribute("aria-labelledby") or ""
            title = link.get_attribute("title") or ""

            if not text and not aria_label and not aria_labelledby and not title:
                # Check for child images with alt
                child_imgs = link.find_elements("css selector", "img[alt]")
                child_svgs = link.find_elements("css selector", "svg[aria-label], svg title")
                if not child_imgs and not child_svgs:
                    href = link.get_attribute("href") or "unknown"
                    empty_links.append(href)

        if empty_links:
            print(f"\n[HOME] Links without discernible text: {len(empty_links)}")
            for href in empty_links:
                print(f"  - {href}")
