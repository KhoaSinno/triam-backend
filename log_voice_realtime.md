===== Application Startup at 2026-06-03 02:15:37 =====

Starting realtime voice agent...
Starting Celery document worker...
Starting Celery notification worker...
Starting Celery Beat...
Starting FastAPI on port 7860...
celery beat v5.6.3 (recovery) is starting.
2026-06-03 02:15:58.304 | INFO | app.db.database:create*db_engine:55 - Database engine configured with NullPool.
2026-06-03 02:15:58.367 | INFO | app.db.database:create_db_engine:55 - Database engine configured with NullPool.
2026-06-03 02:15:58.367 | INFO | app.db.database:create_db_engine:55 - Database engine configured with NullPool.
2026-06-03 02:16:06.573 | INFO | app.db.database:create_db_engine:55 - Database engine configured with NullPool.
2026-06-03 02:16:16.695 | INFO | logging:callHandlers:1762 - starting worker
{"message": "starting worker", "level": "INFO", "name": "livekit.agents", "version": "1.5.8", "rtc-version": "1.1.7", "timestamp": "2026-06-03T02:16:16.693840+00:00"}
2026-06-03 02:16:16.696 | INFO | logging:callHandlers:1762 - plugin registered
{"message": "plugin registered", "level": "INFO", "name": "livekit.agents", "plugin": "livekit.plugins.openai", "version": "1.5.8", "timestamp": "2026-06-03T02:16:16.696266+00:00"}
2026-06-03 02:16:16.699 | INFO | logging:callHandlers:1762 - preloading plugins
{"message": "preloading plugins", "level": "INFO", "name": "livekit.agents", "packages": ["livekit.plugins.openai", "av"], "timestamp": "2026-06-03T02:16:16.699371+00:00"}
2026-06-03 02:16:16.766 | INFO | logging:callHandlers:1762 - HTTP server listening on :8081
{"message": "HTTP server listening on :8081", "level": "INFO", "name": "livekit.agents", "timestamp": "2026-06-03T02:16:16.766498+00:00"}
2026-06-03 02:16:16.776 | INFO | logging:callHandlers:1762 - initializing job runner
{"message": "initializing job runner", "level": "INFO", "name": "livekit.agents", "tid": 43, "timestamp": "2026-06-03T02:16:16.776455+00:00"}
2026-06-03 02:16:16.782 | INFO | logging:callHandlers:1762 - job runner initialized
{"message": "job runner initialized", "level": "INFO", "name": "livekit.agents", "tid": 43, "elapsed_time": 0.0, "timestamp": "2026-06-03T02:16:16.781456+00:00"}
2026-06-03 02:16:16.839 | INFO | logging:callHandlers:1762 - registered worker
{"message": "registered worker", "level": "INFO", "name": "livekit.agents", "agent_name": "triam-voice-agent", "id": "AW_McswzXu6tc2y", "url": "wss://tri-am-bmdl413w.livekit.cloud", "region": "US East B", "protocol": 17, "timestamp": "2026-06-03T02:16:16.839346+00:00"}
** - ... ** - *
LocalTime -> 2026-06-03 02:17:15
Configuration ->
. broker -> redis://default:\*\*@account-discrete-respect-17657.db.redis.io:11610//
. loader -> celery.loaders.app.AppLoader
. scheduler -> celery.beat.PersistentScheduler
. db -> celerybeat-schedule
. logfile -> [stderr]@%INFO
. maxinterval -> 5.00 minutes (300s)
[2026-06-03 02:17:15,078: INFO/MainProcess] beat: Starting...

-------------- celery@r-khoasinoo-tri-am-backend-k8p554ed-52446-scpz6 v5.6.3 (recovery)
--- **\*** -----
-- **\*\*\*** ---- Linux-6.12.88-119.157.amzn2023.x86_64-x86_64-with-glibc2.41 2026-06-03 02:17:15

- _\*\* --- _ ---
- \*\* ---------- [config]
- \*\* ---------- .> app: triam:0x7fb134fca510
- ** ---------- .> transport: redis://default:**@account-discrete-respect-17657.db.redis.io:11610//
- \*\* ---------- .> results: disabled://
- **_ --- _ --- .> concurrency: 1 (prefork)
  -- **\***** ---- .> task events: OFF (enable -E to monitor tasks in this worker)
  --- **\*** -----
  -------------- [queues]
  .> maintenance exchange=maintenance(direct) key=maintenance
  .> notification exchange=notification(direct) key=notification

