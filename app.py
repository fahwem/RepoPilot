from smolagents import CodeAgent, OpenAIServerModel, tool
import requests
import re
import base64

from tools.final_answer import FinalAnswerTool
from Gradio_UI import GradioUI


# ============================================================
# GITHUB URL PARSER
# ============================================================

def parse_github_url(repo_url: str):
    """Extract owner and repository name from a GitHub URL."""

    match = re.match(
        r"https?://github\.com/([^/]+)/([^/#]+)",
        repo_url.strip()
    )

    if not match:
        raise ValueError(
            "Invalid GitHub URL. Example: "
            "https://github.com/owner/repository"
        )

    owner = match.group(1)
    repo = match.group(2)

    if repo.endswith(".git"):
        repo = repo[:-4]

    return owner, repo


# ============================================================
# GITHUB REPOSITORY OVERVIEW
# ============================================================

@tool
def github_repo_overview(repo_url: str) -> str:
    """
    Get a comprehensive but compact overview of a public GitHub
    repository.

    This should normally be the first tool used when the user asks
    a general question about a repository.

    It provides repository metadata, file count, folder count,
    file structure and README contents.

    Args:
        repo_url: Public GitHub repository URL.
    """

    try:
        owner, repo = parse_github_url(repo_url)

        api_base = f"https://api.github.com/repos/{owner}/{repo}"

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "RepoPilot"
        }

        # --------------------------------------------------------
        # Repository metadata
        # --------------------------------------------------------

        response = requests.get(
            api_base,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return (
                f"Could not access repository. "
                f"GitHub returned status {response.status_code}."
            )

        repo_data = response.json()

        # --------------------------------------------------------
        # Recursive file tree
        # --------------------------------------------------------

        branch = repo_data.get("default_branch", "main")

        tree_url = (
            f"{api_base}/git/trees/{branch}"
            f"?recursive=1"
        )

        tree_response = requests.get(
            tree_url,
            headers=headers,
            timeout=15
        )

        files = []
        folders = set()

        if tree_response.status_code == 200:

            tree_data = tree_response.json()

            for item in tree_data.get("tree", []):

                path = item.get("path", "")
                item_type = item.get("type")

                if item_type == "blob":

                    files.append(path)

                    parts = path.split("/")[:-1]

                    for i in range(
                        1,
                        len(parts) + 1
                    ):
                        folders.add(
                            "/".join(parts[:i])
                        )

        # --------------------------------------------------------
        # README
        # --------------------------------------------------------

        readme_text = ""

        readme_url = f"{api_base}/readme"

        readme_response = requests.get(
            readme_url,
            headers=headers,
            timeout=10
        )

        if readme_response.status_code == 200:

            try:

                readme_data = readme_response.json()

                encoded = readme_data.get(
                    "content",
                    ""
                )

                if encoded:

                    readme_text = base64.b64decode(
                        encoded
                    ).decode(
                        "utf-8",
                        errors="replace"
                    )

            except Exception:
                readme_text = ""

        # Keep model context manageable
        if len(readme_text) > 12000:

            readme_text = readme_text[:12000]

            readme_text += (
                "\n\n[README truncated]"
            )

        # --------------------------------------------------------
        # Build result
        # --------------------------------------------------------

        result = []

        result.append("=== REPOSITORY ===")

        result.append(
            f"Name: {repo_data.get('full_name')}"
        )

        result.append(
            f"Description: {repo_data.get('description')}"
        )

        result.append(
            f"Main language: {repo_data.get('language')}"
        )

        result.append(
            f"Stars: {repo_data.get('stargazers_count')}"
        )

        result.append(
            f"Forks: {repo_data.get('forks_count')}"
        )

        result.append(
            f"Default branch: {branch}"
        )

        result.append("")

        result.append(
            "=== REPOSITORY SIZE ==="
        )

        result.append(
            f"Total files: {len(files)}"
        )

        result.append(
            f"Total folders: {len(folders)}"
        )

        result.append("")

        result.append(
            "=== FILE STRUCTURE ==="
        )

        if files:

            for file_path in files[:300]:
                result.append(file_path)

            if len(files) > 300:

                result.append(
                    f"... and "
                    f"{len(files) - 300} more files"
                )

        else:

            result.append(
                "No files found."
            )

        if readme_text:

            result.append("")
            result.append("=== README ===")
            result.append(readme_text)

        return "\n".join(result)

    except Exception as e:

        return (
            f"Error accessing GitHub: {str(e)}"
        )


# ============================================================
# LIST FILES
# ============================================================

@tool
def github_list_files(
    repo_url: str,
    path: str = ""
) -> str:
    """
    List files and folders inside a specific directory.

    Args:
        repo_url: Public GitHub repository URL.
        path: Folder path. Empty means repository root.
    """

    try:

        owner, repo = parse_github_url(repo_url)

        url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/contents/{path}"
        )

        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code != 200:

            return (
                f"Could not access path '{path}'. "
                f"GitHub returned status "
                f"{response.status_code}."
            )

        data = response.json()

        if not isinstance(data, list):

            return (
                f"'{path}' is a file, "
                f"not a folder."
            )

        if not data:

            return "The folder is empty."

        result = []

        for item in data:

            if item["type"] == "dir":

                result.append(
                    f"[FOLDER] {item['path']}"
                )

            else:

                result.append(
                    f"[FILE] {item['path']}"
                )

        return "\n".join(result)

    except Exception as e:

        return (
            f"Error listing repository files: "
            f"{str(e)}"
        )


