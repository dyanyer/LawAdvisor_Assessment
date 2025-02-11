from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=['--start-maximized'])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.goto('https://www.saucedemo.com/')

    #input the username
    page.wait_for_timeout(500)
    page.fill('//input[@name="user-name"]', 'locked_out_user')

    #input the password
    page.wait_for_timeout(500)
    page.fill('//input[@name="password"]', 'secret_sauce')

    #click the login
    page.wait_for_timeout(500)
    page.click('//input[@name="login-button"]')

    #wait then screenshot the page
    page.wait_for_timeout(500)
    page.screenshot(path="check_image.png", full_page=True)

    #check if the validation message: “Epic sadface: Sorry, this user has been locked out” is displayed.
    error_message = page.text_content('//h3[@data-test="error"]') #get the text content of the error message
    expected_message = "Epic sadface: Sorry, this user has been locked out."

    #if expected message exist in error message print the validation message else print other error message
    if expected_message in error_message:
        print("Validation message: " + expected_message + " is displayed.")
    else:
        print(error_message)

    #wait for 1 secs then close.
    page.wait_for_timeout(1000)
    browser.close()
