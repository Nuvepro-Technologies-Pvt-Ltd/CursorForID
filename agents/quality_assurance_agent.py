# agents/quality_assurance_agent.py
from crewai import Agent
from agents.tools.custom_tools import AutomatedTestingTool, AccessibilityTool, LearnerSimulationTool
from pydantic import BaseModel
from typing import List, Dict
from .content_creation_agent import ContentAssets
from .lab_engineer_agent import LabEnvironment  

class QualityReport(BaseModel):
    technical_validation: Dict[str, str]
    content_accuracy: Dict[str, str]
    accessibility_compliance: Dict[str, str]
    user_experience_feedback: Dict[str, str]
    performance_metrics: Dict[str, float]
    recommended_improvements: List[str]

class QualityAssuranceAgent:
    def __init__(self):
        self.qa_agent = Agent(
            role="Testing and Validation Specialist",
            goal="Execute comprehensive testing and validation of learning content and environments",
            backstory="""You are a quality assurance expert with specialized experience 
            in educational technology. You have a keen eye for detail and extensive 
            experience in testing learning systems, ensuring accessibility compliance, 
            and optimizing user experience.""",
            tools=[
                AutomatedTestingTool(),
                AccessibilityTool(),
                LearnerSimulationTool()
            ],
            verbose=True,
            max_iter=30,
            allow_delegation=False,
            memory=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            respect_context_window=True
        )
    
    def get_agent(self):
        return self.qa_agent

    def execute_quality_assurance(self, content_assets: ContentAssets, 
                                 lab_environment: LabEnvironment) -> QualityReport:
        """Execute comprehensive QA process"""
        qa_prompt = f"""
        Conduct comprehensive quality assurance testing on:
        
        Content Assets: {content_assets.model_dump_json()}
        Lab Environment: {lab_environment.model_dump_json()}
        
        Perform testing that includes:
        1. Technical validation of all lab components
        2. Content accuracy and alignment verification
        3. Accessibility compliance assessment
        4. User experience evaluation
        5. Performance and scalability testing
        6. Recommendations for improvement
        """
        
        result = self.qa_agent.kickoff(
            qa_prompt,
            response_format=QualityReport
        )
        
        return result.pydantic
