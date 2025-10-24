"""Main pipeline for automated TradingView screenshot capture."""

import asyncio
import logging
import signal
import sys
from datetime import datetime
from pathlib import Path

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from tradingview_scraper import TradingViewScraper
from config import SCREENSHOT_INTERVAL_MINUTES, LOGS_DIR


class ScreenshotPipeline:
    """Main pipeline orchestrator for automated screenshot capture."""
    
    def __init__(self):
        self.scraper = TradingViewScraper()
        self.scheduler = AsyncIOScheduler()
        self.logger = self._setup_logger()
        self.running = False
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logging configuration with file output."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
            
            # File handler
            log_file = LOGS_DIR / f"pipeline_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.running = False
    
    async def capture_screenshots_job(self):
        """Job function to capture screenshots for all symbols."""
        try:
            self.logger.info("Starting screenshot capture job...")
            
            results = await self.scraper.capture_all_screenshots()
            
            # Log results
            successful = sum(1 for filepath in results.values() if filepath)
            total = len(results)
            
            self.logger.info(f"Screenshot job completed: {successful}/{total} successful")
            
            for symbol, filepath in results.items():
                if filepath:
                    self.logger.info(f"✓ {symbol}: {Path(filepath).name}")
                else:
                    self.logger.error(f"✗ {symbol}: Failed to capture")
                    
        except Exception as e:
            self.logger.error(f"Error in screenshot job: {e}")
    
    async def start(self):
        """Start the screenshot pipeline."""
        try:
            self.logger.info("Starting TradingView Screenshot Pipeline...")
            
            # Initialize browser
            await self.scraper.start_browser()
            
            # Schedule the job to run every minute
            self.scheduler.add_job(
                self.capture_screenshots_job,
                trigger=IntervalTrigger(minutes=SCREENSHOT_INTERVAL_MINUTES),
                id='screenshot_job',
                name='TradingView Screenshot Capture',
                max_instances=1  # Prevent overlapping jobs
            )
            
            # Start scheduler
            self.scheduler.start()
            self.running = True
            
            self.logger.info(f"Pipeline started. Screenshots will be captured every {SCREENSHOT_INTERVAL_MINUTES} minute(s)")
            self.logger.info("Press Ctrl+C to stop the pipeline")
            
            # Run initial capture
            await self.capture_screenshots_job()
            
            # Keep the pipeline running
            while self.running:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            self.logger.info("Pipeline interrupted by user")
        except Exception as e:
            self.logger.error(f"Pipeline error: {e}")
        finally:
            await self.stop()
    
    async def stop(self):
        """Stop the pipeline and cleanup resources."""
        self.logger.info("Stopping pipeline...")
        
        if self.scheduler.running:
            self.scheduler.shutdown()
        
        await self.scraper.close_browser()
        
        self.logger.info("Pipeline stopped successfully")


async def main():
    """Main entry point."""
    pipeline = ScreenshotPipeline()
    await pipeline.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nPipeline stopped by user")
    except Exception as e:
        print(f"Pipeline failed: {e}")
        sys.exit(1)