# ============================================================
# READ FILE
# ============================================================

@tool
def github_read_file(
    repo_url: str,
    file_path: str
) -> str:
    """
    Read a source-code or text file from a public GitHub
    repository.

    Args:
        repo_url: Public GitHub repository URL.
        file_path: Path to the file.
    """

    try:

        owner, repo = parse_github_url(repo_url)

        url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/contents/{file_path}"
        )

        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code != 200:

            return (
                f"Could not read '{file_path}'. "
                f"GitHub returned status "
                f"{response.status_code}."
            )

        data = response.json()

        if data.get("type") != "file":

            return (
                f"'{file_path}' is not a file."
            )

        encoded_content = data.get(
            "content",
            ""
        )

        content = base64.b64decode(
            encoded_content
        ).decode(
            "utf-8",
            errors="replace"
        )

        if len(content) > 20000:

            content = content[:20000]

            content += (
                "\n\n[File truncated]"
            )

        return (
            f"Contents of {file_path}:\n\n"
            f"{content}"
        )

    except Exception as e:

        return (
            f"Error reading file: {str(e)}"
        )


# ============================================================
# FIND CONTRIBUTORS
# ============================================================

@tool
def github_contributors(
    repo_url: str
) -> str:
    """
    Get public contributors to a GitHub repository.

    Args:
        repo_url: Public GitHub repository URL.
    """

    try:

        owner, repo = parse_github_url(repo_url)

        url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/contributors"
        )

        response = requests.get(
            url,
            params={"per_page": 100},
            timeout=10
        )

        if response.status_code != 200:

            return (
                f"Could not access contributors. "
                f"GitHub returned status "
                f"{response.status_code}."
            )

        contributors = response.json()

        if not contributors:

            return (
                "No public contributors "
                "were found."
            )

        result = [
            "=== GITHUB CONTRIBUTORS ==="
        ]

        for contributor in contributors:

            login = contributor.get(
                "login"
            )

            contributions = contributor.get(
                "contributions",
                0
            )

            result.append(
                f"{login} — "
                f"{contributions} contributions"
            )

        return "\n".join(result)

    except Exception as e:

        return (
            f"Error accessing contributors: "
            f"{str(e)}"
        )


# ============================================================
# SEARCH SOURCE CODE / FILES
# ============================================================

