def post_fork_fn(server, worker):
   from psycogreen.gevent import patch_psycopg
   patch_psycopg()
worker_class = "gevent"