#!/usr/bin/env python
"""
Research and Blog Crew - Production Main Entry Point

This module serves as the main entry point for the Research and Blog Crew application.
It provides multiple execution modes for different production scenarios:
- run: Standard content generation
- train: Machine learning model training for improved performance
- replay: Debug and replay specific task executions
- test: Automated testing and evaluation
- interactive: Interactive mode for dynamic topic input
- batch: Batch processing multiple topics

"""

import sys
import os
import warnings
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import logging

from research_and_blog_crew.crew import ResearchAndBlogCrew

# Suppress specific warnings
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
warnings.filterwarnings("ignore", category=UserWarning)

# ============================================
# LOGGING CONFIGURATION
# ============================================

# Create logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configure logging with both file and console handlers
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f'crew_execution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ============================================
# OUTPUT DIRECTORY SETUP
# ============================================

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================
# CORE EXECUTION FUNCTIONS
# ============================================

def run(topic: Optional[str] = None, save_metadata: bool = True) -> Dict:
    """
    Run the crew for standard content generation.
    
    This is the primary execution mode for production use. It generates
    a complete content package including research report, blog post,
    SEO optimization, and quality assurance checks.
    
    Args:
        topic (str, optional): Topic to research and write about. 
                              Defaults to 'What are AI Agents' if not provided.
        save_metadata (bool): Whether to save execution metadata. Default True.
    
    Returns:
        Dict: Execution results and metadata
        
    Example:
        >>> result = run(topic="Quantum Computing in 2024")
    """
    start_time = datetime.now()
    
    # Default topic if none provided
    if topic is None:
        topic = 'What are AI Agents in coding?'
    
    inputs = {
        'topic': topic,
        'current_year': str(datetime.now().year),
        'execution_date': datetime.now().strftime("%Y-%m-%d"),
        'execution_time': datetime.now().strftime("%H:%M:%S")
    }
    
    logger.info("="*70)
    logger.info("RESEARCH AND BLOG CREW - PRODUCTION RUN")
    logger.info("="*70)
    logger.info(f"Topic: {topic}")
    logger.info(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*70)
    
    try:
        # Initialize and run crew
        crew_instance = ResearchAndBlogCrew()
        
        # Display crew information
        crew_info = crew_instance.get_crew_info()
        logger.info(f"Agents: {crew_info['total_agents']}")
        logger.info(f"Tasks: {crew_info['total_tasks']}")
        logger.info(f"Phases: {len(crew_info['phases'])}")
        logger.info("-"*70)
        
        # Execute crew
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        # Calculate execution time
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        # Prepare metadata
        metadata = {
            "topic": topic,
            "execution_date": inputs['execution_date'],
            "execution_time": inputs['execution_time'],
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": execution_time,
            "duration_formatted": f"{int(execution_time // 60)}m {int(execution_time % 60)}s",
            "status": "SUCCESS",
            "output_files": crew_info['output_files']
        }
        
        # Save metadata if requested
        if save_metadata:
            metadata_file = OUTPUT_DIR / f"metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            logger.info(f"Metadata saved to: {metadata_file}")
        
        logger.info("="*70)
        logger.info("EXECUTION COMPLETED SUCCESSFULLY")
        logger.info("="*70)
        logger.info(f"Duration: {metadata['duration_formatted']}")
        logger.info(f"Output Directory: {OUTPUT_DIR.absolute()}")
        logger.info("="*70)
        
        return {
            "result": result,
            "metadata": metadata
        }
        
    except Exception as e:
        logger.error("="*70)
        logger.error("EXECUTION FAILED")
        logger.error("="*70)
        logger.error(f"Error: {str(e)}", exc_info=True)
        
        # Save error metadata
        error_metadata = {
            "topic": topic,
            "execution_date": inputs['execution_date'],
            "status": "FAILED",
            "error": str(e),
            "error_type": type(e).__name__
        }
        
        error_file = OUTPUT_DIR / f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(error_file, 'w') as f:
            json.dump(error_metadata, f, indent=2)
        
        raise Exception(f"An error occurred while running the crew: {e}")


