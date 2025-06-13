# Inverse Reproducibility Challenge Agent

This project aims to develop an intelligent agent that can automatically attempt to reproduce the code and analysis associated with a scientific manuscript and its corresponding dataset.

## Problem Statement

Reproducibility is a cornerstone of scientific integrity. However, many published research manuscripts lack sufficient detail or accessible code to reproduce the reported findings. This creates a significant barrier to validating and building upon existing research.

## Challenge Goal

Given a scientific manuscript (PDF or text) and its corresponding dataset(s), the agent will:
1. Extract relevant information (methodology, results, dependencies) from the manuscript.
2. Process the provided dataset(s) according to the described analysis steps.
3. Generate the Python code required to perform the analysis.
4. Create a virtual environment (e.g., using Docker) with the necessary software dependencies.
5. Execute the generated code within the environment to produce results (tables, figures, statistical values).
6. Compare the generated results with the reported results in the manuscript.
7. Assign a confidence score to the reproducibility attempt.
8. Identify and document potential points of failure or ambiguity.
9. Generate a detailed report summarizing the attempt.

## Project Structure