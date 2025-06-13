import os
import pandas as pd
from config import Config
from .diff_analyzer import DiffAnalyzer
from utils.logger import setup_logger
logger=setup_logger(__name__)
class ResultComparator:
    def __init__(self,generated_results,reported_results_from_manuscript):
        self.generated_results=generated_results
        self.reported_results=reported_results_from_manuscript
        self.config=Config()
        self.comparison_results={}
        self.confidence_score=0.0
        self.failure_points=[]
        self.diff_analyzer=DiffAnalyzer()
    def compare_results(self):
        self._compare_numerical_results()
        self._compare_figures()
        self._compare_tables()
        self._calculate_overall_confidence()
        return self.comaparison_results,self.confidence_score,self.failure_points
    def _compare_numerical_results(self):
        logger.info("Comparing numerical results...")
        reported_numerical=self.reported_results.get("p_values",[])+self.reported_results.get('R_squared',[])
        generated_numerical=[]
        summary_path=os.path.join(self.config.output_dir,"reproduced_results","results_summary.txt")
        if os.path.exists(summary_path):
            with open(summary_path):
                content=f.read()
                import re
                numbers=re.findall(r"[-+]?\d*\.d+|\d+",content)
                generated_numerical.extend([float(n) for n in numbers])
        if not reported_numerical and not generated_numerical:
            self.comparison_results["numerical"]='No numerical results to compare.'
            return
        match_count=0
        total_reported=len(reported_numerical)
        for reported_val in reported_numerical:
            found_match=False
            for gen_val in generated_numerical:
                if abs(reported_val-gen_val)<self.config.comparision_tolerance:
                    match_count+=1
                    found_match=True
                    break
            if not found_match:
                self.failure_points.append(f"Reported numerical value {reported_val} not reproduced accurately.")
        if total_reported>0:
            accuracy=match_count/total_reported
            self.comparison_results["numerical"]=f"Accuracy:{accuracy:.2f}"
            self.confidence_score+=accuracy*0.3
        else:
            self.comparision_results["numerical"]="No reported numerical results found in manuscript for comaparison."
        logger.info(f"Numerical comparison results:{self.comparison_results['numerical']}")
    def _compare_figures(self):
        logger.info('Comparing figures...')
        generated_figures=self.generated_results.get('figures',[])
        reported_figure_count=len([f for f in self.reported_results.get('figures_and_tables_metadata',[]) if f["type"]=="figure"])

        if reported_figure_count>0 and len(generated_figures)>=reported_figure_count:
            self.comparison_results["figures"]="At least the same number of figures were generated as reported."
            self.confidence_score+=0.2
        elif reported_figure_count>0:
            self.comparison_results["figures"]=f"Expected {reported_figure_count} figures, but only {len(generated_figures)} were generated."
            self.failure_points.append(f"Missing {reported_figure_count-len(generated_figures)} expected figures.")
        else:
            self.comparison_results["figures"]="No figures reported in manuscript for comparison."
        logger.info(f"Figure comparison results:{self.comparison_results['figures']}")
    
    def _compare_tables(self):
        logger.info("Comparing tables...")
        generated_tables=self.generated_results.get('tables',[])
        reported_table_count=len([t for t in self.reported_results.get('figures_and_tables_metadata',[]) if t["type"]=="table"])

        if reported_table_count>0 and len(generated_tables)>=reported_table_count:
            self.comparison_results["tables"]="At least the same number of tables were generated as reported."
            self.confidence_score+=0.2
        elif reported_table_count>0:
            self.comparison_results["tables"]=f"Expected {reported_table_count} tables, but only {len(generated_tables)} were generated."
            self.failure_points.append(f"Missing {reported_table_count-len(generated_tables)} expected tables.")
        else:
            self.comparison_results["tables"]="No tables reported in manuscript for comparison."
        logger.info(f"Table comparison results:{self.comparison_results['tables']}")
    
    def _calculate_overall_confidence(self):
        self.confidence_score=min(1.0,max(0.0,self.confidence_score))
        logger.info(f"Overall reproducibility confidence score: {self.confidence_score:.2f}")
        