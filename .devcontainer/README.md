# DevContainer Setup Guide

This project supports multiple workflows for using the development container with Antigravity/VS Code.

> **Note:** The Dockerfile is located at `../docker/Dockerfile.dev`

## 🚀 Workflow Options

### Option 1: Standard DevContainer (Recommended for Beginners)

VS Code automatically builds and manages the container.

**Steps:**
1. Open the project in VS Code
2. Click "Reopen in Container" when prompted
   - Or use Command Palette (`Cmd+Shift+P`) → "Dev Containers: Reopen in Container"
3. VS Code builds the container and connects automatically

**Pros:** Simple, automatic
**Cons:** Container is recreated each time you reopen

---

### Option 2: Docker Compose + Attach (Recommended for Persistent Development)

Run the container independently, then connect from Antigravity.

**Steps:**

1. **Start the container:**
   ```bash
   cd .devcontainer
   docker-compose up -d
   ```

2. **Connect from Antigravity/VS Code:**
   - Command Palette (`Cmd+Shift+P`) → "Dev Containers: Attach to Running Container"
   - Select `ai-business-assistant-dev`

3. **Stop the container when done:**
   ```bash
   docker-compose down
   ```

**Pros:** 
- Container stays running between sessions
- Faster reconnection
- Can manage container independently
- Better for long-running processes

**Cons:** 
- Requires manual container management

---

### Option 3: Manual Docker Run + Attach

Full control over container lifecycle.

**Steps:**

1. **Build the image:**
   ```bash
   docker build -t ai-business-assistant:latest -f docker/Dockerfile.dev .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     --name ai-business-assistant-dev \
     --hostname ai-business-assistant \
     -v "${PWD}:/home/builduser/APP:cached" \
     -v "${HOME}/.ssh:/home/builduser/.ssh:ro" \
     -v "${HOME}/.gitconfig:/home/builduser/.gitconfig:ro" \
     -p 8000:8000 \
     -p 8080:8080 \
     -p 8888:8888 \
     -p 5000:5000 \
     -e PYTHONUNBUFFERED=1 \
     -e PYTHONDONTWRITEBYTECODE=1 \
     --user builduser \
     ai-business-assistant:latest \
     sleep infinity
   ```

3. **Connect from Antigravity:**
   - Command Palette → "Dev Containers: Attach to Running Container"
   - Select `ai-business-assistant-dev`

4. **Manage the container:**
   ```bash
   # Stop
   docker stop ai-business-assistant-dev
   
   # Start again
   docker start ai-business-assistant-dev
   
   # Remove
   docker rm -f ai-business-assistant-dev
   ```

**Pros:** Maximum flexibility
**Cons:** Most manual setup

---

## 🔧 Container Management Commands

### Check if container is running:
```bash
docker ps | grep ai-business-assistant
```

### View container logs:
```bash
docker logs ai-business-assistant-dev
```

### Execute commands in running container:
```bash
docker exec -it ai-business-assistant-dev bash
```

### Restart container:
```bash
docker restart ai-business-assistant-dev
```

---

## 🎨 Customizing Container Name

### For Docker Compose (Option 2):

**Method 1: Using .env file (Recommended)**
```bash
# Create .env file in .devcontainer directory
cp .env.example .env

# Edit .env and change the values:
CONTAINER_NAME=my-custom-name
HOSTNAME=my-hostname
```

**Method 2: Inline environment variable**
```bash
CONTAINER_NAME=my-custom-name docker-compose up -d
```

**Method 3: Edit docker-compose.yml directly**
Change line 14:
```yaml
container_name: my-custom-name
```

### For DevContainer (Option 1):

Edit `devcontainer.json` line 150:
```json
"runArgs": [
  "--name=my-custom-name",
  "--hostname=my-hostname"
],
```

### For Manual Docker Run (Option 3):

Change the `--name` flag in the docker run command:
```bash
docker run -d --name my-custom-name ...
```

---

## 📝 Notes

- **Workspace Location:** `/home/builduser/APP` inside container
- **User:** `builduser` (UID: 20001)
- **Ports Exposed:** 8000, 8080, 8888, 5000
- **SSH/Git:** Automatically mounted from your host machine

## 🎯 Recommended Workflow

For **Antigravity users**, I recommend **Option 2 (Docker Compose)** because:
- Container persists between sessions
- Quick reconnection
- Easy to manage with `docker-compose up/down`
- All configuration in one place