def train(n_iterations: int, filename: str, topic: Optional[str] = None) -> None:
    """
    Train the crew for improved performance over multiple iterations.
    
    WHAT IT DOES:
    Training allows the crew to learn from multiple executions and improve
    its performance over time. The crew will:
    - Execute the same topic multiple times
    - Learn from successful patterns and mistakes
    - Optimize agent collaboration and task execution
    - Save training results for future use
    
    USE CASE:
    - Improving content quality for specific niches
    - Optimizing execution time and resource usage
    - Fine-tuning agent behaviors for your specific needs
    - Building domain expertise in certain topic areas
    
    Args:
        n_iterations (int): Number of training iterations (recommended: 3-10)
        filename (str): Name of file to save training results
        topic (str, optional): Topic to train on. Defaults to "AI LLMs"
    
    Example:
        >>> train(n_iterations=5, filename="ai_training_results", topic="AI in Healthcare")
        
    This will run 5 iterations and save learnings to improve future executions.
    """
    if topic is None:
        topic = "AI LLMs"
    
    inputs = {
        "topic": topic,
        'current_year': str(datetime.now().year)
    }
    
    logger.info("="*70)
    logger.info("CREW TRAINING MODE")
    logger.info("="*70)
    logger.info(f"Topic: {topic}")
    logger.info(f"Iterations: {n_iterations}")
    logger.info(f"Output File: {filename}")
    logger.info("="*70)
    logger.info("Training will help the crew learn and improve performance...")
    logger.info("This may take a while depending on iterations.")
    logger.info("-"*70)
    
    try:
        ResearchAndBlogCrew().crew().train(
            n_iterations=n_iterations,
            filename=filename,
            inputs=inputs
        )
        
        logger.info("="*70)
        logger.info("TRAINING COMPLETED SUCCESSFULLY")
        logger.info("="*70)
        logger.info(f"Training results saved to: {filename}")
        logger.info("The crew has learned from {n_iterations} iterations.")
        logger.info("Future executions will benefit from this training.")
        
    except Exception as e:
        logger.error(f"Training failed: {str(e)}", exc_info=True)
        raise Exception(f"An error occurred while training the crew: {e}")


