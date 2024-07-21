#!/bin/bash

# Scripts Vars
PROJECT_DIR="/Users/shreyasbhat/Code/llms/trip_checklist"
VIRTUAL_ENV_PATH="../bin/activate"
FLASK_APP_COMMAND="flask run"
CELERY_WORKER_COMMAND="celery -A app.celery_app worker --loglevel INFO --concurrency 1 --max-tasks-per-child=1"
FLOWER_COMMAND="celery -A app.celery_app flower"

# Create the tmux session.
tmux new-session -d -s my_session

# Split first pane horizontally
tmux split-window -h -t my_session:0.0

# Split left pane vertically
tmux split-window -v -t my_session:0.0

# Send commands to each pane
# Pane 1: Celery Worker
tmux send-keys -t my_session:0.1 "cd $PROJECT_DIR && source $VIRTUAL_ENV_PATH && $CELERY_WORKER_COMMAND" 'C-m'

# Pane 2: Celery Flower
tmux send-keys -t my_session:0.0 "cd $PROJECT_DIR && source $VIRTUAL_ENV_PATH && $FLOWER_COMMAND" 'C-m'

# Pane 3: Flask Server 
# This is now targeted correctly
tmux send-keys -t my_session:0.2 "cd $PROJECT_DIR && source $VIRTUAL_ENV_PATH && $FLASK_APP_COMMAND" 'C-m'

# Attach to the session
tmux attach -t my_session