import os
from .docker_manager import DockerManager
from .conda_manager import CondaManager
from config import Config
from utils.logger import setup_logger
logger=setup_logger(__name__)
class EnvironmentManager:
    def __init__(self,output_dir,dependencies):
        self.output_dir=output_dir
        self.dependencies=dependencies
        self.config=Config()
        self.env_type=self._determine_env_type()
        self.manager=self._get_env_manager()
    def _determine_env_type(self):
        return "docker"
    def _get_env_manager(self):
        if self.env_type=="docker":
            return DockerManager(self.output_dir,self.dependencies)
        elif self.env_type=="conda":
            return CondaManager(self.output_dir,self.dependencies)
        else:
            raise ValueError(f"Unsupported environment type:{self.env_type}")
    def create_environment(self):
        logger.info(f'Creating {self.env_type} environment... ')
        env_details=self.manager.create_environment()
        logger.info("Environment created:{env_details}")
        return env_details
    def execute_code(self,code,processed_data_paths,results_output_dir):
        logger.info(f"Executing code within the {self.env_type}environment...")
        generated_results=self.manager.execute_code(code,processed_data_paths,results_output_dir)
        logger.error("Code execution Complete.")
        return generated_results    

