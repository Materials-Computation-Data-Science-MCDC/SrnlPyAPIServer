# Define the Python version and virtual environment name
PYTHON_VERSION = 3.11.0  # Replace with the desired Python version
VENV_NAME = SrnlPyAPIServerVenv  # Replace with the desired virtualenv name

# Docker settings
IMAGE_NAME=srnlpyapiserverapp  # Replace with your desired Docker image name
DOCKER_TAG=latest  # Replace with your desired Docker tag

# Install pip-tools for dependency management
.PHONY: pip-tools-install
pip-tools-install:
	@pip3 install pip-tools

# Install pyenv
.PHONY: pyenv-install
pyenv-install:
	@if ! command -v pyenv >/dev/null 2>&1; then \
		echo "Installing pyenv..."; \
		curl https://pyenv.run | bash; \
		export PATH="$${HOME}/.pyenv/bin:$${PATH}"; \
		eval "$$(pyenv init --path)"; \
		eval "$$(pyenv init -)"; \
		eval "$$(pyenv virtualenv-init -)"; \
	else \
		echo "pyenv already installed."; \
	fi

# Install pyenv-virtualenv
.PHONY: pyenv-virtualenv-install
pyenv-virtualenv-install:
	@if [ ! -d "$${HOME}/.pyenv/plugins/pyenv-virtualenv" ]; then \
		echo "Installing pyenv-virtualenv..."; \
		git clone https://github.com/pyenv/pyenv-virtualenv.git $${HOME}/.pyenv/plugins/pyenv-virtualenv; \
		echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc; \
		exec "$SHELL"; \
	else \
		echo "pyenv-virtualenv already installed."; \
	fi

# Install a specific Python version using pyenv
.PHONY: pyenv-python-install
pyenv-python-install: pyenv-install
	@if ! pyenv versions --bare | grep -q $(PYTHON_VERSION); then \
		echo "Installing Python $(PYTHON_VERSION)..."; \
		pyenv install $(PYTHON_VERSION); \
	else \
		echo "Python $(PYTHON_VERSION) already installed."; \
	fi

# Create a virtual environment using pyenv-virtualenv
.PHONY: create-virtualenv
create-virtualenv: pyenv-python-install pyenv-virtualenv-install
	@if ! pyenv virtualenvs --bare | grep -q $(VENV_NAME); then \
		echo "Creating virtualenv $(VENV_NAME)..."; \
		pyenv virtualenv $(PYTHON_VERSION) $(VENV_NAME); \
	else \
		echo "Virtualenv $(VENV_NAME) already exists."; \
	fi

# Set the local Python version using pyenv
.PHONY: pyenv-local
pyenv-local: create-virtualenv
	@echo "Setting local Python version to $(VENV_NAME)..."
	pyenv local $(VENV_NAME)

# Generate requirements.txt from requirements.in using pip-tools
.PHONY: generate-requirements
generate-requirements: pip-tools-install
	@if [ ! -f requirements.txt ]; then \
		echo "Generating requirements.txt from requirements.in..."; \
		pip-compile requirements.in; \
	else \
		echo "requirements.txt already exists."; \
	fi

# Install dependencies from requirements.txt
.PHONY: deps-install
deps-install: generate-requirements pyenv-local
	@echo "Upgrading setuptools..."
	@pip3 install --upgrade setuptools
	@echo "Installing dependencies from requirements.txt..."
	@pip3 install -r requirements.txt

# Combined installation
.PHONY: install
install: deps-install
	@echo "Installation complete."

# Run the application
.PHONY: run
run:
	@echo "Running the application..."
	@python main.py


# Build Docker image
.PHONY: docker-build
docker-build:
	@echo "Building Docker image $(IMAGE_NAME):$(DOCKER_TAG)..."
	@docker build -t srnlpyapiserverapp:latest .


# Run Docker container
.PHONY: docker-run
docker-run:
	@echo "Running Docker container from image $(IMAGE_NAME):$(DOCKER_TAG)..."
	@docker run -p 8000:8000 --name $(IMAGE_NAME)-container $(IMAGE_NAME):$(DOCKER_TAG)

# Stop Docker container if it exists
.PHONY: docker-stop
docker-stop:
	@echo "Checking if Docker container $(IMAGE_NAME)-container exists..."
	@if docker ps -a --format '{{.Names}}' | grep -w $(IMAGE_NAME)-container >/dev/null 2>&1; then \
		echo "Stopping Docker container $(IMAGE_NAME)-container..."; \
		docker stop $(IMAGE_NAME)-container; \
		echo "Removing Docker container $(IMAGE_NAME)-container..."; \
		docker rm $(IMAGE_NAME)-container; \
	else \
		echo "Docker container $(IMAGE_NAME)-container does not exist."; \
	fi

# Remove Docker image
.PHONY: docker-rm-image
docker-rm-image:
	@echo "Removing Docker image $(IMAGE_NAME):$(DOCKER_TAG)..."
	@docker rmi $(IMAGE_NAME):$(DOCKER_TAG) || true

# Check if Docker is running
.PHONY: docker-check
docker-check:
	@if ! docker info >/dev/null 2>&1; then \
		echo "Docker is not running. Please start Docker."; \
		exit 1; \
	else \
		echo "Docker is running."; \
	fi

# Combined Docker setup
.PHONY: docker
docker: docker-check docker-build docker-stop docker-run
	@echo "Docker build and Docker container setup complete."

# Clean up all Docker artifacts (optional)
.PHONY: docker-clean
docker-clean: docker-stop docker-rm-image
	@echo "Docker cleanup complete."