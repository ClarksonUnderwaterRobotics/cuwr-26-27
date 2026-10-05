
## Running the Dev Container (Linux / WSL2)

Follow these steps to set up and launch the development environment using Docker and VS Code on Linux (or Windows with WSL2).

### Prerequisites

1. Docker Engine: Installed and running on your system.
2. VS Code: Installed with the Dev Containers extension.

---

### Step 1: Clone or Move the Repository
Ensure the project directory is located on a native Linux filesystem (e.g., inside `/home/your-user/` or standard `/home/`). 

git clone <repository-url>
cd cuwr-26-27

---

### Step 2: Configure Docker Permissions
To allow VS Code to interact with Docker without `sudo`, ensure your user belongs to the `docker` group and owns the project files.

1. Add your user to the `docker` group:
   sudo usermod -aG docker $USER

2. Apply the new group membership:
   newgrp docker

3. Ensure correct file ownership:
   sudo chown -R $USER:$USER .
   chmod -R 755 .

4. Verify Docker access without `sudo`:
   docker ps
   (If this outputs a container list or empty header without permission errors, you are good to go).

---

### Step 3: Open in VS Code

1. Open the project folder in VS Code:
   code .

2. When prompted by VS Code with "Folder contains a Dev Container configuration file. Reopen in Container?", click Reopen in Container.

   Alternatively:
   - Press `F1` (or `Ctrl+Shift+P`).
   - Select "Dev Containers: Reopen in Container" (or "Dev Containers: Rebuild and Reopen in Container").

3. Wait for Docker to build the image and start the environment. Once completed, your terminal and extensions inside VS Code will be fully configured within the container.