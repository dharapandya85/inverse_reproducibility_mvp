from utils.logger import setup_logger
import os
logger=setup_logger(__name__)
class RuleBasedCodeGenerator:
    def __init__(self,extracted_manuscript_content,processed_data_paths):
        self.extracted_content=extracted_manuscript_content
        self.processed_data_paths=processed_data_paths
        self.code_snippets=[]
        self.dependencies={"pandas":">=1.0.0"}
        self.identified_data_variables={}
    def generate(self):
        self._generate_data_loading()
        self._generate_analysis_code()
        self._generate_plotting_code()
        return "\n".join(self.code_snippets),self.dependencies
    def _generate_data_loading(self):
        self.code_snippets.append("import pandas as pd ")
        self.code_snippets.append("")
        for i,data_path in enumerate(self.processed_data_paths):
            data_id=f"df_{i+1}"
            self.identified_data_variables[data_path]=data_id
            docker_data_path=f"/app/data/processed/{os.path.basename(data_path)}"
            self.code_snippets.append(f"# Load processed data from {docker_data_path}")
            self.code_snippets.append(f"{data_id}=pd.read_csv('{docker_data_path}')")
            self.code_snippets.append("")
        logger.info("Generated data loading code.")
    def _generate_analysis_code(self):
        analysis_steps=self.extracted_content.get("analysis_steps",[])
        for step in analysis_steps:
            step_type=step.get("type")
            step_name=step.get("name")
            if step_type=="statistical_test":
                if step_name=="t-test":
                    self._add_t_test_code()
            elif step_type=="model":
                if step_name=="linear_regression":
                    self._add_linear_regression_code()
        logger.info("Generated analysis code.")
    def _add_t_test_code(self):
        self.code_snippets.append("# Placeholder for t-test code based on manuscript description")
        self.code_snippets.append("from scipy import stats")
        self.dependencies["scipy"]=">=1.0.0"
        self.code_snippets.append("try:")
        self.code_snippets.append("    # Assuming df_1 has 'group_A and 'group_B' columns or similar")
        self.code_snippets.append("    # You would need to infer these columns from the manuscript")
        self.code_snippets.append("    # Example: t_stat, p_val=stats.ttest_ind(df_1['column_A'],df_1['column_B'])")
        self.code_snippets.append("    pass # Add actual t-test logic here")
        self.code_snippets.append("except Exception as e:")
        self.code_snippets.append("    print(f'Error performing)")
        self.code_snippets.append("    print(f'Error performing t-test: {e}')")
        self.code_snippets.append("")
        logger.debug("Added t-test code snippet.")
    def _add_linear_regression_code(self):
        self.code_snippets.append("# Placeholder for linear regression code based on manuscript description")
        self.code_snippets.append("from sklearn.linear_model import LinearRegression")
        self.code_snippets.append("from sklearn.model_selection import train_test_split")
        self.dependencies["scikit-learn"] = ">=0.23.0"
        self.dependencies["numpy"] = ">=1.18.0"
        self.code_snippets.append("try:")
        self.code_snippets.append("    # Assuming df_1 has 'X' (features) and 'y' (target) columns")
        self.code_snippets.append("    # You would need to infer these from the manuscript")
        self.code_snippets.append("    # X = df_1[['feature1', 'feature2']]")
        self.code_snippets.append("    # y = df_1['target_variable']")
        self.code_snippets.append("    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)")
        self.code_snippets.append("    # model = LinearRegression()")
        self.code_snippets.append("    # model.fit(X_train, y_train)")
        self.code_snippets.append("    pass # Add actual linear regression logic here")
        self.code_snippets.append("except Exception as e:")
        self.code_snippets.append("    print(f'Error performing linear regression: {e}')")
        self.code_snippets.append("")
        logger.debug("Added linear regression code snippet.")

    def _generate_plotting_code(self):
        figure_metadata = self.extracted_content.get("figures_and_tables_metadata", [])
        if not figure_metadata:
            return
        
        self.code_snippets.append("import matplotlib.pyplot as plt")
        self.code_snippets.append("import seaborn as sns")
        self.dependencies["matplotlib"] = ">=3.0.0"
        self.dependencies["seaborn"] = ">=0.11.0"
        self.code_snippets.append("import os")  # Add this only once at the top if not already present
        self.code_snippets.append("os.makedirs('output/reproduced_results/figures', exist_ok=True)")
        for fig in figure_metadata:
            fig_type = fig.get("type")
            fig_num = fig.get("number")
            

            # This is highly rudimentary. Requires NLP to understand figure *content*.
            self.code_snippets.append(f"# Placeholder for Figure {fig_num} plotting code")
            self.code_snippets.append(f"try:")
            self.code_snippets.append(f"    # Based on inferred figure type/description:")
            # Example: If manuscript says "scatterplot of X vs Y"
            self.code_snippets.append(f"    # sns.scatterplot(data=df_1, x='feature_X', y='feature_Y')")
            # Example: If manuscript says "histogram of Z"
            self.code_snippets.append(f"    # sns.histplot(data=df_1, x='feature_Z')")
            self.code_snippets.append(f"    plt.title('Reproduced Figure {fig_num}')")
            self.code_snippets.append(f"    plt.savefig('output/reproduced_results/figures/figure_{fig_num}.png')")
            self.code_snippets.append(f"    plt.clf()") # Clear figure for next plot
            self.code_snippets.append(f"except Exception as e:")
            self.code_snippets.append(f"    print(f'Error generating Figure {fig_num}: {{e}}')")
            self.code_snippets.append("")
        logger.info("Generated plotting code.")  