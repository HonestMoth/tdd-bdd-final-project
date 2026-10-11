"""Selenium step definitions for the Product Catalog UI."""

import os

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


WAIT_SECONDS = 10

FIELD_IDS = {
    "id": "product_id",
    "name": "product_name",
    "description": "product_description",
    "available": "product_available",
    "category": "product_category",
    "price": "product_price",
}


def wait_for_element(context, by, selector):
    """Wait until an element is present in the page."""
    return WebDriverWait(context.driver, WAIT_SECONDS).until(
        EC.presence_of_element_located((by, selector))
    )


def get_field(context, field):
    """Resolve a field name to its HTML ID."""
    key = field.strip().lower()
    selector = FIELD_IDS.get(key, key)
    return wait_for_element(context, By.ID, selector)


def get_button(context, button):
    """Find a button by its HTML ID."""
    selector = f"{button.strip().lower()}-btn"
    return wait_for_element(context, By.ID, selector)


def wait_for_search(context):
    """Wait until the search results container is visible."""
    return WebDriverWait(context.driver, WAIT_SECONDS).until(
        EC.visibility_of_element_located((By.ID, "search_results"))
    )


@given('I visit the "{page_name}"')
@when('I visit the "{page_name}"')
def step_visit_page(context, page_name):
    """Open the requested application page."""
    if page_name.strip().lower() != "home page":
        raise AssertionError(f"Unsupported page: {page_name}")

    base_url = os.getenv(
        "PRODUCTS_BASE_URL",
        "http://localhost:8080",
    ).rstrip("/")

    context.driver.get(f"{base_url}/")


@when('I set the "{field}" to "{value}"')
def step_set_field(context, field, value):
    """Enter a value into a form field."""
    element = get_field(context, field)
    element.clear()
    element.send_keys(value)


@when('I select "{value}" in the "{field}" dropdown')
def step_select_dropdown(context, value, field):
    """Select an option from a dropdown."""
    Select(get_field(context, field)).select_by_visible_text(value)


@when('I press the "{button}" button')
def step_press_button(context, button):
    """Click the requested button."""
    get_button(context, button).click()


@when('I copy the "{field}" field')
def step_copy_field(context, field):
    """Copy a field's current value into the test context."""
    context.copied_value = get_field(
        context, field
    ).get_attribute("value")


@when('I paste the "{field}" field')
def step_paste_field(context, field):
    """Paste the copied value into a field."""
    element = get_field(context, field)
    element.clear()
    element.send_keys(context.copied_value)


@then('I should see "{value}" in the "{field}" field')
def step_check_field(context, value, field):
    """Verify that a field contains the expected value."""
    def field_value_matches(_driver):
        element = get_field(context, field)
        actual = element.get_attribute("value") or element.text
        return actual if actual == value else False

    actual = WebDriverWait(context.driver, WAIT_SECONDS).until(
        field_value_matches
    )

    assert actual == value, (
        f"Expected {field}={value!r}, got {actual!r}"
    )


@then('the "{field}" checkbox should be checked')
def step_checkbox_checked(context, field):
    """Verify that the requested control is selected."""
    element = get_field(context, field)

    assert element.is_selected(), (
        f"{field} control should be selected"
    )


@then('the "{field}" dropdown should be set to "{value}"')
def step_dropdown_value(context, field, value):
    """Verify the selected dropdown option."""
    selected = Select(
        get_field(context, field)
    ).first_selected_option.text

    assert selected == value, (
        f"Expected {field}={value!r}, got {selected!r}"
    )


@then('I should see "{value}" in the results')
def step_result_present(context, value):
    """Wait until the expected value appears in search results."""

    def value_is_present(driver):
        results = driver.find_element(By.ID, "search_results")
        return value in results.text

    WebDriverWait(context.driver, WAIT_SECONDS).until(
        value_is_present
    )

    results = context.driver.find_element(By.ID, "search_results")
    assert value in results.text, (
        f"Expected {value!r} in results: {results.text}"
    )


@then('I should not see "{value}" in the results')
def step_result_absent(context, value):
    """Verify that the search results do not contain a value."""
    results = wait_for_search(context)

    assert value not in results.text, (
        f"Did not expect {value!r} in results: {results.text}"
    )


@then('I should see the message "{message}"')
def step_flash_message(context, message):
    """Wait for the expected flash message."""
    def matching_message(driver):
        element = driver.find_element(By.ID, "flash_message")
        actual = element.text.strip()
        return actual if message in actual else False

    try:
        actual = WebDriverWait(context.driver, WAIT_SECONDS).until(
            matching_message
        )
    except Exception as exc:
        element = wait_for_element(
            context,
            By.ID,
            "flash_message",
        )
        actual = element.text.strip()

        raise AssertionError(
            f"Expected flash message {message!r}; "
            f"actual message: {actual!r}"
        ) from exc

    assert message in actual
