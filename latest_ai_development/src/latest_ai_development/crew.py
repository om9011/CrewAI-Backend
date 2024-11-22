from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
from latest_ai_development.tools.Leetcode.leetcode_tool import LeetcodeTool
# from latest_ai_development.tools.Google_Scholar.google_scholar_tool import GoogleScholarTool
from latest_ai_development.tools.LinkedIn.linkedin_tool import LinkedInTool
from latest_ai_development.tools.Github.github_tool import GithubTool
from latest_ai_development.tools.Google_Scholar.google_scholar_tool import GoogleScholarTool


# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class LatestAiDevelopment():
    """LatestAiDevelopment crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def candidate_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['candidate_manager'],
            tools=[GoogleScholarTool()],  # Example of custom tool, loaded on the beginning of file
            verbose=True
        )

    # @agent
    # def google_scholar_analyser(self) -> Agent:  # Define google_scholar_analyser
    # 	return Agent(
    # 		config=self.agents_config['google_scholar_analyser'],
    # 		verbose=True
    # 	)

    # @agent
    # def reporting_analyst(self) -> Agent:
    # 	return Agent(
    # 		config=self.agents_config['reporting_analyst'],
    # 		verbose=True
    # 	)

    # @task
    # def leetcode_data_collector(self) -> Task:
    # 	return Task(
    # 		config=self.tasks_config['leetcode_data_collector'],
    # 	)
    #
    # @task
    # def linkedin_data_collector(self) -> Task:
    # 	return Task(
    # 		config=self.tasks_config['linkedin_data_collector'],
    # 	)

    # @task
    # def github_data_collector(self) -> Task:
    # 	return Task(
    # 		config=self.tasks_config['github_data_collector'],
    # 	)

    @task
    def scholar_data_collector(self) -> Task:  # Define google_scholar_data_collector
        return Task(
            config=self.tasks_config['scholar_data_collector'],
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
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            cache=True
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
