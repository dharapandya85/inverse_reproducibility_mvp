import os
import subprocess
from config import Config
from utils.logger import setup_logger
logger=setup_logger(__name__)
class DockerManager:
    def __init__(self,output_dir,dependencies):
        self.output_dir=output_dir
        self.dependencies=dependencies
        self.config=Config()
        self.dockerfile_path=os.path.join(self.output_dir,"virtual_environment","Dockerfile")
        self.script_path=os.path.join(self.output_dir,"virtual_environment","reproduced_code.py")
        self.processed_data_source_path=os.path.join(self.output_dir,"data","processed")
    def create_environment(self):
        self._generate_dockerfile()
        logger.info(f'Building Docker image:{self.config.docker_image_name}...')
        docker_build_context=os.path.dirname(self.dockerfile_path)
        try:
            subprocess.run(
                ["docker","build","-t",self.config.docker_image_name,"-f",self.dockerfile_path,docker_build_context],
                check=True,capture_output=True,text=True,encoding="utf-8"
            )
            logger.info("Docker image built successfully.")
            return {"type":"docker","image_name":self.config.docker_image_name, "dockerfile": self.dockerfile_path}
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to build Docker image.")
            logger.error(f"Command: {''.join(e.cmd)} ")
            logger.error(f"Docker STDOUT:\n{str(e.stdout)}")
            logger.error(f"Docker STDERR:\n{str(e.stderr)}")
            raise
        except FileNotFoundError:
            logger.error("Docker command not found. Is Docker installed and in your PATH")
            raise
    def _generate_dockerfile(self):
        python_version=self.dependencies.get("python",["3.9"])[0]
        requirements_content=self._generate_requirements_txt()
        
        dockerfile_script_name=os.path.basename(self.script_path)
        dockerfile_content=f"""
FROM python:{python_version}-slim-buster

WORKDIR /app

# Copy generated requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create directories for data and results
RUN mkdir -p /app/output/reproduced_results/figures
RUN mkdir -p /app/output/reproduced_results/tables


# Copy the generated code script
COPY {dockerfile_script_name} /app/{dockerfile_script_name}

CMD ["python", "{dockerfile_script_name}"]
"""
        os.makedirs(os.path.dirname(self.dockerfile_path),exist_ok=True)
        with open(self.dockerfile_path,"w") as f:
            f.write(dockerfile_content.strip())
        logger.info(f"Dockerfile generated at: {self.dockerfile_path}")

        with open(os.path.join(os.path.dirname(self.dockerfile_path),"requirements.txt"),"w") as f:
            f.write(requirements_content)
        logger.info(f"requirements.txt generated for Docker at: {os.path.join(os.path.dirname(self.dockerfile_path),'requirements.txt')}")

    def _generate_requirements_txt(self):
        requirements = []
        for dep, version_info in self.dependencies.items():
            # Simple mapping, needs more robust handling for specific version ranges
            if dep == "python": # Python version is handled by FROM
                continue
            package_name=dep
            req_version=""
            if isinstance(version_info,list):
                if version_info:
                    req_version=version_info[-1]
            elif isinstance(version_info,str):
                req_version=version_info
            if req_version: 
                if any(op in req_version for op in ['==','>=','<=','>','<','~=']):
                    requirements.append(f"{package_name}{req_version}")
                else:
                    requirements.append(f"{package_name}")
        return "\n".join(requirements)
             
    def execute_code(self,code,processed_data_paths,results_output_dir):
        # script_file_path=os.path.join(self.output_dir,"reproduced_code.py")
        with open(self.script_path,"w") as f:
            f.write(code)
        logger.info(f"Generated code saved to  {self.script_path}")
        if not os.path.exists(self.processed_data_source_path):
            logger.warning(f"Processed data directory not found: {self.processed_data_source_path}. This might cause issues during execution.")
            # Depending on your project, you might want to raise an error here:
            # raise FileNotFoundError(f"Processed data directory not found: {processed_data_source_path}")
        
        try:
            abs_processed_data_source_path=os.path.abspath(self.processed_data_source_path)
            abs_results_output_dir=os.path.abspath(results_output_dir)
            cmd = [
                "docker", "run", "--rm",
                # Mount the processed data directory from host to container
                # ':ro' makes it read-only inside the container
                "-v", f"{abs_processed_data_source_path}:/app/data/processed:ro",
                # Mount the results output directory from host to container
                "-v", f"{abs_results_output_dir}:/app/output/reproduced_results",
                self.config.docker_image_name,
                "python", os.path.basename(self.script_path) # CORRECTED: Use base name as it's in /app
            ]
        # processed_data_source_path = os.path.join(self.output_dir, "data", "processed")
        # reproduced_results_target_path_figures = os.path.join("/app/output/reproduced_results/figures")
        # reproduced_results_target_path_tables = os.path.join("/app/output/reproduced_results/tables")
            logger.info(f"Running Docker command:{' '.join(cmd)}")
            process=subprocess.run(cmd,check=False,capture_output=True, text=True,encoding="utf-8")
            
            if process.returncode !=0:
                logger.error(f"Docker container exited with error: {process.stderr}")
                logger.error(f"Docker stdout:{process.stdout}")
                raise RuntimeError(f"Code execution failed in Docker: {process.stderr} ")
            else:
                logger.info(f"Docker container output:\n{process.stdout}")
                if process.stderr:
                    logger.warning(f"Docker container warning/errors (stderr):\n{process.stderr}")
            host_figures_dir=os.path.join(results_output_dir,"figures")
            host_tables_dir=os.path.join(results_output_dir,"tables")
            generated_figure_paths=[]
            if os.path.exits(host_figures_dir):
                generated_figure_paths=[
                    os.path.join(host_figures_dir,f)
                    for f in os.listdir(host_figures_dir)
                    if f.endswith((".png", ".jpg", ".jpeg", ".pdf"))
                ]
            generated_table_paths=[]
            if os.path.exits(host_tables_dir):
                generated_table_paths=[
                    os.path.join(host_tables_dir,f)
                    for f in os.listdir(host_tables_dir)
                    if f.endswith((".png", ".jpg", ".jpeg", ".pdf"))
                ]
            return {"figures":generated_figure_paths,"tables": generated_table_paths}
        except FileNotFoundError:
            logger.error("Docker command not found.Is Docker installed and in your PATH?")
            raise
        except Exception as e:
            logger.error(f"Error running Docker container: {e}")
            raise

