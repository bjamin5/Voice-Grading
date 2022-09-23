# from constants import CONF


# def when_ready(server):
#     GunicornPrometheusMetrics.start_http_server_when_ready(int(CONF["ports"]["metrics"]) if CONF.get("ports").get("metrics") is not None else 8081)


# def child_exit(server, worker):
#     GunicornPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)


# THESE HAVE TO BE LOWERCASE EVEN THOUGH CONSTANTS ARE USUALLY CAPITALIZED IN PYTHON see docs for variable names https://docs.gunicorn.org/en/stable/settings.html#logging
# bind = f'0.0.0.0:{CONF["ports"]["app"]}'
# accesslog = CONF["accessLog"]
# access_log_format = CONF['formatters']['accessLog']['format']
# workers = CONF["workers"]
# loglevel = CONF["logLevel"]
# worker_tmp_dir = CONF["workerTempDirectory"]
# worker_class = CONF['workerClass']
# logconfig_dict = CONF
# timeout = 60 if the process takes a long time to start up. Default timeout for gunicorn workers is 30 seconds.
