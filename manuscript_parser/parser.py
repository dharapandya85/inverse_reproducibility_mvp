# inverse_reproducibility/manuscript_parser/parser.py
import re
from .pdf_extractor import PDFExtractor
from .text_extractor import TextExtractor
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ManuscriptParser:
    def __init__(self, manuscript_path):
        self.manuscript_path = manuscript_path
        self.extracted_content = {}

    def parse(self):
        file_extension = self.manuscript_path.split('.')[-1].lower()

        if file_extension == 'pdf':
            logger.info(f"Extracting content from PDF: {self.manuscript_path}")
            extractor = PDFExtractor(self.manuscript_path)
            raw_text = extractor.extract_text()
            # More sophisticated PDF parsing would involve layout analysis
            # and potentially table/figure extraction
        elif file_extension in ['txt', 'md']:
            logger.info(f"Extracting content from text file: {self.manuscript_path}")
            extractor = TextExtractor(self.manuscript_path)
            raw_text = extractor.extract_text()
        else:
            raise ValueError(f"Unsupported manuscript file type: {file_extension}")

        self.extracted_content["raw_text"] = raw_text
        self._identify_sections(raw_text)
        self._extract_key_information()
        return self.extracted_content

    def _identify_sections(self, text):
        # Basic section identification using keywords and regex
        # This needs to be significantly more robust for real-world manuscripts
        methodology_keywords = ["methodology", "methods", "experimental setup", "approach", "materials and methods"]
        results_keywords = ["results", "findings", "experimental results"]
        discussion_keywords = ["discussion", "conclusion"]

        self.extracted_content["methodology_sections"] = self._find_sections(text, methodology_keywords)
        self.extracted_content["results_sections"] = self._find_sections(text, results_keywords)
        self.extracted_content["discussion_sections"] = self._find_sections(text, discussion_keywords)

    def _find_sections(self, text, keywords):
        found_sections = []
        # Simple regex for finding sections. A more advanced approach would use NLP libraries.
        for keyword in keywords:
            # This is a very simplistic approach. Real NLP would be needed.
            if keyword in text.lower():
                # For demonstration, just taking the first 1000 chars after the keyword
                # A robust implementation would parse until the next section header
                start_idx = text.lower().find(keyword)
                if start_idx != -1:
                    found_sections.append(text[start_idx:start_idx + 1000]) # Placeholder
        return found_sections

    def _extract_key_information(self):
        # This is the crucial part where NLP or pattern matching comes in.
        # It needs to extract:
        # - Data processing steps (e.g., "normalized data", "removed outliers")
        # - Statistical methods (e.g., "t-test", "ANOVA", "linear regression")
        # - Machine learning models (e.g., "Random Forest classifier", "CNN")
        # - Libraries/Software versions (e.g., "Python 3.8", "Scikit-learn 0.24.1", "R 4.0")
        # - Reported results (numerical values, figure descriptions, table data)

        raw_text = self.extracted_content.get("raw_text", "")
        methodology_text = " ".join(self.extracted_content.get("methodology_sections", []))
        results_text = " ".join(self.extracted_content.get("results_sections", []))

        # --- Placeholder for sophisticated NLP/Regex ---
        # Data Processing Instructions
        self.extracted_content["data_processing_instructions"] = self._extract_data_processing_instructions(methodology_text)

        # Analysis Steps (e.g., statistical tests, ML models)
        self.extracted_content["analysis_steps"] = self._extract_analysis_steps(methodology_text)

        # Reported Results (Tables, Figures, Statistical Values)
        self.extracted_content["reported_results"] = self._extract_reported_results(results_text)

        # Software Dependencies and Versions
        self.extracted_content["dependencies_mentioned"] = self._extract_dependencies(raw_text)

        # Figures and Tables Metadata (e.g., "Figure 1 shows...", "Table 2 summarizes...")
        self.extracted_content["figures_and_tables_metadata"] = self._extract_figure_table_metadata(raw_text)

    def _extract_data_processing_instructions(self, text):
        # Example: look for phrases like "data was normalized", "outliers removed", "missing values imputed"
        instructions = {}
        if "normalized" in text:
            instructions["normalization"] = True
        if "outliers removed" in text:
            instructions["outlier_removal"] = True
        # This would involve more advanced NLP to identify specific transformations and parameters.
        return instructions

    def _extract_analysis_steps(self, text):
        # Example: identify "t-test", "ANOVA", "linear regression", "random forest"
        analysis_steps = []
        if "t-test" in text:
            analysis_steps.append({"type": "statistical_test", "name": "t-test"})
        if "linear regression" in text:
            analysis_steps.append({"type": "model", "name": "linear_regression"})
        # More sophisticated NLP for identifying parameters, features, targets.
        return analysis_steps

    def _extract_reported_results(self, text):
        # This is extremely challenging. Requires OCR for figures/tables in PDFs,
        # or advanced NLP for extracting numerical values from text.
        # For a first pass, we might look for common patterns like "p < 0.05", "R^2 = 0.75"
        reported_results = {}
        # Example: Extracting numerical values
        import re
        p_value_matches = re.findall(r"p\s*[<=>]\s*(\d(?:\.\d+)?(?:e[+\-]?\d+)?)", text)
        if p_value_matches:
            reported_results["p_values"] = [float(p) for p in p_value_matches]

        r_squared_matches = re.findall(r"R\^2\s*=\s*(\d(?:\.\d+)?)", text)
        if r_squared_matches:
            reported_results["R_squared"] = [float(r) for r in r_squared_matches]
        # This needs to be expanded significantly to capture all reported results.
        return reported_results

    def _extract_dependencies(self, text):
        # Look for mentions of software, libraries, and versions
        dependencies = {}
        # Example: "Python 3.9", "scikit-learn 1.0", "RStudio", "numpy 1.22"
        python_versions = re.findall(r"Python\s*(\d(?:\.\d+){1,2})", text, re.IGNORECASE)
        if python_versions:
            dependencies["python"] = sorted(list(set(python_versions))) # Get unique, sorted
        
        # Example for a library
        sklearn_versions = re.findall(r"scikit-learn\s*(\d(?:\.\d+){1,2})", text, re.IGNORECASE)
        if sklearn_versions:
            dependencies["scikit-learn"] = sorted(list(set(sklearn_versions)))

        # Add more regex patterns for other common scientific software/libraries
        return dependencies

    def _extract_figure_table_metadata(self, text):
        # Identify captions and mentions of figures/tables
        metadata = []
        # Example: "Figure 1 shows...", "Table S1 provides..."
        figure_matches = re.findall(r"(Figure|Fig\.)\s*(\d+)", text, re.IGNORECASE)
        for fig_type, fig_num in figure_matches:
            metadata.append({"type": "figure", "number": fig_num})
        
        table_matches = re.findall(r"(Table|Tab\.)\s*(S?\d+)", text, re.IGNORECASE)
        for tab_type, tab_num in table_matches:
            metadata.append({"type": "table", "number": tab_num})
        return metadata