[tasks]
. triam.books.process
. triam.books.switch_mode
. triam.notifications.deliver_due
. triam.notifications.scan_due

-------------- celery@r-khoasinoo-tri-am-backend-k8p554ed-52446-scpz6 v5.6.3 (recovery)
--- **\*** -----
-- **\*\*\*** ---- Linux-6.12.88-119.157.amzn2023.x86_64-x86_64-with-glibc2.41 2026-06-03 02:17:15

- _\*\* --- _ ---
- \*\* ---------- [config]
- \*\* ---------- .> app: triam:0x7f295c16f2f0
- ** ---------- .> transport: redis://default:**@account-discrete-respect-17657.db.redis.io:11610//
- \*\* ---------- .> results: disabled://
- **_ --- _ --- .> concurrency: 1 (prefork)
  -- **\***** ---- .> task events: OFF (enable -E to monitor tasks in this worker)
  --- **\*** -----
  -------------- [queues]
  .> document exchange=document(direct) key=document

[tasks]
. triam.books.process
. triam.books.switch_mode
. triam.notifications.deliver_due
. triam.notifications.scan_due

[2026-06-03 02:17:16,349: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-06-03 02:17:16,599: ERROR/MainProcess] consumer: Cannot connect to redis://default:\*\*@account-discrete-respect-17657.db.redis.io:11610//: max number of clients reached.
Trying again in 2.00 seconds... (1/100)

[2026-06-03 02:17:17,608: ERROR/MainProcess] consumer: Cannot connect to redis://default:\*\*@account-discrete-respect-17657.db.redis.io:11610//: max number of clients reached.
Trying to reconnect...

2026-06-03 02:17:17.803 | INFO | logging:callHandlers:1762 - Started server process [30]
2026-06-03 02:17:17.804 | INFO | logging:callHandlers:1762 - Waiting for application startup.
2026-06-03 02:17:17.805 | INFO | app.main:lifespan:17 - Khởi động hệ thống... (TRIAM)
2026-06-03 02:17:17.806 | INFO | logging:callHandlers:1762 - Application startup complete.
2026-06-03 02:17:17.806 | INFO | logging:callHandlers:1762 - Uvicorn running on http://0.0.0.0:7860 (Press CTRL+C to quit)
[2026-06-03 02:17:18,060: ERROR/MainProcess] consumer: Cannot connect to redis://default:\*\*@account-discrete-respect-17657.db.redis.io:11610//: max number of clients reached.
Trying again in 2.00 seconds... (1/100)

