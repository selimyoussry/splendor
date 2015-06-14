web: gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker --log-file=- server:app
init: python db_create.py
upgrade: python db_upgrade.py
