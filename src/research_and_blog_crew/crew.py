from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, tool
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileReadTool
from typing import List, Optional
import logging
from datetime import datetime

# Configure logging for production monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================
# PRODUCTION-GRADE CREW CONFIGURATION
# ============================================

@CrewBase
class ResearchAndBlogCrew():
    """
    Production-grade ResearchAndBlogCrew for generating comprehensive reports 
    and engaging blog content with multi-agent collaboration, quality assurance,
    and optimization capabilities.
    
    This crew orchestrates 12 specialized agents across 6 phases:
    - Phase 1: Research & Intelligence Gathering
    - Phase 2: Strategic Report Creation
    - Phase 3: Blog Content Strategy & Creation
    - Phase 4: Optimization & Enhancement
    - Phase 5: Quality Assurance & Final Polish
    - Phase 6: Final Package Delivery
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    # Define the paths of config files
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # ============================================
    # TOOL DEFINITIONS 
    # ============================================
    
    @tool
    def web_search_tool(self):
        """Web search tool for finding information online"""
        return SerperDevTool()
    
    @tool
    def scraping_tool(self):
        """Tool for scraping website content"""
        return ScrapeWebsiteTool()
    
    @tool
    def file_read_tool(self):
        """Tool for reading files"""
        return FileReadTool()
    
    @tool
    def academic_search_tool(self):
        """Academic search tool (using SerperDev for now)"""
        return SerperDevTool()
    
    @tool
    def fact_checking_tool(self):
        """Fact checking tool (using web search)"""
        return SerperDevTool()
    
    @tool
    def source_verification_tool(self):
        """Source verification tool (using web search)"""
        return SerperDevTool()
    
    @tool
    def trend_analysis_tool(self):
        """Trend analysis tool (using web search)"""
        return SerperDevTool()
    
    @tool
    def market_data_tool(self):
        """Market data tool (using web search)"""
        return SerperDevTool()
    
    @tool
    def keyword_research_tool(self):
        """Keyword research tool (using web search)"""
        return SerperDevTool()
    
    @tool
    def seo_analysis_tool(self):
        """SEO analysis tool (using web search)"""
        return SerperDevTool()
    
    @tool
    def plagiarism_detection_tool(self):
        """Plagiarism detection tool (using web search)"""
        return SerperDevTool()
    
    @tool
    def citation_validator_tool(self):
        """Citation validator tool (using web search)"""
        return SerperDevTool()

    # ============================================
    # TOOL INITIALIZATION
    # ============================================
    
    @agent
    def research_analyst(self) -> Agent:
        """Combined research, fact-checking, and trend analysis"""
        return Agent(
            config=self.agents_config["research_analyst"],
            verbose=True
        )

    @agent
    def report_writer(self) -> Agent:
        """Strategic report creation"""
        return Agent(
            config=self.agents_config["report_writer"],
            verbose=True
        )

    @agent
    def blog_content_creator(self) -> Agent:
        """Blog writing + SEO optimization combined"""
        return Agent(
            config=self.agents_config["blog_content_creator"],
            verbose=True
        )

    @agent
    def quality_editor(self) -> Agent:
        """Final editing, QA, and accessibility checks"""
        return Agent(
            config=self.agents_config["quality_editor"],
            verbose=True
        )

    # ============================================
    # TASK DEFINITIONS (Order matters!)
    # ============================================

    @task
    def comprehensive_research_task(self) -> Task:
        return Task(
            config=self.tasks_config["comprehensive_research_task"],
            agent=self.research_analyst()
        )

    @task
    def strategic_report_task(self) -> Task:
        return Task(
            config=self.tasks_config["strategic_report_task"],
            agent=self.report_writer(),
            context=[self.comprehensive_research_task()],
            output_file="output/strategic_report.md"
        )

    @task
    def seo_blog_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config["seo_blog_creation_task"],
            agent=self.blog_content_creator(),
            context=[self.strategic_report_task()],
            output_file="output/blog_post_with_seo.md"
        )

    @task
    def final_quality_review_task(self) -> Task:
        return Task(
            config=self.tasks_config["final_quality_review_task"],
            agent=self.quality_editor(),
            context=[self.strategic_report_task(), self.seo_blog_creation_task()],
            output_file="output/final_content_package.md"
        )

    # ============================================
    # CREW ASSEMBLY
    # ============================================

    @crew
    def crew(self) -> Crew:
        """
        Assembles the production-grade crew with all agents and tasks.
        Uses sequential process for logical workflow execution.
        
        Process Flow:
        Research → Report → Strategy → Blog → Optimization → QA → Delivery
        
        Returns:
            Crew: Configured crew ready for execution
        """
        try:
            logger.info("Assembling Research and Blog Crew...")
            logger.info(f"Total Agents: {len(self.agents)}")
            logger.info(f"Total Tasks: {len(self.tasks)}")
            
            return Crew(
                agents=self.agents,  # All 12 agents
                tasks=self.tasks,    # All 14 tasks in order
                process=Process.sequential,  # Execute tasks in order
                verbose=True,
                memory=True,  # Enable memory for context retention
                cache=True,   # Cache results to avoid redundant work
                max_rpm=30,   # Rate limiting for API calls
                share_crew=False,  # Keep crew private
                output_log_file=True
            )
        except Exception as e:
            logger.error(f"Error assembling crew: {str(e)}")
            raise

    # ============================================
    # UTILITY METHODS FOR PRODUCTION
    # ============================================

    def kickoff(self, inputs: dict) -> str:
        """
        Convenience method to start the crew with inputs and error handling.
        
        Args:
            inputs (dict): Input parameters including 'topic'
            
        Returns:
            str: Final output from the crew
        """
        try:
            logger.info(f"Starting crew kickoff at {datetime.now()}")
            logger.info(f"Topic: {inputs.get('topic', 'Not specified')}")
            
            result = self.crew().kickoff(inputs=inputs)
            
            logger.info(f"Crew completed successfully at {datetime.now()}")
            return result
            
        except Exception as e:
            logger.error(f"Crew execution failed: {str(e)}")
            raise

    def get_crew_info(self) -> dict:
        """
        Returns information about the crew configuration.
        Useful for monitoring and debugging.
        
        Returns:
            dict: Crew configuration details
        """
        agents = getattr(self, "_agents", [])
        tasks = getattr(self, "_tasks", [])

        return {
            "total_agents": len(agents),
            "total_tasks": len(tasks),
            "process_type": "sequential",
            "phases": [
                "Research & Intelligence",
                "Report Creation",
                "Blog Content",
                "Optimization",
                "Quality Assurance",
                "Final Delivery"
            ],
            "output_files": [
                "strategic_report.md",
                "blog_post.md",
                "seo_optimized_blog.md",
                "visual_content_guide.md",
                "engagement_optimized_blog.md",
                "final_edited_content.md",
                "plagiarism_report.md",
                "accessibility_report.md",
                "final_content_package.md"
            ]
        }


# ============================================
# PRODUCTION EXECUTION
# ============================================

if __name__ == "__main__":
    """
    Example production execution with error handling and logging
    """
    try:
        # Initialize crew
        crew_instance = ResearchAndBlogCrew()
        
        # Display crew info
        info = crew_instance.get_crew_info()
        print(f"\n{'='*50}")
        print("RESEARCH AND BLOG CREW - PRODUCTION MODE")
        print(f"{'='*50}")
        print(f"Total Agents: {info['total_agents']}")
        print(f"Total Tasks: {info['total_tasks']}")
        print(f"Process: {info['process_type']}")
        print(f"{'='*50}\n")
        
        # Define inputs
        inputs = {
            "topic": "Artificial Intelligence in Healthcare"  # Example topic
        }
        
        # Execute crew
        print(f"Starting content generation for: {inputs['topic']}\n")
        result = crew_instance.kickoff(inputs=inputs)
        
        print(f"\n{'='*50}")
        print("EXECUTION COMPLETED SUCCESSFULLY")
        print(f"{'='*50}")
        print(f"\nFinal Output:\n{result}")
        
    except Exception as e:
        logger.error(f"Production execution failed: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        print("Please check logs for details.")