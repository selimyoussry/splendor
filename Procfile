web: gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker module:app
init: python db_create.py
upgrade: python db_upgrade.py
