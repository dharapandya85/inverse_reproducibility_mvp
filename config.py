class Config:
    def __init__(self):
        self.output_dir="output"
        self.docker_image_name="reproducibility_env"
        self.conda_env_name="repro_env"
        self.code_generation_model="GPT_MODEL_NAME"
        self.max_tokens=2000
        self.temperature=0.7
        self.comparison_tolerance=1e-6
