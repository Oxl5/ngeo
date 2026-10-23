
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse

PAGE_URL = (
    "https://www.elahmad.ru/tv/mobiletv/"
    "glarb.php?id=natgeo_1"
)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        def on_response(response):
            url = response.url
            host = urlparse(url).netloc.lower()

            if (
                "apistorageworks.shop" in host
                or "m3u8" in url.lower()
                or "playlist.html" in url.lower()
                or "mpd" in url.lower()
            ):
                print("MATCH:", response.status, url)

        page.on("response", on_response)

        try:
            response = page.goto(
                PAGE_URL,
                wait_until="domcontentloaded",
                timeout=60000,
            )

            print("PAGE:", page.url)
            print(
                "STATUS:",
                response.status if response else "No response",
            )
            print("TITLE:", page.title())

            page.wait_for_timeout(30000)
            print("Finished 30-second observation.")

        except Exception as exc:
            print("ERROR:", repr(exc))

        finally:
            browser.close()

if __name__ == "__main__":
    main()
