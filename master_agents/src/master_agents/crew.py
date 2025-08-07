from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# from crewai_tools import SerperDevTool  # Disabled for now - will add web search later
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class MasterAgents():
    """MasterAgents crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def data_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['data_analyst'], # type: ignore[index]
            verbose=True
        )

    @agent
    def ml_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['ml_engineer'], # type: ignore[index]
            verbose=True
        )

    @agent
    def dependency_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['dependency_manager'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def dependency_check_task(self) -> Task:
        return Task(
            config=self.tasks_config['dependency_check_task'], # type: ignore[index]
            output_file='setup_environment.py'
        )

    @task
    def initial_model_task(self) -> Task:
        return Task(
            config=self.tasks_config['initial_model_task'], # type: ignore[index]
            output_file='model_v1.py'
        )

    @task
    def performance_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['performance_analysis_task'], # type: ignore[index]
            output_file='performance_analysis.md'
        )

    @task
    def model_improvement_task(self) -> Task:
        return Task(
            config=self.tasks_config['model_improvement_task'], # type: ignore[index]
            output_file='model_improved.py',
            context=[self.dependency_check_task()]  # Ensure dependencies are checked first
        )

    @task
    def final_results_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_results_task'], # type: ignore[index]
            output_file='final_results.md',
            context=[self.initial_model_task(), self.performance_analysis_task(), self.model_improvement_task()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MasterAgents crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,  # Sequential works better for our flow
            verbose=True,
            max_execution_time=3600,  # 1 hour max
            # max_iter=5,  # Not available in sequential mode
        )