def replay(task_id: str) -> None:
    """
    Replay a specific task execution from a previous crew run.
    
    WHAT IT DOES:
    Replay allows you to re-execute a specific task from a previous crew run.
    This is incredibly useful for:
    - Debugging issues with specific tasks
    - Understanding what went wrong in a failed execution
    - Testing fixes without running the entire crew
    - Analyzing task outputs and agent behaviors
    
    USE CASE:
    - Your crew failed at task 8 (SEO optimization), replay from task 8
    - You want to see exactly what the fact_checker agent did
    - Testing improvements to a specific task without full execution
    - Debugging task context and data flow issues
    
    Args:
        task_id (str): The ID of the task to replay (e.g., "task_8" or "seo_optimization_task")
    
    Example:
        >>> replay(task_id="seo_optimization_task")
        
    This will re-run only the SEO optimization task with the same inputs
    from the previous execution, allowing you to debug or test changes.
    """
    logger.info("="*70)
    logger.info("CREW REPLAY MODE")
    logger.info("="*70)
    logger.info(f"Replaying Task ID: {task_id}")
    logger.info("="*70)
    logger.info("Replay mode allows you to re-execute a specific task")
    logger.info("from a previous crew run for debugging purposes.")
    logger.info("-"*70)
    
    try:
        ResearchAndBlogCrew().crew().replay(task_id=task_id)
        
        logger.info("="*70)
        logger.info("REPLAY COMPLETED")
        logger.info("="*70)
        logger.info(f"Task {task_id} has been re-executed successfully.")
        
    except Exception as e:
        logger.error(f"Replay failed: {str(e)}", exc_info=True)
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test(n_iterations: int, eval_llm: str, topic: Optional[str] = None) -> None:
    """
    Test the crew with automated evaluation using an LLM judge.
    
    WHAT IT DOES:
    Testing runs the crew multiple times and uses an evaluation LLM to
    automatically assess the quality of outputs. It provides:
    - Automated quality scoring
    - Performance benchmarking
    - Consistency analysis across runs
    - Identification of weak points
    
    USE CASE:
    - Quality assurance before production deployment
    - Comparing different crew configurations
    - Validating improvements after training
    - Automated regression testing
    - Performance monitoring and benchmarking
    
    Args:
        n_iterations (int): Number of test iterations (recommended: 3-5)
        eval_llm (str): LLM model to use for evaluation (e.g., "gpt-4", "claude-3")
        topic (str, optional): Topic to test with. Defaults to "AI LLMs"
    
    Example:
        >>> test(n_iterations=3, eval_llm="gpt-4", topic="Blockchain Technology")
        
    This will run 3 test iterations and use GPT-4 to evaluate output quality,
    providing detailed scores and feedback for improvement.
    """
    if topic is None:
        topic = "AI LLMs"
        
    inputs = {
        "topic": topic,
        "current_year": str(datetime.now().year)
    }
    
    logger.info("="*70)
    logger.info("CREW TESTING MODE")
    logger.info("="*70)
    logger.info(f"Topic: {topic}")
    logger.info(f"Test Iterations: {n_iterations}")
    logger.info(f"Evaluation LLM: {eval_llm}")
    logger.info("="*70)
    logger.info("Testing will run multiple iterations and evaluate quality...")
    logger.info("This helps ensure consistent, high-quality output.")
    logger.info("-"*70)
    
    try:
        ResearchAndBlogCrew().crew().test(
            n_iterations=n_iterations,
            openai_model_name=eval_llm,
            inputs=inputs
        )
        
        logger.info("="*70)
        logger.info("TESTING COMPLETED")
        logger.info("="*70)
        logger.info(f"Ran {n_iterations} test iterations successfully.")
        logger.info("Check test results for quality scores and feedback.")
        
    except Exception as e:
        logger.error(f"Testing failed: {str(e)}", exc_info=True)
        raise Exception(f"An error occurred while testing the crew: {e}")


# ============================================
# ADDITIONAL PRODUCTION FEATURES
# ============================================

def interactive() -> None:
    """
    Interactive mode for dynamic topic input and execution.
    
    Allows users to input topics on-the-fly and run the crew interactively.
    Useful for:
    - Quick content generation
    - Testing different topics
    - Demo and presentation purposes
    """
    logger.info("="*70)
    logger.info("INTERACTIVE MODE")
    logger.info("="*70)
    print("\nWelcome to Research and Blog Crew Interactive Mode!")
    print("Enter topics to generate content, or 'quit' to exit.\n")
    
    while True:
        try:
            topic = input("Enter topic (or 'quit' to exit): ").strip()
            
            if topic.lower() in ['quit', 'exit', 'q']:
                print("\nExiting interactive mode. Goodbye!")
                break
            
            if not topic:
                print("Please enter a valid topic.\n")
                continue
            
            print(f"\n🚀 Generating content for: {topic}\n")
            run(topic=topic)
            print("\n✅ Content generation complete!\n")
            
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Exiting...")
            break
        except Exception as e:
            logger.error(f"Error in interactive mode: {str(e)}")
            print(f"\n❌ Error: {str(e)}\n")


