import subprocess
import sys

EMAIL = "pranav.lohar@skedgroup.in"
USERNAME = "pranavlohar19"
def run_command(command, error_message):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"{error_message}\n{e.stderr}")
        sys.exit(1)

def check_and_set_git_config():
    """Ensure Git is configured with user.name and user.email."""
    breakpoint()
    try:
        run_command(["git", "config", "--global", "user.name", USERNAME], "Failed to set user.name.")
        run_command(["git", "config", "--global", "user.email", EMAIL], "Failed to set user.email.")

    except Exception as e:
        
        print(f"Error checking or setting Git config: {str(e)}")
        sys.exit(1)

def git_add():
    """Add all changes to the staging area."""
    run_command(["git", "add", "--all"], "Error adding files to staging area.")

def git_commit(message):
    """Commit changes with a given message."""
    if not message:
        print("Commit message is required!")
        sys.exit(1)
    run_command(["git", "commit", "-m", message], "Error committing changes.")

def git_push(branch):
    """Push changes to the remote repository."""
    run_command(["git", "push", "origin", branch], f"Error pushing changes to branch '{branch}'.")

def main():
    """Automate Git process with configuration."""
    print("Starting automated Git process...")

    # Step 1: Ensure Git configuration
    check_and_set_git_config()
    # Step 2: Get commit message and branch name
    commit_message = input("Enter commit message: ").strip()
    if not commit_message:
        print("Commit message cannot be empty.")
        sys.exit(1)

    branch_name = input("Enter branch name (default: 'main'): ").strip() or "main"

    # Step 3: Automate Git add, commit, and push
    git_add()
    git_commit(commit_message)
    git_push(branch_name)

    print(f"Files successfully pushed to branch '{branch_name}'.")

if __name__ == "__main__":
    main()