[2026-06-03 02:17:18,363: ERROR/MainProcess] Message Error: Couldn't apply scheduled task scan-due-notifications: max number of clients reached
[' File "/home/user/app/.venv/bin/celery", line 10, in <module>\n sys.exit(main())\n', ' File "/home/user/app/.venv/lib/python3.12/site-packages/celery/__main__.py", line 15, in main\n sys.exit(_main())\n', ' File "/home/user/app/.venv/lib/python3.12/site-packages/celery/bin/celery.py", line 227, in main\n return celery(auto_envvar_prefix="CELERY")\n', ' File "/home/user/app/.venv/lib/python3.12/site-packages/click/core.py", line 1485, in __call__\n return self.main(*args, **kwargs)\n', ' File "/home/user/app/.venv/lib/python3.12/site-packages/click/core.py", line 1406, in main\n rv = self.invoke(ctx)\n', ' File "/home/user/app/.venv/lib/python3.12/site-packages/click/core.py", line 1873, in invoke\n return _process_result(sub_ctx.command.invoke(sub_ctx))\n', ' File "/home/user/app/.venv/lib/python3.12/site-packages/click/core.py", line 1269, in invoke\n return ctx.invoke(self.callback, **ctx.params)\n', ' File "/home/user/app/.venv/lib/python3.12/site-packages/click/core.py", line 824, in invoke\n return callback(*args, **kwargs)\n', ' File "/home/user/app/.venv/lib/python3.12/site-packages/click/decorators.py", line 34, in new_func\n return f(get_current_context(), *args, **kwargs)\n', ' File "/home/user/app/.venv/lib/python3.12/site-packages/celery/bin/base.py", line 158, in caller\n return f(ctx, *args, **kwargs)\n', ' File "/home/user/app/.venv/lib/python3.12/site-packages/celery/bin/beat.py", line 72, in beat\n return beat().run()\n', ' File "/home/user/app/.venv/lib/python3.12/site-packages/celery/apps/beat.py", line 84, in run\n self.start_scheduler()\n', ' File "/home/user/app/.venv/lib/python3.12/site-packages/celery/apps/beat.py", line 113, in start_scheduler\n service.start()\n', ' File "/home/user/app/.venv/lib/python3.12/site-packages/celery/beat.py", line 645, in start\n interval = self.scheduler.tick()\n', ' File "/home/user/app/.venv/lib/python3.12/site-packages/celery/beat.py", line 355, in tick\n self.apply_entry(entry, producer=self.producer)\n', ' File "/home/user/app/.venv/lib/python3.12/site-packages/celery/beat.py", line 285, in apply_entry\n exc, traceback.format_stack(), exc_info=True)\n']
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/connection.py", line 474, in \_reraise_as_library_errors
yield
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/connection.py", line 558, in \_ensured
return fun(*args, \*\*kwargs)
^^^^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/common.py", line 155, in \_maybe_declare
entity.declare(channel=channel)
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/entity.py", line 617, in declare
self.\_create_queue(nowait=nowait, channel=channel)
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/entity.py", line 626, in \_create_queue
self.queue_declare(nowait=nowait, passive=False, channel=channel)
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/entity.py", line 655, in queue_declare
ret = channel.queue_declare(
^^^^^^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/transport/virtual/base.py", line 538, in queue_declare
return queue_declare_ok_t(queue, self.\_size(queue), 0)
^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/transport/redis.py", line 1020, in \_size
sizes = pipe.execute()
^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/redis/client.py", line 1603, in execute
conn = self.connection_pool.get_connection()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/redis/utils.py", line 195, in wrapper
return func(*args, \*\*kwargs)
^^^^^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/redis/connection.py", line 1533, in get_connection
connection.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/redis/connection.py", line 380, in connect
self.connect_check_health(check_health=True)
File "/home/user/app/.venv/lib/python3.12/site-packages/redis/connection.py", line 403, in connect_check_health
self.on_connect_check_health(check_health=check_health)
File "/home/user/app/.venv/lib/python3.12/site-packages/redis/connection.py", line 475, in on_connect_check_health
auth_response = self.read_response()
^^^^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/redis/connection.py", line 650, in read_response
response = self.\_parser.read_response(disable_decoding=disable_decoding)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/redis/\_parsers/resp2.py", line 15, in read_response
result = self.\_read_response(disable_decoding=disable_decoding)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/redis/\_parsers/resp2.py", line 38, in \_read_response
raise error
redis.exceptions.ConnectionError: max number of clients reached

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/celery/beat.py", line 404, in apply_async
return task.apply_async(entry_args, entry_kwargs,
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/celery/app/task.py", line 627, in apply_async
return app.send_task(
^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/celery/app/base.py", line 969, in send_task
amqp.send_task_message(P, name, message, **options)
File "/home/user/app/.venv/lib/python3.12/site-packages/celery/app/amqp.py", line 559, in send_task_message
ret = producer.publish(
^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/messaging.py", line 190, in publish
return \_publish(
^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/connection.py", line 558, in \_ensured
return fun(\*args, **kwargs)
^^^^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/messaging.py", line 208, in \_publish
maybe_declare(entity, retry=retry, **retry_policy)
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/messaging.py", line 107, in maybe_declare
return maybe_declare(entity, self.channel, retry, **retry_policy)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/common.py", line 112, in maybe_declare
return \_imaybe_declare(entity, channel, \*\*retry_policy)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/common.py", line 169, in \_imaybe_declare
return entity.channel.connection.client.ensure(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/connection.py", line 555, in \_ensured
with self.\_reraise_as_library_errors():
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/local/lib/python3.12/contextlib.py", line 158, in **exit**
self.gen.throw(value)
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/connection.py", line 478, in \_reraise_as_library_errors
raise ConnectionError(str(exc)) from exc
kombu.exceptions.OperationalError: max number of clients reached

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/celery/beat.py", line 282, in apply_entry
result = self.apply_async(entry, producer=producer, advance=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/celery/beat.py", line 412, in apply_async
reraise(SchedulingError, SchedulingError(
File "/home/user/app/.venv/lib/python3.12/site-packages/celery/exceptions.py", line 109, in reraise
raise value.with_traceback(tb)
File "/home/user/app/.venv/lib/python3.12/site-packages/celery/beat.py", line 404, in apply_async
return task.apply_async(entry_args, entry_kwargs,
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/celery/app/task.py", line 627, in apply_async
return app.send_task(
^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/celery/app/base.py", line 969, in send_task
amqp.send_task_message(P, name, message, **options)
File "/home/user/app/.venv/lib/python3.12/site-packages/celery/app/amqp.py", line 559, in send_task_message
ret = producer.publish(
^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/messaging.py", line 190, in publish
return \_publish(
^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/connection.py", line 558, in \_ensured
return fun(\*args, **kwargs)
^^^^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/messaging.py", line 208, in \_publish
maybe_declare(entity, retry=retry, **retry_policy)
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/messaging.py", line 107, in maybe_declare
return maybe_declare(entity, self.channel, retry, **retry_policy)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/common.py", line 112, in maybe_declare
return \_imaybe_declare(entity, channel, **retry_policy)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/common.py", line 169, in \_imaybe_declare
return entity.channel.connection.client.ensure(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/connection.py", line 555, in \_ensured
with self.\_reraise_as_library_errors():
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/local/lib/python3.12/contextlib.py", line 158, in **exit**
self.gen.throw(value)
File "/home/user/app/.venv/lib/python3.12/site-packages/kombu/connection.py", line 478, in \_reraise_as_library_errors
raise ConnectionError(str(exc)) from exc
celery.beat.SchedulingError: Couldn't apply scheduled task scan-due-notifications: max number of clients reached
[2026-06-03 02:17:19,042: ERROR/MainProcess] consumer: Cannot connect to redis://default:**@account-discrete-respect-17657.db.redis.io:11610//: max number of clients reached.
Trying again in 4.00 seconds... (2/100)

[2026-06-03 02:17:20,494: ERROR/MainProcess] consumer: Cannot connect to redis://default:\*\*@account-discrete-respect-17657.db.redis.io:11610//: max number of clients reached.
Trying again in 4.00 seconds... (2/100)

[2026-06-03 02:17:23,486: ERROR/MainProcess] consumer: Cannot connect to redis://default:\*\*@account-discrete-respect-17657.db.redis.io:11610//: max number of clients reached.
Trying again in 6.00 seconds... (3/100)

[2026-06-03 02:17:24,943: ERROR/MainProcess] consumer: Cannot connect to redis://default:\*\*@account-discrete-respect-17657.db.redis.io:11610//: max number of clients reached.
Trying again in 6.00 seconds... (3/100)

[2026-06-03 02:17:32,134: INFO/MainProcess] Connected to redis://default:**@account-discrete-respect-17657.db.redis.io:11610//
[2026-06-03 02:17:33,618: INFO/MainProcess] Connected to redis://default:**@account-discrete-respect-17657.db.redis.io:11610//
[2026-06-03 02:17:34,269: INFO/MainProcess] mingle: searching for neighbors
[2026-06-03 02:17:34,767: INFO/MainProcess] mingle: searching for neighbors
[2026-06-03 02:17:38,596: INFO/MainProcess] mingle: all alone
[2026-06-03 02:17:39,037: INFO/MainProcess] mingle: all alone
[2026-06-03 02:17:44,328: INFO/MainProcess] celery@r-khoasinoo-tri-am-backend-k8p554ed-52446-scpz6 ready.
[2026-06-03 02:17:45,470: INFO/MainProcess] celery@r-khoasinoo-tri-am-backend-k8p554ed-52446-scpz6 ready.
[2026-06-03 02:18:15,201: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-06-03 02:18:18,249: INFO/MainProcess] Task triam.notifications.scan_due[a089553f-4498-4854-bee4-5e9edf7f2480] received
2026-06-03 02:18:27.651 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-06-03 02:18:27,654: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a089553f-4498-4854-bee4-5e9edf7f2480] succeeded in 9.402381742009311s: None
[2026-06-03 02:19:15,201: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-06-03 02:19:15,855: INFO/MainProcess] Task triam.notifications.scan_due[714da3cb-8d44-4b16-b9bb-44c72c65a499] received
2026-06-03 02:19:22.974 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-06-03 02:19:22,975: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[714da3cb-8d44-4b16-b9bb-44c72c65a499] succeeded in 7.11656267401122s: None
[2026-06-03 02:20:15,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-06-03 02:20:16,077: INFO/MainProcess] Task triam.notifications.scan_due[28df4fc1-d1d7-43b4-8343-0121fd317927] received
2026-06-03 02:20:23.375 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-06-03 02:20:23,376: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[28df4fc1-d1d7-43b4-8343-0121fd317927] succeeded in 7.2981908329966245s: None
[2026-06-03 02:21:15,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-06-03 02:21:15,850: INFO/MainProcess] Task triam.notifications.scan_due[b0e3e37d-a1a4-425c-8f6c-9fbbf5c9bb61] received
2026-06-03 02:21:22.972 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-06-03 02:21:22,973: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b0e3e37d-a1a4-425c-8f6c-9fbbf5c9bb61] succeeded in 7.122448876005365s: None
[2026-06-03 02:22:15,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-06-03 02:22:16,072: INFO/MainProcess] Task triam.notifications.scan_due[cd65e38a-846c-4da4-981f-a6b85242133e] received
2026-06-03 02:22:23.236 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-06-03 02:22:23,238: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[cd65e38a-846c-4da4-981f-a6b85242133e] succeeded in 7.165029394993326s: None
[2026-06-03 02:23:15,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-06-03 02:23:16,073: INFO/MainProcess] Task triam.notifications.scan_due[560445e7-3561-45e1-bef3-714099c80522] received
2026-06-03 02:23:23.267 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-06-03 02:23:23,268: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[560445e7-3561-45e1-bef3-714099c80522] succeeded in 7.194298041998991s: None
[2026-06-03 02:24:15,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-06-03 02:24:15,850: INFO/MainProcess] Task triam.notifications.scan_due[e0b6d289-0ce8-4472-9eb9-4572c54e8093] received
2026-06-03 02:24:22.824 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-06-03 02:24:22,825: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e0b6d289-0ce8-4472-9eb9-4572c54e8093] succeeded in 6.973208519004402s: None
2026-06-03 02:25:03.383 | INFO | logging:callHandlers:1762 - 10.16.17.88:51561 - "GET /api/v1/books/9e66b856-acaa-47d8-a26e-647918492117 HTTP/1.1" 200
2026-06-03 02:25:07.438 | INFO | logging:callHandlers:1762 - 10.16.3.80:12858 - "GET /api/v1/books/9e66b856-acaa-47d8-a26e-647918492117/details?mode=full HTTP/1.1" 200
[2026-06-03 02:25:15,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-06-03 02:25:16,074: INFO/MainProcess] Task triam.notifications.scan_due[9a56ee44-ef7f-4be1-9cd6-ac7ecdc62f2a] received
2026-06-03 02:25:23.364 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-06-03 02:25:23,365: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[9a56ee44-ef7f-4be1-9cd6-ac7ecdc62f2a] succeeded in 7.290984125997056s: None
2026-06-03 02:25:30.059 | INFO | logging:callHandlers:1762 - 10.16.25.26:20904 - "GET /api/v1/books/9e66b856-acaa-47d8-a26e-647918492117/details?mode=full HTTP/1.1" 200
2026-06-03 02:25:33.985 | INFO | logging:callHandlers:1762 - 10.16.17.88:61277 - "GET /api/v1/books/9e66b856-acaa-47d8-a26e-647918492117/learning-progress?mode=pareto HTTP/1.1" 200
2026-06-03 02:25:36.669 | INFO | logging:callHandlers:1762 - 10.16.17.88:61277 - "GET /api/v1/books/9e66b856-acaa-47d8-a26e-647918492117/details?mode=full HTTP/1.1" 200
2026-06-03 02:25:57.559 | INFO | logging:callHandlers:1762 - 10.16.37.205:6219 - "GET /api/v1/threads/for-book/9e66b856-acaa-47d8-a26e-647918492117 HTTP/1.1" 200
2026-06-03 02:26:01.813 | INFO | logging:callHandlers:1762 - 10.16.25.26:20622 - "GET /api/v1/live-token/thread/c9c950e0-10c4-4012-9d70-8430e6ed7975 HTTP/1.1" 200
2026-06-03 02:26:03.415 | INFO | logging:callHandlers:1762 - received job request
{"message": "received job request", "level": "INFO", "name": "livekit.agents", "job_id": "AJ_pXDaYm5vuZU6", "dispatch_id": "AD_Sn9wmpR5ZPpr", "room": "triam_c9c950e0_b3e26c", "room_id": "RM_H9yH7QhP2WpF", "agent_name": "triam-voice-agent", "resuming": false, "enable_recording": false, "timestamp": "2026-06-03T02:26:03.415435+00:00"}
2026-06-03 02:26:03.509 | INFO | logging:callHandlers:1762 - initializing job runner
{"message": "initializing job runner", "level": "INFO", "name": "livekit.agents", "tid": 60, "timestamp": "2026-06-03T02:26:03.508941+00:00"}
2026-06-03 02:26:03.513 | INFO | logging:callHandlers:1762 - job runner initialized
{"message": "job runner initialized", "level": "INFO", "name": "livekit.agents", "tid": 60, "elapsed_time": 0.0, "timestamp": "2026-06-03T02:26:03.513389+00:00"}
2026-06-03 02:26:03.755 | INFO | **main**:entrypoint:304 - ✅ Document IDs từ metadata: ['9e66b856-acaa-47d8-a26e-647918492117']
2026-06-03 02:26:03.757 | INFO | **main**:entrypoint:305 - 🏠 Room Name (session): triam_c9c950e0_b3e26c
2026-06-03 02:26:03.759 | INFO | **main**:entrypoint:306 - Bat dau phien doc sach cho Thread ID: c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:26:03.793 | INFO | **main**:entrypoint:591 - Starting realtime session with model: gpt-realtime, voice: cedar
2026-06-03 02:26:10.248 | INFO | **main**:flush:185 - Text output flushed | chars=128 | topic=lk.chat
[2026-06-03 02:26:15,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-06-03 02:26:15,852: INFO/MainProcess] Task triam.notifications.scan_due[bad690ec-5e8a-4f0d-a327-9c1f97489dc6] received
2026-06-03 02:26:15.967 | INFO | **main**:\_handle_conversation_item_added:575 - Assistant voice speech saved | text_len=128 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:26:22.927 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-06-03 02:26:22,929: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[bad690ec-5e8a-4f0d-a327-9c1f97489dc6] succeeded in 7.074558699998306s: None
2026-06-03 02:26:59.385 | INFO | **main**:\_handle_user_input_transcribed:555 - user_input_transcribed received | final=False | chars=0 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:26:59.814 | INFO | **main**:\_handle_user_input_transcribed:555 - user_input_transcribed received | final=True | chars=4 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:26:59.815 | INFO | **main**:\_handle_conversation_item_added:571 - User voice speech saved | text_len=4 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:27:00.942 | INFO | **main**:flush:185 - Text output flushed | chars=75 | topic=lk.chat
2026-06-03 02:27:04.382 | INFO | **main**:\_handle_conversation_item_added:575 - Assistant voice speech saved | text_len=75 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:27:11.721 | INFO | **main**:\_handle_user_input_transcribed:555 - user_input_transcribed received | final=False | chars=0 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:27:13.255 | INFO | **main**:\_handle_user_input_transcribed:555 - user_input_transcribed received | final=True | chars=34 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:27:13.258 | INFO | **main**:\_handle_conversation_item_added:571 - User voice speech saved | text_len=34 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
[2026-06-03 02:27:15,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-06-03 02:27:16,072: INFO/MainProcess] Task triam.notifications.scan_due[4ff6c844-78d3-4463-b21f-b42871ad2e93] received
2026-06-03 02:27:22.452 | INFO | **main**:flush:185 - Text output flushed | chars=355 | topic=lk.chat
2026-06-03 02:27:23.229 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-06-03 02:27:23,232: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4ff6c844-78d3-4463-b21f-b42871ad2e93] succeeded in 7.158925103998627s: None
2026-06-03 02:27:38.205 | INFO | **main**:\_handle_conversation_item_added:575 - Assistant voice speech saved | text_len=355 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:27:41.402 | INFO | **main**:\_handle_user_input_transcribed:555 - user_input_transcribed received | final=False | chars=0 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:27:42.555 | INFO | **main**:\_handle_user_input_transcribed:555 - user_input_transcribed received | final=True | chars=33 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:27:42.559 | INFO | **main**:\_handle_conversation_item_added:571 - User voice speech saved | text_len=33 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:27:45.194 | INFO | **main**:flush:185 - Text output flushed | chars=240 | topic=lk.chat
2026-06-03 02:27:52.835 | INFO | **main**:\_handle_conversation_item_added:575 - Assistant voice speech saved | text_len=240 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:27:57.819 | INFO | **main**:\_handle_user_input_transcribed:555 - user_input_transcribed received | final=False | chars=0 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:27:58.801 | INFO | **main**:\_handle_user_input_transcribed:555 - user_input_transcribed received | final=True | chars=10 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:27:58.805 | INFO | **main**:\_handle_conversation_item_added:571 - User voice speech saved | text_len=10 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:28:00.015 | INFO | **main**:flush:185 - Text output flushed | chars=129 | topic=lk.chat
2026-06-03 02:28:05.537 | INFO | **main**:\_handle_conversation_item_added:575 - Assistant voice speech saved | text_len=129 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
[2026-06-03 02:28:15,204: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-06-03 02:28:15.312 | INFO | **main**:\_handle_user_input_transcribed:555 - user_input_transcribed received | final=False | chars=0 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:28:16.009 | INFO | **main**:ask_web_search_permission:289 - Voice web search permission requested | query_chars=25
2026-06-03 02:28:16.010 | INFO | app.services.voice_agent.web_permission_policy:request_permission:95 - Voice web permission requested | request_id=c4db78d7-b94b-438a-af9e-89de0571a5ae | query_chars=25
[2026-06-03 02:28:16,073: INFO/MainProcess] Task triam.notifications.scan_due[5672e94e-3d21-4a46-bfc5-cb5b6abf9c6d] received
2026-06-03 02:28:16.957 | INFO | **main**:\_handle_user_input_transcribed:555 - user_input_transcribed received | final=True | chars=49 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:28:16.961 | INFO | **main**:\_handle_conversation_item_added:571 - User voice speech saved | text_len=49 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:28:18.077 | INFO | **main**:flush:185 - Text output flushed | chars=112 | topic=lk.chat
2026-06-03 02:28:22.861 | INFO | **main**:\_handle_conversation_item_added:575 - Assistant voice speech saved | text_len=112 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:28:23.545 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-06-03 02:28:23,548: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5672e94e-3d21-4a46-bfc5-cb5b6abf9c6d] succeeded in 7.250078561002738s: None
2026-06-03 02:28:25.475 | INFO | **main**:\_handle_user_input_transcribed:555 - user_input_transcribed received | final=False | chars=0 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:28:25.933 | INFO | **main**:\_handle_user_input_transcribed:555 - user_input_transcribed received | final=True | chars=8 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:28:25.934 | INFO | **main**:\_handle_conversation_item_added:571 - User voice speech saved | text_len=8 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:28:26.290 | INFO | app.services.voice_agent.web_permission_policy:\_classify_reply:125 - Voice web permission intent classified | mode=pending | request_id=c4db78d7-b94b-438a-af9e-89de0571a5ae | intent=grant | confidence=0.94 | source=fast_path
2026-06-03 02:28:26.297 | INFO | **main**:execute_web_search:269 - Voice web search executing | query_chars=25
2026-06-03 02:28:26.297 | INFO | app.services.web_search_service:search_web:25 - Web Search (Tavily): thời tiết Cần Thơ hôm nay
2026-06-03 02:28:29.332 | INFO | **main**:flush:185 - Text output flushed | chars=105 | topic=lk.chat
2026-06-03 02:28:34.876 | INFO | **main**:\_handle_conversation_item_added:575 - Assistant voice speech saved | text_len=105 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:28:43.215 | INFO | **main**:\_handle_user_input_transcribed:555 - user_input_transcribed received | final=False | chars=0 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:28:44.442 | INFO | **main**:\_handle_user_input_transcribed:555 - user_input_transcribed received | final=True | chars=50 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:28:44.443 | INFO | **main**:\_handle_conversation_item_added:571 - User voice speech saved | text_len=50 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:28:46.190 | INFO | **main**:\_handle_user_input_transcribed:555 - user_input_transcribed received | final=False | chars=0 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:28:46.781 | INFO | **main**:\_handle_user_input_transcribed:555 - user_input_transcribed received | final=True | chars=15 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:28:46.783 | INFO | **main**:\_handle_conversation_item_added:571 - User voice speech saved | text_len=15 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:28:49.246 | INFO | **main**:flush:185 - Text output flushed | chars=198 | topic=lk.chat
2026-06-03 02:28:57.489 | INFO | **main**:\_handle_conversation_item_added:575 - Assistant voice speech saved | text_len=198 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:29:01.877 | INFO | **main**:\_handle_user_input_transcribed:555 - user_input_transcribed received | final=False | chars=0 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:29:02.329 | INFO | **main**:\_handle_user_input_transcribed:555 - user_input_transcribed received | final=True | chars=25 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:29:02.330 | INFO | **main**:\_handle_conversation_item_added:571 - User voice speech saved | text_len=25 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
2026-06-03 02:29:02.827 | INFO | app.services.voice_agent.web_permission_policy:\_classify_reply:125 - Voice web permission intent classified | mode=implicit | request_id=None | intent=grant | confidence=0.96 | source=fast_path
2026-06-03 02:29:02.828 | INFO | **main**:execute_web_search:269 - Voice web search executing | query_chars=54
2026-06-03 02:29:02.829 | INFO | app.services.web_search_service:search_web:25 - Web Search (Tavily): dự báo phần trăm mưa ở quận Ninh Kiều, Cần Thơ hôm nay
2026-06-03 02:29:06.839 | INFO | **main**:flush:185 - Text output flushed | chars=143 | topic=lk.chat
[2026-06-03 02:29:15,204: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-06-03 02:29:15.360 | INFO | **main**:\_handle_conversation_item_added:575 - Assistant voice speech saved | text_len=143 | thread_id=c9c950e0-10c4-4012-9d70-8430e6ed7975
[2026-06-03 02:29:15,853: INFO/MainProcess] Task triam.notifications.scan_due[971bb564-226d-4a62-b11a-12d30287aaa4] received
2026-06-03 02:29:20.885 | INFO | logging:callHandlers:1762 - closing agent session due to participant disconnect (disable via `RoomInputOptions.close_on_disconnect=False`)
{"message": "closing agent session due to participant disconnect (disable via `RoomInputOptions.close_on_disconnect=False`)", "level": "INFO", "name": "livekit.agents", "room": "triam_c9c950e0_b3e26c", "participant": "user_c4213e", "reason": "CLIENT_INITIATED", "timestamp": "2026-06-03T02:29:20.884812+00:00"}
2026-06-03 02:29:22.962 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-06-03 02:29:22,963: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[971bb564-226d-4a62-b11a-12d30287aaa4] succeeded in 7.10913938099111s: None
2026-06-03 02:29:31.926 | INFO | logging:callHandlers:1762 - 10.16.25.26:39679 - "GET /api/v1/books/9e66b856-acaa-47d8-a26e-647918492117/details?mode=full HTTP/1.1" 200
[2026-06-03 02:30:15,207: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-06-03 02:30:16,079: INFO/MainProcess] Task triam.notifications.scan_due[43b67b22-3f54-4d64-9a87-279256bbea57] received
