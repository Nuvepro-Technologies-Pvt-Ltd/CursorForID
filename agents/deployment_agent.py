# agents/deployment_agent.py
from crewai import Agent
from agents.tools.custom_tools import LMSIntegrationTool, SCORMPackagingTool, AnalyticsTool
from pydantic import BaseModel
from typing import List, Dict
from .content_creation_agent import ContentAssets
from .quality_assurance_agent import QualityReport



class DeploymentPackage(BaseModel):
    lms_package: Dict[str, str]
    instructor_guide: Dict[str, str]
    learner_materials: List[Dict[str, str]]
    analytics_configuration: Dict[str, str]
    deployment_instructions: List[str]
    maintenance_procedures: List[str]

class DeploymentAgent:
    def __init__(self):
        self.deployment_agent = Agent(
            role="Learning Experience Platform Specialist",
            goal="Package and deploy content to LMS/LXP systems with comprehensive analytics",
            backstory="""You are a learning technology specialist with extensive experience 
            in LMS implementation and deployment. You understand the intricacies of 
            SCORM packaging, xAPI integration, and learning analytics configuration.""",
            tools=[
                LMSIntegrationTool(),
                SCORMPackagingTool(),
                AnalyticsTool()
            ],
            verbose=True,
            max_iter=20,
            allow_delegation=False,
            memory=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            respect_context_window=True
        )
    
    def get_agent(self):
        return self.deployment_agent

    def create_deployment_package(self, content_assets: ContentAssets, 
                                qa_report: QualityReport) -> DeploymentPackage:
        """Create complete deployment package"""
        deployment_prompt = f"""
        Create a comprehensive deployment package based on:
        
        Content Assets: {content_assets.model_dump_json()}
        QA Report: {qa_report.model_dump_json()}
        
        Package everything for deployment including:
        1. LMS-compatible content package (SCORM/xAPI)
        2. Comprehensive instructor guide
        3. Learner materials and resources
        4. Analytics and reporting configuration
        5. Step-by-step deployment instructions
        6. Ongoing maintenance procedures
        """
        
        result = self.deployment_agent.kickoff(
            deployment_prompt,
            response_format=DeploymentPackage
        )
        
        return result.pydantic
