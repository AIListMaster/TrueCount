import json

from playwright.async_api import Playwright, async_playwright


async def extract_data(page) -> list:
    """
    Extracts the results information from the page

    Args:
        page: Playwright page object

    Returns:
        A list containing details of results as dictionary. The dictionary
         has title, review count, rating, address of various results
    """

    # Xpaths.
    review_box_xpath = '//div[@jscontroller="fIQYlf"] '
    review_xpath = '//span[@data-expandable-section]'
    secondary_review_xpath = '//span[@class="review-full-text"]'
    author_xpath = '//div[@class="TSUbDb"]'
    title_xpath = '//div[@data-attrid="title"]'
    address_xpath = '//div[@data-attrid="kc:/location/location:address"]'
    image_xpath = '//button[data-clid="local-photo-browser"]//img'

    # Scraped data
    data = []

    # Scrap title.
    try:
        title = await page.locator(title_xpath).inner_text()
    except:
        title = ""

    # Scrap address
    try:
        address = await page.locator(address_xpath).inner_text()
    except:
        address = ""

    # Scrap Image
    # try:
    #     image = await page.locator(image_xpath).get_attribute("src")
    # except:
    #     image = ""

    data.append({
        "title": title,
        "address": address,
        "items": []
    })

    await page.wait_for_selector(review_box_xpath)
    review_box = page.locator(review_box_xpath)
    items = []
    for review_box_index in range(await review_box.count()):
        result_elem = review_box.nth(review_box_index)
        # Scrap review text.
        elements = await result_elem.locator(review_xpath).element_handles()
        try:
            review = await elements[0].inner_text()
            review = review if review else await result_elem.locator(
                secondary_review_xpath).inner_text()
        except:
            review = ""

        # Scrap author name.
        try:
            author_name = await result_elem.locator(author_xpath).inner_text()
        except:
            author_name = ""

        # Prepare list.
        items.append({
            'author_name': author_name,
            'review': review,
        })

    data[0]['items'] = items

    return data


async def run(playwright: Playwright, search_term: str) -> None:
    """
    Main function which launches browser instance and performs browser
    interactions

    Args:
        playwright: Playwright instance
    """
    browser = await playwright.chromium.launch(
        headless=True,
        # proxy={'server': '127.0.0.1', 'port': 4444}
    )
    context = await browser.new_context()

    # Open new page
    page = await context.new_page()

    # Go to https://www.google.com/
    await page.goto("https://www.google.com/")

    # Type search query
    await page.locator("[aria-label=\"Search\"]").type(search_term)

    # Press enter to search in google
    await page.keyboard.press('Enter')

    # wait for review button
    await page.locator(
        '//a[@data-async-trigger="reviewDialog"]').first.wait_for(
        timeout=10000)

    # Click reviews button
    await page.locator('//a[@data-async-trigger="reviewDialog"]').first.click()

    # Initialize the number of pagination required
    pagination_limit = 3

    # Iterate to load reviews for mentioned number of pages
    for page_number in range(pagination_limit):
        await page.locator('//div[@class="review-dialog-list"]').hover()
        await page.mouse.wheel(0, 100000)
        page_number += 1
        await page.wait_for_timeout(2000)

    # Extract all displayed reviews
    data = await extract_data(page)

    # Save all extracted data as a JSON file
    with open('google_reviews.json', 'w') as f:
        json.dump(data, f, indent=2)

    # ---------------------
    await context.close()
    await browser.close()


async def scraper(text=None) -> None:
    if text:
        async with async_playwright() as playwright:
            await run(playwright, search_term=text)
