# agents/content_creation_agent.py
from crewai import Agent
from agents.tools.custom_tools import ContentGenerationTool, MediaCreationTool, CodeSnippetTool
from pydantic import BaseModel
from typing import List, Dict
from .content_architect_agent import LearningBlueprint

class LabEnvironment(BaseModel):
    platform: str
    tools: List[str]
    infrastructure: Dict[str, str]
    access_method: str

class ContentAssets(BaseModel):
    presentations: List[Dict[str, str]]
    lab_guides: List[Dict[str, str]]
    assessments: List[Dict[str, str]]
    video_scripts: List[Dict[str, str]]
    code_examples: List[Dict[str, str]]
    supporting_materials: List[Dict[str, str]]

class ContentCreationAgent:
    def __init__(self):
        self.content_creator = Agent(
            role="Multi-media Content Developer",
            goal="Generate comprehensive instructional materials, code samples, and assessment content",
            backstory="""You are a versatile content creator with expertise in technical 
            writing, instructional design, and multimedia development. You excel at 
            creating engaging, accessible content that facilitates hands-on learning 
            and skill development.""",
            tools=[
                ContentGenerationTool(),
                MediaCreationTool(),
                CodeSnippetTool()
            ],
            verbose=True,
            max_iter=35,
            allow_delegation=False,
            memory=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            multimodal=True,
            respect_context_window=True
        )
    
    def get_agent(self):
        return self.content_creator

    def generate_content(self, blueprint: LearningBlueprint, 
                        lab_environment: LabEnvironment) -> ContentAssets:
        """Generate all content assets"""
        content_prompt = f"""
        Generate comprehensive content assets based on:
        
        Learning Blueprint: {blueprint.model_dump_json()}
        Lab Environment: {lab_environment.model_dump_json()}
        
        Create content that includes:
        1. Interactive presentations with slide notes
        2. Step-by-step lab guides with troubleshooting
        3. Formative and summative assessments
        4. Video scripts for demonstrations
        5. Code examples with explanations
        6. Supporting materials (cheat sheets, references)
        """
        
        result = self.content_creator.kickoff(
            content_prompt,
            response_format=ContentAssets
        )
        
        return result.pydantic
