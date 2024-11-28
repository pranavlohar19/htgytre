
import subprocess
import sys
import os

# Use environment variables for sensitive data
DEV_TOKEN = os.getenv("GITHUB_TOKEN")
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
    try:
        # Check current config
        current_username = run_command(["git", "config",  "--get", "user.name"], "")
        current_email = run_command(["git", "config",  "--get", "user.email"], "")

        # Prompt for overrides
        if not current_username or current_username != USERNAME:
            print(f"Updating Git user.name to {USERNAME}...")
            run_command(["git", "config",  "user.name", USERNAME], "Failed to set user.name.")
        
        if not current_email or current_email != EMAIL:
            print(f"Updating Git user.email to {EMAIL}...")
            run_command(["git", "config",  "user.email", EMAIL], "Failed to set user.email.")

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
    run_command(["git", "commit", "-m", f"{message}"], f"Error committing changes. Message: {message}")

def git_push(branch):
    """Push changes to the remote repository using the token."""
    if not DEV_TOKEN:
        print("Developer token not set. Set the GITHUB_TOKEN environment variable.")
        sys.exit(1)
    
    remote_url = run_command(["git", "remote", "get-url", "origin"], "Error fetching remote URL.")
    if "https://" in remote_url:
        auth_url = remote_url.replace("https://", f"https://{DEV_TOKEN}@")
        # first take pull to update the local repo
        run_command(["git", "pull", auth_url, branch], f"Error pulling changes from branch '{branch}' using token.")
        run_command(["git", "push", auth_url, branch], f"Error pushing changes to branch '{branch}' using token.")
    else:
        run_command(["git", "push", "origin", branch], f"Error pushing changes to branch '{branch}'.")

# Other functions remain unchanged

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
