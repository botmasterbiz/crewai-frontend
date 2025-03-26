from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import List

load_dotenv()

openai_llm = LLM(
	model="gpt-3.5-turbo",
	api_key=os.getenv("OPENAI_API_KEY"),
	temperature=0.7
)

class ResearchOutput(BaseModel):
    summary: str
    key_points: List[str]
    quick_summary: str
    extended_summary: str
    actionable_insights: List[str]
    source_document_list: List[str]
    potential_biases_and_limitations: str

@CrewBase
class FileCrew():

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			verbose=True,
			llm=openai_llm
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			output_pydantic=ResearchOutput
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the FileCrew crew"""

		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True
		)
