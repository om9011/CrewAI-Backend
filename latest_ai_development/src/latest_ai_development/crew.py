from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
from latest_ai_development.tools.Leetcode.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class LatestAiDevelopment():
	"""LatestAiDevelopment crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def leetcode_analyser(self) -> Agent:
		return Agent(
			config=self.agents_config['leetcode_analyser'],
			tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)
	@agent
	def google_scholar_analyser(self) -> Agent:  # Define google_scholar_analyser
		return Agent(
			config=self.agents_config['google_scholar_analyser'],
			verbose=True
		)


	# @agent
	# def reporting_analyst(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['reporting_analyst'],
	# 		verbose=True
	# 	)

	@task
	def leetcode_data_collector(self) -> Task:
		return Task(
			config=self.tasks_config['leetcode_data_collector'],
		)
	@task
	def google_scholar_data_collector(self) -> Task:  # Define google_scholar_data_collector
		return Task(
			config=self.tasks_config['google_scholar_data_collector'],
		)
	# @task
	# def reporting_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['reporting_task'],
	# 		output_file='report.md'
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the LatestAiDevelopment crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
