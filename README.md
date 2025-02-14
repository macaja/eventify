
# Eventify

Eventify is a playground repository that recommends events based on the music you like. This project integrates Spotify data to suggest relevant local events.

## Setup

### 1. **Create and Activate Virtual Environment**

Run the following commands to create a virtual environment and install the required dependencies:

```bash
chmod +x setup_venv.sh   # Make the setup script executable
./setup_venv.sh           # Run the setup script
```

After running the script, your terminal prompt should change to indicate that the virtual environment is active, like this:

```
(venv) <user>@machine
```

### 2. **Run the Application**

Once you're in the virtual environment, start the application with:

```bash
python3 app.py
```

This will launch the Eventify app, which will use your music preferences to recommend events near you.

## Notes

- If you need to add more dependencies, you can either modify the `setup_venv.sh` script or manually install them within the virtual environment.
- Feel free to customize the project and get creative with the recommendation logic!
