import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.airbnb.co.in/")
    page.get_by_role("link", name="Available in Varanasi this").click()
    page.get_by_role("button", name="Close").click()
    with page.expect_popup() as page1_info:
        page.locator(".cnjlbcx.atm_1hykvs1_n7od8j.atm_ej6m29_kb7nvz.atm_15nrvwg_grho7r.atm_1rk3ums_1osqo2v.atm_60t519_idpfg4.atm_1c4w25h_idpfg4.atm_1ujhsu9_idpfg4.atm_or2a6r_idpfg4.atm_5z5wgg_idpfg4.atm_2i514i_oga405.atm_22tueg_kqbfsy.atm_bno8qn_kb7nvz.cp0pqp0 > .s1yvqyx7 > div > .awuxh4x > .cw9aemg > .c14whb16 > a").first.click()
    

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)