import argparse
import os
import datetime
from config import Config
from manuscript_parser.parser import ManuscriptParser
from data_processor.processor import DataProcessor
from environment_generator.manager import EnvironmentManager
from result_comparator.comparator import ResultComparator
from code_generator.generator import CodeGenerator
from report_generator.generator import ReportGenerator
from utils.logger import setup_logger

logger=setup_logger(__name__)

def main():
    parser=argparse.ArgumentParser(description="Reproduce research findings from a manuscript and dataset.")
    parser.add_argument("--manuscript",type=str,required=True,help="Path to the scientific manuscript(PDF or text).")
    parser.add_argument("--dataset",nargs='+',required=True,help="Path to the dataset(s)(e.g.,CSV,JSON).")
    parser.add_argument("--output-dir",type=str,default="output",help="Directory to store reproduction outputs")
    args=parser.parse_args()

    config=Config()
    config.output_dir=args.output_dir
    os.makedirs(os.path.join(config.output_dir,"reproduced_results","figures"),exist_ok=True)
    os.makedirs(os.path.join(config.output_dir,"reproduced_results","tables"),exist_ok=True)
    os.makedirs(os.path.join(config.output_dir,"virtual_environment"),exist_ok=True)
    os.makedirs(os.path.join(config.output_dir,"reports"),exist_ok=True)

    logger.info(f"Starting reproducibility attempt for manuscript:{args.manuscript}")
    logger.info(f"Using datasets:{','.join(args.dataset)}")

    reproducibility_report={
        "timestamp":datetime.datetime.now().isoformat(),
        "manuscript_path":args.manuscript,
        "dataset_path":args.dataset,
        "reproduction_steps":[],
        "overall_confidence_score":0.0,
        "identified_failure_points":[],
        "software_versions_identified":{},
        "reproduced_code":" ",
        "virtual_environment_details":{}
    }
    try:
        # 1. Manuscript Parsing
        logger.info("Step 1: Parsing manuscript...")
        manuscript_parser=ManuscriptParser(args.manuscript)
        extracted_content=manuscript_parser.parse()
        reproducibility_report["reproduction_steps"].append({"step":"Manuscript Parsing","status":"Success"})
        reproducibility_report["extracted_manuscript_content"]={
            "methodology_sections":extracted_content.get("methodology_sections","N/A"),
            "results_sections":extracted_content.get("results_sections","N/A"),
            "figures_and_tables_metadata":extracted_content.get("figures_and_tables_metadata","N/A"),
            "dependencies_mentioned":extracted_content.get("dependencies_mentioned","N/A"),
        }
        reproducibility_report["software_versions_identified"].update(extracted_content.get("dependencies_mentioned",{}))
        # 2.Data Processing
        logger.info("Step 2: Processing data...")
        data_processor=DataProcessor(args.dataset,config.output_dir)
        processed_data_paths=data_processor.process_data(
            extracted_content.get("data_processing_instructions",{})
        )
        reproducibility_report["reproduction_steps"].append({"step":"Data Processing","status":"Success","details":{"processed_files":processed_data_paths}})

        #3.Code Generation
        logger.info("Step 3: Generating code...")
        code_generator=CodeGenerator(extracted_content,processed_data_paths)
        generated_code,identified_dependencies=code_generator.generate_code()
        reproducibility_report["reproduced_code"]=generated_code
        reproducibility_report["software_versions_identified"].update(identified_dependencies)
        reproducibility_report["reproduction_steps"].append({"step":"Code Generation","status":"Success"})

        temp_env_manager_for_path = EnvironmentManager(config.output_dir, {})
        script_file_path_for_docker = temp_env_manager_for_path.manager.script_path
        
        # Ensure the directory exists before writing the file
        os.makedirs(os.path.dirname(script_file_path_for_docker), exist_ok=True)
        with open(script_file_path_for_docker, "w") as f:
            f.write(generated_code)
        logger.info(f"Generated code saved to disk at: {script_file_path_for_docker}")
        # --- End temporary workaround ---
         #4.Environment Recreation
        logger.info("Step 4: Recreating environment...")
        env_manager=EnvironmentManager(config.output_dir,reproducibility_report["software_versions_identified"])
        env_details=env_manager.create_environment()
        reproducibility_report["virtual_environment_details"]=env_details
        reproducibility_report["reproduction_steps"].append({"step":"Environment Recreation","status":"Success","details":env_details})

        #5.Result Generation
        logger.info("Step 5: Executing Generated code to produce results ...")
        generated_results=env_manager.execute_code(generated_code,processed_data_paths,config.output_dir)
        reproducibility_report["reproduction_steps"].append({"step":"Result Generation","status":"Success","details":{"generated_results_paths":generated_results}})

        #6.Code Generation
        logger.info("Step 6: Comparing Generated Results with manuscript results...")
        result_comparator=ResultComparator(generated_results,extracted_content.get("reported_results",{}))
        comparison_results,confidence_score,failure_points=result_comparator.compare_results()
        reproducibility_report["comparison_results"]=comparison_results
        reproducibility_report["overall_confidence_score"]=confidence_score
        reproducibility_report["identified_failure_points"].extend(failure_points)
        reproducibility_report["reproduction_steps"].append({"step":"Comparison and Evaluation","status":"Success","confidence":confidence_score})
    except Exception as e:
        logger.error(f'An error occurred during reproducibility attempt:{e}',exc_info=True)
        reproducibility_report["status"]="Failed"
        reproducibility_report["error_message"]=str(e)
        reproducibility_report["reproduction_steps"].append({"step":"Overall","status":"Failed","error":str(e)})

    finally:
        # 7. Reporting
        logger.info("Step 7: Generating reproducibility reports...")
        report_generator=ReportGenerator(config.output_dir)
        report_path=report_generator.generate_report(reproducibility_report)
        logger.info(f"Reproducibility report generated:{report_path}")

        logger.info("Reproducibility attempts finished.")


if __name__=="__main__":
    main()