def batch(topics_file: str) -> None:
    """
    Batch processing mode for multiple topics.
    
    Reads topics from a file (one per line) and processes them sequentially.
    Useful for:
    - Bulk content generation
    - Scheduled content creation
    - Processing topic lists
    
    Args:
        topics_file (str): Path to file containing topics (one per line)
    
    Example:
        Create a file 'topics.txt' with:
            AI in Healthcare
            Quantum Computing
            Climate Change Solutions
        
        Then run: batch("topics.txt")
    """
    logger.info("="*70)
    logger.info("BATCH PROCESSING MODE")
    logger.info("="*70)
    
    try:
        with open(topics_file, 'r') as f:
            topics = [line.strip() for line in f if line.strip()]
        
        total = len(topics)
        logger.info(f"Found {total} topics to process")
        logger.info("-"*70)
        
        results = []
        for i, topic in enumerate(topics, 1):
            logger.info(f"\n[{i}/{total}] Processing: {topic}")
            try:
                result = run(topic=topic)
                results.append({"topic": topic, "status": "SUCCESS", "result": result})
            except Exception as e:
                logger.error(f"Failed to process '{topic}': {str(e)}")
                results.append({"topic": topic, "status": "FAILED", "error": str(e)})
        
        # Save batch results
        batch_file = OUTPUT_DIR / f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(batch_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info("="*70)
        logger.info("BATCH PROCESSING COMPLETED")
        logger.info("="*70)
        successful = sum(1 for r in results if r["status"] == "SUCCESS")
        logger.info(f"Successful: {successful}/{total}")
        logger.info(f"Results saved to: {batch_file}")
        
    except FileNotFoundError:
        logger.error(f"Topics file not found: {topics_file}")
        raise
    except Exception as e:
        logger.error(f"Batch processing failed: {str(e)}", exc_info=True)
        raise


# ============================================
# COMMAND LINE INTERFACE
# ============================================

def main():
    """
    Main entry point with argument parsing for different execution modes.
    """
    parser = argparse.ArgumentParser(
        description="Research and Blog Crew - Production Content Generation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default topic
  python main.py run
  
  # Run with custom topic
  python main.py run --topic "Quantum Computing in 2024"
  
  # Train the crew
  python main.py train --iterations 5 --filename training_results
  
  # Test the crew
  python main.py test --iterations 3 --eval-llm gpt-4
  
  # Replay a specific task
  python main.py replay --task-id seo_optimization_task
  
  # Interactive mode
  python main.py interactive
  
  # Batch processing
  python main.py batch --file topics.txt
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Execution mode')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run content generation')
    run_parser.add_argument('--topic', type=str, help='Topic to research and write about')
    
    # Train command
    train_parser = subparsers.add_parser('train', help='Train the crew')
    train_parser.add_argument('--iterations', type=int, required=True, help='Number of training iterations')
    train_parser.add_argument('--filename', type=str, required=True, help='Output filename for training results')
    train_parser.add_argument('--topic', type=str, help='Topic to train on')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test the crew')
    test_parser.add_argument('--iterations', type=int, required=True, help='Number of test iterations')
    test_parser.add_argument('--eval-llm', type=str, required=True, help='LLM model for evaluation')
    test_parser.add_argument('--topic', type=str, help='Topic to test with')
    
    # Replay command
    replay_parser = subparsers.add_parser('replay', help='Replay a specific task')
    replay_parser.add_argument('--task-id', type=str, required=True, help='Task ID to replay')
    
    # Interactive command
    subparsers.add_parser('interactive', help='Interactive mode')
    
    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch process multiple topics')
    batch_parser.add_argument('--file', type=str, required=True, help='File containing topics')
    
    args = parser.parse_args()
    
    # Execute appropriate command
    try:
        if args.command == 'run':
            run(topic=args.topic if hasattr(args, 'topic') else None)
        elif args.command == 'train':
            train(args.iterations, args.filename, args.topic if hasattr(args, 'topic') else None)
        elif args.command == 'test':
            test(args.iterations, args.eval_llm, args.topic if hasattr(args, 'topic') else None)
        elif args.command == 'replay':
            replay(args.task_id)
        elif args.command == 'interactive':
            interactive()
        elif args.command == 'batch':
            batch(args.file)
        else:
            parser.print_help()
    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        sys.exit(1)


# ============================================
# ENTRY POINT
# ============================================

if __name__ == "__main__":
    main()