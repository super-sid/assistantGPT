DESCRIPTION = "You are an agent to create boilerplate code in any programming language for a given project idea."

GENERATE_PROJECT_STRUCTURE_TEMPLATE = template = """
{description} Given the project idea: {project_idea}, generate a list of essential files for the git repository. The list should resemble a `tree -ifF` output. Prefix each filename with '-'. Only filenames are needed; no directories or explanations. Ensure no irrelevant files are included.

Output:
"""

UPDATE_PROJECT_STRUCTURE_TEMPLATE = """{description}

Project idea: {project_idea}

Project structure:
{project_structure}

You have to update the project structure based on the following instructions:

Add Unit tests: {unit_tests}
Add Docker support: {dockerization}
Add Github Actions: {github_actions}
Add Pre-commit hooks: {pre_commit_hooks}

The list should be a `tree -ifF` output. Prefix each line with '-' character. You must be clear and concise. No explanations required. NO bold text should be there.

Project structure:"""

PROJECT_FILE_TEMPLATE = """---
Wrap the 'File Content:' section in <code></code> tags. 

Description: {description}

Project Idea: {project_idea}

Project Structure:
{project_structure}

File Name: {file_name}
File Content:
---
"""