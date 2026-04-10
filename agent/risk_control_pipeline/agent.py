from google.adk.agents import SequentialAgent

from .agents.risk_engine_agent import risk_engine_agent
from .agents.decision_engine_agent import decision_engine_agent
from .agents.action_engine_agent import action_engine_agent

root_agent = SequentialAgent(
    name="risk_control_pipeline",
    description=(
        "End-to-end risk control pipeline that sequentially assesses risk, "
        "applies decision policy, and executes enforcement actions."
    ),
    sub_agents=[
        risk_engine_agent,
        decision_engine_agent,
        action_engine_agent,
    ],
)
