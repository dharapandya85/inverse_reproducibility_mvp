# inverse_reproducibility/code_generator/generator.py

from .rule_based_generator import RuleBasedCodeGenerator
# from .ml_code_generator import MLCodeGenerator # For advanced ML-based generation
from utils.logger import setup_logger

logger = setup_logger(__name__)

class CodeGenerator:
    def __init__(self, extracted_manuscript_content, processed_data_paths):
        self.extracted_content = extracted_manuscript_content
        self.processed_data_paths = processed_data_paths
        self.generated_code = ""
        self.identified_dependencies = {}

    def generate_code(self):
        # Prioritize rule-based generation for common patterns.
        # Fallback to ML-based if rules are insufficient or for complex scenarios.
        
        # 1. Rule-based generation (e.g., for common statistical tests, basic plots)
        logger.info("Attempting rule-based code generation...")
        rule_based_generator = RuleBasedCodeGenerator(self.extracted_content, self.processed_data_paths)
        generated_code_rb, identified_deps_rb = rule_based_generator.generate()
        
        self.generated_code += generated_code_rb
        self.identified_dependencies.update(identified_deps_rb)

        # 2. ML-based generation (if needed and implemented)
        # This would require a powerful large language model (LLM) fine-tuned for code generation.
        # if not self.generated_code: # Or if rule-based was incomplete/low confidence
        #     logger.info("Attempting ML-based code generation...")
        #     ml_code_generator = MLCodeGenerator(self.extracted_content, self.processed_data_paths)
        #     generated_code_ml, identified_deps_ml = ml_code_generator.generate()
        #     self.generated_code += generated_code_ml
        #     self.identified_dependencies.update(identified_deps_ml)
        
        if not self.generated_code:
            logger.warning("No code could be generated based on the manuscript content.")
            self.generated_code = "# No code generated based on manuscript instructions."

        return self.generated_code, self.identified_dependencies