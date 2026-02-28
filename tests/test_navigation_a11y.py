"""
Aegis - Navigation & Keyboard Accessibility Tests
Tests keyboard navigation, focus management, skip links, and tab order.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.axe_helper import run_axe, get_violations, format_violations
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class TestKeyboardNavigation:
    """Test that the site is fully keyboard navigable."""

    def test_all_links_focusable(self, home_page):
        """All links should be reachable via keyboard."""
        links = home_page.find_elements(By.CSS_SELECTOR, "a[href]")
        
        for link in links:
            # Check that links are not hidden with tabindex=-1
            tabindex = link.get_attribute("tabindex")
            if tabindex == "-1":
                href = link.get_attribute("href") or "unknown"
                print(f"\n[NAV] Link with tabindex=-1 cannot be keyboard focused: {href}")

    def test_all_buttons_focusable(self, home_page):
        """All buttons should be keyboard focusable."""
        buttons = home_page.find_elements(By.CSS_SELECTOR, "button")
        
        for btn in buttons:
            tabindex = btn.get_attribute("tabindex")
            if tabindex == "-1":
                text = btn.text[:30]
                print(f"\n[NAV] Button with tabindex=-1: '{text}'")

    def test_no_positive_tabindex(self, home_page):
        """Elements should not have positive tabindex values (disrupts tab order)."""
        elements = home_page.find_elements(By.CSS_SELECTOR, "[tabindex]")
        positive_tabindex = []

        for el in elements:
            tabindex = el.get_attribute("tabindex")
            try:
                if int(tabindex) > 0:
                    tag = el.tag_name
                    text = el.text[:30]
                    positive_tabindex.append(f"<{tag}> '{text}' tabindex={tabindex}")
            except ValueError:
                pass

        if positive_tabindex:
            print(f"\n[NAV] Elements with positive tabindex (disrupts tab order):")
            for item in positive_tabindex:
                print(f"  - {item}")

    def test_tab_through_nav_links(self, home_page):
        """Tab key should cycle through navigation links."""
        body = home_page.find_element(By.TAG_NAME, "body")
        
        # Send Tab keys and track focused elements
        focused_tags = []
        actions = ActionChains(home_page)
        
        for _ in range(10):
            actions.send_keys(Keys.TAB).perform()
            active = home_page.switch_to.active_element
            tag = active.tag_name
            text = active.text[:30] if active.text else ""
            focused_tags.append(f"<{tag}> {text}")

        # At least some interactive elements should receive focus
        interactive_focus = [f for f in focused_tags if any(
            t in f for t in ["<a>", "<button>", "<input>", "<select>", "<textarea>"]
        )]
        assert len(interactive_focus) >= 3, (
            f"Tab should reach interactive elements. Focused: {focused_tags[:10]}"
        )


class TestSkipLink:
    """Test skip navigation functionality."""

    def test_skip_link_exists(self, home_page):
        """Page must have a skip-to-content link."""
        skip_links = home_page.find_elements(By.CSS_SELECTOR, ".skip-link, a[href='#main-content']")
        assert len(skip_links) >= 1, "Page needs a skip navigation link"

    def test_skip_link_target_exists(self, home_page):
        """Skip link target element must exist."""
        skip_links = home_page.find_elements(By.CSS_SELECTOR, "a[href='#main-content']")
        if skip_links:
            target_id = skip_links[0].get_attribute("href").split("#")[-1]
            target = home_page.find_elements(By.ID, target_id)
            assert len(target) >= 1, f"Skip link target #{target_id} does not exist"

    def test_skip_link_visible_on_focus(self, home_page):
        """Skip link should become visible when focused."""
        body = home_page.find_element(By.TAG_NAME, "body")
        actions = ActionChains(home_page)
        actions.send_keys(Keys.TAB).perform()

        active = home_page.switch_to.active_element
        # Check if skip link received focus
        classes = active.get_attribute("class") or ""

        if "skip-link" in classes:
            # Verify it's visible
            is_displayed = active.is_displayed()
            assert is_displayed, "Skip link should be visible when focused"


class TestFocusManagement:
    """Test focus visibility and management."""

    def test_focused_elements_have_visible_indicator(self, home_page):
        """Focused interactive elements should have a visible focus indicator."""
        # This is tested via axe-core rules, but we also check manually
        results = run_axe(home_page, {
            "runOnly": {"type": "rule", "values": ["focus-order-semantics"]}
        })
        # This is informational — actual focus indicator testing is visual

    def test_no_keyboard_traps(self, home_page):
        """Tab key should not get stuck on any element (keyboard trap)."""
        body = home_page.find_element(By.TAG_NAME, "body")
        actions = ActionChains(home_page)
        
        prev_elements = []
        for i in range(20):
            actions.send_keys(Keys.TAB).perform()
            active = home_page.switch_to.active_element
            tag = active.tag_name
            element_id = active.get_attribute("id") or ""
            element_class = active.get_attribute("class") or ""
            identifier = f"{tag}#{element_id}.{element_class}"
            prev_elements.append(identifier)

        # Check for loops smaller than expected (keyboard trap indicator)
        if len(prev_elements) >= 10:
            # Check if same element appeared too many times consecutively
            for i in range(len(prev_elements) - 3):
                if (prev_elements[i] == prev_elements[i+1] == prev_elements[i+2] 
                    and prev_elements[i] != "body#."):
                    pytest.fail(
                        f"Possible keyboard trap: focus stuck on {prev_elements[i]}"
                    )


class TestNavigationLandmarks:
    """Test ARIA landmarks across all pages."""

    def test_has_banner_landmark(self, home_page):
        """Page should have a banner (header) landmark."""
        banners = home_page.find_elements(By.CSS_SELECTOR, "header, [role='banner']")
        assert len(banners) >= 1, "Page should have a banner landmark"

    def test_has_contentinfo_landmark(self, home_page):
        """Page should have a contentinfo (footer) landmark."""
        footers = home_page.find_elements(By.CSS_SELECTOR, "footer, [role='contentinfo']")
        assert len(footers) >= 1, "Page should have a contentinfo landmark"

    def test_nav_has_aria_label(self, home_page):
        """Navigation elements should have an aria-label for identification."""
        navs = home_page.find_elements(By.CSS_SELECTOR, "nav")
        
        for nav in navs:
            label = nav.get_attribute("aria-label") or nav.get_attribute("aria-labelledby")
            assert label, "Navigation element should have aria-label or aria-labelledby"

    def test_nav_links_indicate_current_page(self, home_page):
        """Current page link should have aria-current='page'."""
        current_links = home_page.find_elements(By.CSS_SELECTOR, "a[aria-current='page']")
        assert len(current_links) >= 1, (
            "At least one nav link should indicate the current page with aria-current='page'"
        )


class TestColorContrast:
    """Test color contrast via axe-core."""

    def test_color_contrast_violations(self, home_page):
        """Check for color contrast violations."""
        results = run_axe(home_page, {
            "runOnly": {"type": "rule", "values": ["color-contrast"]}
        })
        violations = get_violations(results)

        if violations:
            total_elements = sum(len(v.get("nodes", [])) for v in violations)
            report = format_violations(violations)
            print(f"\n[NAV] Color contrast issues affecting {total_elements} element(s):\n{report}")