@tool
def github_search_code(
    repo_url: str,
    search_term: str
) -> str:
    """
    Search the repository file tree for a filename or path.

    Args:
        repo_url: Public GitHub repository URL.
        search_term: Filename or path text.
    """

    try:

        owner, repo = parse_github_url(repo_url)

        api_base = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}"
        )

        repo_response = requests.get(
            api_base,
            timeout=10
        )

        if repo_response.status_code != 200:

            return (
                "Could not access repository."
            )

        branch = repo_response.json().get(
            "default_branch",
            "main"
        )

        tree_url = (
            f"{api_base}/git/trees/"
            f"{branch}?recursive=1"
        )

        response = requests.get(
            tree_url,
            timeout=15
        )

        if response.status_code != 200:

            return (
                "Could not retrieve repository "
                "file tree."
            )

        tree = response.json().get(
            "tree",
            []
        )

        term = search_term.lower()

        matches = []

        for item in tree:

            path = item.get(
                "path",
                ""
            )

            if term in path.lower():

                matches.append(path)

        if not matches:

            return (
                f"No files or folders matching "
                f"'{search_term}' were found."
            )

        return "\n".join(
            matches[:100]
        )

    except Exception as e:

        return (
            f"Error searching repository: "
            f"{str(e)}"
        )


# ============================================================
# FINAL ANSWER
# ============================================================

final_answer = FinalAnswerTool()


# ============================================================
# LOCAL OLLAMA MODEL
# ============================================================

model = OpenAIServerModel(
    model_id="qwen2.5-coder:7b",

    api_base=(
        "http://localhost:11434/v1"
    ),

    api_key="ollama",

    max_tokens=2048,

    temperature=0.2,
)


# ============================================================
# REPOPILOT AGENT
# ============================================================

agent = CodeAgent(

    model=model,

    tools=[
        final_answer,

        github_repo_overview,
        github_list_files,
        github_read_file,
        github_contributors,
        github_search_code,
    ],

    # Reduced from 4.
    # Simple questions should terminate after
    # one tool call + final answer.
    max_steps=3,

    verbosity_level=1,

    planning_interval=None,

    name="RepoPilot",

    description="""
You are RepoPilot, an AI GitHub repository analysis agent.

Your goal is to answer the user's question using the
SMALLEST number of tool calls possible.

IMPORTANT:

1. When the user provides a GitHub repository URL and asks
   a general question, call github_repo_overview FIRST.

2. github_repo_overview already provides:
   - repository metadata
   - total file count
   - total folder count
   - file structure
   - README

3. If github_repo_overview contains the answer, STOP.
   Do NOT call another tool.

4. For simple factual questions such as:
   - "How many files?"
   - "How many folders?"
   - "What language?"
   - "What is this repo?"
   - "Explain this repo briefly"
   use ONE overview call and answer immediately.

5. NEVER repeat a tool call with the same information.

6. For contributor questions, use github_contributors.

7. For questions about a specific file, use
   github_read_file.

8. For questions about a particular filename or path,
   use github_search_code.

9. Only inspect individual source files when the overview
   cannot answer the question.

10. NEVER explore the entire repository unnecessarily.

11. Do not verify information that has already been returned
   by a tool.

12. Do not make up information.

13. When the user asks for a short explanation, keep it short.

14. When the user asks for a detailed explanation, explain:
   - purpose
   - architecture
   - important files
   - technologies
   - important code
   - how the pieces interact

15. Even for detailed questions, only inspect files relevant
   to the question.

16. Once sufficient information has been collected,
   immediately provide the final answer.

17. Do not use additional steps simply to make the answer
   more detailed.

18. Efficiency is important. Prefer 1 tool call over multiple
   tool calls whenever possible.
"""
)


# ============================================================
# LAUNCH
# ============================================================

if __name__ == "__main__":

    GradioUI(agent).launch(
        share=True
    )