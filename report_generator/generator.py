import os
import json
from jinja2 import Environment,FileSystemLoader
from utils.logger import setup_logger
logger=setup_logger(__name__)

class ReportGenerator:
    def __init__(self,output_dir):
        self.output_dir=os.path.join(output_dir,"reports")
        os.makedirs(self.output_dir,exist_ok=True)
        self.template_env=Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')))
    def generate_report(self,reproducibility_data):
        timestamp_str=reproducibility_data["timestamp"]  .replace(":","-").replace(".","-")
        report_filename_json=f"reproducibility_report_{timestamp_str}.json"
        report_filename_md=f"reproducibility_report_{timestamp_str}.md"

        json_report_path=os.path.join(self.output_dir,report_filename_json)
        with open(json_report_path,'w',encoding='utf-8') as f:
            json.dump(reproducibility_data,f,indent=4)
        logger.info(f"JSON report saved to:{json_report_path}")

        markdown_template=self.template_env.get_template("reproducibility_report.md.j2")
        markdown_content=markdown_template.render(report=reproducibility_data)
        md_report_path=os.path.join(self.output_dir,report_filename_md)
        with open(md_report_path,'w',encoding='utf-8') as f:
            f.write(markdown_content)
        logger.info(f"Markdown report saved to:{md_report_path}")

        return json_report_path