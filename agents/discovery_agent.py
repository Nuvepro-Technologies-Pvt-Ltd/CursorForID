# agents/discovery_agent.py
from crewai import Agent
from crewai_tools import SerperDevTool, FileReadTool
from agents.tools.custom_tools import StakeholderInterviewTool, GapAnalysisTool
from pydantic import BaseModel
from typing import List, Dict

class LearningRequirements(BaseModel):
    target_audience: str
    skill_level: str
    learning_objectives: List[str]
    success_metrics: List[str]
    constraints: Dict[str, str]
    priority_level: str

class DiscoveryAgent:
    def __init__(self):
        self.discovery_agent = Agent(
            role="Business Requirements Analyst",
            goal="Extract and validate comprehensive learning requirements from stakeholders",
            backstory="""You are an expert instructional design consultant with over 15 years 
            of experience in technical training needs analysis. You excel at translating 
            business requirements into actionable learning objectives and identifying 
            skill gaps in technical teams.""",
            tools=[
                SerperDevTool(),
                FileReadTool(),
                StakeholderInterviewTool(),
                GapAnalysisTool()
            ],
            verbose=True,
            max_iter=25,
            allow_delegation=False,
            memory=True,
            reasoning=True,
            max_reasoning_attempts=3,
            inject_date=True,
            date_format="%B %d, %Y"
        )
    
    def get_agent(self):
        return self.discovery_agent

    def execute_discovery(self, inputs: Dict[str, str]) -> LearningRequirements:
        """Execute discovery process with structured output"""
        discovery_prompt = f"""
        Analyze the following business requirements for a hands-on technical course:
        
        Course Topic: {inputs.get('course_topic', 'Not specified')}
        Target Audience: {inputs.get('target_audience', 'Not specified')}
        Business Context: {inputs.get('business_context', 'Not specified')}
        Timeline: {inputs.get('timeline', 'Not specified')}
        
        Conduct a comprehensive requirements analysis and provide structured output.
        """
        
        result = self.discovery_agent.kickoff(
            discovery_prompt,
            response_format=LearningRequirements
        )
        
        return result.pydantic
