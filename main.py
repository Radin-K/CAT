from playwright.sync_api import sync_playwright


from proxies import proxy_rotation
import pandas as pd
data = {
    "part-number": [],
    "name": [],
    "properties": [],
    "img": []
}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    proxies = proxy_rotation()
    context = browser.new_context(proxy={
        "server": f"http://{proxies[0]}:{proxies[1]}",
        "username": proxies[2],
        "password": proxies[3]
    },user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://parts.cat.com/en/catcorp")
    page.wait_for_load_state("domcontentloaded")
    category = page.get_by_alt_text("Image for Attachments")
    category.click()
    page.wait_for_timeout(5000)
    cards = page.locator("//div[contains(@class,'product-comparison-grid_product-comparison__card-container__b3YZa p-3 px-md-3 pb-md-2 px-2 d-grid position-relative pb-sm-3 category-product-grid-wrapper_category-grid-card-information__wrapper__vDBsL')]").all()
    for card in cards:
        id_name = card.locator("xpath=.//h2").text_content().split(":")
        data['part-number'] = id_name[0]
        data['name'] = id_name[1]
        prs = card.locator("xpath=.//div[contains(@data-testid, 'product-attributes')]").all()
        attrs = {}
        for pr in prs:
            pr_texts = pr.locator("xpath=./p").all()
            attrs[pr_texts[0].text_content()] = pr_texts[1].text_content()

        data['properties'].append(attrs)
        img = card.locator("xpath=./div/a/img").get_attribute("src")
        print(img)
        data["img"].append(img)


pd_df = pd.DataFrame(data)
pd_df.to_csv("products.csv")
