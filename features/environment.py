"""Behave browser lifecycle hooks."""

from selenium import webdriver


def before_scenario(context, scenario):
    """Start a headless Chrome session for each scenario."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1440,1000")
    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(2)


def after_scenario(context, scenario):
    """Always close the browser, including after failed scenarios."""
    driver = getattr(context, "driver", None)
    if driver is not None:
        driver.quit()
