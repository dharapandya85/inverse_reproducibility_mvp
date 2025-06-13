import os
import subprocess
from config import Config
from utils.logger import setup_logger
logger=setup_logger(__name__)
class CondaManager:
    def __init__(self,output_dir,dependencies):
        self.output_dir=output_dir
        self.dependencies=dependencies
        self.config=Config()
        self.env_path=os.path.join(output_dir,"virtual_environment",self.config.conda_env_name)
    def create_environment(self):
        logger.info(f'Creating Conda environment:{self.config.conda_env_name} at {self.env_path}')
        try:
            subprocess.run(
                ["conda","create","--prefix",self.env_path,"python=3.9","-y"],
                check=True,capture_output=True,text=True
            )
            requirements_content=self._generate_conda_requirements()
            temp_req_file=os.path.join(self.output_dir,"virtual_environment","conda_requirements.txt")
            with open(temp_req_file,"w") as f:
                f.write(requirements_content)
            subprocess.run(
                ["conda","install","--prefix",self.env_path, "--file", temp_req_file, "-y"],
                check=True,capture_output=True,text=True
            )
            logger.info("Conda environment created and dependencies installed successfully.")
            return {"type":"conda","env_name":self.config.conda_env_name, "env_path": self.env_path}
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create Conda environment or install dependencies: {e.stderr} ")
            raise
        except FileNotFoundError:
            logger.error('Conda command not found.Is Anaconda/Miniconda installed and in your PATH?')
            raise
    def _generate_conda_requirements(self):
        requirements=[]
        for dep, version in self.dependencies.items():
            if dep=="python":continue
            if isinstance(version,list):
                req_version=version[-1]
            else:
                req_version=version
            requirements.append(f"{dep}={req_version}")
        return "\n".join(requirements)
    def execute_code(self,code,processed_data_paths,results_output_dir):
        script_file_path=os.path.join(self.output_dir,"reproduced_code.py")
        with open(script_file_path,"w") as f:
            f.write(code)
        logger.info(f"Executing code in Conda Environment {self.config.conda_env_name}...")
        try:
            python_executable=os.path.join(self.env_path,"bin","python")
            cmd=[
                python_executable,
                script_file_path
            ]
            original_cwd=os.getcwd()
            os.chdir(self.output_dir)
            process=subprocess.run(cmd,check=False,capture_output=True, text=True)
            os.chdir(original_cwd)
            if process.returncode !=0:
                logger.error(f"Conda script execution failed: {process.stderr}")
                raise RuntimeError(f"Code execution failed in Conda: {process.stderr} ")
            else:
                logger.info(f"Conda script output:\n{process.stdout}")
                if process.stderr:
                    logger.warning(f"Conda script warning/errors (stderr):\n{process.stderr}")
            generated_figure_paths=[os.path.join(results_output_dir, "figures", f) for f in os.listdir(os.path.join(results_output_dir, "figures")) if f.endswith((".png", ".jpg", ".jpeg", ".pdf"))]
            generated_table_paths=[os.path.join(results_output_dir, "tables", f) for f in os.listdir(os.path.join(results_output_dir, "tables")) if f.endswith((".csv", ".txt", ".json"))]
            return {"figures":generated_figure_paths,"tables": generated_table_paths}
        except FileNotFoundError:
            logger.error("Python executable not found in Conda environment. Check Conda installation.")
            raise
        except Exception as e:
            logger.error(f"Error running script in Conda environment: {e}")
            raise

