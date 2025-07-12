# crew_manager.py
from crewai import Crew, Process
from agents.discovery_agent import DiscoveryAgent
from agents.content_architect_agent import ContentArchitectAgent
from agents.lab_engineer_agent import LabEngineerAgent
from agents.content_creation_agent import ContentCreationAgent
from agents.quality_assurance_agent import QualityAssuranceAgent
from agents.deployment_agent import DeploymentAgent
from typing import Dict, Any

class InstructionalDesignCrew:
    def __init__(self):
        self.discovery_agent = DiscoveryAgent()
        self.architect_agent = ContentArchitectAgent()
        self.lab_engineer = LabEngineerAgent()
        self.content_creator = ContentCreationAgent()
        self.qa_agent = QualityAssuranceAgent()
        self.deployment_agent = DeploymentAgent()
    
    def create_course(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the complete course creation workflow"""
        
        # Phase 1: Discovery
        requirements = self.discovery_agent.execute_discovery(inputs)
        
        # Phase 2: Architecture
        blueprint = self.architect_agent.create_blueprint(requirements)
        
        # Phase 3: Lab Environment
        lab_environment = self.lab_engineer.design_lab_environment(blueprint, requirements)
        
        # Phase 4: Content Creation
        content_assets = self.content_creator.generate_content(blueprint, lab_environment)
        
        # Phase 5: Quality Assurance
        qa_report = self.qa_agent.execute_quality_assurance(content_assets, lab_environment)
        
        # Phase 6: Deployment
        deployment_package = self.deployment_agent.create_deployment_package(content_assets, qa_report)
        
        return {
            "requirements": requirements,
            "blueprint": blueprint,
            "lab_environment": lab_environment,
            "content_assets": content_assets,
            "qa_report": qa_report,
            "deployment_package": deployment_package
        }

# Usage example
if __name__ == "__main__":
    crew = InstructionalDesignCrew()
    
    inputs = {
        "course_topic": "Kubernetes for DevOps Engineers",
        "target_audience": "Mid-level DevOps engineers",
        "business_context": "Upskill engineering team for cloud migration",
        "timeline": "4 weeks development, 2 weeks testing"
    }
    
    result = crew.create_course(inputs)
    print("Course creation completed!")
