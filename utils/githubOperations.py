import logging
from git import Repo
from github import Github, Auth

logger = logging.getLogger(__name__)

def githubOperations(private: bool, commit_message: str, repository_name: str, target_folder: str):
    # default_commit_message = "Initial commit"
    default_remote = "origin"
    username = "super-sid"
    email = "siddhant.ag7@gmail.com"
    # repository_name = 'babyagi-upload'
    token = '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'
    print('token',token)
    user = Github(token).get_user()
    github_repo = user.create_repo(repository_name, private=private)
    logger.info(f"Repository created: {github_repo.html_url}")
    # initialize the local repository
    default_branch_name = github_repo.default_branch
    git_repo = Repo.init(target_folder, initial_branch=default_branch_name)
    git_repo.config_writer().set_value("user", "name", username).release()
    git_repo.config_writer().set_value("user", "email", email).release()
    # commit files
    git_repo.git.add(A=True)
    git_repo.git.commit(m=commit_message)
    # push changes
    git_repo.create_remote(
        default_remote,
        github_repo.clone_url.replace("https://", f"https://{token}@"),
    )
    git_repo.git.push(default_remote, default_branch_name)
    logger.info("GitHub repository setup complete.")
    return github_repo.html_url
