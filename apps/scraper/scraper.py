import json

from playwright.async_api import Playwright, async_playwright
from apps.scraper.models import Business, Reviews
from apps.utils.utils import slugify
import re


async def extract_reviews_data(page) -> list:
    """
    Extracts the results information from the page

    Args:
        page: Playwright page object

    Returns:
        A list containing details of results as dictionary. The dictionary
         has contributor name and review.
    """

    # Xpaths.
    review_box_xpath = '//div[@jscontroller="fIQYlf"] '
    review_xpath = '//span[@data-expandable-section]'
    secondary_review_xpath = '//span[@class="review-full-text"]'
    contributor_name_xpath = '//div[@class="TSUbDb"]'
    contributor_id_xpath = '//div[@class="TSUbDb"]//a'
    review_id_xpath = '//button[@data-ri]'
    rating_xpath = '//span[contains(@aria-label, "Rated")]'

    # Regex patterns
    rating_pattern = r"(\d+\.\d+)"

    # Scraped data
    data = []

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

        # Scrap contributor name.
        try:
            name = await result_elem.locator(contributor_name_xpath).inner_text()
        except:
            name = ""

        # Scrap review id
        try:
            review_id = await result_elem.locator(review_id_xpath).first.get_attribute('data-ri')
        except:
            review_id = ""

        try:
            contributor_id = ""
            _href = await result_elem.locator(contributor_id_xpath).first.get_attribute('href')
            if _href is not None:
                temp = re.findall(r'\d+', _href)
                res = list(map(int, temp))
                if res[0]:
                    contributor_id = str(res[0])
        except:
            contributor_id = ""

        # Scrap rating.
        try:
            rating_text = await result_elem.locator(rating_xpath).first.get_attribute(
                'aria-label')
            match = re.search(rating_pattern, rating_text)
            if match:
                rating = float(match.group(1))
            else:
                rating = 0.0
        except:
            rating = 0.0

        # Sentiment
        sentiment_mapping = {rating < 2.5: 0, 2.5 <= rating < 3.5: 1, rating > 3.5: 2}
        sentiment = sentiment_mapping.get(True, 0)

        # Prepare list.
        data.append({
            'id': review_id,
            'contributor_name': name,
            'contributor_id': contributor_id,
            'review': review,
            'rating': rating,
            'sentiment': sentiment
        })

    return data


async def extract_business_data(page) -> dict:
    """
    Extracts business information from the page

    Args:
        page: Playwright page object

    Returns:
        A dictionary containing business information from the page
    """

    data = {}

    # Xpaths
    business_title_xpath = '//div[@role="main"]//h1'
    business_address_xpath = '//button[@data-item-id="address"]'
    business_website_xpath = '//a[@data-item-id="authority"]'
    business_phone_xpath = '//button[starts-with(@data-item-id, "phone:tel:")]'
    business_category_xpath = '//button[contains(@jsaction, "category")]'
    business_image_url_xpath = '//button[contains(@jsaction, "heroHeaderImage")]//img'

    # Business title
    try:
        business_title = await page.locator(business_title_xpath).first.inner_text()
    except:
        business_title = ''

    # Business address
    try:
        business_address = await page.locator(business_address_xpath).first.inner_text()
    except:
        business_address = ""

    # Business website
    try:
        business_website = await page.locator(business_website_xpath).first.get_attribute('href')
    except:
        business_website = ""

    # Business phone
    try:
        business_phone = await page.locator(business_phone_xpath).first.inner_text()
    except:
        business_phone = ""

    # Business category
    try:
        business_category = await page.locator(business_category_xpath).first.inner_text()
    except:
        business_category = ''

    # Business image
    try:
        business_image = await page.locator(business_image_url_xpath).first.get_attribute('src')
    except:
        business_image = ""

    data = {
        'title': business_title,
        'address': business_address,
        'website': business_website,
        'phone': business_phone,
        'category': business_category,
        'image': business_image
    }

    return data


def add_business(pid: str, data: dict):
    # Insert data to database.
    business = None
    if pid and data.get('title'):
        title = data.get('title')
        business = Business(
            business_id=pid,
            title=title,
            address=data.get('address'),
            website=data.get('website'),
            phone=data.get('phone'),
            category=data.get('category'),
            image=data.get('image'),
            slug=slugify(title)
        )
        if business.exist():
            business = business.update()
        else:
            business = business.create()

    return business


def add_business_reviews(business_id: int, data: list) -> list:
    reviews = []
    if business_id:
        for item in data:
            review = Reviews(
                review_id=item.get('id'),
                rating=item.get('rating'),
                sentiment=item.get('sentiment'),
                contributor_name=item.get('contributor_name'),
                contributor_id=item.get('contributor_id'),
                review=item.get('review'),
                business_id=business_id
            )
            if review.exist():
                review = review.update()
            else:
                review = review.create()
            reviews.append(review)
    return reviews


async def run(playwright: Playwright, search_term: str) -> Business | None:
    """
    Main function which launches browser instance and performs browser
    interactions

    Args:
        playwright: Playwright instance
    """
    browser = await playwright.chromium.launch(
        headless=False,
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

    # Get place id.
    try:
        pid = await page.locator(
            '//div[@data-attribution="lu-rap-thank-you-dialog"]').first.get_attribute('data-pid')
    except:
        pid = None

    # Returnable business.
    business = None
    if pid:
        # Click reviews button
        await page.locator('//a[@data-async-trigger="reviewDialog"]').first.click()

        # Initialize the number of pagination required
        pagination_limit = 10

        # Iterate to load reviews for mentioned number of pages
        for page_number in range(pagination_limit):
            await page.locator('//div[@class="review-dialog-list"]').hover()
            await page.mouse.wheel(0, 100000)
            page_number += 1
            await page.wait_for_timeout(2000)

        # Extract all displayed reviews
        reviews = await extract_reviews_data(page)

        # Close review dialog.
        await page.locator('//g-lightbox//div[@aria-label="Close"]').last.click()

        # Wait for map button
        await page.locator(
            '//a[starts-with(@href, "/maps/place/")]').first.wait_for(
            timeout=10000)

        # Click map link
        await page.locator('//a[starts-with(@href, "/maps/place/")]').first.click()

        # Wait form main container
        await page.locator('[role="main"]').first.wait_for(
            timeout=10000)

        # Extract all displayed reviews
        data = await extract_business_data(page)
        if data:
            business = add_business(pid, data)

        # Insert reviews.
        if reviews and business:
            new_reviews = add_business_reviews(business.id, reviews)

        # Save all extracted data as a JSON file - Used for testing
        with open('google_reviews.json', 'w') as f:
            json.dump(reviews, f, indent=2)

    # ---------------------
    await context.close()
    await browser.close()

    return business


async def scraper(text=None) -> Business | None:
    business = None
    if text:
        async with async_playwright() as playwright:
            business = await run(playwright, search_term=text)
    return business
