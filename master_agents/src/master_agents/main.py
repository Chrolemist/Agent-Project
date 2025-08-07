#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from master_agents.crew import MasterAgents

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew iteratively until target performance is achieved.
    """
    inputs = {
        'dataset': '7nr.csv',
        'target_r2': 0.8,
        'target_rmse': 5.0
    }
    
    max_iterations = 3
    
    for iteration in range(1, max_iterations + 1):
        print(f"\n🔄 ITERATION {iteration}/{max_iterations}")
        print("=" * 50)
        
        try:
            result = MasterAgents().crew().kickoff(inputs=inputs)
            print(f"\n✅ Iteration {iteration} completed")
            
            # Check if we should continue based on performance analysis
            if hasattr(result, 'raw') and "CONTINUE_ITERATION: NO" in str(result.raw):
                print("🎯 Target achieved! Stopping iterations.")
                break
                
        except Exception as e:
            print(f"❌ Iteration {iteration} failed: {e}")
            continue
    
    print("\n🏁 All iterations completed!")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        MasterAgents().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        MasterAgents().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        MasterAgents().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
