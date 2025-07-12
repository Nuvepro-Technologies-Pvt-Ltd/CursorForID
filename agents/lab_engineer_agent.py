# agents/lab_engineer_agent.py
from crewai import Agent
from agents.tools.custom_tools import CloudProvisioningTool, SecurityPolicyTool, InfrastructureTool
from pydantic import BaseModel
from typing import List, Dict
from .content_architect_agent import LearningBlueprint, LearningRequirements

class LabEnvironment(BaseModel):
    environment_type: str
    cloud_provider: str
    resource_specifications: Dict[str, str]
    security_configuration: Dict[str, str]
    cost_estimates: Dict[str, float]
    setup_scripts: List[str]
    teardown_procedures: List[str]
    access_controls: Dict[str, str]

class LabEngineerAgent:
    def __init__(self):
        self.lab_engineer = Agent(
            role="Technical Environment Specialist",
            goal="Design and provision secure, scalable lab environments for hands-on learning",
            backstory="""You are a cloud infrastructure expert with deep experience in 
            educational technology platforms. You specialize in creating secure, 
            cost-effective lab environments that can scale to thousands of concurrent 
            learners while maintaining security and performance.""",
            tools=[
                CloudProvisioningTool(),
                SecurityPolicyTool(),
                InfrastructureTool()
            ],
            verbose=True,
            max_iter=25,
            allow_delegation=False,
            memory=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=600,
            respect_context_window=True
        )
    
    def get_agent(self):
        return self.lab_engineer

    def design_lab_environment(self, blueprint: LearningBlueprint, 
                              requirements: LearningRequirements) -> LabEnvironment:
        """Design comprehensive lab environment"""
        lab_prompt = f"""
        Design a hands-on lab environment based on:
        
        Learning Blueprint: {blueprint.model_dump_json()}
        Requirements: {requirements.model_dump_json()}
        
        Create a production-ready lab environment that includes:
        1. Cloud infrastructure specifications
        2. Security configurations and access controls
        3. Cost optimization strategies
        4. Automated setup and teardown procedures
        5. Scalability considerations
        6. Monitoring and logging setup
        """
        
        result = self.lab_engineer.kickoff(
            lab_prompt,
            response_format=LabEnvironment
        )
        
        return result.pydantic
