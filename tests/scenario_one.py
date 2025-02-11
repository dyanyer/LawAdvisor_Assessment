from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=['--start-maximized'])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.goto('https://www.saucedemo.com/')

    #input the username 'standard_user'
    page.wait_for_timeout(300)    
    page.fill('//input[@name="user-name"]', 'standard_user')

    #input the password 'secret_sauce'
    page.wait_for_timeout(300)
    page.fill('//input[@name="password"]', 'secret_sauce')

    #click the login button
    page.wait_for_timeout(300)
    page.click('//input[@name="login-button"]')

    #add the sauce labs bolt t-shirt
    page.wait_for_timeout(500)
    page.click('//button[@name="add-to-cart-sauce-labs-bolt-t-shirt"]')
 
    #add the sauce labs fleece jacket 
    page.wait_for_timeout(500)
    page.click('//button[@name="add-to-cart-sauce-labs-fleece-jacket"]')

    #extra items just to check the total price, $29.99
    #page.wait_for_timeout(300)
    #page.click('//button[@name="add-to-cart-sauce-labs-backpack"]')

    #click the cart
    page.wait_for_timeout(500)
    page.click('//a[@class="shopping_cart_link"]')

    #check that the items were correctly added to the cart.
    page.wait_for_timeout(500)
    page.screenshot(path="selected_items.png", full_page=True)
    items = 0
    selected_items = page.query_selector_all('//div[@class="cart_item"]')

    for item in selected_items:
        item_name = item.query_selector('//div[@class="inventory_item_name"]').inner_text()
        items += 1

    print("Total of selected Items: " + str(items) + "\n")

    #click the checkout button
    page.wait_for_timeout(500)
    page.click('//button[@name="checkout"]')

    #fill the first name
    page.wait_for_timeout(300)
    page.fill('//input[@name="firstName"]', 'john rey')

    #fill the last name
    page.wait_for_timeout(300)
    page.fill('//input[@name="lastName"]', 'rebusquillo')

    #fill the postal code
    page.wait_for_timeout(300)
    page.fill('//input[@name="postalCode"]', '9999')

    #click the continue button
    page.wait_for_timeout(300)
    page.click('//input[@name="continue"]')


    #check if the price is correct
    page.wait_for_timeout(500)
    page.screenshot(path="items_in_the_cart.png", full_page=True)

    total_price = 0
    price_per_item = page.locator('//div[@class="inventory_item_price"]')
    
    for prices in range(price_per_item.count()):
        price_as_text = price_per_item.nth(prices).inner_text()  #get text like "$15.99"
        item_price = float(price_as_text.replace('$', ''))  #convert to number and remove the dollar sign $
        total_price += item_price  #increment to the total_price
        print ("Item price: $" + str(item_price))

    #print the total price
    print("----------------------")
    print(f"Total Price: ${total_price:.2f}") 
    print("")

    #get the sub total number
    sub_total_label = page.inner_text('//div[@class="summary_subtotal_label"]')
    sub_total = float(sub_total_label.replace('Item total: $', ''))

    print ("Sub Total: $" + str(sub_total) + "\n")

    #if total_price and sub_total is equal, print they are the same. Else print not the same
    if total_price == sub_total:
        print("The total price of the items is equal to the subtotal. \n")
    else:
        print ("not the same \n")
    
    #wait for a while then click the button finish,
    page.wait_for_timeout(500)
    page.click('//button[@name="finish"]')
    page.screenshot(path="finish.png", full_page=True)

    #check if the thank you for your order page is displayed
    display_message = page.text_content('//h2[@class="complete-header"]') #get the text content of the error message
    expected_message = "Thank you for your order!"

    #if expected message exist in error message print the validation message else print other error message
    if expected_message in display_message:
        print(expected_message + " page is displayed.")
    else:
        print("ERROR")

    #wait for 2 seconds then close the browser
    page.wait_for_timeout(2000)
    browser.close()