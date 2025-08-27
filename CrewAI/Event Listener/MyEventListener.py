from crewai.utilities.events import (
    CrewKickoffStartedEvent,
    CrewKickoffCompletedEvent,
    AgentExecutionCompletedEvent,
    TaskStartedEvent,
    ToolUsageStartedEvent,
    ToolUsageFinishedEvent
)
from crewai.utilities.events.base_event_listener import BaseEventListener

class MyCustomListener(BaseEventListener):
    def __init__(self):
        super().__init__()
#------------------------------------------------------------------------------
# Crew Event Listener
#------------------------------------------------------------------------------
    def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(CrewKickoffStartedEvent)
        def on_crew_started(source, event):
            print("\n CrewKickoffStartedEvent has started execution!")
            print(f"Crew '{event.crew_name}' has started execution!")

        @crewai_event_bus.on(CrewKickoffCompletedEvent)
        def on_crew_completed(source, event):
            print("\n CrewKickoffCompletedEvent has started execution!")
            print(f"Crew '{event.crew_name}' has completed execution!")
            print(f"Output: {event.output}")
#------------------------------------------------------------------------------
# Task Event Listener
#------------------------------------------------------------------------------
        @crewai_event_bus.on(TaskStartedEvent)
        def on_task_started(source, event):
            print("\n TaskStartedEvent has started execution!")
            print(f"\n Task '{event.task.description}' completed")
        
#------------------------------------------------------------------------------
# Agent Event Listener
#------------------------------------------------------------------------------
        @crewai_event_bus.on(AgentExecutionCompletedEvent)
        def on_agent_execution_completed(source, event):
            print("\n AgentExecutionCompletedEvent has started execution!")
            print(f"\n Agent '{event.agent.role}' completed task")
            print(f"Output: {event.output}")
#------------------------------------------------------------------------------
# Tool Event Listeners
#------------------------------------------------------------------------------
        @crewai_event_bus.on(ToolUsageStartedEvent)
        def on_tool_started(source, event):
            print("\n\n ToolUsageStartedEvent has started execution!")
            print(f"\n Tool '{event.tool_name}' started")
            
        @crewai_event_bus.on(ToolUsageFinishedEvent)
        def on_tool_finished(source, event):
            print("\n\n ToolUsageFinishedEvent has started execution!")
            print(f"\n Tool '{event.tool_name}' completed")
            print(f"Output: {event.output}")

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
