# agents/content_architect_agent.py
from crewai import Agent
from agents.tools.custom_tools import BloomsTaxonomyTool, CurriculumMappingTool, FileReadTool
from pydantic import BaseModel
from typing import List, Dict

class LearningRequirements(BaseModel):
    subject: str
    target_audience: str
    duration: str
    skill_level: str
    learning_goals: List[str]

class LearningBlueprint(BaseModel):
    course_structure: List[Dict[str, str]]
    learning_objectives: List[str]
    assessment_strategy: Dict[str, str]
    instructional_methods: List[str]
    content_outline: List[Dict[str, str]]
    prerequisite_skills: List[str]

class ContentArchitectAgent:
    def __init__(self):
        self.architect_agent = Agent(
            role="Learning Design Strategist",
            goal="Create comprehensive learning blueprints and assessment strategies for hands-on technical courses",
            backstory="""You are a master instructional designer with expertise in 
            technical skill development and hands-on learning methodologies. You have 
            designed award-winning technical courses for Fortune 500 companies and 
            understand how to create engaging, practical learning experiences.""",
            tools=[
                BloomsTaxonomyTool(),
                CurriculumMappingTool(),
                FileReadTool()
            ],
            verbose=True,
            max_iter=30,
            allow_delegation=True,
            memory=True,
            reasoning=True,
            max_reasoning_attempts=2,
            inject_date=True,
            respect_context_window=True
        )
    
    def get_agent(self):
        return self.architect_agent

    def create_blueprint(self, requirements: LearningRequirements) -> LearningBlueprint:
        """Create detailed learning blueprint"""
        blueprint_prompt = f"""
        Based on the following learning requirements, create a comprehensive learning blueprint:
        
        Requirements: {requirements.model_dump_json()}
        
        Design a hands-on learning experience that includes:
        1. Modular course structure with clear progression
        2. Measurable learning objectives (Apply/Analyze level)
        3. Assessment strategy with both formative and summative elements
        4. Instructional methods optimized for skill development
        5. Detailed content outline with time estimates
        6. Prerequisites and skill dependencies
        """
        
        result = self.architect_agent.kickoff(
            blueprint_prompt,
            response_format=LearningBlueprint
        )
        
        return result.pydantic
