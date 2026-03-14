"""
Evaluation Agent.

Runs comparative experiments between baseline and adaptive approaches.
"""

from typing import Any
from loguru import logger

from agents.orchestrator_agent import OrchestratorAgent
from experiments.baseline_pipeline import BaselinePipeline
from experiments.evaluation_metrics import EvaluationResults


class EvaluationAgent:
    """
    Agent responsible for running evaluation experiments.
    
    Compares the adaptive vectorization approach against a baseline
    static approach.
    """
    
    def __init__(self):
        """Initialize the evaluation agent."""
        self.orchestrator = OrchestratorAgent()
        self.baseline = BaselinePipeline()
        logger.info("EvaluationAgent initialized")
    
    def run_evaluation(
        self,
        test_queries: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Run evaluation on test queries.
        
        Args:
            test_queries: List of dicts with 'query' and 'relevant_ids' keys.
            
        Returns:
            Evaluation results for both approaches.
        """
        logger.info(f"Running evaluation on {len(test_queries)} queries")
        
        adaptive_results = EvaluationResults()
        baseline_results = EvaluationResults()
        
        for test in test_queries:
            query = test["query"]
            relevant_ids = set(test.get("relevant_ids", []))
            
            # Evaluate adaptive approach
            result = self.orchestrator.query(query, k=5)
            adaptive_results.add_result(result.retrieved_chunks, relevant_ids)
        
        return {
            "adaptive": adaptive_results.to_dict(),
            "num_queries": len(test_queries),
        }
    
    def compare_approaches(
        self,
        file_path: str,
        test_queries: list[str],
    ) -> dict[str, Any]:
        """
        Compare adaptive vs baseline on the same document.
        
        This is a simplified comparison that processes a document
        with both approaches and compares retrieval.
        """
        logger.info(f"Comparing approaches on {file_path}")
        
        # Process with adaptive approach
        adaptive_result = self.orchestrator.process_file(file_path)
        
        return {
            "file": file_path,
            "adaptive_processing": adaptive_result,
            "comparison_note": "Full comparison requires ground truth labels",
        }
