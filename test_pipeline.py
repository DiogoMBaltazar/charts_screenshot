"""Test script to run the pipeline for a short duration."""

import asyncio
import signal
from screenshot_pipeline import ScreenshotPipeline


async def test_pipeline():
    """Test the pipeline for 2 minutes then stop."""
    pipeline = ScreenshotPipeline()
    
    print("Starting pipeline test (will run for 2 minutes)...")
    
    # Start the pipeline in a task
    pipeline_task = asyncio.create_task(pipeline.start())
    
    try:
        # Wait for 2 minutes (120 seconds)
        await asyncio.wait_for(pipeline_task, timeout=120)
    except asyncio.TimeoutError:
        print("\nTest completed - stopping pipeline...")
        pipeline.running = False
        await pipeline.stop()
        print("Pipeline test finished successfully!")
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        pipeline.running = False
        await pipeline.stop()


if __name__ == "__main__":
    try:
        asyncio.run(test_pipeline())
    except KeyboardInterrupt:
        print("\nTest stopped by user")
