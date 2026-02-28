"""
Aegis - Form Page Accessibility Tests
Tests form labels, error handling, required fields, and fieldsets.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.axe_helper import (
    run_axe, run_axe_wcag2aa, get_violations, get_violations_by_impact,
    format_violations
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class TestFormAxeScan:
    """axe-core scans of the form page."""

    def test_full_scan(self, form_page):
        """Run full axe-core scan on the contact form page."""
        results = run_axe(form_page)
        violations = get_violations(results)

        if violations:
            report = format_violations(violations)
            print(f"\n[FORM] Full scan found {len(violations)} violation(s):\n{report}")

    def test_wcag2aa_compliance(self, form_page):
        """Check WCAG 2.0 AA compliance on form page."""
        results = run_axe_wcag2aa(form_page)

        critical = get_violations_by_impact(results, "critical")
        assert len(critical) == 0, (
            f"Found {len(critical)} critical violation(s):\n"
            f"{format_violations(critical)}"
        )


class TestFormLabels:
    """Test that form inputs have proper labels."""

    def test_text_inputs_have_labels(self, form_page):
        """All text inputs should have associated labels."""
        inputs = form_page.find_elements(By.CSS_SELECTOR,
            "input[type='text'], input[type='email'], input[type='tel'], "
            "input[type='password'], input[type='url'], input[type='search']"
        )
        unlabeled = []

        for inp in inputs:
            inp_id = inp.get_attribute("id")
            aria_label = inp.get_attribute("aria-label")
            aria_labelledby = inp.get_attribute("aria-labelledby")
            
            has_label = False
            if inp_id:
                labels = form_page.find_elements(By.CSS_SELECTOR, f"label[for='{inp_id}']")
                if labels:
                    has_label = True
            if aria_label or aria_labelledby:
                has_label = True
            # Check if wrapped in a label
            if not has_label:
                try:
                    parent = inp.find_element(By.XPATH, "./ancestor::label")
                    if parent:
                        has_label = True
                except:
                    pass

            if not has_label:
                name = inp.get_attribute("name") or inp.get_attribute("id") or "unnamed"
                unlabeled.append(name)

        if unlabeled:
            print(f"\n[FORM] Unlabeled text inputs: {unlabeled}")
            # This is an expected failure (phone field has no label)
        
        # All inputs must have labels
        assert len(unlabeled) == 0, (
            f"Unlabeled inputs found: {unlabeled}"
        )

    def test_select_has_label(self, form_page):
        """Select elements should have labels."""
        selects = form_page.find_elements(By.CSS_SELECTOR, "select")

        for select in selects:
            sel_id = select.get_attribute("id")
            if sel_id:
                labels = form_page.find_elements(By.CSS_SELECTOR, f"label[for='{sel_id}']")
                assert len(labels) >= 1, f"Select #{sel_id} is missing a label"

    def test_textarea_has_label(self, form_page):
        """Textarea elements should have labels."""
        textareas = form_page.find_elements(By.CSS_SELECTOR, "textarea")

        for ta in textareas:
            ta_id = ta.get_attribute("id")
            if ta_id:
                labels = form_page.find_elements(By.CSS_SELECTOR, f"label[for='{ta_id}']")
                assert len(labels) >= 1, f"Textarea #{ta_id} is missing a label"


class TestFormRequiredFields:
    """Test required field indicators and validation."""

    def test_required_fields_have_aria(self, form_page):
        """Required inputs should have aria-required='true'."""
        required_inputs = form_page.find_elements(By.CSS_SELECTOR, "input[required], select[required], textarea[required]")
        
        assert len(required_inputs) >= 1, "Form should have at least one required field"

        for inp in required_inputs:
            aria_req = inp.get_attribute("aria-required")
            name = inp.get_attribute("name") or inp.get_attribute("id")
            assert aria_req == "true", (
                f"Required input '{name}' should have aria-required='true'"
            )

    def test_error_messages_associated(self, form_page):
        """Error messages should be properly associated with inputs."""
        error_msgs = form_page.find_elements(By.CSS_SELECTOR, ".error-msg[id]")
        
        for err in error_msgs:
            err_id = err.get_attribute("id")
            role = err.get_attribute("role")
            assert role in ("alert", "status", None), (
                f"Error message #{err_id} should have role='alert'"
            )


class TestFormValidation:
    """Test form validation accessibility."""

    def test_invalid_input_gets_aria_invalid(self, form_page):
        """Invalid inputs should get aria-invalid='true' on submission."""
        submit_btn = form_page.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()

        import time
        time.sleep(0.5)

        invalid_inputs = form_page.find_elements(By.CSS_SELECTOR, "[aria-invalid='true']")
        assert len(invalid_inputs) >= 1, (
            "Invalid form inputs should have aria-invalid='true'"
        )

    def test_focus_moves_to_first_error(self, form_page):
        """Focus should move to the first field with an error."""
        submit_btn = form_page.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()

        import time
        time.sleep(0.5)

        active = form_page.switch_to.active_element
        active_tag = active.tag_name
        assert active_tag in ("input", "select", "textarea"), (
            f"Focus should move to first error input, but active element is <{active_tag}>"
        )


class TestFormFieldsets:
    """Test fieldset and legend usage."""

    def test_fieldsets_have_legends(self, form_page):
        """Each fieldset should have a legend."""
        fieldsets = form_page.find_elements(By.CSS_SELECTOR, "fieldset")

        for i, fs in enumerate(fieldsets):
            legends = fs.find_elements(By.CSS_SELECTOR, "legend")
            assert len(legends) >= 1, f"Fieldset {i+1} is missing a legend"

    def test_radio_group_in_fieldset(self, form_page):
        """Radio button groups should be within a fieldset."""
        radios = form_page.find_elements(By.CSS_SELECTOR, "input[type='radio']")

        for radio in radios:
            try:
                parent_fs = radio.find_element(By.XPATH, "./ancestor::fieldset")
                assert parent_fs is not None
            except:
                name = radio.get_attribute("name")
                pytest.fail(f"Radio button '{name}' is not within a fieldset")
