import argparse
import asyncio
import os
from oagi import AsyncScreenshotMaker 
from oagi import AsyncAgentObserver
# Controls your local keyboard and mouse based on the model predicted actions
from oagi import AsyncPyautoguiActionHandler
from oagi.agent.tasker import TaskerAgent

from oagi import TaskerAgent
from dotenv import load_dotenv

from scraper import get_live_sports_urls

load_dotenv()

async def main(team1, team2, sport):
    observer = AsyncAgentObserver()
    tasker = TaskerAgent(model="lux-actor-1", step_observer=observer)

    urls = get_live_sports_urls()

    for url in urls:
        # TODO: we need to check if video is playing. If not, mark as failed.
        # Currently it marks as successful even if video is not playing.
        tasker.set_task(
            task="Find the live " + sport + " stream for: '" + team1 + " vs " + team2 + "'. Use Chrome and NEVER exit Chrome. Search for the stream in the following URL: " + url,
            todos=[
                "Open Chrome and go to the first URL in the list: " + url,
                "Click in the category of sports: " + sport,
                "Click on the stream containing the team names: " + team1 + " or " + team2 + " and wait for the site to load",
                "Click the play button at around the center of the page",
                "Hover over the bottom right corner of the video player and click the full screen button",
            ]
        )
        success = await tasker.execute(
            instruction="",
            action_handler=AsyncPyautoguiActionHandler(),
            image_provider=AsyncScreenshotMaker(),
        )
        if success:
            break
    memory = tasker.get_memory()

    print("\n" + "=" * 60)
    print("EXECUTION SUMMARY")
    print("=" * 60)
    print(f"Overall success: {success}")
    print(f"\nTask execution summary:\n{memory.task_execution_summary}")

    print("\nTodo Status:")
    for i, todo in enumerate(memory.todos):
        status_icon = {
            "completed": "✅",
            "pending": "⏳",
            "in_progress": "🔄",
            "skipped": "⏭️",
        }.get(todo.status.value, "❓")
        print(f"  {status_icon} [{i + 1}] {todo.description} - {todo.status.value}")

    status_summary = memory.get_todo_status_summary()
    print("\nExecution Statistics:")
    print(f"  Completed: {status_summary.get('completed', 0)}")
    print(f"  Pending: {status_summary.get('pending', 0)}")
    print(f"  In Progress: {status_summary.get('in_progress', 0)}")
    print(f"  Skipped: {status_summary.get('skipped', 0)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for live sports streams")
    parser.add_argument('team1', help='First team name (e.g., "liverpool")')
    parser.add_argument('team2', help='Second team name (e.g., "chelsea")')
    parser.add_argument('sport', help='Sport type (e.g., "football")')
    
    args = parser.parse_args()
    
    asyncio.run(main(args.team1, args.team2, args.sport))

