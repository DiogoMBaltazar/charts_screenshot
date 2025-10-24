"""TradingView screenshot scraper using Playwright."""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from playwright.async_api import async_playwright, Browser, Page
from config import (
    CRYPTO_SYMBOLS, SCREENSHOTS_DIR, SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT,
    BROWSER_HEADLESS, BROWSER_TIMEOUT, TIMESTAMP_FORMAT
)


class TradingViewScraper:
    """Handles browser automation and screenshot capture for TradingView charts."""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    async def start_browser(self) -> None:
        """Initialize the browser instance."""
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=BROWSER_HEADLESS,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            self.logger.info("Browser started successfully")
        except Exception as e:
            self.logger.error(f"Failed to start browser: {e}")
            raise
    
    async def close_browser(self) -> None:
        """Close the browser instance."""
        if self.browser:
            await self.browser.close()
            self.logger.info("Browser closed")
    
    async def _wait_for_chart_load(self, page: Page) -> None:
        """Wait for TradingView chart to fully load."""
        try:
            # Wait for the chart container to be visible
            await page.wait_for_selector('[data-name="legend-source-item"]', timeout=BROWSER_TIMEOUT)
            
            # Additional wait for chart data to load
            await asyncio.sleep(3)
            
            self.logger.info("Chart loaded successfully")
        except Exception as e:
            self.logger.warning(f"Chart loading timeout or error: {e}")
            # Continue anyway, might still capture something useful
    
    async def _configure_chart_view(self, page: Page) -> None:
        """Configure chart for optimal screenshot capture."""
        try:
            # Try to hide unnecessary UI elements for cleaner screenshots
            await page.evaluate("""
                // Hide header if possible
                const header = document.querySelector('[data-name="header"]');
                if (header) header.style.display = 'none';
                
                // Hide bottom toolbar if possible
                const toolbar = document.querySelector('[data-name="bottom-toolbar"]');
                if (toolbar) toolbar.style.display = 'none';
            """)
            
            self.logger.info("Chart view configured")
        except Exception as e:
            self.logger.warning(f"Could not configure chart view: {e}")
    
    async def capture_screenshot(self, symbol: str, url: str) -> Optional[str]:
        """Capture a screenshot for a specific cryptocurrency symbol."""
        if not self.browser:
            raise RuntimeError("Browser not initialized. Call start_browser() first.")
        
        page = None
        try:
            # Create new page
            page = await self.browser.new_page()
            await page.set_viewport_size({"width": SCREENSHOT_WIDTH, "height": SCREENSHOT_HEIGHT})
            
            self.logger.info(f"Navigating to {symbol} chart...")
            await page.goto(url, timeout=BROWSER_TIMEOUT)
            
            # Wait for chart to load
            await self._wait_for_chart_load(page)
            
            # Configure chart view
            await self._configure_chart_view(page)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
            filename = f"{symbol}_{timestamp}.png"
            filepath = SCREENSHOTS_DIR / filename
            
            # Take screenshot
            await page.screenshot(path=str(filepath), full_page=False)
            
            self.logger.info(f"Screenshot saved: {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Failed to capture screenshot for {symbol}: {e}")
            return None
        finally:
            if page:
                await page.close()
    
    async def capture_all_screenshots(self) -> Dict[str, Optional[str]]:
        """Capture screenshots for all configured cryptocurrency symbols."""
        results = {}
        
        for symbol, url in CRYPTO_SYMBOLS.items():
            try:
                filepath = await self.capture_screenshot(symbol, url)
                results[symbol] = filepath
            except Exception as e:
                self.logger.error(f"Error capturing {symbol}: {e}")
                results[symbol] = None
        
        return results


async def main():
    """Test function to capture screenshots once."""
    scraper = TradingViewScraper()
    
    try:
        await scraper.start_browser()
        results = await scraper.capture_all_screenshots()
        
        print("Screenshot results:")
        for symbol, filepath in results.items():
            if filepath:
                print(f"✓ {symbol}: {filepath}")
            else:
                print(f"✗ {symbol}: Failed")
                
    finally:
        await scraper.close_browser()


if __name__ == "__main__":
    asyncio.run(main())
