===== Application Startup at 2026-05-28 06:04:25 =====

Starting realtime voice agent...
Starting Celery document worker...
Starting Celery notification worker...
Starting Celery Beat...
Starting FastAPI on port 7860...
celery beat v5.6.3 (recovery) is starting.
2026-05-28 06:08:29.133 | INFO | logging:callHandlers:1762 - starting worker
{"message": "starting worker", "level": "INFO", "name": "livekit.agents", "version": "1.5.8", "rtc-version": "1.1.7", "timestamp": "2026-05-28T06:08:29.133415+00:00"}
2026-05-28 06:08:29.134 | INFO | logging:callHandlers:1762 - plugin registered
{"message": "plugin registered", "level": "INFO", "name": "livekit.agents", "plugin": "livekit.plugins.openai", "version": "1.5.8", "timestamp": "2026-05-28T06:08:29.134109+00:00"}
2026-05-28 06:08:29.134 | INFO | logging:callHandlers:1762 - preloading plugins
{"message": "preloading plugins", "level": "INFO", "name": "livekit.agents", "packages": ["livekit.plugins.openai", "av"], "timestamp": "2026-05-28T06:08:29.134717+00:00"}
2026-05-28 06:08:29.229 | INFO | logging:callHandlers:1762 - HTTP server listening on :8081
{"message": "HTTP server listening on :8081", "level": "INFO", "name": "livekit.agents", "timestamp": "2026-05-28T06:08:29.229533+00:00"}
2026-05-28 06:08:29.232 | INFO | logging:callHandlers:1762 - initializing job runner
{"message": "initializing job runner", "level": "INFO", "name": "livekit.agents", "tid": 44, "timestamp": "2026-05-28T06:08:29.232201+00:00"}
2026-05-28 06:08:29.233 | INFO | logging:callHandlers:1762 - job runner initialized
{"message": "job runner initialized", "level": "INFO", "name": "livekit.agents", "tid": 44, "elapsed*time": 0.0, "timestamp": "2026-05-28T06:08:29.233572+00:00"}
2026-05-28 06:08:29.318 | INFO | logging:callHandlers:1762 - registered worker
{"message": "registered worker", "level": "INFO", "name": "livekit.agents", "agent_name": "triam-voice-agent", "id": "AW_P7hrbDStMhcD", "url": "wss://tri-am-bmdl413w.livekit.cloud", "region": "US East B", "protocol": 17, "timestamp": "2026-05-28T06:08:29.318608+00:00"}
** - ... ** - *
LocalTime -> 2026-05-28 06:09:02
Configuration ->
. broker -> redis://default:\*\*@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0
. loader -> celery.loaders.app.AppLoader
. scheduler -> celery.beat.PersistentScheduler
. db -> celerybeat-schedule
. logfile -> [stderr]@%INFO
. maxinterval -> 5.00 minutes (300s)
[2026-05-28 06:09:02,124: INFO/MainProcess] beat: Starting...

-------------- celery@r-khoasinoo-tri-am-backend-ofjmbaz7-c0686-d77hc v5.6.3 (recovery)
--- **\*** -----
-- **\*\*\*** ---- Linux-6.12.79-101.147.amzn2023.x86_64-x86_64-with-glibc2.41 2026-05-28 06:09:02

- _\*\* --- _ ---
- \*\* ---------- [config]
- \*\* ---------- .> app: triam:0x7f785139aa80
- ** ---------- .> transport: redis://default:**@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0
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

-------------- celery@r-khoasinoo-tri-am-backend-ofjmbaz7-c0686-d77hc v5.6.3 (recovery)
--- **\*** -----
-- **\*\*\*** ---- Linux-6.12.79-101.147.amzn2023.x86_64-x86_64-with-glibc2.41 2026-05-28 06:09:02

- _\*\* --- _ ---
- \*\* ---------- [config]
- \*\* ---------- .> app: triam:0x7f04b956de20
- ** ---------- .> transport: redis://default:**@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0
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

2026-05-28 06:09:02.450 | INFO | logging:callHandlers:1762 - Started server process [32]
2026-05-28 06:09:02.450 | INFO | logging:callHandlers:1762 - Waiting for application startup.
2026-05-28 06:09:02.451 | INFO | app.main:lifespan:16 - Khởi động hệ thống... (TRIAM)
2026-05-28 06:09:02.451 | INFO | logging:callHandlers:1762 - Application startup complete.
2026-05-28 06:09:02.452 | INFO | logging:callHandlers:1762 - Uvicorn running on http://0.0.0.0:7860 (Press CTRL+C to quit)
[2026-05-28 06:09:04,978: INFO/MainProcess] Connected to redis://default:**@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0
[2026-05-28 06:09:05,344: INFO/MainProcess] Connected to redis://default:**@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0
[2026-05-28 06:09:05,436: ERROR/MainProcess] consumer: Cannot connect to redis://default:\*\*@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0: max number of clients reached.
Trying again in 2.00 seconds... (1/100)

[2026-05-28 06:09:05,783: ERROR/MainProcess] consumer: Cannot connect to redis://default:\*\*@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0: max number of clients reached.
Trying again in 2.00 seconds... (1/100)

[2026-05-28 06:09:07,863: ERROR/MainProcess] consumer: Cannot connect to redis://default:\*\*@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0: max number of clients reached.
Trying again in 4.00 seconds... (2/100)

[2026-05-28 06:09:08,221: ERROR/MainProcess] consumer: Cannot connect to redis://default:\*\*@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0: max number of clients reached.
Trying again in 4.00 seconds... (2/100)

[2026-05-28 06:09:12,288: ERROR/MainProcess] consumer: Cannot connect to redis://default:\*\*@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0: max number of clients reached.
Trying again in 6.00 seconds... (3/100)

[2026-05-28 06:09:12,674: ERROR/MainProcess] consumer: Cannot connect to redis://default:\*\*@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0: max number of clients reached.
Trying again in 6.00 seconds... (3/100)

[2026-05-28 06:09:19,389: INFO/MainProcess] mingle: searching for neighbors
[2026-05-28 06:09:19,777: INFO/MainProcess] mingle: searching for neighbors
[2026-05-28 06:09:23,690: INFO/MainProcess] mingle: all alone
[2026-05-28 06:09:24,034: INFO/MainProcess] mingle: all alone
[2026-05-28 06:09:30,034: INFO/MainProcess] celery@r-khoasinoo-tri-am-backend-ofjmbaz7-c0686-d77hc ready.
[2026-05-28 06:09:30,861: INFO/MainProcess] celery@r-khoasinoo-tri-am-backend-ofjmbaz7-c0686-d77hc ready.
[2026-05-28 06:10:03,292: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:10:05,351: INFO/MainProcess] Task triam.notifications.scan_due[af30fd6e-f4a1-455d-9457-198fd8966b5c] received
2026-05-28 06:10:15.570 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:10:15,578: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[af30fd6e-f4a1-455d-9457-198fd8966b5c] succeeded in 10.212388067971915s: None
2026-05-28 06:10:26.780 | INFO | logging:callHandlers:1762 - 10.16.40.242:33713 - "GET /?logs=container HTTP/1.1" 200
[2026-05-28 06:11:02,197: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:11:03,028: INFO/MainProcess] Task triam.notifications.scan_due[db4d7f70-80e7-4dcb-a891-d9b81d809e30] received
2026-05-28 06:11:09.818 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:11:09,820: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[db4d7f70-80e7-4dcb-a891-d9b81d809e30] succeeded in 6.790447605773807s: None
[2026-05-28 06:12:02,197: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:12:03,248: INFO/MainProcess] Task triam.notifications.scan_due[54292f7e-8886-4254-88f4-72c67a558e9e] received
2026-05-28 06:12:10.160 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:12:10,161: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[54292f7e-8886-4254-88f4-72c67a558e9e] succeeded in 6.909589137881994s: None
[2026-05-28 06:13:02,197: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:13:03,092: INFO/MainProcess] Task triam.notifications.scan_due[c2f6042d-4d3b-406b-92fe-bf3ea79bda4a] received
2026-05-28 06:13:09.890 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:13:09,891: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c2f6042d-4d3b-406b-92fe-bf3ea79bda4a] succeeded in 6.797447188291699s: None
[2026-05-28 06:14:02,197: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:14:03,092: INFO/MainProcess] Task triam.notifications.scan_due[38e426fd-f12a-4847-b2f6-db2672a8800c] received
2026-05-28 06:14:10.026 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:14:10,026: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[38e426fd-f12a-4847-b2f6-db2672a8800c] succeeded in 6.9322219071909785s: None
[2026-05-28 06:15:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:15:03,250: INFO/MainProcess] Task triam.notifications.scan_due[fc98d4a4-d25b-4008-9691-3641df6543d9] received
2026-05-28 06:15:10.255 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:15:10,257: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[fc98d4a4-d25b-4008-9691-3641df6543d9] succeeded in 6.7932839510031044s: None
[2026-05-28 06:16:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:16:02,881: INFO/MainProcess] Task triam.notifications.scan_due[d129b29b-a05e-4ae6-9dd3-415d807480f3] received
2026-05-28 06:16:09.677 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:16:09,678: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d129b29b-a05e-4ae6-9dd3-415d807480f3] succeeded in 6.795206600800157s: None
[2026-05-28 06:17:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:17:03,095: INFO/MainProcess] Task triam.notifications.scan_due[8c88af0b-ac42-409d-bb80-ba119d7fe49e] received
2026-05-28 06:17:09.891 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:17:09,892: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8c88af0b-ac42-409d-bb80-ba119d7fe49e] succeeded in 6.793804292101413s: None
2026-05-28 06:17:27.472 | INFO | logging:callHandlers:1762 - 10.16.40.242:40149 - "GET /api/v1/health HTTP/1.1" 200
2026-05-28 06:17:34.032 | INFO | logging:callHandlers:1762 - 10.16.3.80:52187 - "GET /api/v1/books HTTP/1.1" 200
2026-05-28 06:17:37.942 | INFO | logging:callHandlers:1762 - 10.16.3.80:52187 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
[2026-05-28 06:18:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:18:02,880: INFO/MainProcess] Task triam.notifications.scan_due[f31a0060-1afc-4716-b7e5-f17d68063db6] received
2026-05-28 06:18:09.694 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:18:09,695: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f31a0060-1afc-4716-b7e5-f17d68063db6] succeeded in 6.813330692239106s: None
[2026-05-28 06:19:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:19:03,101: INFO/MainProcess] Task triam.notifications.scan_due[f365c3bc-658b-47cd-a495-ea3d544aff4f] received
2026-05-28 06:19:10.102 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:19:10,102: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f365c3bc-658b-47cd-a495-ea3d544aff4f] succeeded in 6.787746785674244s: None
[2026-05-28 06:20:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:20:03,095: INFO/MainProcess] Task triam.notifications.scan_due[235261d1-5682-4ce9-9ddb-510995bd607b] received
2026-05-28 06:20:10.098 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:20:10,101: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[235261d1-5682-4ce9-9ddb-510995bd607b] succeeded in 6.792639417108148s: None
[2026-05-28 06:21:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:21:02,879: INFO/MainProcess] Task triam.notifications.scan_due[c7f59b41-aadc-4f89-825c-ff8882ee221e] received
2026-05-28 06:21:09.878 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:21:09,879: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c7f59b41-aadc-4f89-825c-ff8882ee221e] succeeded in 6.787392590194941s: None
[2026-05-28 06:22:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:22:03,294: INFO/MainProcess] Task triam.notifications.scan_due[769f1f11-59b5-456e-8d04-a296264ac75e] received
2026-05-28 06:22:10.094 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:22:10,094: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[769f1f11-59b5-456e-8d04-a296264ac75e] succeeded in 6.798758867196739s: None
[2026-05-28 06:23:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:23:02,878: INFO/MainProcess] Task triam.notifications.scan_due[eeaa8116-1467-42c0-b797-9dbcd0eaed4d] received
2026-05-28 06:23:09.772 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:23:09,772: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[eeaa8116-1467-42c0-b797-9dbcd0eaed4d] succeeded in 6.892187801189721s: None
[2026-05-28 06:24:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:24:03,090: INFO/MainProcess] Task triam.notifications.scan_due[07cbf3a4-7267-45e1-b529-4792e389a659] received
2026-05-28 06:24:09.873 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:24:09,873: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[07cbf3a4-7267-45e1-b529-4792e389a659] succeeded in 6.782318769022822s: None
[2026-05-28 06:25:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:25:03,241: INFO/MainProcess] Task triam.notifications.scan_due[2ecacfdf-af48-4916-bc18-6f89af7b21aa] received
2026-05-28 06:25:10.026 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:25:10,027: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2ecacfdf-af48-4916-bc18-6f89af7b21aa] succeeded in 6.785237507894635s: None
[2026-05-28 06:26:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:26:02,876: INFO/MainProcess] Task triam.notifications.scan_due[06e39236-a7fc-46f6-9065-71c5702add9a] received
2026-05-28 06:26:09.659 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:26:09,659: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[06e39236-a7fc-46f6-9065-71c5702add9a] succeeded in 6.781679209321737s: None
[2026-05-28 06:27:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:27:03,090: INFO/MainProcess] Task triam.notifications.scan_due[2a72cb1b-f793-4c1c-b952-b6df63347ca6] received
2026-05-28 06:27:09.872 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:27:09,872: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2a72cb1b-f793-4c1c-b952-b6df63347ca6] succeeded in 6.781776058021933s: None
[2026-05-28 06:28:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:28:02,876: INFO/MainProcess] Task triam.notifications.scan_due[534ff810-19bf-4acf-b5ed-3247cd445996] received
2026-05-28 06:28:08.008 | INFO | logging:callHandlers:1762 - 10.16.3.80:44447 - "GET / HTTP/1.1" 200
2026-05-28 06:28:09.677 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:28:09,677: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[534ff810-19bf-4acf-b5ed-3247cd445996] succeeded in 6.797402455005795s: None
[2026-05-28 06:29:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:29:03,091: INFO/MainProcess] Task triam.notifications.scan_due[030995de-cd93-4fd0-ac7e-931b7ce547ce] received
2026-05-28 06:29:09.876 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:29:09,878: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[030995de-cd93-4fd0-ac7e-931b7ce547ce] succeeded in 6.785682723857462s: None
[2026-05-28 06:30:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:30:03,089: INFO/MainProcess] Task triam.notifications.scan_due[e1dee4b5-5289-4c69-90f9-23b993300767] received
2026-05-28 06:30:09.932 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:30:09,935: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e1dee4b5-5289-4c69-90f9-23b993300767] succeeded in 6.843789919279516s: None
[2026-05-28 06:31:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:31:02,876: INFO/MainProcess] Task triam.notifications.scan_due[f365484d-607a-4a44-af19-d135ca2070c8] received
2026-05-28 06:31:09.663 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:31:09,664: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f365484d-607a-4a44-af19-d135ca2070c8] succeeded in 6.786422214936465s: None
[2026-05-28 06:32:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:32:03,244: INFO/MainProcess] Task triam.notifications.scan_due[b84f442b-7ddb-42d2-99b3-e8b371a4c08c] received
2026-05-28 06:32:10.241 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:32:10,242: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b84f442b-7ddb-42d2-99b3-e8b371a4c08c] succeeded in 6.783887667115778s: None
[2026-05-28 06:33:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:33:02,876: INFO/MainProcess] Task triam.notifications.scan_due[7f52b0e0-9a37-4052-b162-477aefa34255] received
2026-05-28 06:33:09.656 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:33:09,659: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7f52b0e0-9a37-4052-b162-477aefa34255] succeeded in 6.782298969104886s: None
[2026-05-28 06:34:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:34:03,090: INFO/MainProcess] Task triam.notifications.scan_due[4c9d41e3-0972-4290-8c54-93095345b12a] received
2026-05-28 06:34:10.264 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:34:10,265: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4c9d41e3-0972-4290-8c54-93095345b12a] succeeded in 6.959174024872482s: None
2026-05-28 06:34:31.626 | INFO | logging:callHandlers:1762 - 10.16.3.80:48286 - "GET /api/v1/health HTTP/1.1" 200
2026-05-28 06:34:34.899 | INFO | logging:callHandlers:1762 - 10.16.3.80:51397 - "GET /api/v1/books HTTP/1.1" 200
2026-05-28 06:34:38.008 | INFO | logging:callHandlers:1762 - 10.16.47.7:51995 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
[2026-05-28 06:35:02,198: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:35:03,091: INFO/MainProcess] Task triam.notifications.scan_due[44a8dedb-128b-4c37-93b9-7c521ae0abff] received
2026-05-28 06:35:10.102 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:35:10,102: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[44a8dedb-128b-4c37-93b9-7c521ae0abff] succeeded in 6.799039995763451s: None
[2026-05-28 06:36:02,199: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:36:03,088: INFO/MainProcess] Task triam.notifications.scan_due[95549640-a809-4419-980d-be341946f59d] received
2026-05-28 06:36:10.787 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:36:10,790: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[95549640-a809-4419-980d-be341946f59d] succeeded in 6.828691740054637s: None
[2026-05-28 06:37:02,199: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:37:03,087: INFO/MainProcess] Task triam.notifications.scan_due[409a44ef-81f2-4e5e-bd5b-8ee8c9f1242e] received
2026-05-28 06:37:09.880 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:37:09,880: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[409a44ef-81f2-4e5e-bd5b-8ee8c9f1242e] succeeded in 6.791601167060435s: None
[2026-05-28 06:38:02,201: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:38:02,875: INFO/MainProcess] Task triam.notifications.scan_due[aba0e928-22b5-4cef-b1c4-fcd981e42572] received
2026-05-28 06:38:09.696 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:38:09,697: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[aba0e928-22b5-4cef-b1c4-fcd981e42572] succeeded in 6.8209928520955145s: None
[2026-05-28 06:39:02,201: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:39:03,087: INFO/MainProcess] Task triam.notifications.scan_due[aa79a206-cc80-4b1e-8e16-1ccfcc81f692] received
2026-05-28 06:39:09.880 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:39:09,880: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[aa79a206-cc80-4b1e-8e16-1ccfcc81f692] succeeded in 6.792523484677076s: None
[2026-05-28 06:40:02,201: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:40:03,088: INFO/MainProcess] Task triam.notifications.scan_due[1b71da31-07ec-4455-bce8-eb4225d57702] received
2026-05-28 06:40:09.876 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:40:09,877: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1b71da31-07ec-4455-bce8-eb4225d57702] succeeded in 6.7871805019676685s: None
2026-05-28 06:40:12.271 | INFO | logging:callHandlers:1762 - 10.16.47.7:14191 - "GET /api/v1/health HTTP/1.1" 200
[2026-05-28 06:41:02,201: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:41:03,087: INFO/MainProcess] Task triam.notifications.scan_due[db3bf392-d88b-4df8-a1e2-cbb72e5764a7] received
2026-05-28 06:41:11.336 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:41:11,336: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[db3bf392-d88b-4df8-a1e2-cbb72e5764a7] succeeded in 8.247492149937898s: None
[2026-05-28 06:42:02,201: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:42:03,087: INFO/MainProcess] Task triam.notifications.scan_due[5064e2cb-5e4f-4652-b1b4-cf2e3210fab5] received
2026-05-28 06:42:09.995 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:42:09,995: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5064e2cb-5e4f-4652-b1b4-cf2e3210fab5] succeeded in 6.906825081910938s: None
[2026-05-28 06:43:02,201: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:43:02,999: INFO/MainProcess] Task triam.notifications.scan_due[3545b9dd-5f80-45df-99da-09a303ad6892] received
2026-05-28 06:43:09.996 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:43:09,996: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3545b9dd-5f80-45df-99da-09a303ad6892] succeeded in 6.997033821884543s: None
[2026-05-28 06:44:02,201: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:44:03,253: INFO/MainProcess] Task triam.notifications.scan_due[8594a6d8-4931-4ad3-8ae8-4e08cadb9c65] received
2026-05-28 06:44:10.160 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:44:10,160: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8594a6d8-4931-4ad3-8ae8-4e08cadb9c65] succeeded in 6.906446731183678s: None
2026-05-28 06:44:29.037 | INFO | logging:callHandlers:1762 - 10.16.47.7:44892 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
[2026-05-28 06:45:02,201: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:45:03,299: INFO/MainProcess] Task triam.notifications.scan_due[acc32f28-1ce0-4bf9-a5f3-898b249ab642] received
2026-05-28 06:45:10.201 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:45:10,202: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[acc32f28-1ce0-4bf9-a5f3-898b249ab642] succeeded in 6.902319876942784s: None
[2026-05-28 06:46:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:46:03,085: INFO/MainProcess] Task triam.notifications.scan_due[fe4b474d-2ffb-46cd-9f61-a861b03569df] received
2026-05-28 06:46:09.987 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:46:09,987: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[fe4b474d-2ffb-46cd-9f61-a861b03569df] succeeded in 6.901679057162255s: None
[2026-05-28 06:47:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:47:03,085: INFO/MainProcess] Task triam.notifications.scan_due[de9cc480-4129-4679-a5e2-c8ac4b972631] received
2026-05-28 06:47:09.987 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:47:09,987: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[de9cc480-4129-4679-a5e2-c8ac4b972631] succeeded in 6.901585694868118s: None
[2026-05-28 06:48:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:48:02,872: INFO/MainProcess] Task triam.notifications.scan_due[b2b1fa2c-5c31-46cd-a08f-cd627f497965] received
2026-05-28 06:48:09.774 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:48:09,775: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b2b1fa2c-5c31-46cd-a08f-cd627f497965] succeeded in 6.90167282987386s: None
[2026-05-28 06:49:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:49:03,084: INFO/MainProcess] Task triam.notifications.scan_due[282d22ab-0b71-4580-b884-ce4df301bf95] received
2026-05-28 06:49:09.983 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:49:09,983: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[282d22ab-0b71-4580-b884-ce4df301bf95] succeeded in 6.897963349241763s: None
[2026-05-28 06:50:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:50:03,084: INFO/MainProcess] Task triam.notifications.scan_due[55de6ce9-6b4a-4e0d-81d9-fa16a385197a] received
2026-05-28 06:50:09.985 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:50:09,985: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[55de6ce9-6b4a-4e0d-81d9-fa16a385197a] succeeded in 6.900057975202799s: None
[2026-05-28 06:51:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:51:03,085: INFO/MainProcess] Task triam.notifications.scan_due[180597bb-3fec-4bd2-a064-33f88c1bda94] received
2026-05-28 06:51:09.991 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:51:09,992: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[180597bb-3fec-4bd2-a064-33f88c1bda94] succeeded in 6.906507876701653s: None
[2026-05-28 06:52:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:52:03,236: INFO/MainProcess] Task triam.notifications.scan_due[49bb5cfa-03ef-4c2b-993b-328dffff727a] received
2026-05-28 06:52:10.138 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:52:10,139: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[49bb5cfa-03ef-4c2b-993b-328dffff727a] succeeded in 6.901723179034889s: None
[2026-05-28 06:53:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:53:03,013: INFO/MainProcess] Task triam.notifications.scan_due[b0306a03-1444-4c3d-97d8-d4dcce73b096] received
2026-05-28 06:53:09.913 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:53:09,914: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b0306a03-1444-4c3d-97d8-d4dcce73b096] succeeded in 6.900041827000678s: None
[2026-05-28 06:54:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:54:03,212: INFO/MainProcess] Task triam.notifications.scan_due[4d05e670-fa5e-4613-9c64-aa2cf682412a] received
2026-05-28 06:54:10.112 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:54:10,113: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4d05e670-fa5e-4613-9c64-aa2cf682412a] succeeded in 6.899896621704102s: None
[2026-05-28 06:55:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:55:02,990: INFO/MainProcess] Task triam.notifications.scan_due[9ad95c5e-5687-42d8-b770-69b25e9de7a8] received
2026-05-28 06:55:09.910 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:55:09,911: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[9ad95c5e-5687-42d8-b770-69b25e9de7a8] succeeded in 6.919849149882793s: None
[2026-05-28 06:56:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:56:03,193: INFO/MainProcess] Task triam.notifications.scan_due[364ade56-e2d4-4113-add3-7ec24770924b] received
2026-05-28 06:56:10.096 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:56:10,096: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[364ade56-e2d4-4113-add3-7ec24770924b] succeeded in 6.901863920968026s: None
[2026-05-28 06:57:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:57:03,086: INFO/MainProcess] Task triam.notifications.scan_due[54809951-2e0a-414e-8c40-f9b2cd943b81] received
2026-05-28 06:57:10.213 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:57:10,213: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[54809951-2e0a-414e-8c40-f9b2cd943b81] succeeded in 6.905551167204976s: None
[2026-05-28 06:58:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:58:02,873: INFO/MainProcess] Task triam.notifications.scan_due[47e1d917-9396-4444-9283-a68fbad7101b] received
2026-05-28 06:58:09.776 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:58:09,776: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[47e1d917-9396-4444-9283-a68fbad7101b] succeeded in 6.902746827807277s: None
[2026-05-28 06:59:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 06:59:03,086: INFO/MainProcess] Task triam.notifications.scan_due[cccd8e30-77f2-41e7-bd87-58eafd749e77] received
2026-05-28 06:59:10.221 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 06:59:10,221: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[cccd8e30-77f2-41e7-bd87-58eafd749e77] succeeded in 6.913414222188294s: None
[2026-05-28 07:00:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:00:02,862: INFO/MainProcess] Task triam.notifications.scan_due[eea29963-16eb-4c9c-8bc4-3a596424f0a8] received
2026-05-28 07:00:09.765 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:00:09,767: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[eea29963-16eb-4c9c-8bc4-3a596424f0a8] succeeded in 6.903585999738425s: None
[2026-05-28 07:01:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:01:03,075: INFO/MainProcess] Task triam.notifications.scan_due[a251e059-38fb-4bb8-84c0-55303adf5fd4] received
2026-05-28 07:01:10.002 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:01:10,003: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a251e059-38fb-4bb8-84c0-55303adf5fd4] succeeded in 6.926612085197121s: None
[2026-05-28 07:02:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:02:03,075: INFO/MainProcess] Task triam.notifications.scan_due[829a1c09-8d7f-4d99-9b51-d45d078eac50] received
2026-05-28 07:02:09.979 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:02:09,980: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[829a1c09-8d7f-4d99-9b51-d45d078eac50] succeeded in 6.903132820967585s: None
[2026-05-28 07:03:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:03:02,862: INFO/MainProcess] Task triam.notifications.scan_due[cfec424b-98e7-46ee-9631-6cc8a1f38cc4] received
2026-05-28 07:03:09.775 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:03:09,776: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[cfec424b-98e7-46ee-9631-6cc8a1f38cc4] succeeded in 6.91221809387207s: None
[2026-05-28 07:04:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:04:03,232: INFO/MainProcess] Task triam.notifications.scan_due[04966ae0-09a2-4db2-a78d-b3f88f43b937] received
2026-05-28 07:04:10.135 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:04:10,135: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[04966ae0-09a2-4db2-a78d-b3f88f43b937] succeeded in 6.902097518090159s: None
[2026-05-28 07:05:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:05:03,019: INFO/MainProcess] Task triam.notifications.scan_due[69f48566-2d82-44fe-8183-466ae67c9415] received
2026-05-28 07:05:09.923 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:05:09,924: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[69f48566-2d82-44fe-8183-466ae67c9415] succeeded in 6.9049409329891205s: None
[2026-05-28 07:06:02,202: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:06:03,075: INFO/MainProcess] Task triam.notifications.scan_due[da5aac1f-fd73-40fa-a0b8-3993f98effab] received
2026-05-28 07:06:09.976 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:06:09,977: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[da5aac1f-fd73-40fa-a0b8-3993f98effab] succeeded in 6.901496951002628s: None
[2026-05-28 07:07:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-28 07:07:02.816 | INFO | logging:callHandlers:1762 - 10.16.3.80:24050 - "GET /api/v1/study-contexts HTTP/1.1" 200
[2026-05-28 07:07:03,075: INFO/MainProcess] Task triam.notifications.scan_due[58d30de5-94e5-4d2a-bf3a-676d5eaec43f] received
2026-05-28 07:07:09.974 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:07:09,974: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[58d30de5-94e5-4d2a-bf3a-676d5eaec43f] succeeded in 6.896189296152443s: None
2026-05-28 07:07:13.625 | INFO | logging:callHandlers:1762 - 10.16.3.80:51476 - "GET /api/v1/study-contexts/7d6970f1-3808-42df-a99e-46a59eb0b280/threads HTTP/1.1" 200
2026-05-28 07:07:16.692 | INFO | logging:callHandlers:1762 - 10.16.3.80:25656 - "GET /api/v1/threads/42a57333-9536-431c-9657-0e1e9c800b6b/messages HTTP/1.1" 200
[2026-05-28 07:08:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:08:02,865: INFO/MainProcess] Task triam.notifications.scan_due[e1fb428b-ed51-4a7b-9fc7-bb3a0b54c780] received
2026-05-28 07:08:09.586 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:08:09,587: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e1fb428b-ed51-4a7b-9fc7-bb3a0b54c780] succeeded in 6.721000343095511s: None
[2026-05-28 07:09:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:09:03,075: INFO/MainProcess] Task triam.notifications.scan_due[2ecb02a8-0ed0-4166-90f2-3c4328fbf58e] received
2026-05-28 07:09:09.799 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:09:09,800: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2ecb02a8-0ed0-4166-90f2-3c4328fbf58e] succeeded in 6.723572090268135s: None
[2026-05-28 07:10:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:10:02,863: INFO/MainProcess] Task triam.notifications.scan_due[7a7853f8-5c13-4bcc-baf8-aeb8997164a2] received
2026-05-28 07:10:09.597 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:10:09,598: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7a7853f8-5c13-4bcc-baf8-aeb8997164a2] succeeded in 6.7340112859383225s: None
[2026-05-28 07:11:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:11:03,075: INFO/MainProcess] Task triam.notifications.scan_due[46890122-fb03-49d6-9c43-91abbba4d7ab] received
2026-05-28 07:11:11.306 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:11:11,307: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[46890122-fb03-49d6-9c43-91abbba4d7ab] succeeded in 8.229848390910774s: None
[2026-05-28 07:12:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:12:03,077: INFO/MainProcess] Task triam.notifications.scan_due[8df9cbf5-fa99-4e94-80ad-b54c498645ce] received
2026-05-28 07:12:10.002 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:12:10,003: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8df9cbf5-fa99-4e94-80ad-b54c498645ce] succeeded in 6.924669043626636s: None
[2026-05-28 07:13:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:13:03,053: INFO/MainProcess] Task triam.notifications.scan_due[6aff4508-ca5d-4d00-be1a-7707a5373522] received
2026-05-28 07:13:09.963 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:13:09,964: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[6aff4508-ca5d-4d00-be1a-7707a5373522] succeeded in 6.910018523223698s: None
[2026-05-28 07:14:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:14:03,076: INFO/MainProcess] Task triam.notifications.scan_due[338d1bbb-59fe-4be5-93e2-a30a2d66c121] received
2026-05-28 07:14:09.989 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:14:09,990: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[338d1bbb-59fe-4be5-93e2-a30a2d66c121] succeeded in 6.913862471003085s: None
[2026-05-28 07:15:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:15:03,050: INFO/MainProcess] Task triam.notifications.scan_due[98180dae-a0ea-419c-af57-2c06a198ffb1] received
2026-05-28 07:15:09.968 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:15:09,969: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[98180dae-a0ea-419c-af57-2c06a198ffb1] succeeded in 6.917733127716929s: None
[2026-05-28 07:16:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:16:03,261: INFO/MainProcess] Task triam.notifications.scan_due[d4b97d77-1a76-4d73-9d2d-974578852416] received
2026-05-28 07:16:10.172 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:16:10,173: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d4b97d77-1a76-4d73-9d2d-974578852416] succeeded in 6.910708277020603s: None
[2026-05-28 07:17:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:17:03,076: INFO/MainProcess] Task triam.notifications.scan_due[f6fa2b5b-ef7b-42a5-a5c8-2f0c8f5ee403] received
2026-05-28 07:17:10.062 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:17:10,063: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f6fa2b5b-ef7b-42a5-a5c8-2f0c8f5ee403] succeeded in 6.984553160145879s: None
[2026-05-28 07:18:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:18:03,075: INFO/MainProcess] Task triam.notifications.scan_due[50a8a1f9-34c5-413d-9ff3-c75d5c0d1669] received
2026-05-28 07:18:10.064 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:18:10,065: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[50a8a1f9-34c5-413d-9ff3-c75d5c0d1669] succeeded in 6.988355400040746s: None
[2026-05-28 07:19:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:19:03,198: INFO/MainProcess] Task triam.notifications.scan_due[bf0c18ab-5e95-49b3-8f08-fef5b91101a6] received
2026-05-28 07:19:10.184 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:19:10,184: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[bf0c18ab-5e95-49b3-8f08-fef5b91101a6] succeeded in 6.9862095061689615s: None
[2026-05-28 07:20:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:20:02,984: INFO/MainProcess] Task triam.notifications.scan_due[ef5cfe11-4709-4532-89b5-9578ada941e8] received
2026-05-28 07:20:09.971 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:20:09,971: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ef5cfe11-4709-4532-89b5-9578ada941e8] succeeded in 6.986597455106676s: None
[2026-05-28 07:21:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:21:03,273: INFO/MainProcess] Task triam.notifications.scan_due[b9f100cf-0ba0-4db7-af8f-f8a116da3ed6] received
2026-05-28 07:21:10.408 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:21:10,409: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b9f100cf-0ba0-4db7-af8f-f8a116da3ed6] succeeded in 7.134497518185526s: None
[2026-05-28 07:22:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:22:03,359: INFO/MainProcess] Task triam.notifications.scan_due[4f1b4949-1b20-4c36-9b6c-744137efdc2a] received
2026-05-28 07:22:10.351 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:22:10,352: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4f1b4949-1b20-4c36-9b6c-744137efdc2a] succeeded in 6.990766230970621s: None
[2026-05-28 07:23:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:23:03,082: INFO/MainProcess] Task triam.notifications.scan_due[4bb59e81-49c7-48ec-93ff-b5ec1d921975] received
2026-05-28 07:23:10.297 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:23:10,298: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4bb59e81-49c7-48ec-93ff-b5ec1d921975] succeeded in 6.991166092921048s: None
[2026-05-28 07:24:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:24:03,164: INFO/MainProcess] Task triam.notifications.scan_due[4da2ae90-673e-4478-bff3-b93f59cfa557] received
2026-05-28 07:24:10.149 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:24:10,150: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4da2ae90-673e-4478-bff3-b93f59cfa557] succeeded in 6.98524193232879s: None
[2026-05-28 07:25:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:25:02,870: INFO/MainProcess] Task triam.notifications.scan_due[4c0eb7d8-b9a4-4c96-91d7-f5ac714062ba] received
2026-05-28 07:25:09.855 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:25:09,856: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4c0eb7d8-b9a4-4c96-91d7-f5ac714062ba] succeeded in 6.985883651301265s: None
[2026-05-28 07:26:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:26:03,083: INFO/MainProcess] Task triam.notifications.scan_due[f6902f1f-fe8c-4b50-a2e3-ba97208a8cdf] received
2026-05-28 07:26:10.116 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:26:10,117: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f6902f1f-fe8c-4b50-a2e3-ba97208a8cdf] succeeded in 7.033220028039068s: None
[2026-05-28 07:27:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:27:03,076: INFO/MainProcess] Task triam.notifications.scan_due[b2993677-d065-4d4b-92a3-0cfa08e40f5e] received
2026-05-28 07:27:10.179 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:27:10,180: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b2993677-d065-4d4b-92a3-0cfa08e40f5e] succeeded in 7.101335027255118s: None
[2026-05-28 07:28:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:28:03,076: INFO/MainProcess] Task triam.notifications.scan_due[7b3232b6-3e00-4fc0-9c7e-2ecb9387bc91] received
2026-05-28 07:28:10.175 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:28:10,176: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7b3232b6-3e00-4fc0-9c7e-2ecb9387bc91] succeeded in 7.098671338986605s: None
[2026-05-28 07:29:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:29:03,287: INFO/MainProcess] Task triam.notifications.scan_due[8bdc23f8-de53-473e-8b50-0abb549e5549] received
2026-05-28 07:29:10.391 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:29:10,391: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8bdc23f8-de53-473e-8b50-0abb549e5549] succeeded in 7.102700752671808s: None
[2026-05-28 07:30:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:30:03,015: INFO/MainProcess] Task triam.notifications.scan_due[7464fec4-b900-46d6-b038-102c366c7e92] received
2026-05-28 07:30:10.123 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:30:10,123: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7464fec4-b900-46d6-b038-102c366c7e92] succeeded in 7.106716078706086s: None
[2026-05-28 07:31:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:31:03,394: INFO/MainProcess] Task triam.notifications.scan_due[ed5fedd6-d6ff-4d49-8427-2ae697153f79] received
2026-05-28 07:31:10.537 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:31:10,538: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ed5fedd6-d6ff-4d49-8427-2ae697153f79] succeeded in 7.143285558093339s: None
2026-05-28 07:31:41.450 | INFO | logging:callHandlers:1762 - 10.16.3.80:36493 - "GET /api/v1/health HTTP/1.1" 200
2026-05-28 07:31:44.413 | INFO | logging:callHandlers:1762 - 10.16.3.80:36493 - "GET /api/v1/books HTTP/1.1" 200
2026-05-28 07:31:47.768 | INFO | logging:callHandlers:1762 - 10.16.40.242:40850 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
[2026-05-28 07:32:02,203: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:32:03,340: INFO/MainProcess] Task triam.notifications.scan_due[08577b5c-38f1-469b-a2cb-34f04a3e6fb8] received
2026-05-28 07:32:10.476 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:32:10,477: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[08577b5c-38f1-469b-a2cb-34f04a3e6fb8] succeeded in 7.136023113038391s: None
[2026-05-28 07:33:02,204: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:33:03,077: INFO/MainProcess] Task triam.notifications.scan_due[f027cd54-6194-4c22-94c5-48284f5a6c26] received
2026-05-28 07:33:10.182 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:33:10,182: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f027cd54-6194-4c22-94c5-48284f5a6c26] succeeded in 7.104735851753503s: None
[2026-05-28 07:34:02,204: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:34:03,076: INFO/MainProcess] Task triam.notifications.scan_due[1af2b3a6-29f3-4572-b5ae-abcffc8b9786] received
2026-05-28 07:34:04.411 | INFO | logging:callHandlers:1762 - 10.16.3.80:54565 - "GET /api/v1/health HTTP/1.1" 200
2026-05-28 07:34:10.173 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:34:10,174: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1af2b3a6-29f3-4572-b5ae-abcffc8b9786] succeeded in 7.095945790410042s: None
[2026-05-28 07:35:02,204: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:35:02,957: INFO/MainProcess] Task triam.notifications.scan_due[70a0b528-ebc1-44de-8557-af607ff91e56] received
2026-05-28 07:35:10.055 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:35:10,056: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[70a0b528-ebc1-44de-8557-af607ff91e56] succeeded in 7.0981801599264145s: None
[2026-05-28 07:36:02,204: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:36:03,076: INFO/MainProcess] Task triam.notifications.scan_due[f837ba28-499e-4031-8a3e-2d64cb96229a] received
2026-05-28 07:36:10.176 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:36:10,176: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f837ba28-499e-4031-8a3e-2d64cb96229a] succeeded in 7.097882652189583s: None
[2026-05-28 07:37:02,204: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:37:03,052: INFO/MainProcess] Task triam.notifications.scan_due[a194f3cf-1dcd-4a08-a7b9-13f4be60a370] received
2026-05-28 07:37:10.151 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:37:10,151: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a194f3cf-1dcd-4a08-a7b9-13f4be60a370] succeeded in 7.0987260029651225s: None
[2026-05-28 07:38:02,204: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:38:03,186: INFO/MainProcess] Task triam.notifications.scan_due[3bdf8ba9-960d-4d41-9dfa-cb42a73c7fce] received
2026-05-28 07:38:10.314 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:38:10,315: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3bdf8ba9-960d-4d41-9dfa-cb42a73c7fce] succeeded in 7.127609102986753s: None
[2026-05-28 07:39:02,204: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:39:03,108: INFO/MainProcess] Task triam.notifications.scan_due[d1f0069a-fc0f-427b-8028-f6468198cea2] received
2026-05-28 07:39:10.205 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:39:10,206: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d1f0069a-fc0f-427b-8028-f6468198cea2] succeeded in 7.097240075003356s: None
[2026-05-28 07:40:02,204: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:40:02,871: INFO/MainProcess] Task triam.notifications.scan_due[aa78d7d0-05f0-4aba-8bd5-8d7ececb9817] received
2026-05-28 07:40:09.983 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:40:09,984: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[aa78d7d0-05f0-4aba-8bd5-8d7ececb9817] succeeded in 7.110447803046554s: None
[2026-05-28 07:41:02,204: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:41:03,087: INFO/MainProcess] Task triam.notifications.scan_due[f288d332-34d4-43f9-a68a-4be02ca1e8ac] received
2026-05-28 07:41:11.263 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:41:11,264: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f288d332-34d4-43f9-a68a-4be02ca1e8ac] succeeded in 8.176240263041109s: None
[2026-05-28 07:42:02,204: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:42:02,871: INFO/MainProcess] Task triam.notifications.scan_due[830c7211-4832-430a-9547-9202a3f3ea84] received
2026-05-28 07:42:09.911 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:42:09,912: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[830c7211-4832-430a-9547-9202a3f3ea84] succeeded in 6.820889793802053s: None
[2026-05-28 07:43:02,204: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:43:03,087: INFO/MainProcess] Task triam.notifications.scan_due[5b4200d5-a2e5-4c47-9a5a-e8dc05f6f678] received
2026-05-28 07:43:10.122 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:43:10,122: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5b4200d5-a2e5-4c47-9a5a-e8dc05f6f678] succeeded in 6.816309588961303s: None
[2026-05-28 07:44:02,204: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:44:03,088: INFO/MainProcess] Task triam.notifications.scan_due[be9ff522-1403-4795-86e5-d49908eeb537] received
2026-05-28 07:44:10.168 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:44:10,168: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[be9ff522-1403-4795-86e5-d49908eeb537] succeeded in 6.859332383144647s: None
[2026-05-28 07:45:02,204: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:45:02,873: INFO/MainProcess] Task triam.notifications.scan_due[1a5757f7-c872-4abd-8c7a-6b047a84e1b6] received
2026-05-28 07:45:09.784 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:45:09,785: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1a5757f7-c872-4abd-8c7a-6b047a84e1b6] succeeded in 6.910651762038469s: None
[2026-05-28 07:46:02,204: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:46:03,280: INFO/MainProcess] Task triam.notifications.scan_due[4a55c238-ea8d-42a3-be16-103f7dfd5f6a] received
2026-05-28 07:46:10.338 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:46:10,339: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4a55c238-ea8d-42a3-be16-103f7dfd5f6a] succeeded in 6.8384899059310555s: None
[2026-05-28 07:47:02,204: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:47:02,873: INFO/MainProcess] Task triam.notifications.scan_due[c89cd370-64fe-4041-be51-2339f1b4a359] received
2026-05-28 07:47:09.704 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:47:09,705: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c89cd370-64fe-4041-be51-2339f1b4a359] succeeded in 6.830488417763263s: None
[2026-05-28 07:48:02,205: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:48:03,091: INFO/MainProcess] Task triam.notifications.scan_due[7be5f4f5-14a1-42a6-b9df-46228050e041] received
2026-05-28 07:48:09.941 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:48:09,942: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7be5f4f5-14a1-42a6-b9df-46228050e041] succeeded in 6.84889155626297s: None
2026-05-28 07:48:42.519 | INFO | logging:callHandlers:1762 - 10.16.37.205:46116 - "GET /api/v1/study-contexts HTTP/1.1" 200
[2026-05-28 07:49:02,205: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:49:03,295: INFO/MainProcess] Task triam.notifications.scan_due[4b88a29a-927e-4174-9301-b85402a8a311] received
2026-05-28 07:49:10.049 | INFO | logging:callHandlers:1762 - 10.16.3.80:4643 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/details HTTP/1.1" 200
2026-05-28 07:49:10.342 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:49:10,343: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4b88a29a-927e-4174-9301-b85402a8a311] succeeded in 6.827811449300498s: None
2026-05-28 07:49:17.247 | INFO | logging:callHandlers:1762 - 10.16.47.7:33816 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/ae4c9c22-c00d-4f4a-93cf-81146ef32cbf/progress HTTP/1.1" 200
2026-05-28 07:49:43.341 | INFO | logging:callHandlers:1762 - 10.16.37.205:30851 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/ae4c9c22-c00d-4f4a-93cf-81146ef32cbf/progress HTTP/1.1" 200
2026-05-28 07:50:01.333 | INFO | logging:callHandlers:1762 - 10.16.3.80:6600 - "GET /api/v1/study-contexts/7d6970f1-3808-42df-a99e-46a59eb0b280/threads HTTP/1.1" 200
[2026-05-28 07:50:02,205: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:50:02,873: INFO/MainProcess] Task triam.notifications.scan_due[2d370c49-641a-4e95-af47-2690b51f7c91] received
2026-05-28 07:50:03.786 | INFO | logging:callHandlers:1762 - 10.16.3.80:6600 - "GET /api/v1/threads/42a57333-9536-431c-9657-0e1e9c800b6b/messages HTTP/1.1" 200
2026-05-28 07:50:09.702 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:50:09,703: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2d370c49-641a-4e95-af47-2690b51f7c91] succeeded in 6.829026915132999s: None
[2026-05-28 07:51:02,205: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:51:03,086: INFO/MainProcess] Task triam.notifications.scan_due[5cc6ef15-1d93-4aa8-85b0-8aea61c79e50] received
2026-05-28 07:51:10.051 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:51:10,052: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5cc6ef15-1d93-4aa8-85b0-8aea61c79e50] succeeded in 6.965425415895879s: None
[2026-05-28 07:52:02,205: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:52:02,871: INFO/MainProcess] Task triam.notifications.scan_due[d2956d43-2036-4fe7-af94-21ead60be5e4] received
2026-05-28 07:52:09.701 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:52:09,702: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d2956d43-2036-4fe7-af94-21ead60be5e4] succeeded in 6.829723700881004s: None
[2026-05-28 07:53:02,205: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:53:03,084: INFO/MainProcess] Task triam.notifications.scan_due[e24390b7-4194-42fc-8ffc-a754977d5104] received
2026-05-28 07:53:09.901 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:53:09,902: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e24390b7-4194-42fc-8ffc-a754977d5104] succeeded in 6.816488265991211s: None
[2026-05-28 07:54:02,205: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:54:03,085: INFO/MainProcess] Task triam.notifications.scan_due[6c89f011-a79c-4b4d-9be8-164fdc0aa9bf] received
2026-05-28 07:54:09.914 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:54:09,914: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[6c89f011-a79c-4b4d-9be8-164fdc0aa9bf] succeeded in 6.8281366541050375s: None
[2026-05-28 07:55:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:55:03,377: INFO/MainProcess] Task triam.notifications.scan_due[80baf004-d607-486b-ae4b-f78113d635d9] received
2026-05-28 07:55:10.197 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:55:10,198: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[80baf004-d607-486b-ae4b-f78113d635d9] succeeded in 6.819988512434065s: None
[2026-05-28 07:56:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:56:03,084: INFO/MainProcess] Task triam.notifications.scan_due[80234f41-5c07-488a-9d71-bbce0a216c4a] received
2026-05-28 07:56:09.904 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:56:09,905: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[80234f41-5c07-488a-9d71-bbce0a216c4a] succeeded in 6.819942032918334s: None
[2026-05-28 07:57:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:57:02,869: INFO/MainProcess] Task triam.notifications.scan_due[57c8b4cb-6891-42cc-aed1-3c825562565d] received
2026-05-28 07:57:09.687 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:57:09,688: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[57c8b4cb-6891-42cc-aed1-3c825562565d] succeeded in 6.8169865920208395s: None
[2026-05-28 07:58:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:58:03,085: INFO/MainProcess] Task triam.notifications.scan_due[b6b44d2f-1741-4e20-ae3b-643d0ab6328c] received
2026-05-28 07:58:09.902 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:58:09,903: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b6b44d2f-1741-4e20-ae3b-643d0ab6328c] succeeded in 6.817210379987955s: None
2026-05-28 07:58:38.959 | INFO | logging:callHandlers:1762 - 10.16.40.242:46738 - "GET /api/v1/health HTTP/1.1" 200
2026-05-28 07:58:51.785 | INFO | logging:callHandlers:1762 - 10.16.3.80:29357 - "GET /api/v1/health HTTP/1.1" 200
2026-05-28 07:58:54.927 | INFO | logging:callHandlers:1762 - 10.16.37.205:63776 - "GET /api/v1/books HTTP/1.1" 200
2026-05-28 07:58:56.680 | INFO | logging:callHandlers:1762 - 10.16.40.242:22785 - "GET /api/v1/study-contexts HTTP/1.1" 200
[2026-05-28 07:59:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 07:59:03,087: INFO/MainProcess] Task triam.notifications.scan_due[8f02d5b4-4d5d-4341-9b25-82ee9e0710c2] received
2026-05-28 07:59:09.915 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 07:59:09,916: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8f02d5b4-4d5d-4341-9b25-82ee9e0710c2] succeeded in 6.827769506257027s: None
2026-05-28 07:59:18.183 | INFO | logging:callHandlers:1762 - 10.16.3.80:58746 - "GET /api/v1/books HTTP/1.1" 200
2026-05-28 07:59:21.157 | INFO | logging:callHandlers:1762 - 10.16.3.80:58746 - "GET /api/v1/books/a9453a82-6e22-42c7-bc4a-c8bd9125c422/details HTTP/1.1" 200
2026-05-28 07:59:36.649 | INFO | logging:callHandlers:1762 - 10.16.40.242:46293 - "GET /api/v1/books HTTP/1.1" 200
2026-05-28 07:59:39.025 | INFO | logging:callHandlers:1762 - 10.16.3.80:37878 - "GET /api/v1/books/a9453a82-6e22-42c7-bc4a-c8bd9125c422/details HTTP/1.1" 200
2026-05-28 07:59:41.492 | INFO | logging:callHandlers:1762 - 10.16.3.80:37878 - "GET /api/v1/books/a9453a82-6e22-42c7-bc4a-c8bd9125c422/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 07:59:44.074 | INFO | logging:callHandlers:1762 - 10.16.3.80:37878 - "GET /api/v1/books/a9453a82-6e22-42c7-bc4a-c8bd9125c422/learning-progress?mode=pareto HTTP/1.1" 200
2026-05-28 07:59:47.430 | INFO | logging:callHandlers:1762 - 10.16.47.7:9413 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/details HTTP/1.1" 200
2026-05-28 07:59:50.093 | INFO | logging:callHandlers:1762 - 10.16.37.205:37631 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 07:59:52.511 | INFO | logging:callHandlers:1762 - 10.16.3.80:56118 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=pareto HTTP/1.1" 200
2026-05-28 07:59:55.879 | INFO | logging:callHandlers:1762 - 10.16.47.7:61607 - "GET /api/v1/books/4ef0ad48-0e8f-457d-b278-3d3fe3da0905/details HTTP/1.1" 200
[2026-05-28 08:00:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:00:03,106: INFO/MainProcess] Task triam.notifications.scan_due[9bed2f29-f468-4102-8fa7-9353f47602a6] received
2026-05-28 08:00:07.805 | INFO | logging:callHandlers:1762 - 10.16.37.205:60701 - "GET /api/v1/books/4ef0ad48-0e8f-457d-b278-3d3fe3da0905/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:00:09.951 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:00:09,951: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[9bed2f29-f468-4102-8fa7-9353f47602a6] succeeded in 6.8447355479002s: None
2026-05-28 08:00:11.013 | INFO | logging:callHandlers:1762 - 10.16.3.80:58536 - "GET /api/v1/books/4ef0ad48-0e8f-457d-b278-3d3fe3da0905/learning-progress?mode=pareto HTTP/1.1" 200
2026-05-28 08:00:13.310 | INFO | logging:callHandlers:1762 - 10.16.3.80:40361 - "GET /api/v1/notifications/settings HTTP/1.1" 200
2026-05-28 08:00:15.084 | INFO | logging:callHandlers:1762 - 10.16.37.205:56823 - "GET /api/v1/study-contexts HTTP/1.1" 200
[2026-05-28 08:01:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:01:03,089: INFO/MainProcess] Task triam.notifications.scan_due[d5c4b721-fdf8-4ce0-8f9f-d9cd277a4ec4] received
2026-05-28 08:01:09.912 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:01:09,913: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d5c4b721-fdf8-4ce0-8f9f-d9cd277a4ec4] succeeded in 6.823098618071526s: None
[2026-05-28 08:02:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:02:03,011: INFO/MainProcess] Task triam.notifications.scan_due[426df27f-a42a-4b41-ad72-ea5c97ef7af7] received
2026-05-28 08:02:10.025 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:02:10,026: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[426df27f-a42a-4b41-ad72-ea5c97ef7af7] succeeded in 7.014439806807786s: None
[2026-05-28 08:03:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:03:03,088: INFO/MainProcess] Task triam.notifications.scan_due[3160e9ed-3f76-47ce-bddc-93c7f56dfa05] received
2026-05-28 08:03:10.119 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:03:10,120: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3160e9ed-3f76-47ce-bddc-93c7f56dfa05] succeeded in 6.819739042781293s: None
[2026-05-28 08:04:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:04:03,238: INFO/MainProcess] Task triam.notifications.scan_due[aa1326f0-3f1c-4412-979c-4e5ec106e2eb] received
2026-05-28 08:04:10.268 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:04:10,269: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[aa1326f0-3f1c-4412-979c-4e5ec106e2eb] succeeded in 6.819252544082701s: None
[2026-05-28 08:05:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:05:03,241: INFO/MainProcess] Task triam.notifications.scan_due[031a985b-aef4-4644-8bfb-71279d4848c1] received
2026-05-28 08:05:10.288 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:05:10,289: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[031a985b-aef4-4644-8bfb-71279d4848c1] succeeded in 6.834050707053393s: None
2026-05-28 08:05:38.864 | INFO | logging:callHandlers:1762 - 10.16.37.205:29822 - "GET /api/v1/health HTTP/1.1" 200
2026-05-28 08:05:41.679 | INFO | logging:callHandlers:1762 - 10.16.3.80:43508 - "GET /api/v1/books HTTP/1.1" 200
2026-05-28 08:05:45.345 | INFO | logging:callHandlers:1762 - 10.16.3.80:14143 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-28 08:05:54.305 | INFO | logging:callHandlers:1762 - 10.16.3.80:44148 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
[2026-05-28 08:06:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:06:03,232: INFO/MainProcess] Task triam.notifications.scan_due[79c2a802-2029-41f6-900b-f2a02222d1ce] received
2026-05-28 08:06:10.275 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:06:10,275: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[79c2a802-2029-41f6-900b-f2a02222d1ce] succeeded in 6.831185076851398s: None
2026-05-28 08:06:19.112 | INFO | logging:callHandlers:1762 - 10.16.37.205:30197 - "GET /api/v1/books/4ef0ad48-0e8f-457d-b278-3d3fe3da0905/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:06:21.615 | INFO | logging:callHandlers:1762 - 10.16.3.80:6544 - "GET /api/v1/books/4ef0ad48-0e8f-457d-b278-3d3fe3da0905/details HTTP/1.1" 200
2026-05-28 08:06:49.288 | INFO | logging:callHandlers:1762 - 10.16.3.80:63122 - "GET /api/v1/books/4ef0ad48-0e8f-457d-b278-3d3fe3da0905/learning-progress?mode=full HTTP/1.1" 200
[2026-05-28 08:07:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:07:03,021: INFO/MainProcess] Task triam.notifications.scan_due[36239bd0-10e7-4cc5-852f-e95558fa6f9b] received
2026-05-28 08:07:10.062 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:07:10,063: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[36239bd0-10e7-4cc5-852f-e95558fa6f9b] succeeded in 6.8291681138798594s: None
[2026-05-28 08:08:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:08:03,075: INFO/MainProcess] Task triam.notifications.scan_due[f0e35be5-82a3-406c-96aa-c2b1f4ecdbe2] received
2026-05-28 08:08:09.932 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:08:09,932: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f0e35be5-82a3-406c-96aa-c2b1f4ecdbe2] succeeded in 6.645613299217075s: None
[2026-05-28 08:09:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:09:03,237: INFO/MainProcess] Task triam.notifications.scan_due[94b470d1-c9c3-4535-b214-8adfdcad8517] received
2026-05-28 08:09:09.846 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:09:09,846: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[94b470d1-c9c3-4535-b214-8adfdcad8517] succeeded in 6.608402410987765s: None
2026-05-28 08:09:32.509 | INFO | logging:callHandlers:1762 - 10.16.37.205:46174 - "GET /api/v1/books/4ef0ad48-0e8f-457d-b278-3d3fe3da0905/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:36.104 | INFO | logging:callHandlers:1762 - 10.16.3.80:4254 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:40.278 | INFO | logging:callHandlers:1762 - 10.16.37.205:61283 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:41.751 | INFO | logging:callHandlers:1762 - 10.16.47.7:63181 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:43.407 | INFO | logging:callHandlers:1762 - 10.16.3.80:38988 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:43.814 | INFO | logging:callHandlers:1762 - 10.16.3.80:23232 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/ae4c9c22-c00d-4f4a-93cf-81146ef32cbf/progress HTTP/1.1" 200
2026-05-28 08:09:44.158 | INFO | logging:callHandlers:1762 - 10.16.3.80:1171 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:44.184 | INFO | logging:callHandlers:1762 - 10.16.47.7:40724 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:44.213 | INFO | logging:callHandlers:1762 - 10.16.37.205:17648 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:44.261 | INFO | logging:callHandlers:1762 - 10.16.40.242:1300 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:44.263 | INFO | logging:callHandlers:1762 - 10.16.37.205:61283 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:44.265 | INFO | logging:callHandlers:1762 - 10.16.3.80:7949 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:44.281 | INFO | logging:callHandlers:1762 - 10.16.40.242:1294 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:44.422 | INFO | logging:callHandlers:1762 - 10.16.47.7:30826 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:44.433 | INFO | logging:callHandlers:1762 - 10.16.3.80:2128 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:44.519 | INFO | logging:callHandlers:1762 - 10.16.47.7:31242 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:44.684 | INFO | logging:callHandlers:1762 - 10.16.37.205:31288 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:44.713 | INFO | logging:callHandlers:1762 - 10.16.37.205:33703 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:44.801 | INFO | logging:callHandlers:1762 - 10.16.40.242:27929 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:44.867 | INFO | logging:callHandlers:1762 - 10.16.3.80:17538 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:44.925 | INFO | logging:callHandlers:1762 - 10.16.47.7:63181 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:44.969 | INFO | logging:callHandlers:1762 - 10.16.3.80:19541 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:45.246 | INFO | logging:callHandlers:1762 - 10.16.40.242:64265 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:45.285 | INFO | logging:callHandlers:1762 - 10.16.37.205:17882 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:45.332 | INFO | logging:callHandlers:1762 - 10.16.40.242:17272 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:45.373 | INFO | logging:callHandlers:1762 - 10.16.3.80:48839 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:45.400 | INFO | logging:callHandlers:1762 - 10.16.47.7:8466 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:45.406 | INFO | logging:callHandlers:1762 - 10.16.3.80:53485 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:45.411 | INFO | logging:callHandlers:1762 - 10.16.40.242:59439 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:45.518 | INFO | logging:callHandlers:1762 - 10.16.40.242:61888 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:45.523 | INFO | logging:callHandlers:1762 - 10.16.3.80:64502 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:45.625 | INFO | logging:callHandlers:1762 - 10.16.3.80:8560 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:45.793 | INFO | logging:callHandlers:1762 - 10.16.40.242:54597 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:45.823 | INFO | logging:callHandlers:1762 - 10.16.3.80:26102 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:45.922 | INFO | logging:callHandlers:1762 - 10.16.37.205:23778 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:45.991 | INFO | logging:callHandlers:1762 - 10.16.3.80:7608 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:46.046 | INFO | logging:callHandlers:1762 - 10.16.3.80:55663 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:46.062 | INFO | logging:callHandlers:1762 - 10.16.3.80:1687 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:46.338 | INFO | logging:callHandlers:1762 - 10.16.3.80:60462 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:46.412 | INFO | logging:callHandlers:1762 - 10.16.40.242:43865 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:46.453 | INFO | logging:callHandlers:1762 - 10.16.40.242:45804 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:46.473 | INFO | logging:callHandlers:1762 - 10.16.3.80:40968 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:46.516 | INFO | logging:callHandlers:1762 - 10.16.40.242:28130 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:46.527 | INFO | logging:callHandlers:1762 - 10.16.3.80:16651 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:09:46.529 | INFO | logging:callHandlers:1762 - 10.16.3.80:1171 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
[2026-05-28 08:10:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:10:03,238: INFO/MainProcess] Task triam.notifications.scan_due[aa97ee97-7375-46a6-b177-7924d5d698d2] received
2026-05-28 08:10:10.099 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:10:10,100: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[aa97ee97-7375-46a6-b177-7924d5d698d2] succeeded in 6.649499274324626s: None
[2026-05-28 08:11:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:11:03,075: INFO/MainProcess] Task triam.notifications.scan_due[977dce1d-cdc6-48fa-9b7b-c3b89bff3a8f] received
2026-05-28 08:11:11.611 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:11:11,612: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[977dce1d-cdc6-48fa-9b7b-c3b89bff3a8f] succeeded in 8.323931222781539s: None
[2026-05-28 08:12:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:12:02,859: INFO/MainProcess] Task triam.notifications.scan_due[3017152e-85ab-409c-b2ab-ced698bb9973] received
2026-05-28 08:12:09.854 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:12:09,855: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3017152e-85ab-409c-b2ab-ced698bb9973] succeeded in 6.994887323584408s: None
[2026-05-28 08:13:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:13:03,079: INFO/MainProcess] Task triam.notifications.scan_due[c8349b51-9dcb-4e66-8bbc-37aae77a9b82] received
2026-05-28 08:13:10.289 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:13:10,290: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c8349b51-9dcb-4e66-8bbc-37aae77a9b82] succeeded in 6.998076086863875s: None
[2026-05-28 08:14:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:14:02,860: INFO/MainProcess] Task triam.notifications.scan_due[0c66736e-95ef-4342-9ac5-4abb90b31666] received
2026-05-28 08:14:10.064 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:14:10,064: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[0c66736e-95ef-4342-9ac5-4abb90b31666] succeeded in 6.992423439864069s: None
[2026-05-28 08:15:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:15:03,250: INFO/MainProcess] Task triam.notifications.scan_due[76870576-f8b2-49e5-a37b-0153027b8083] received
2026-05-28 08:15:10.341 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:15:10,342: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[76870576-f8b2-49e5-a37b-0153027b8083] succeeded in 7.09062821790576s: None
[2026-05-28 08:16:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:16:03,227: INFO/MainProcess] Task triam.notifications.scan_due[3019f1ca-2916-469b-b262-6ec609dd4784] received
2026-05-28 08:16:10.223 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:16:10,224: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3019f1ca-2916-469b-b262-6ec609dd4784] succeeded in 6.995264035649598s: None
[2026-05-28 08:17:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:17:03,008: INFO/MainProcess] Task triam.notifications.scan_due[94a88f96-78ff-4f1a-8b52-83856cdbe0be] received
2026-05-28 08:17:10.006 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:17:10,006: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[94a88f96-78ff-4f1a-8b52-83856cdbe0be] succeeded in 6.997118304017931s: None
[2026-05-28 08:18:02,206: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:18:03,075: INFO/MainProcess] Task triam.notifications.scan_due[40aa53c5-6057-4073-97bc-d8d5aceeefec] received
2026-05-28 08:18:10.071 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:18:10,072: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[40aa53c5-6057-4073-97bc-d8d5aceeefec] succeeded in 6.995834039058536s: None
[2026-05-28 08:19:02,207: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:19:02,861: INFO/MainProcess] Task triam.notifications.scan_due[75abe9a1-9213-4dba-8891-132ce8f29149] received
2026-05-28 08:19:09.855 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:19:09,856: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[75abe9a1-9213-4dba-8891-132ce8f29149] succeeded in 6.9942561108618975s: None
[2026-05-28 08:20:02,207: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:20:03,077: INFO/MainProcess] Task triam.notifications.scan_due[644a3add-1261-4342-bd55-e708750b4946] received
2026-05-28 08:20:10.084 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:20:10,084: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[644a3add-1261-4342-bd55-e708750b4946] succeeded in 7.00602207519114s: None
[2026-05-28 08:21:02,207: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:21:03,149: INFO/MainProcess] Task triam.notifications.scan_due[f7c3dacb-f106-4bce-aee3-4e7d59e031f5] received
2026-05-28 08:21:04.024 | INFO | logging:callHandlers:1762 - 10.16.47.7:20902 - "GET /api/v1/books/4ef0ad48-0e8f-457d-b278-3d3fe3da0905/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:21:10.255 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:21:10,257: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f7c3dacb-f106-4bce-aee3-4e7d59e031f5] succeeded in 7.103132228832692s: None
2026-05-28 08:21:17.852 | INFO | logging:callHandlers:1762 - 10.16.3.80:19795 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:21:40.237 | INFO | logging:callHandlers:1762 - 10.16.37.205:7856 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-28 08:21:40.866 | INFO | logging:callHandlers:1762 - 10.16.3.80:58305 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 08:21:43.525 | INFO | logging:callHandlers:1762 - 10.16.37.205:7856 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
[2026-05-28 08:22:02,207: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:22:02,862: INFO/MainProcess] Task triam.notifications.scan_due[71875262-f183-4f3f-be3f-fa6862e3bde4] received
2026-05-28 08:22:09.872 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:22:09,874: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[71875262-f183-4f3f-be3f-fa6862e3bde4] succeeded in 7.010389807168394s: None
[2026-05-28 08:23:02,207: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:23:03,077: INFO/MainProcess] Task triam.notifications.scan_due[4d84a66a-bdbf-4420-9c4f-f59c665631b5] received
2026-05-28 08:23:10.173 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:23:10,174: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4d84a66a-bdbf-4420-9c4f-f59c665631b5] succeeded in 7.095611142925918s: None
[2026-05-28 08:24:02,207: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:24:02,867: INFO/MainProcess] Task triam.notifications.scan_due[0a0f0776-2cfd-4074-9033-d1cc2eb628e0] received
2026-05-28 08:24:09.974 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:24:09,975: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[0a0f0776-2cfd-4074-9033-d1cc2eb628e0] succeeded in 7.107321428135037s: None
[2026-05-28 08:25:02,207: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:25:03,081: INFO/MainProcess] Task triam.notifications.scan_due[dc80f035-a3bc-4c3a-a38a-3cb2afd5b922] received
2026-05-28 08:25:10.176 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:25:10,176: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[dc80f035-a3bc-4c3a-a38a-3cb2afd5b922] succeeded in 7.0944744613952935s: None
[2026-05-28 08:26:02,208: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:26:03,089: INFO/MainProcess] Task triam.notifications.scan_due[91d7ee61-3a94-4329-a2b1-54645764cbcf] received
2026-05-28 08:26:10.194 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:26:10,195: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[91d7ee61-3a94-4329-a2b1-54645764cbcf] succeeded in 7.1056398479267955s: None
[2026-05-28 08:27:02,208: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:27:02,874: INFO/MainProcess] Task triam.notifications.scan_due[1f3088bc-ed67-4eb6-80d2-95604cf3ef40] received
2026-05-28 08:27:09.983 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:27:09,984: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1f3088bc-ed67-4eb6-80d2-95604cf3ef40] succeeded in 7.107355104293674s: None
[2026-05-28 08:28:02,209: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:28:03,293: INFO/MainProcess] Task triam.notifications.scan_due[3b45df46-9c8a-4cdf-beb6-df8df422cdba] received
2026-05-28 08:28:10.404 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:28:10,404: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3b45df46-9c8a-4cdf-beb6-df8df422cdba] succeeded in 7.110689942725003s: None
[2026-05-28 08:29:02,209: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:29:03,109: INFO/MainProcess] Task triam.notifications.scan_due[dd89382b-406c-406a-b0cb-6a576e04f20f] received
2026-05-28 08:29:10.222 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:29:10,223: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[dd89382b-406c-406a-b0cb-6a576e04f20f] succeeded in 7.111430236138403s: None
[2026-05-28 08:30:02,209: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:30:03,090: INFO/MainProcess] Task triam.notifications.scan_due[ccef2a6f-29ed-42c6-bf3e-7b0b7b2c89a8] received
2026-05-28 08:30:10.033 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:30:10,033: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ccef2a6f-29ed-42c6-bf3e-7b0b7b2c89a8] succeeded in 6.94240335887298s: None
[2026-05-28 08:31:02,209: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:31:03,087: INFO/MainProcess] Task triam.notifications.scan_due[5c1e216f-aee2-46fb-b5e1-088fbae7e5b8] received
2026-05-28 08:31:10.030 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:31:10,031: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5c1e216f-aee2-46fb-b5e1-088fbae7e5b8] succeeded in 6.942683978006244s: None
[2026-05-28 08:32:02,209: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:32:02,946: INFO/MainProcess] Task triam.notifications.scan_due[e1aa6b01-9b95-4c9f-b89b-6d41b2e6b6d6] received
2026-05-28 08:32:09.878 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:32:09,879: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e1aa6b01-9b95-4c9f-b89b-6d41b2e6b6d6] succeeded in 6.93172640632838s: None
[2026-05-28 08:33:02,209: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:33:03,086: INFO/MainProcess] Task triam.notifications.scan_due[bb8037ae-b833-439e-93f8-1cea46c98d83] received
2026-05-28 08:33:10.033 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:33:10,033: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[bb8037ae-b833-439e-93f8-1cea46c98d83] succeeded in 6.946331021841615s: None
[2026-05-28 08:34:02,211: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:34:02,867: INFO/MainProcess] Task triam.notifications.scan_due[cc40f3c2-7175-4e93-83db-d749d5445e1f] received
2026-05-28 08:34:09.929 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:34:09,929: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[cc40f3c2-7175-4e93-83db-d749d5445e1f] succeeded in 7.060843609273434s: None
[2026-05-28 08:35:02,211: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:35:03,238: INFO/MainProcess] Task triam.notifications.scan_due[2c2f10f7-4673-4a44-8a5b-7236793befcd] received
2026-05-28 08:35:10.175 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:35:10,176: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2c2f10f7-4673-4a44-8a5b-7236793befcd] succeeded in 6.936458626296371s: None
[2026-05-28 08:36:02,211: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:36:03,081: INFO/MainProcess] Task triam.notifications.scan_due[2e7da2a6-fba8-4999-bb8b-b8c0feef06f3] received
2026-05-28 08:36:10.010 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:36:10,011: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2e7da2a6-fba8-4999-bb8b-b8c0feef06f3] succeeded in 6.929476422723383s: None
[2026-05-28 08:37:02,211: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:37:03,081: INFO/MainProcess] Task triam.notifications.scan_due[9cdabe79-772d-457b-8b60-1c794a602dbd] received
2026-05-28 08:37:10.018 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:37:10,018: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[9cdabe79-772d-457b-8b60-1c794a602dbd] succeeded in 6.936994994059205s: None
[2026-05-28 08:38:02,211: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:38:03,080: INFO/MainProcess] Task triam.notifications.scan_due[acea1ee5-6f38-40a6-af95-8a2ee54772ac] received
2026-05-28 08:38:10.124 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:38:10,127: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[acea1ee5-6f38-40a6-af95-8a2ee54772ac] succeeded in 7.045628394931555s: None
[2026-05-28 08:39:02,211: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:39:02,865: INFO/MainProcess] Task triam.notifications.scan_due[7527150e-9147-420f-8ccc-830ecc448857] received
2026-05-28 08:39:09.907 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:39:09,908: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7527150e-9147-420f-8ccc-830ecc448857] succeeded in 7.041985672898591s: None
[2026-05-28 08:40:02,211: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:40:03,240: INFO/MainProcess] Task triam.notifications.scan_due[bbb5ecf7-f4dd-4e10-b24e-22840385519d] received
2026-05-28 08:40:10.481 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:40:10,482: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[bbb5ecf7-f4dd-4e10-b24e-22840385519d] succeeded in 7.0295520490035415s: None
[2026-05-28 08:41:02,211: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:41:03,238: INFO/MainProcess] Task triam.notifications.scan_due[946be3d8-4b03-435e-9f1c-3c99a2c74814] received
2026-05-28 08:41:11.629 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:41:11,629: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[946be3d8-4b03-435e-9f1c-3c99a2c74814] succeeded in 8.178305707871914s: None
[2026-05-28 08:42:02,211: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:42:03,206: INFO/MainProcess] Task triam.notifications.scan_due[75bacd96-7977-4d44-bb08-c0d5d3466d1e] received
2026-05-28 08:42:10.338 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:42:10,339: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[75bacd96-7977-4d44-bb08-c0d5d3466d1e] succeeded in 6.920507172122598s: None
[2026-05-28 08:43:02,211: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:43:03,240: INFO/MainProcess] Task triam.notifications.scan_due[d784829e-71c4-4a17-88a0-c9c628ba597a] received
2026-05-28 08:43:10.295 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:43:10,295: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d784829e-71c4-4a17-88a0-c9c628ba597a] succeeded in 6.842553173657507s: None
[2026-05-28 08:44:02,211: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:44:03,023: INFO/MainProcess] Task triam.notifications.scan_due[8b40481d-f39a-445f-9c74-f8cfef6fe066] received
2026-05-28 08:44:09.854 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:44:09,855: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8b40481d-f39a-445f-9c74-f8cfef6fe066] succeeded in 6.8312530922703445s: None
[2026-05-28 08:45:02,212: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:45:03,080: INFO/MainProcess] Task triam.notifications.scan_due[17fcd011-bd85-4781-b8af-62b91c584f7c] received
2026-05-28 08:45:09.915 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:45:09,915: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[17fcd011-bd85-4781-b8af-62b91c584f7c] succeeded in 6.8340134979225695s: None
[2026-05-28 08:46:02,212: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:46:03,078: INFO/MainProcess] Task triam.notifications.scan_due[23b44b15-fefc-4ce2-acab-63a3a3485dcb] received
2026-05-28 08:46:09.907 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:46:09,907: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[23b44b15-fefc-4ce2-acab-63a3a3485dcb] succeeded in 6.828490153886378s: None
[2026-05-28 08:47:02,212: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:47:03,081: INFO/MainProcess] Task triam.notifications.scan_due[ad7a33b0-e5c3-4742-befb-d7d61eb44cf3] received
2026-05-28 08:47:09.927 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:47:09,928: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ad7a33b0-e5c3-4742-befb-d7d61eb44cf3] succeeded in 6.842114177998155s: None
[2026-05-28 08:48:02,212: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:48:03,078: INFO/MainProcess] Task triam.notifications.scan_due[9cb5ca0b-b20b-4bfb-8e55-13614a1bdcc8] received
2026-05-28 08:48:09.917 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:48:09,918: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[9cb5ca0b-b20b-4bfb-8e55-13614a1bdcc8] succeeded in 6.838613457977772s: None
[2026-05-28 08:49:02,212: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:49:02,863: INFO/MainProcess] Task triam.notifications.scan_due[99526d39-df18-4c00-9bd0-845a02c22038] received
2026-05-28 08:49:09.692 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:49:09,692: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[99526d39-df18-4c00-9bd0-845a02c22038] succeeded in 6.828725622966886s: None
[2026-05-28 08:50:02,213: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:50:03,238: INFO/MainProcess] Task triam.notifications.scan_due[10b90b25-c0de-42c9-a1ab-f25a1a13f01d] received
2026-05-28 08:50:10.070 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:50:10,070: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[10b90b25-c0de-42c9-a1ab-f25a1a13f01d] succeeded in 6.831703982781619s: None
[2026-05-28 08:51:02,221: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:51:03,093: INFO/MainProcess] Task triam.notifications.scan_due[b2e9d964-c271-4efe-9d78-2de52a012a0a] received
2026-05-28 08:51:09.932 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:51:09,933: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b2e9d964-c271-4efe-9d78-2de52a012a0a] succeeded in 6.838475220836699s: None
[2026-05-28 08:52:02,221: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:52:03,087: INFO/MainProcess] Task triam.notifications.scan_due[701ace87-ad85-4d24-99d4-76c194a00e9b] received
2026-05-28 08:52:09.924 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:52:09,924: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[701ace87-ad85-4d24-99d4-76c194a00e9b] succeeded in 6.83527739206329s: None
[2026-05-28 08:53:02,221: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:53:03,087: INFO/MainProcess] Task triam.notifications.scan_due[dca08d72-c8e3-4b01-89fa-d757bfa7b0f7] received
2026-05-28 08:53:09.925 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:53:09,926: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[dca08d72-c8e3-4b01-89fa-d757bfa7b0f7] succeeded in 6.838103772141039s: None
[2026-05-28 08:54:02,221: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:54:02,872: INFO/MainProcess] Task triam.notifications.scan_due[cea93720-0a5e-45c0-90c4-f6020e8351e7] received
2026-05-28 08:54:09.781 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:54:09,782: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[cea93720-0a5e-45c0-90c4-f6020e8351e7] succeeded in 6.909069872926921s: None
[2026-05-28 08:55:02,221: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:55:03,088: INFO/MainProcess] Task triam.notifications.scan_due[23d32a1e-1988-496b-afd0-d80a9e284e6a] received
2026-05-28 08:55:09.921 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:55:09,921: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[23d32a1e-1988-496b-afd0-d80a9e284e6a] succeeded in 6.8321841498836875s: None
[2026-05-28 08:56:02,221: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:56:02,876: INFO/MainProcess] Task triam.notifications.scan_due[388f9a7e-289a-49e5-b492-a7115388a3f1] received
2026-05-28 08:56:09.717 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:56:09,718: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[388f9a7e-289a-49e5-b492-a7115388a3f1] succeeded in 6.840053224004805s: None
[2026-05-28 08:57:02,221: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:57:03,089: INFO/MainProcess] Task triam.notifications.scan_due[b4a408e2-e752-41cc-aa5e-5f5068c64fff] received
2026-05-28 08:57:09.923 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:57:09,924: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b4a408e2-e752-41cc-aa5e-5f5068c64fff] succeeded in 6.834110274910927s: None
[2026-05-28 08:58:02,221: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:58:03,088: INFO/MainProcess] Task triam.notifications.scan_due[ff7a75e4-7afc-428a-bde1-f821ce514046] received
2026-05-28 08:58:09.934 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:58:09,935: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ff7a75e4-7afc-428a-bde1-f821ce514046] succeeded in 6.8456138712354s: None
[2026-05-28 08:59:02,222: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 08:59:02,877: INFO/MainProcess] Task triam.notifications.scan_due[2f18e176-7484-4ecf-a146-49234139327b] received
2026-05-28 08:59:09.714 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 08:59:09,714: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2f18e176-7484-4ecf-a146-49234139327b] succeeded in 6.836004716809839s: None
[2026-05-28 09:00:02,222: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:00:03,088: INFO/MainProcess] Task triam.notifications.scan_due[02c0bfbb-f008-4203-90dd-d4f60c94a13f] received
2026-05-28 09:00:09.920 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:00:09,922: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[02c0bfbb-f008-4203-90dd-d4f60c94a13f] succeeded in 6.8311311192810535s: None
[2026-05-28 09:01:02,222: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:01:02,874: INFO/MainProcess] Task triam.notifications.scan_due[5b677719-5373-46de-ab65-c98b18239562] received
2026-05-28 09:01:09.708 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:01:09,709: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5b677719-5373-46de-ab65-c98b18239562] succeeded in 6.834376900922507s: None
[2026-05-28 09:02:02,222: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:02:03,090: INFO/MainProcess] Task triam.notifications.scan_due[e8b90eaa-8a1f-4360-aefb-880760881dd1] received
2026-05-28 09:02:09.928 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:02:09,929: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e8b90eaa-8a1f-4360-aefb-880760881dd1] succeeded in 6.8377561857923865s: None
[2026-05-28 09:03:02,222: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:03:03,091: INFO/MainProcess] Task triam.notifications.scan_due[e6571e93-8b96-4d51-9525-07cca55cbb79] received
2026-05-28 09:03:09.927 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:03:09,930: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e6571e93-8b96-4d51-9525-07cca55cbb79] succeeded in 6.837989019695669s: None
[2026-05-28 09:04:02,222: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:04:02,873: INFO/MainProcess] Task triam.notifications.scan_due[e18be430-c938-4002-b2ca-465db4be2c7f] received
2026-05-28 09:04:09.704 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:04:09,705: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e18be430-c938-4002-b2ca-465db4be2c7f] succeeded in 6.8304335358552635s: None
[2026-05-28 09:05:02,222: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:05:03,088: INFO/MainProcess] Task triam.notifications.scan_due[083e01f9-fd9d-4122-a22a-bbc86cdb5878] received
2026-05-28 09:05:10.015 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:05:10,016: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[083e01f9-fd9d-4122-a22a-bbc86cdb5878] succeeded in 6.926021289080381s: None
[2026-05-28 09:06:02,222: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:06:03,023: INFO/MainProcess] Task triam.notifications.scan_due[2df1f6ac-5bf4-49ce-9321-c47e761ed006] received
2026-05-28 09:06:09.871 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:06:09,873: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2df1f6ac-5bf4-49ce-9321-c47e761ed006] succeeded in 6.848697013221681s: None
[2026-05-28 09:07:02,223: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:07:03,239: INFO/MainProcess] Task triam.notifications.scan_due[2d4d5da3-43f2-4007-b5cc-d927e143b594] received
2026-05-28 09:07:10.082 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:07:10,082: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2d4d5da3-43f2-4007-b5cc-d927e143b594] succeeded in 6.84181026276201s: None
[2026-05-28 09:08:02,223: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:08:03,201: INFO/MainProcess] Task triam.notifications.scan_due[e0c5f6db-8417-4924-83cb-6e33b409bee6] received
2026-05-28 09:08:10.054 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:08:10,055: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e0c5f6db-8417-4924-83cb-6e33b409bee6] succeeded in 6.8523884220048785s: None
[2026-05-28 09:09:02,223: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:09:02,941: INFO/MainProcess] Task triam.notifications.scan_due[cb0672ca-c14a-443b-8337-3ea5c9942903] received
2026-05-28 09:09:09.778 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:09:09,779: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[cb0672ca-c14a-443b-8337-3ea5c9942903] succeeded in 6.836806203238666s: None
[2026-05-28 09:10:02,223: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:10:03,096: INFO/MainProcess] Task triam.notifications.scan_due[9d965458-47f0-4d74-97db-5a5e1b6932b0] received
2026-05-28 09:10:09.925 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:10:09,925: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[9d965458-47f0-4d74-97db-5a5e1b6932b0] succeeded in 6.828755149617791s: None
[2026-05-28 09:11:02,224: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:11:03,108: INFO/MainProcess] Task triam.notifications.scan_due[69d18716-b73f-452a-afb3-91ca49c900ec] received
2026-05-28 09:11:10.034 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:11:10,036: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[69d18716-b73f-452a-afb3-91ca49c900ec] succeeded in 6.923556094989181s: None
[2026-05-28 09:12:02,224: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:12:03,091: INFO/MainProcess] Task triam.notifications.scan_due[5f65a5e9-735c-4440-b23f-75bc04ce763e] received
2026-05-28 09:12:11.308 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:12:11,309: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5f65a5e9-735c-4440-b23f-75bc04ce763e] succeeded in 8.216529783792794s: None
[2026-05-28 09:13:02,224: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:13:03,090: INFO/MainProcess] Task triam.notifications.scan_due[4d818fa2-5dcd-46e8-bb74-427181a4c028] received
2026-05-28 09:13:09.976 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:13:09,976: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4d818fa2-5dcd-46e8-bb74-427181a4c028] succeeded in 6.885570950806141s: None
[2026-05-28 09:14:02,224: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:14:03,145: INFO/MainProcess] Task triam.notifications.scan_due[6d6a19e9-a869-49aa-b2f5-55f03d899d21] received
2026-05-28 09:14:10.019 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:14:10,020: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[6d6a19e9-a869-49aa-b2f5-55f03d899d21] succeeded in 6.874398028943688s: None
[2026-05-28 09:15:02,224: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:15:03,091: INFO/MainProcess] Task triam.notifications.scan_due[45683f4b-26fa-4539-98a9-b69a8910c918] received
2026-05-28 09:15:09.969 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:15:09,970: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[45683f4b-26fa-4539-98a9-b69a8910c918] succeeded in 6.877983562648296s: None
[2026-05-28 09:16:02,224: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:16:02,875: INFO/MainProcess] Task triam.notifications.scan_due[08169c43-767e-4a73-91f0-28def591f752] received
2026-05-28 09:16:09.747 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:16:09,748: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[08169c43-767e-4a73-91f0-28def591f752] succeeded in 6.87196817714721s: None
[2026-05-28 09:17:02,225: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:17:03,092: INFO/MainProcess] Task triam.notifications.scan_due[3cc8f9c3-f441-4f13-a260-bc87159ac485] received
2026-05-28 09:17:09.975 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:17:09,976: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3cc8f9c3-f441-4f13-a260-bc87159ac485] succeeded in 6.879947931971401s: None
[2026-05-28 09:18:02,225: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:18:03,091: INFO/MainProcess] Task triam.notifications.scan_due[b9ae68b0-3dc0-467f-9f0a-b3f5f7ee907e] received
2026-05-28 09:18:09.969 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:18:09,975: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b9ae68b0-3dc0-467f-9f0a-b3f5f7ee907e] succeeded in 6.882687246892601s: None
[2026-05-28 09:19:02,225: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:19:03,185: INFO/MainProcess] Task triam.notifications.scan_due[1e1698dd-17b6-419d-adec-6c6447e94e46] received
2026-05-28 09:19:10.063 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:19:10,063: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1e1698dd-17b6-419d-adec-6c6447e94e46] succeeded in 6.877772302832454s: None
[2026-05-28 09:20:02,225: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:20:03,177: INFO/MainProcess] Task triam.notifications.scan_due[efc8aac1-5d89-4a91-94d9-2653bfe8c7cb] received
2026-05-28 09:20:10.053 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:20:10,054: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[efc8aac1-5d89-4a91-94d9-2653bfe8c7cb] succeeded in 6.876136058010161s: None
[2026-05-28 09:21:02,225: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:21:02,915: INFO/MainProcess] Task triam.notifications.scan_due[32f12a10-569d-4088-b363-eeff32213165] received
2026-05-28 09:21:09.794 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:21:09,794: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[32f12a10-569d-4088-b363-eeff32213165] succeeded in 6.877928473986685s: None
[2026-05-28 09:22:02,226: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:22:03,092: INFO/MainProcess] Task triam.notifications.scan_due[748a5bf3-56ff-4964-a74e-4544f94d7fa9] received
2026-05-28 09:22:09.975 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:22:09,976: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[748a5bf3-56ff-4964-a74e-4544f94d7fa9] succeeded in 6.883612047880888s: None
[2026-05-28 09:23:02,226: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:23:03,236: INFO/MainProcess] Task triam.notifications.scan_due[ce8c426a-7f61-4bcd-b1c0-3538bcc36468] received
2026-05-28 09:23:10.120 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:23:10,121: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ce8c426a-7f61-4bcd-b1c0-3538bcc36468] succeeded in 6.883156147785485s: None
[2026-05-28 09:24:02,226: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:24:03,092: INFO/MainProcess] Task triam.notifications.scan_due[cd504514-1061-4d3d-a1ca-0b711e9b93e4] received
2026-05-28 09:24:13.170 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=1 | recovered=0 | should_deliver=True
[2026-05-28 09:24:16,095: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[cd504514-1061-4d3d-a1ca-0b711e9b93e4] succeeded in 13.002342548687011s: None
[2026-05-28 09:24:16,964: INFO/MainProcess] Task triam.notifications.deliver_due[2ff37cc9-3fc5-4bea-b4fd-e2ae42b98c9a] received
2026-05-28 09:24:21.243 | INFO | app.tasks.notification_tasks:deliver_due_notifications_task:67 - Notification delivery batch done | worker_id=notification-worker:6aac17f1-c0be-4692-91b2-922eca77d7d4 | delivered_attempts=1
[2026-05-28 09:24:21,244: INFO/ForkPoolWorker-1] Task triam.notifications.deliver_due[2ff37cc9-3fc5-4bea-b4fd-e2ae42b98c9a] succeeded in 4.278416201006621s: None
[2026-05-28 09:25:02,226: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:25:03,094: INFO/MainProcess] Task triam.notifications.scan_due[3572f872-4521-4e54-9f7d-0ec6f514c9b6] received
2026-05-28 09:25:13.207 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=1 | recovered=0 | should_deliver=True
[2026-05-28 09:25:13,664: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3572f872-4521-4e54-9f7d-0ec6f514c9b6] succeeded in 10.348817557096481s: None
[2026-05-28 09:25:14,317: INFO/MainProcess] Task triam.notifications.deliver_due[e0220946-6287-449a-9634-493a1940c414] received
2026-05-28 09:25:18.757 | INFO | app.tasks.notification_tasks:deliver_due_notifications_task:67 - Notification delivery batch done | worker_id=notification-worker:4ebcac8b-b541-48b3-9905-50d2c39dcb8e | delivered_attempts=1
[2026-05-28 09:25:18,758: INFO/ForkPoolWorker-1] Task triam.notifications.deliver_due[e0220946-6287-449a-9634-493a1940c414] succeeded in 4.217507341876626s: None
[2026-05-28 09:26:02,226: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:26:02,879: INFO/MainProcess] Task triam.notifications.scan_due[6633ff6c-b5cb-49ff-b0d3-180f30d3aac4] received
2026-05-28 09:26:09.775 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:26:09,777: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[6633ff6c-b5cb-49ff-b0d3-180f30d3aac4] succeeded in 6.89670060062781s: None
[2026-05-28 09:27:02,227: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:27:03,095: INFO/MainProcess] Task triam.notifications.scan_due[04b0e71b-34a1-494c-8505-72404dabb45c] received
2026-05-28 09:27:10.080 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:27:10,082: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[04b0e71b-34a1-494c-8505-72404dabb45c] succeeded in 6.984914120286703s: None
[2026-05-28 09:28:02,227: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:28:03,243: INFO/MainProcess] Task triam.notifications.scan_due[cb63cb9a-6161-4e09-a294-2682772de0c8] received
2026-05-28 09:28:10.214 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:28:10,214: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[cb63cb9a-6161-4e09-a294-2682772de0c8] succeeded in 6.969701127614826s: None
[2026-05-28 09:29:02,227: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:29:03,093: INFO/MainProcess] Task triam.notifications.scan_due[e1e48c32-6d6f-402a-a447-d067c438cdcc] received
2026-05-28 09:29:10.065 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:29:10,066: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e1e48c32-6d6f-402a-a447-d067c438cdcc] succeeded in 6.971194413024932s: None
[2026-05-28 09:30:02,227: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:30:03,094: INFO/MainProcess] Task triam.notifications.scan_due[9d760d9e-6c58-4905-8a1f-4fb4e5917ce6] received
2026-05-28 09:30:10.063 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:30:10,063: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[9d760d9e-6c58-4905-8a1f-4fb4e5917ce6] succeeded in 6.968523758929223s: None
[2026-05-28 09:31:02,227: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:31:02,878: INFO/MainProcess] Task triam.notifications.scan_due[3152e4af-d561-49e9-bef0-a2768658b56b] received
2026-05-28 09:31:09.850 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:31:09,851: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3152e4af-d561-49e9-bef0-a2768658b56b] succeeded in 6.971630041021854s: None
[2026-05-28 09:32:02,227: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:32:03,096: INFO/MainProcess] Task triam.notifications.scan_due[6de45c7e-d7a8-445d-85e6-727314a90072] received
2026-05-28 09:32:10.085 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:32:10,086: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[6de45c7e-d7a8-445d-85e6-727314a90072] succeeded in 6.989190544001758s: None
[2026-05-28 09:33:02,227: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:33:02,879: INFO/MainProcess] Task triam.notifications.scan_due[e04dc1c0-4da5-4996-a489-777e49173470] received
2026-05-28 09:33:09.858 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:33:09,859: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e04dc1c0-4da5-4996-a489-777e49173470] succeeded in 6.978807561099529s: None
[2026-05-28 09:34:02,227: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:34:03,094: INFO/MainProcess] Task triam.notifications.scan_due[c3cde958-45fc-481e-8eb5-4a10fb8cf31f] received
2026-05-28 09:34:09.916 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:34:09,916: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c3cde958-45fc-481e-8eb5-4a10fb8cf31f] succeeded in 6.818031964823604s: None
[2026-05-28 09:35:02,228: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:35:03,091: INFO/MainProcess] Task triam.notifications.scan_due[67deb11c-e23e-421b-b1ea-c2bfef5963f6] received
2026-05-28 09:35:10.049 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:35:10,050: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[67deb11c-e23e-421b-b1ea-c2bfef5963f6] succeeded in 6.958250334952027s: None
[2026-05-28 09:36:02,228: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:36:02,878: INFO/MainProcess] Task triam.notifications.scan_due[fc099ac9-9854-4309-a069-83ecd5fe3346] received
2026-05-28 09:36:09.781 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:36:09,781: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[fc099ac9-9854-4309-a069-83ecd5fe3346] succeeded in 6.90290604904294s: None
[2026-05-28 09:37:02,228: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:37:03,234: INFO/MainProcess] Task triam.notifications.scan_due[a2f5b621-af75-4ce2-8055-4c21cea945df] received
2026-05-28 09:37:10.109 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:37:10,117: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a2f5b621-af75-4ce2-8055-4c21cea945df] succeeded in 6.882662820164114s: None
[2026-05-28 09:38:02,228: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:38:02,877: INFO/MainProcess] Task triam.notifications.scan_due[97a18970-30cb-41e4-a300-352c7f0d7a30] received
2026-05-28 09:38:09.756 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:38:09,756: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[97a18970-30cb-41e4-a300-352c7f0d7a30] succeeded in 6.87746702414006s: None
[2026-05-28 09:39:02,228: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:39:03,092: INFO/MainProcess] Task triam.notifications.scan_due[7eec11c8-b1b2-45b3-9336-0082b7a631cc] received
2026-05-28 09:39:09.962 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:39:09,963: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7eec11c8-b1b2-45b3-9336-0082b7a631cc] succeeded in 6.870110529009253s: None
[2026-05-28 09:40:02,228: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:40:03,089: INFO/MainProcess] Task triam.notifications.scan_due[9edd43be-1139-46ea-bb18-7afb174b2b8e] received
2026-05-28 09:40:09.963 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:40:09,964: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[9edd43be-1139-46ea-bb18-7afb174b2b8e] succeeded in 6.8713224972598255s: None
[2026-05-28 09:41:02,228: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:41:02,877: INFO/MainProcess] Task triam.notifications.scan_due[720a0ed6-7054-4b12-b30d-56edec55bb23] received
2026-05-28 09:41:09.881 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:41:09,881: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[720a0ed6-7054-4b12-b30d-56edec55bb23] succeeded in 7.002216395922005s: None
[2026-05-28 09:42:02,228: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:42:03,164: INFO/MainProcess] Task triam.notifications.scan_due[f22fc4c2-00d7-4c6a-b8ad-0f5f8c4e4b99] received
2026-05-28 09:42:11.298 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:42:11,298: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f22fc4c2-00d7-4c6a-b8ad-0f5f8c4e4b99] succeeded in 8.133281601127237s: None
[2026-05-28 09:43:02,228: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:43:02,877: INFO/MainProcess] Task triam.notifications.scan_due[2f2e18f2-b30d-47f1-a95e-848bdb177d8f] received
2026-05-28 09:43:09.690 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:43:09,690: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2f2e18f2-b30d-47f1-a95e-848bdb177d8f] succeeded in 6.811841670423746s: None
[2026-05-28 09:44:02,228: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:44:03,093: INFO/MainProcess] Task triam.notifications.scan_due[24cc3283-eba3-426c-a11f-6a879a085be9] received
2026-05-28 09:44:09.915 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:44:09,915: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[24cc3283-eba3-426c-a11f-6a879a085be9] succeeded in 6.8211015104316175s: None
[2026-05-28 09:45:02,228: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:45:03,089: INFO/MainProcess] Task triam.notifications.scan_due[58f6dc3c-6a29-48ee-af91-a1b57c0c678a] received
2026-05-28 09:45:12.818 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=1 | recovered=0 | should_deliver=True
[2026-05-28 09:45:13,278: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[58f6dc3c-6a29-48ee-af91-a1b57c0c678a] succeeded in 10.18854502774775s: None
[2026-05-28 09:45:13,927: INFO/MainProcess] Task triam.notifications.deliver_due[fa4d5296-fb71-4611-8cf9-717d40aecae1] received
2026-05-28 09:45:18.110 | INFO | app.tasks.notification_tasks:deliver_due_notifications_task:67 - Notification delivery batch done | worker_id=notification-worker:d71cebcf-11a4-40dd-a171-517f13e18ae6 | delivered_attempts=1
[2026-05-28 09:45:18,111: INFO/ForkPoolWorker-1] Task triam.notifications.deliver_due[fa4d5296-fb71-4611-8cf9-717d40aecae1] succeeded in 4.182648809161037s: None
[2026-05-28 09:46:02,228: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:46:02,878: INFO/MainProcess] Task triam.notifications.scan_due[0646d84e-4655-416e-a0bc-50525402db24] received
2026-05-28 09:46:09.703 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:46:09,705: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[0646d84e-4655-416e-a0bc-50525402db24] succeeded in 6.824729116167873s: None
[2026-05-28 09:47:02,228: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:47:03,090: INFO/MainProcess] Task triam.notifications.scan_due[9f7fbb07-eeaf-49f8-bc03-8ac3b41701c2] received
2026-05-28 09:47:12.778 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=1 | recovered=0 | should_deliver=True
[2026-05-28 09:47:13,237: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[9f7fbb07-eeaf-49f8-bc03-8ac3b41701c2] succeeded in 10.144946893677115s: None
[2026-05-28 09:47:14,102: INFO/MainProcess] Task triam.notifications.deliver_due[770be932-e2a7-4ca1-bd84-82cc7e6b1be0] received
2026-05-28 09:47:18.277 | INFO | app.tasks.notification_tasks:deliver_due_notifications_task:67 - Notification delivery batch done | worker_id=notification-worker:4a9a7eaa-2bf0-4319-abac-6b8896c69c6b | delivered_attempts=1
[2026-05-28 09:47:18,278: INFO/ForkPoolWorker-1] Task triam.notifications.deliver_due[770be932-e2a7-4ca1-bd84-82cc7e6b1be0] succeeded in 4.175801503006369s: None
[2026-05-28 09:48:02,228: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:48:02,877: INFO/MainProcess] Task triam.notifications.scan_due[d1f89bb3-76c1-405f-9875-b3d11321cd35] received
2026-05-28 09:48:12.564 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=1 | recovered=0 | should_deliver=True
[2026-05-28 09:48:13,026: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d1f89bb3-76c1-405f-9875-b3d11321cd35] succeeded in 10.148132321890444s: None
[2026-05-28 09:48:13,828: INFO/MainProcess] Task triam.notifications.deliver_due[40a56c83-eeab-4e52-b1f5-4d02f2a56556] received
2026-05-28 09:48:18.004 | INFO | app.tasks.notification_tasks:deliver_due_notifications_task:67 - Notification delivery batch done | worker_id=notification-worker:91dcded3-5052-46f5-8b72-2b19f2698a06 | delivered_attempts=1
[2026-05-28 09:48:18,005: INFO/ForkPoolWorker-1] Task triam.notifications.deliver_due[40a56c83-eeab-4e52-b1f5-4d02f2a56556] succeeded in 4.175661758054048s: None
[2026-05-28 09:49:02,229: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:49:03,090: INFO/MainProcess] Task triam.notifications.scan_due[6fbbddb8-e35e-4d79-9780-3f05596da756] received
2026-05-28 09:49:09.938 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:49:09,939: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[6fbbddb8-e35e-4d79-9780-3f05596da756] succeeded in 6.8477268582209945s: None
[2026-05-28 09:50:02,229: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:50:03,095: INFO/MainProcess] Task triam.notifications.scan_due[066d80f6-8b5f-463f-8501-48ce018ae383] received
2026-05-28 09:50:12.666 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=1 | recovered=0 | should_deliver=True
[2026-05-28 09:50:13,122: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[066d80f6-8b5f-463f-8501-48ce018ae383] succeeded in 10.025897118262947s: None
[2026-05-28 09:50:13,991: INFO/MainProcess] Task triam.notifications.deliver_due[ce69ff03-0d6d-4ef2-93b0-08376596df3c] received
2026-05-28 09:50:18.121 | INFO | app.tasks.notification_tasks:deliver_due_notifications_task:67 - Notification delivery batch done | worker_id=notification-worker:4342e11c-ddd0-4505-bdda-fa41c20d0ccc | delivered_attempts=1
[2026-05-28 09:50:18,122: INFO/ForkPoolWorker-1] Task triam.notifications.deliver_due[ce69ff03-0d6d-4ef2-93b0-08376596df3c] succeeded in 4.130233873147517s: None
[2026-05-28 09:51:02,229: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:51:03,150: INFO/MainProcess] Task triam.notifications.scan_due[76e6b176-1680-4cf9-83d9-d796c0783ecf] received
2026-05-28 09:51:09.891 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:51:09,892: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[76e6b176-1680-4cf9-83d9-d796c0783ecf] succeeded in 6.740569890011102s: None
[2026-05-28 09:52:02,229: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:52:03,310: INFO/MainProcess] Task triam.notifications.scan_due[b410155b-6f79-4d70-8548-a9fa743f3116] received
2026-05-28 09:52:10.257 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:52:10,258: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b410155b-6f79-4d70-8548-a9fa743f3116] succeeded in 6.945425957906991s: None
[2026-05-28 09:53:02,229: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:53:02,882: INFO/MainProcess] Task triam.notifications.scan_due[9fc9a624-819b-4ecb-9297-fcf19618eada] received
2026-05-28 09:53:09.826 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:53:09,827: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[9fc9a624-819b-4ecb-9297-fcf19618eada] succeeded in 6.943753772880882s: None
[2026-05-28 09:54:02,231: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:54:03,100: INFO/MainProcess] Task triam.notifications.scan_due[d954cb69-b5c8-4024-8c5f-e20a880bb659] received
2026-05-28 09:54:09.933 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:54:09,934: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d954cb69-b5c8-4024-8c5f-e20a880bb659] succeeded in 6.832899750210345s: None
[2026-05-28 09:55:02,231: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:55:03,096: INFO/MainProcess] Task triam.notifications.scan_due[fe1d466c-b950-4b3b-a735-1f4059a61eaf] received
2026-05-28 09:55:09.932 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:55:09,934: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[fe1d466c-b950-4b3b-a735-1f4059a61eaf] succeeded in 6.836180847138166s: None
[2026-05-28 09:56:02,231: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:56:03,118: INFO/MainProcess] Task triam.notifications.scan_due[ac180fb3-d216-4116-bf41-7e6ee69824b9] received
2026-05-28 09:56:09.958 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:56:09,960: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ac180fb3-d216-4116-bf41-7e6ee69824b9] succeeded in 6.8401937442831695s: None
[2026-05-28 09:57:02,231: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:57:03,117: INFO/MainProcess] Task triam.notifications.scan_due[73d164e9-c0d6-41ae-8c4f-ee615a8437a8] received
2026-05-28 09:57:10.168 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:57:10,169: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[73d164e9-c0d6-41ae-8c4f-ee615a8437a8] succeeded in 6.831822942942381s: None
[2026-05-28 09:58:02,231: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:58:02,904: INFO/MainProcess] Task triam.notifications.scan_due[721305ea-5f37-417c-bfed-b5294e1e4603] received
2026-05-28 09:58:09.744 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:58:09,744: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[721305ea-5f37-417c-bfed-b5294e1e4603] succeeded in 6.83994306717068s: None
[2026-05-28 09:59:02,231: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 09:59:03,119: INFO/MainProcess] Task triam.notifications.scan_due[ca9d55d7-a001-4c3d-8e38-d3e83a3f4687] received
2026-05-28 09:59:10.062 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 09:59:10,063: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ca9d55d7-a001-4c3d-8e38-d3e83a3f4687] succeeded in 6.942065842915326s: None
[2026-05-28 10:00:02,231: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:00:03,119: INFO/MainProcess] Task triam.notifications.scan_due[f46e1ea4-7c4a-446b-a4c6-7a784c879913] received
2026-05-28 10:00:10.066 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:00:10,067: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f46e1ea4-7c4a-446b-a4c6-7a784c879913] succeeded in 6.944675230886787s: None
[2026-05-28 10:01:02,231: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:01:03,119: INFO/MainProcess] Task triam.notifications.scan_due[3c1474ee-a553-4bde-8a69-ce3992e6ef84] received
2026-05-28 10:01:10.064 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:01:10,065: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3c1474ee-a553-4bde-8a69-ce3992e6ef84] succeeded in 6.944868000224233s: None
[2026-05-28 10:02:02,231: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:02:03,120: INFO/MainProcess] Task triam.notifications.scan_due[295c237b-a7f4-4f60-b01e-a22563189eab] received
2026-05-28 10:02:10.068 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:02:10,068: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[295c237b-a7f4-4f60-b01e-a22563189eab] succeeded in 6.946793590206653s: None
[2026-05-28 10:03:02,231: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:03:02,903: INFO/MainProcess] Task triam.notifications.scan_due[d2585d4e-ad7a-44a0-a574-56203b9ab8c7] received
2026-05-28 10:03:09.820 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:03:09,821: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d2585d4e-ad7a-44a0-a574-56203b9ab8c7] succeeded in 6.917225851211697s: None
[2026-05-28 10:04:02,231: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:04:03,120: INFO/MainProcess] Task triam.notifications.scan_due[10040ba4-a1e0-4f09-b3a6-04f5b4a1672a] received
2026-05-28 10:04:10.048 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:04:10,049: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[10040ba4-a1e0-4f09-b3a6-04f5b4a1672a] succeeded in 6.928207385819405s: None
[2026-05-28 10:05:02,231: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:05:03,163: INFO/MainProcess] Task triam.notifications.scan_due[11eef134-fcf1-4576-8026-1cd71c542ef3] received
2026-05-28 10:05:10.150 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:05:10,151: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[11eef134-fcf1-4576-8026-1cd71c542ef3] succeeded in 6.9869479443877935s: None
[2026-05-28 10:06:02,231: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:06:03,120: INFO/MainProcess] Task triam.notifications.scan_due[892604c3-1a7b-4c42-a700-f0de6f9e93b6] received
2026-05-28 10:06:10.053 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:06:10,054: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[892604c3-1a7b-4c42-a700-f0de6f9e93b6] succeeded in 6.932720708660781s: None
[2026-05-28 10:07:02,232: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:07:03,122: INFO/MainProcess] Task triam.notifications.scan_due[bf2ba971-8658-47ab-8501-a3f661124155] received
2026-05-28 10:07:10.048 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:07:10,049: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[bf2ba971-8658-47ab-8501-a3f661124155] succeeded in 6.925228745210916s: None
[2026-05-28 10:08:02,232: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:08:02,904: INFO/MainProcess] Task triam.notifications.scan_due[463596ff-3539-4050-ac0d-0c8f7aae8db3] received
2026-05-28 10:08:09.821 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:08:09,821: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[463596ff-3539-4050-ac0d-0c8f7aae8db3] succeeded in 6.916446920949966s: None
[2026-05-28 10:09:02,232: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:09:03,121: INFO/MainProcess] Task triam.notifications.scan_due[f1d1d678-cbab-483a-8f8e-f1e5118a54f8] received
2026-05-28 10:09:10.056 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:09:10,057: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f1d1d678-cbab-483a-8f8e-f1e5118a54f8] succeeded in 6.934630574658513s: None
[2026-05-28 10:10:02,232: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:10:03,119: INFO/MainProcess] Task triam.notifications.scan_due[68db7fa2-418f-4db3-b1f3-c5d057afc47d] received
2026-05-28 10:10:10.034 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:10:10,034: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[68db7fa2-418f-4db3-b1f3-c5d057afc47d] succeeded in 6.913678833749145s: None
2026-05-28 10:10:11.480 | INFO | logging:callHandlers:1762 - 10.16.3.80:21127 - "GET /robots.txt HTTP/1.1" 404
2026-05-28 10:10:11.623 | INFO | logging:callHandlers:1762 - 10.16.47.7:1324 - "GET /robots.txt HTTP/1.1" 404
[2026-05-28 10:11:02,232: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:11:03,120: INFO/MainProcess] Task triam.notifications.scan_due[96b18a0e-d4a0-4d14-95bf-80a9016e6b6c] received
2026-05-28 10:11:10.049 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:11:10,050: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[96b18a0e-d4a0-4d14-95bf-80a9016e6b6c] succeeded in 6.926763999275863s: None
[2026-05-28 10:12:02,232: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:12:03,121: INFO/MainProcess] Task triam.notifications.scan_due[8363455c-9426-4f74-9c2b-f1ec2245a432] received
2026-05-28 10:12:11.195 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:12:11,196: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8363455c-9426-4f74-9c2b-f1ec2245a432] succeeded in 8.072339226026088s: None
[2026-05-28 10:13:02,232: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:13:02,905: INFO/MainProcess] Task triam.notifications.scan_due[ffc358f3-e339-4fda-8218-24729d2104d3] received
2026-05-28 10:13:09.661 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:13:09,662: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ffc358f3-e339-4fda-8218-24729d2104d3] succeeded in 6.755532042589039s: None
[2026-05-28 10:14:02,232: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:14:03,121: INFO/MainProcess] Task triam.notifications.scan_due[172da889-0fe1-4973-9d71-010d13226894] received
2026-05-28 10:14:09.808 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:14:09,811: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[172da889-0fe1-4973-9d71-010d13226894] succeeded in 6.687341055832803s: None
[2026-05-28 10:15:02,232: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:15:03,108: INFO/MainProcess] Task triam.notifications.scan_due[8356d2b2-24d3-4845-b3a9-ef7918e48272] received
2026-05-28 10:15:09.810 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:15:09,811: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8356d2b2-24d3-4845-b3a9-ef7918e48272] succeeded in 6.701110607013106s: None
[2026-05-28 10:16:02,233: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:16:03,149: INFO/MainProcess] Task triam.notifications.scan_due[9581c5b0-7666-4dfd-90ec-e5f08e1526bc] received
2026-05-28 10:16:09.846 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:16:09,847: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[9581c5b0-7666-4dfd-90ec-e5f08e1526bc] succeeded in 6.696308687329292s: None
[2026-05-28 10:17:02,233: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:17:03,199: INFO/MainProcess] Task triam.notifications.scan_due[692f0581-5b4b-4b30-89f8-8e0eb9ec7811] received
2026-05-28 10:17:09.905 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:17:09,907: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[692f0581-5b4b-4b30-89f8-8e0eb9ec7811] succeeded in 6.706360676791519s: None
[2026-05-28 10:18:02,233: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:18:03,051: INFO/MainProcess] Task triam.notifications.scan_due[f4fa8484-8952-4c95-8f36-6ade8e121b9e] received
2026-05-28 10:18:09.751 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:18:09,752: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f4fa8484-8952-4c95-8f36-6ade8e121b9e] succeeded in 6.697891300078481s: None
[2026-05-28 10:19:02,233: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:19:03,306: INFO/MainProcess] Task triam.notifications.scan_due[8ac52a5f-4431-442d-8b06-26768d893efc] received
2026-05-28 10:19:10.008 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:19:10,009: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8ac52a5f-4431-442d-8b06-26768d893efc] succeeded in 6.701067558955401s: None
[2026-05-28 10:20:02,233: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:20:02,891: INFO/MainProcess] Task triam.notifications.scan_due[3982b7ba-1f80-4518-ba0e-c8226552ed3b] received
2026-05-28 10:20:09.581 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:20:09,583: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3982b7ba-1f80-4518-ba0e-c8226552ed3b] succeeded in 6.690594683866948s: None
[2026-05-28 10:21:02,233: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:21:03,144: INFO/MainProcess] Task triam.notifications.scan_due[7e068292-b15a-4d96-a43a-97b71e98c39c] received
2026-05-28 10:21:09.863 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:21:09,864: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7e068292-b15a-4d96-a43a-97b71e98c39c] succeeded in 6.716080258600414s: None
[2026-05-28 10:22:02,233: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:22:03,106: INFO/MainProcess] Task triam.notifications.scan_due[a692e73c-36bb-4a60-894d-a3c1a8c234d3] received
2026-05-28 10:22:12.658 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=1 | recovered=0 | should_deliver=True
[2026-05-28 10:22:13,115: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a692e73c-36bb-4a60-894d-a3c1a8c234d3] succeeded in 10.005007313098758s: None
[2026-05-28 10:22:13,767: INFO/MainProcess] Task triam.notifications.deliver_due[8ee698e4-ac73-4123-b3a7-25cf04e509ca] received
2026-05-28 10:22:17.870 | INFO | app.tasks.notification_tasks:deliver_due_notifications_task:67 - Notification delivery batch done | worker_id=notification-worker:7dd44a6e-107e-45d3-888f-f7d216d5aaf6 | delivered_attempts=1
[2026-05-28 10:22:17,871: INFO/ForkPoolWorker-1] Task triam.notifications.deliver_due[8ee698e4-ac73-4123-b3a7-25cf04e509ca] succeeded in 4.103115870151669s: None
[2026-05-28 10:23:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:23:03,029: INFO/MainProcess] Task triam.notifications.scan_due[0814e321-b999-4144-a903-673966eb56f7] received
2026-05-28 10:23:09.727 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:23:09,729: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[0814e321-b999-4144-a903-673966eb56f7] succeeded in 6.699307875242084s: None
[2026-05-28 10:24:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:24:03,283: INFO/MainProcess] Task triam.notifications.scan_due[e9e7c645-d59e-44b3-ad68-cface3997f43] received
2026-05-28 10:24:09.975 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:24:09,976: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e9e7c645-d59e-44b3-ad68-cface3997f43] succeeded in 6.691096296068281s: None
[2026-05-28 10:25:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:25:02,893: INFO/MainProcess] Task triam.notifications.scan_due[b867f06d-fdfc-40ce-9769-394e6b7e3323] received
2026-05-28 10:25:09.593 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:25:09,593: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b867f06d-fdfc-40ce-9769-394e6b7e3323] succeeded in 6.699365444947034s: None
[2026-05-28 10:26:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:26:03,107: INFO/MainProcess] Task triam.notifications.scan_due[06434f07-a650-427c-9b6f-4943d95ac9fd] received
2026-05-28 10:26:09.791 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:26:09,792: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[06434f07-a650-427c-9b6f-4943d95ac9fd] succeeded in 6.684279602020979s: None
[2026-05-28 10:27:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:27:03,094: INFO/MainProcess] Task triam.notifications.scan_due[a84a3da9-3e44-4ae0-9b3d-4f313252115d] received
2026-05-28 10:27:09.779 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:27:09,780: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a84a3da9-3e44-4ae0-9b3d-4f313252115d] succeeded in 6.684223101008683s: None
[2026-05-28 10:28:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:28:02,966: INFO/MainProcess] Task triam.notifications.scan_due[1ff6119b-3db1-4a42-a9b8-034aa7adf625] received
2026-05-28 10:28:09.656 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:28:09,657: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1ff6119b-3db1-4a42-a9b8-034aa7adf625] succeeded in 6.689510356169194s: None
[2026-05-28 10:29:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:29:03,439: INFO/MainProcess] Task triam.notifications.scan_due[d9da125a-7ef1-4610-94ea-b82c835a4f98] received
2026-05-28 10:29:10.128 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:29:10,128: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d9da125a-7ef1-4610-94ea-b82c835a4f98] succeeded in 6.688630641903728s: None
[2026-05-28 10:30:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:30:02,888: INFO/MainProcess] Task triam.notifications.scan_due[0dcb2478-7a14-47dc-8170-0a1b19384465] received
2026-05-28 10:30:09.577 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:30:09,578: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[0dcb2478-7a14-47dc-8170-0a1b19384465] succeeded in 6.6887363800778985s: None
[2026-05-28 10:31:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:31:03,100: INFO/MainProcess] Task triam.notifications.scan_due[ad1dc72d-2f77-4910-8f99-0c65b8a863c0] received
2026-05-28 10:31:09.799 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:31:09,799: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ad1dc72d-2f77-4910-8f99-0c65b8a863c0] succeeded in 6.6983518758788705s: None
[2026-05-28 10:32:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:32:03,232: INFO/MainProcess] Task triam.notifications.scan_due[f6960c7e-e971-4949-af63-dcaf4f63a701] received
2026-05-28 10:32:09.924 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:32:09,925: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f6960c7e-e971-4949-af63-dcaf4f63a701] succeeded in 6.6911572609096766s: None
[2026-05-28 10:33:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:33:03,358: INFO/MainProcess] Task triam.notifications.scan_due[b6c3c301-23a4-4b36-9499-461940538d0f] received
2026-05-28 10:33:10.048 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:33:10,048: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b6c3c301-23a4-4b36-9499-461940538d0f] succeeded in 6.689486006274819s: None
[2026-05-28 10:34:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:34:03,101: INFO/MainProcess] Task triam.notifications.scan_due[31fef25b-9ffa-4c02-a6be-f680c2c377d3] received
2026-05-28 10:34:10.011 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:34:10,012: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[31fef25b-9ffa-4c02-a6be-f680c2c377d3] succeeded in 6.687595917843282s: None
[2026-05-28 10:35:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:35:02,889: INFO/MainProcess] Task triam.notifications.scan_due[5a5d3add-3e70-42c4-8079-8170ba7d8fa9] received
2026-05-28 10:35:09.580 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:35:09,581: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5a5d3add-3e70-42c4-8079-8170ba7d8fa9] succeeded in 6.691230483353138s: None
[2026-05-28 10:36:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:36:03,100: INFO/MainProcess] Task triam.notifications.scan_due[a10fcd16-971e-485c-9625-877ef8988636] received
2026-05-28 10:36:09.794 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:36:09,796: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a10fcd16-971e-485c-9625-877ef8988636] succeeded in 6.689986021257937s: None
[2026-05-28 10:37:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-28 10:37:02.495 | INFO | logging:callHandlers:1762 - 10.16.40.242:20235 - "GET /api/v1/health HTTP/1.1" 200
[2026-05-28 10:37:03,274: INFO/MainProcess] Task triam.notifications.scan_due[a68f1640-aec5-4c75-a726-b99be591ca6e] received
2026-05-28 10:37:09.961 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:37:09,962: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a68f1640-aec5-4c75-a726-b99be591ca6e] succeeded in 6.6874073427170515s: None
2026-05-28 10:37:38.622 | INFO | logging:callHandlers:1762 - 10.16.3.80:20882 - "GET /api/v1/health HTTP/1.1" 200
2026-05-28 10:37:56.519 | INFO | logging:callHandlers:1762 - 10.16.3.80:12828 - "GET /api/v1/health HTTP/1.1" 200
[2026-05-28 10:38:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:38:03,106: INFO/MainProcess] Task triam.notifications.scan_due[f3e14702-b1aa-488e-960f-67c74f20ec37] received
2026-05-28 10:38:09.797 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:38:09,798: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f3e14702-b1aa-488e-960f-67c74f20ec37] succeeded in 6.6906685419380665s: None
[2026-05-28 10:39:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:39:03,101: INFO/MainProcess] Task triam.notifications.scan_due[5e2a5fa3-1f61-4e48-8f30-0c40aba92483] received
2026-05-28 10:39:10.017 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:39:10,018: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5e2a5fa3-1f61-4e48-8f30-0c40aba92483] succeeded in 6.68872617604211s: None
2026-05-28 10:39:56.717 | INFO | logging:callHandlers:1762 - 10.16.40.242:15109 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
[2026-05-28 10:40:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:40:02,888: INFO/MainProcess] Task triam.notifications.scan_due[b1b960c4-f5b8-4c1d-8e08-73597d53d9bf] received
2026-05-28 10:40:04.886 | INFO | logging:callHandlers:1762 - 10.16.3.80:43044 - "GET /api/v1/study-contexts HTTP/1.1" 200
2026-05-28 10:40:09.575 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:40:09,576: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b1b960c4-f5b8-4c1d-8e08-73597d53d9bf] succeeded in 6.686848070006818s: None
2026-05-28 10:40:09.728 | INFO | logging:callHandlers:1762 - 10.16.3.80:17423 - "GET /api/v1/health HTTP/1.1" 200
2026-05-28 10:40:13.573 | INFO | logging:callHandlers:1762 - 10.16.3.80:29757 - "GET /api/v1/books HTTP/1.1" 200
[2026-05-28 10:41:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:41:03,100: INFO/MainProcess] Task triam.notifications.scan_due[290997cc-01c4-4b3e-83d3-8930c98de25b] received
2026-05-28 10:41:09.798 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:41:09,798: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[290997cc-01c4-4b3e-83d3-8930c98de25b] succeeded in 6.696252373047173s: None
2026-05-28 10:41:15.993 | INFO | logging:callHandlers:1762 - 10.16.37.205:63788 - "POST /api/v1/study-contexts HTTP/1.1" 200
2026-05-28 10:41:19.684 | INFO | logging:callHandlers:1762 - 10.16.3.80:22526 - "GET /api/v1/study-contexts HTTP/1.1" 200
2026-05-28 10:41:35.172 | INFO | logging:callHandlers:1762 - 10.16.37.205:26705 - "GET /api/v1/study-contexts/74688440-8a52-47bd-ac5c-a6fcf58e1a3a/threads HTTP/1.1" 200
2026-05-28 10:41:41.215 | INFO | logging:callHandlers:1762 - 10.16.47.7:29112 - "POST /api/v1/study-contexts/74688440-8a52-47bd-ac5c-a6fcf58e1a3a/threads HTTP/1.1" 200
2026-05-28 10:41:45.486 | INFO | logging:callHandlers:1762 - 10.16.37.205:1795 - "GET /api/v1/threads/1196260c-3dc7-48ed-a760-b0212e2ae6e8/messages HTTP/1.1" 200
2026-05-28 10:41:46.182 | INFO | logging:callHandlers:1762 - 10.16.37.205:1935 - "GET /api/v1/study-contexts/74688440-8a52-47bd-ac5c-a6fcf58e1a3a/threads HTTP/1.1" 200
[2026-05-28 10:42:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:42:03,102: INFO/MainProcess] Task triam.notifications.scan_due[de2eba1e-f557-4b2c-b019-beafcf40f9ff] received
2026-05-28 10:42:11.441 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:42:11,441: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[de2eba1e-f557-4b2c-b019-beafcf40f9ff] succeeded in 8.33820776315406s: None
[2026-05-28 10:43:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:43:03,276: INFO/MainProcess] Task triam.notifications.scan_due[e51cf139-27d7-4770-90b3-c171fafd5abe] received
2026-05-28 10:43:10.213 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:43:10,214: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e51cf139-27d7-4770-90b3-c171fafd5abe] succeeded in 6.936269646976143s: None
[2026-05-28 10:44:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:44:03,103: INFO/MainProcess] Task triam.notifications.scan_due[3ca61dee-4536-4b91-b5b1-4ae00f60d6ff] received
2026-05-28 10:44:10.033 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:44:10,034: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3ca61dee-4536-4b91-b5b1-4ae00f60d6ff] succeeded in 6.930112223140895s: None
[2026-05-28 10:45:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:45:02,889: INFO/MainProcess] Task triam.notifications.scan_due[f6316289-c87e-46c1-ab02-065549a8b93a] received
2026-05-28 10:45:09.822 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:45:09,822: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f6316289-c87e-46c1-ab02-065549a8b93a] succeeded in 6.93165084393695s: None
[2026-05-28 10:46:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:46:03,233: INFO/MainProcess] Task triam.notifications.scan_due[828f94b0-2612-4f72-8c5e-7fed0167454f] received
2026-05-28 10:46:10.167 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:46:10,167: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[828f94b0-2612-4f72-8c5e-7fed0167454f] succeeded in 6.933284766972065s: None
[2026-05-28 10:47:02,234: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:47:03,101: INFO/MainProcess] Task triam.notifications.scan_due[6d88a892-b03a-4161-833d-26ef9388b1e7] received
2026-05-28 10:47:10.033 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:47:10,033: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[6d88a892-b03a-4161-833d-26ef9388b1e7] succeeded in 6.931065169163048s: None
[2026-05-28 10:48:02,235: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:48:03,205: INFO/MainProcess] Task triam.notifications.scan_due[33647f6a-49ed-45dd-8a6c-9c614d5b8bab] received
2026-05-28 10:48:10.138 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:48:10,139: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[33647f6a-49ed-45dd-8a6c-9c614d5b8bab] succeeded in 6.93328403821215s: None
[2026-05-28 10:49:02,235: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:49:03,232: INFO/MainProcess] Task triam.notifications.scan_due[4baebb8d-3df1-4374-b347-697a4f842c18] received
2026-05-28 10:49:10.381 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:49:10,381: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4baebb8d-3df1-4374-b347-697a4f842c18] succeeded in 6.923669085837901s: None
[2026-05-28 10:50:02,235: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:50:03,020: INFO/MainProcess] Task triam.notifications.scan_due[1f15d0f7-b140-4c8c-8413-b38e3a2a617e] received
2026-05-28 10:50:09.951 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:50:09,951: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1f15d0f7-b140-4c8c-8413-b38e3a2a617e] succeeded in 6.930620722007006s: None
[2026-05-28 10:51:02,235: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:51:03,101: INFO/MainProcess] Task triam.notifications.scan_due[5330b758-774c-4374-8b8f-b857295ef344] received
2026-05-28 10:51:10.034 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:51:10,035: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5330b758-774c-4374-8b8f-b857295ef344] succeeded in 6.931789682246745s: None
[2026-05-28 10:52:02,235: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:52:03,124: INFO/MainProcess] Task triam.notifications.scan_due[36aef632-a3f3-4cb5-8cd4-991910e680bd] received
2026-05-28 10:52:10.052 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:52:10,053: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[36aef632-a3f3-4cb5-8cd4-991910e680bd] succeeded in 6.9273941670544446s: None
[2026-05-28 10:53:02,235: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:53:03,101: INFO/MainProcess] Task triam.notifications.scan_due[38e4ee08-750c-48d5-b646-b8c1d145073c] received
2026-05-28 10:53:10.035 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:53:10,036: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[38e4ee08-750c-48d5-b646-b8c1d145073c] succeeded in 6.934247514232993s: None
[2026-05-28 10:54:02,237: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:54:03,232: INFO/MainProcess] Task triam.notifications.scan_due[be4a0b65-6592-48a9-a8da-054b8e1a80f7] received
2026-05-28 10:54:10.382 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:54:10,383: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[be4a0b65-6592-48a9-a8da-054b8e1a80f7] succeeded in 6.9252304448746145s: None
[2026-05-28 10:55:02,237: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:55:03,023: INFO/MainProcess] Task triam.notifications.scan_due[0bd240f0-9015-4a05-b673-76b660c1ebbd] received
2026-05-28 10:55:09.950 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:55:09,951: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[0bd240f0-9015-4a05-b673-76b660c1ebbd] succeeded in 6.926286710426211s: None
[2026-05-28 10:56:02,237: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:56:03,090: INFO/MainProcess] Task triam.notifications.scan_due[78b65c59-a7b2-4a28-ab8b-b0ac07ad775d] received
2026-05-28 10:56:10.027 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:56:10,027: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[78b65c59-a7b2-4a28-ab8b-b0ac07ad775d] succeeded in 6.933909663930535s: None
[2026-05-28 10:57:02,237: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:57:02,876: INFO/MainProcess] Task triam.notifications.scan_due[7b5d8950-8c6c-454c-ad43-55e7f7e5b9b0] received
2026-05-28 10:57:09.807 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:57:09,808: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7b5d8950-8c6c-454c-ad43-55e7f7e5b9b0] succeeded in 6.927520470228046s: None
[2026-05-28 10:58:02,237: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:58:03,192: INFO/MainProcess] Task triam.notifications.scan_due[7080cb75-f31b-45a0-960c-e807a758e443] received
2026-05-28 10:58:10.122 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:58:10,123: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7080cb75-f31b-45a0-960c-e807a758e443] succeeded in 6.92908354010433s: None
[2026-05-28 10:59:02,237: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 10:59:03,090: INFO/MainProcess] Task triam.notifications.scan_due[301df57e-a665-4ea2-b504-44dba13df445] received
2026-05-28 10:59:10.246 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 10:59:10,247: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[301df57e-a665-4ea2-b504-44dba13df445] succeeded in 6.924005358945578s: None
[2026-05-28 11:00:02,238: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:00:02,876: INFO/MainProcess] Task triam.notifications.scan_due[19001627-74e1-4723-8755-b07e1f031c12] received
2026-05-28 11:00:09.802 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:00:09,803: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[19001627-74e1-4723-8755-b07e1f031c12] succeeded in 6.926132921129465s: None
[2026-05-28 11:01:02,238: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:01:03,092: INFO/MainProcess] Task triam.notifications.scan_due[bb2ebe45-0f16-47dc-bea6-a77527b0a449] received
2026-05-28 11:01:10.024 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:01:10,024: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[bb2ebe45-0f16-47dc-bea6-a77527b0a449] succeeded in 6.930938366334885s: None
[2026-05-28 11:02:02,238: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:02:02,877: INFO/MainProcess] Task triam.notifications.scan_due[e8d98a44-cb98-4319-a2c7-5328d063d7b8] received
2026-05-28 11:02:09.821 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:02:09,822: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e8d98a44-cb98-4319-a2c7-5328d063d7b8] succeeded in 6.944116979371756s: None
[2026-05-28 11:03:02,238: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:03:03,206: INFO/MainProcess] Task triam.notifications.scan_due[b6547f5f-ef6c-4f85-9d46-4f40fd265f25] received
2026-05-28 11:03:10.146 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:03:10,146: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b6547f5f-ef6c-4f85-9d46-4f40fd265f25] succeeded in 6.939052173867822s: None
[2026-05-28 11:04:02,238: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:04:03,289: INFO/MainProcess] Task triam.notifications.scan_due[04eca4ee-33b5-4686-b442-b03fdf09f148] received
2026-05-28 11:04:10.466 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:04:10,468: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[04eca4ee-33b5-4686-b442-b03fdf09f148] succeeded in 6.953445678111166s: None
[2026-05-28 11:05:02,238: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:05:02,889: INFO/MainProcess] Task triam.notifications.scan_due[75000b81-cda2-4b24-8123-c173f62fdb43] received
2026-05-28 11:05:09.818 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:05:09,818: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[75000b81-cda2-4b24-8123-c173f62fdb43] succeeded in 6.928469360806048s: None
[2026-05-28 11:06:02,238: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:06:03,104: INFO/MainProcess] Task triam.notifications.scan_due[e0125848-700a-47de-a172-a2109ad1d7fa] received
2026-05-28 11:06:10.034 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:06:10,035: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e0125848-700a-47de-a172-a2109ad1d7fa] succeeded in 6.929693886078894s: None
[2026-05-28 11:07:02,238: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:07:02,888: INFO/MainProcess] Task triam.notifications.scan_due[f0373374-e751-467f-a309-dd8e162c20b5] received
2026-05-28 11:07:09.819 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:07:09,819: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f0373374-e751-467f-a309-dd8e162c20b5] succeeded in 6.9268194092437625s: None
[2026-05-28 11:08:02,238: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:08:03,103: INFO/MainProcess] Task triam.notifications.scan_due[a0859bf1-ff86-4544-b43b-747c2cb3d9a9] received
2026-05-28 11:08:10.034 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:08:10,035: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a0859bf1-ff86-4544-b43b-747c2cb3d9a9] succeeded in 6.930081236641854s: None
[2026-05-28 11:09:02,238: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:09:03,105: INFO/MainProcess] Task triam.notifications.scan_due[26717fe9-4020-43aa-8e9a-3b6ff692945a] received
2026-05-28 11:09:10.256 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:09:10,257: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[26717fe9-4020-43aa-8e9a-3b6ff692945a] succeeded in 6.9269939279183745s: None
[2026-05-28 11:10:02,238: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:10:02,883: INFO/MainProcess] Task triam.notifications.scan_due[ea5a43bf-19e9-4d85-9609-82a4079dfb44] received
2026-05-28 11:10:09.815 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:10:09,815: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ea5a43bf-19e9-4d85-9609-82a4079dfb44] succeeded in 6.930943400133401s: None
[2026-05-28 11:11:02,238: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:11:03,099: INFO/MainProcess] Task triam.notifications.scan_due[8d2dad59-912f-4dcd-a6f8-40ec726f8cfc] received
2026-05-28 11:11:10.032 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:11:10,033: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8d2dad59-912f-4dcd-a6f8-40ec726f8cfc] succeeded in 6.932188021019101s: None
[2026-05-28 11:12:02,238: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:12:02,885: INFO/MainProcess] Task triam.notifications.scan_due[30e16a37-0143-49df-83e9-1bcea07a646b] received
2026-05-28 11:12:09.821 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:12:09,822: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[30e16a37-0143-49df-83e9-1bcea07a646b] succeeded in 6.935741011984646s: None
[2026-05-28 11:13:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:13:03,098: INFO/MainProcess] Task triam.notifications.scan_due[dd17b0e6-5252-4ed5-90f9-ad4def4c05c1] received
2026-05-28 11:13:11.253 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:13:11,253: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[dd17b0e6-5252-4ed5-90f9-ad4def4c05c1] succeeded in 8.15456592105329s: None
[2026-05-28 11:14:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:14:03,098: INFO/MainProcess] Task triam.notifications.scan_due[de5c71e1-4a31-402b-aeb0-349cb1032ed9] received
2026-05-28 11:14:09.971 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:14:09,972: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[de5c71e1-4a31-402b-aeb0-349cb1032ed9] succeeded in 6.87264895811677s: None
[2026-05-28 11:15:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:15:02,883: INFO/MainProcess] Task triam.notifications.scan_due[14ccc15a-9856-4ba1-97c4-5954ba78ca5f] received
2026-05-28 11:15:09.713 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:15:09,713: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[14ccc15a-9856-4ba1-97c4-5954ba78ca5f] succeeded in 6.830038949847221s: None
[2026-05-28 11:16:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:16:03,102: INFO/MainProcess] Task triam.notifications.scan_due[47eae68a-c00e-4e35-aa3c-1363dd0de143] received
2026-05-28 11:16:10.005 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:16:10,006: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[47eae68a-c00e-4e35-aa3c-1363dd0de143] succeeded in 6.903113335836679s: None
2026-05-28 11:16:59.905 | INFO | logging:callHandlers:1762 - 10.16.3.80:40426 - "GET /api/v1/health HTTP/1.1" 200
[2026-05-28 11:17:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:17:03,006: INFO/MainProcess] Task triam.notifications.scan_due[90e78f69-aab0-4a73-aa4a-1b6ae903afc4] received
2026-05-28 11:17:09.903 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:17:09,904: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[90e78f69-aab0-4a73-aa4a-1b6ae903afc4] succeeded in 6.897123167756945s: None
[2026-05-28 11:18:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:18:03,268: INFO/MainProcess] Task triam.notifications.scan_due[b05101f5-5dd1-4c84-925e-42be6b4733cf] received
2026-05-28 11:18:10.186 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:18:10,188: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b05101f5-5dd1-4c84-925e-42be6b4733cf] succeeded in 6.91828195611015s: None
[2026-05-28 11:19:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:19:03,106: INFO/MainProcess] Task triam.notifications.scan_due[72833a3b-c808-4b6e-bbf5-660501410022] received
2026-05-28 11:19:10.005 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:19:10,005: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[72833a3b-c808-4b6e-bbf5-660501410022] succeeded in 6.89757254300639s: None
[2026-05-28 11:20:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:20:03,151: INFO/MainProcess] Task triam.notifications.scan_due[2d8b6db9-53b9-407a-b841-9372aa1a463f] received
2026-05-28 11:20:10.060 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:20:10,060: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2d8b6db9-53b9-407a-b841-9372aa1a463f] succeeded in 6.908397097140551s: None
[2026-05-28 11:21:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:21:03,108: INFO/MainProcess] Task triam.notifications.scan_due[89bf2f6b-e17a-426c-9e2d-c05284b61558] received
2026-05-28 11:21:10.029 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:21:10,031: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[89bf2f6b-e17a-426c-9e2d-c05284b61558] succeeded in 6.922405369114131s: None
[2026-05-28 11:22:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:22:03,000: INFO/MainProcess] Task triam.notifications.scan_due[cdc40889-d8b5-41c1-a1f6-f5502be7180f] received
2026-05-28 11:22:09.922 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:22:09,922: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[cdc40889-d8b5-41c1-a1f6-f5502be7180f] succeeded in 6.920592234004289s: None
[2026-05-28 11:23:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:23:03,273: INFO/MainProcess] Task triam.notifications.scan_due[94a074f9-b7fb-44a0-a415-8bff43b11972] received
2026-05-28 11:23:10.190 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:23:10,191: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[94a074f9-b7fb-44a0-a415-8bff43b11972] succeeded in 6.917126311920583s: None
[2026-05-28 11:24:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:24:03,108: INFO/MainProcess] Task triam.notifications.scan_due[81dd6a70-b592-46eb-9729-406e082d2101] received
2026-05-28 11:24:10.007 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:24:10,009: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[81dd6a70-b592-46eb-9729-406e082d2101] succeeded in 6.899554641917348s: None
2026-05-28 11:24:49.535 | INFO | logging:callHandlers:1762 - 10.16.40.242:56640 - "GET /api/v1/health HTTP/1.1" 200
[2026-05-28 11:25:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:25:03,107: INFO/MainProcess] Task triam.notifications.scan_due[70a87f3e-818f-4c60-ba40-65667775fbcc] received
2026-05-28 11:25:10.109 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:25:10,111: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[70a87f3e-818f-4c60-ba40-65667775fbcc] succeeded in 7.003297979012132s: None
[2026-05-28 11:26:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:26:03,107: INFO/MainProcess] Task triam.notifications.scan_due[d18f2ea0-132c-46a5-afdc-2b9e055a0669] received
2026-05-28 11:26:10.114 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:26:10,115: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d18f2ea0-132c-46a5-afdc-2b9e055a0669] succeeded in 7.006890197750181s: None
[2026-05-28 11:27:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:27:02,989: INFO/MainProcess] Task triam.notifications.scan_due[23c62a6a-9028-4745-9a6e-5117b3fe2124] received
2026-05-28 11:27:09.999 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:27:09,999: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[23c62a6a-9028-4745-9a6e-5117b3fe2124] succeeded in 7.008538939990103s: None
[2026-05-28 11:28:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:28:03,306: INFO/MainProcess] Task triam.notifications.scan_due[28ff1b00-cbce-4d5c-9742-360c607b82d4] received
2026-05-28 11:28:10.312 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:28:10,313: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[28ff1b00-cbce-4d5c-9742-360c607b82d4] succeeded in 7.005113183055073s: None
[2026-05-28 11:29:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:29:03,125: INFO/MainProcess] Task triam.notifications.scan_due[82c5546b-e67e-4e63-a1e3-7a1faee7cc8e] received
2026-05-28 11:29:10.131 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:29:10,131: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[82c5546b-e67e-4e63-a1e3-7a1faee7cc8e] succeeded in 7.005437669809908s: None
[2026-05-28 11:30:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:30:03,126: INFO/MainProcess] Task triam.notifications.scan_due[3ad5be86-2e7b-404c-8097-a81fa834323a] received
2026-05-28 11:30:10.130 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:30:10,131: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3ad5be86-2e7b-404c-8097-a81fa834323a] succeeded in 7.0043394370004535s: None
[2026-05-28 11:31:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:31:03,124: INFO/MainProcess] Task triam.notifications.scan_due[ca2472b0-72fd-44e9-823b-9118ac80db0b] received
2026-05-28 11:31:10.133 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:31:10,133: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ca2472b0-72fd-44e9-823b-9118ac80db0b] succeeded in 7.007988907396793s: None
[2026-05-28 11:32:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:32:03,005: INFO/MainProcess] Task triam.notifications.scan_due[d599e3d5-e321-4293-9fae-abc7b8911233] received
2026-05-28 11:32:10.032 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:32:10,033: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d599e3d5-e321-4293-9fae-abc7b8911233] succeeded in 7.027020854875445s: None
[2026-05-28 11:33:02,239: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:33:03,322: INFO/MainProcess] Task triam.notifications.scan_due[8a74efc5-65e4-4f69-9202-7cd24ca1bf7c] received
2026-05-28 11:33:10.333 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:33:10,334: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8a74efc5-65e4-4f69-9202-7cd24ca1bf7c] succeeded in 7.0107372920028865s: None
[2026-05-28 11:34:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:34:03,124: INFO/MainProcess] Task triam.notifications.scan_due[12108dee-bb08-4c50-acf4-03ac8e129129] received
2026-05-28 11:34:10.305 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:34:10,306: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[12108dee-bb08-4c50-acf4-03ac8e129129] succeeded in 7.180742880795151s: None
[2026-05-28 11:35:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:35:03,126: INFO/MainProcess] Task triam.notifications.scan_due[7c67c072-e19c-4078-9423-418353bd22d8] received
2026-05-28 11:35:10.138 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:35:10,139: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7c67c072-e19c-4078-9423-418353bd22d8] succeeded in 7.011498664971441s: None
2026-05-28 11:35:36.484 | INFO | logging:callHandlers:1762 - 10.16.3.80:27734 - "GET /api/v1/health HTTP/1.1" 200
2026-05-28 11:35:53.478 | INFO | logging:callHandlers:1762 - 10.16.3.80:44358 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
[2026-05-28 11:36:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:36:03,133: INFO/MainProcess] Task triam.notifications.scan_due[c7782ad6-d1b4-47e4-986e-6cb223bf43d3] received
2026-05-28 11:36:05.138 | INFO | logging:callHandlers:1762 - 10.16.37.205:22791 - "GET /api/v1/study-contexts HTTP/1.1" 200
2026-05-28 11:36:10.153 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:36:10,154: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c7782ad6-d1b4-47e4-986e-6cb223bf43d3] succeeded in 7.020669877994806s: None
[2026-05-28 11:37:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:37:02,978: INFO/MainProcess] Task triam.notifications.scan_due[06e20f1e-766a-4789-8ca7-522205335890] received
2026-05-28 11:37:09.993 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:37:09,993: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[06e20f1e-766a-4789-8ca7-522205335890] succeeded in 7.012536789290607s: None
2026-05-28 11:37:49.876 | INFO | app.services.upload_service:handle_upload_document:107 - ☁️ PDF uploaded to Storage: 0fb7d58f-9482-4903-8fee-6557072f61ea/original.pdf
2026-05-28 11:37:52.103 | INFO | app.services.upload_service:handle_upload_document:139 - 📘 Created DRAFT book 0fb7d58f-9482-4903-8fee-6557072f61ea | 3 chapters | file_url saved
2026-05-28 11:37:52.104 | INFO | logging:callHandlers:1762 - 10.16.3.80:58852 - "POST /api/v1/upload HTTP/1.1" 200
2026-05-28 11:37:55.957 | INFO | logging:callHandlers:1762 - 10.16.3.80:58852 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
[2026-05-28 11:38:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:38:03,298: INFO/MainProcess] Task triam.notifications.scan_due[435770bf-9d5a-472d-be9d-258d51c0acc2] received
2026-05-28 11:38:08.802 | INFO | logging:callHandlers:1762 - 10.16.40.242:30266 - "GET /api/v1/notifications/settings HTTP/1.1" 200
2026-05-28 11:38:10.344 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:38:10,345: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[435770bf-9d5a-472d-be9d-258d51c0acc2] succeeded in 7.0455317767336965s: None
2026-05-28 11:38:26.929 | INFO | app.services.upload_service:handle_generate_plan:213 - 📋 ReadingPlan created for book 0fb7d58f-9482-4903-8fee-6557072f61ea | mode=full | job=573861f9-b10a-4428-87de-198119ca15e0
2026-05-28 11:38:29.890 | INFO | logging:callHandlers:1762 - 10.16.37.205:11824 - "POST /api/v1/generate-plan HTTP/1.1" 200
[2026-05-28 11:38:30,088: INFO/MainProcess] Task triam.books.process[4612f236-81cf-4493-8ee0-d8ff27bc19a9] received
2026-05-28 11:38:30.169 | INFO | app.tasks.book_tasks:process_book_task:23 - Celery process_book_task started | book_id=0fb7d58f-9482-4903-8fee-6557072f61ea | mode=full | job_id=573861f9-b10a-4428-87de-198119ca15e0
2026-05-28 11:38:32.775 | INFO | logging:callHandlers:1762 - 10.16.3.80:51331 - "GET /?logs=container HTTP/1.1" 200
2026-05-28 11:38:33.178 | INFO | logging:callHandlers:1762 - 10.16.47.7:8617 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-28 11:38:35.559 | INFO | logging:callHandlers:1762 - 10.16.3.80:46720 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:38:36.867 | INFO | app.services.workers.book_pipeline:run_background_processing:303 - ⬇️ Downloading PDF from Storage: 0fb7d58f-9482-4903-8fee-6557072f61ea/original.pdf
2026-05-28 11:38:39.473 | INFO | logging:callHandlers:1762 - 10.16.37.205:63526 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:38:43.986 | INFO | logging:callHandlers:1762 - 10.16.37.205:16866 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:38:46.739 | INFO | app.services.workers.chapter_worker:process_chapter:102 - Chapter processing start | chapter=1 | mode=full | title=Chương 4: Phương pháp luận nghiên cứu | chars=3552 | estimated_tokens=1680 | estimated_audio_seconds=350
2026-05-28 11:38:48.442 | INFO | logging:callHandlers:1762 - 10.16.3.80:1359 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:38:48.996 | INFO | app.services.workers.chapter_worker:process_chapter:130 - Chapter pipelines dispatch | chapter=1 | mode=full | rag=true | tts=true
2026-05-28 11:38:50.260 | INFO | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=1 | mode=full | title=Chương 4: Phương pháp luận nghiên cứu | raw_chars=3552
2026-05-28 11:38:50.263 | INFO | app.services.llm_service:normalize_text_for_speech:227 - Normalize preflight | mode=full | title=Chương 4: Phương pháp luận nghiên cứu | chars=3552 | estimated_tokens=1680 | estimated_audio_seconds=350
2026-05-28 11:38:50.265 | INFO | app.services.llm_service:normalize_text_for_speech:236 - Normalize strategy | mode=full | strategy=single_call | title=Chương 4: Phương pháp luận nghiên cứu
2026-05-28 11:38:50.267 | INFO | app.services.llm_service:\_call_normalize_llm:190 - LLM normalize start | mode=full | context=single | chars=3552 | attempt=1/2
2026-05-28 11:38:52.276 | INFO | logging:callHandlers:1762 - 10.16.3.80:1779 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:38:52.917 | INFO | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 4 vectors for chapter_id=2be1315f-c635-4c4d-ab28-0d5cd401641c
2026-05-28 11:38:56.125 | INFO | logging:callHandlers:1762 - 10.16.3.80:26030 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:38:59.909 | INFO | logging:callHandlers:1762 - 10.16.3.80:24220 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
[2026-05-28 11:39:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:39:03,125: INFO/MainProcess] Task triam.notifications.scan_due[b5862dba-16b6-4027-919c-ba883e9254e4] received
2026-05-28 11:39:03.800 | INFO | logging:callHandlers:1762 - 10.16.37.205:60191 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:39:05.132 | INFO | app.services.llm_service:\_call_normalize_llm:203 - LLM normalize done | mode=full | context=single | scripts=11 | review_chars=711
2026-05-28 11:39:05.132 | INFO | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=1 | mode=full | main_scripts=11 | review_chars=711
2026-05-28 11:39:05.132 | INFO | app.services.workers.tts_worker:\_generate_main_segments:46 - TTS main segments start | chapter=1 | mode=full | total_scripts=11
2026-05-28 11:39:05.133 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=1/11 | chars=40
2026-05-28 11:39:06.488 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=1/11 | duration_ms=2856
2026-05-28 11:39:06.488 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=2/11 | chars=322
2026-05-28 11:39:07.732 | INFO | logging:callHandlers:1762 - 10.16.3.80:1744 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:39:10.166 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:39:10,166: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b5862dba-16b6-4027-919c-ba883e9254e4] succeeded in 7.038318871986121s: None
2026-05-28 11:39:11.039 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=2/11 | duration_ms=20208
2026-05-28 11:39:11.040 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=3/11 | chars=355
2026-05-28 11:39:11.701 | INFO | logging:callHandlers:1762 - 10.16.47.7:8059 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:39:12.457 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=3/11 | duration_ms=19128
2026-05-28 11:39:12.457 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=4/11 | chars=304
2026-05-28 11:39:15.490 | INFO | logging:callHandlers:1762 - 10.16.37.205:16961 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:39:17.035 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=4/11 | duration_ms=17856
2026-05-28 11:39:17.036 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=5/11 | chars=483
2026-05-28 11:39:19.296 | INFO | logging:callHandlers:1762 - 10.16.3.80:9272 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:39:21.834 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=5/11 | duration_ms=26568
2026-05-28 11:39:21.834 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=6/11 | chars=405
2026-05-28 11:39:23.168 | INFO | logging:callHandlers:1762 - 10.16.47.7:47360 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:39:27.080 | INFO | logging:callHandlers:1762 - 10.16.3.80:15198 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:39:29.271 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=6/11 | duration_ms=25104
2026-05-28 11:39:29.272 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=7/11 | chars=267
2026-05-28 11:39:30.934 | INFO | logging:callHandlers:1762 - 10.16.40.242:48062 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:39:34.613 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=7/11 | duration_ms=16152
2026-05-28 11:39:34.613 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=8/11 | chars=457
2026-05-28 11:39:35.128 | INFO | logging:callHandlers:1762 - 10.16.37.205:21376 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:39:38.926 | INFO | logging:callHandlers:1762 - 10.16.37.205:6697 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:39:41.164 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=8/11 | duration_ms=27168
2026-05-28 11:39:41.165 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=9/11 | chars=503
2026-05-28 11:39:42.851 | INFO | logging:callHandlers:1762 - 10.16.47.7:32570 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:39:46.913 | INFO | logging:callHandlers:1762 - 10.16.47.7:40868 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:39:49.783 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=9/11 | duration_ms=29952
2026-05-28 11:39:49.783 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=10/11 | chars=372
2026-05-28 11:39:50.739 | INFO | logging:callHandlers:1762 - 10.16.37.205:46158 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:39:54.635 | INFO | logging:callHandlers:1762 - 10.16.40.242:30700 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:39:56.538 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=10/11 | duration_ms=23280
2026-05-28 11:39:56.538 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=11/11 | chars=382
2026-05-28 11:39:58.499 | INFO | logging:callHandlers:1762 - 10.16.40.242:43241 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
[2026-05-28 11:40:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-28 11:40:02.433 | INFO | logging:callHandlers:1762 - 10.16.47.7:6056 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
[2026-05-28 11:40:03,242: INFO/MainProcess] Task triam.notifications.scan_due[04c9f34c-299a-4499-8b54-bd280c57158a] received
2026-05-28 11:40:03.414 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=11/11 | duration_ms=22968
2026-05-28 11:40:03.414 | INFO | app.services.workers.tts_worker:\_generate_main_segments:80 - TTS main segments done | chapter=1 | mode=full | created_segments=11/11
2026-05-28 11:40:03.415 | INFO | app.services.workers.tts_worker:\_generate_review_audio:99 - TTS review start | chapter=1 | mode=full | chars=711
2026-05-28 11:40:06.213 | INFO | logging:callHandlers:1762 - 10.16.47.7:17003 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:40:10.007 | INFO | logging:callHandlers:1762 - 10.16.40.242:60103 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:40:10.253 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:40:10,253: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[04c9f34c-299a-4499-8b54-bd280c57158a] succeeded in 7.010468405671418s: None
2026-05-28 11:40:13.577 | INFO | app.services.workers.tts_worker:\_generate_review_audio:103 - TTS review done | chapter=1 | mode=full
2026-05-28 11:40:13.579 | INFO | app.services.workers.tts_worker:\_store_tts_result:120 - TTS DB store start | chapter_id=2be1315f-c635-4c4d-ab28-0d5cd401641c | mode=full | segments=11 | review_audio=True
2026-05-28 11:40:13.786 | INFO | logging:callHandlers:1762 - 10.16.3.80:19210 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:40:16.717 | INFO | app.services.workers.tts_worker:\_store_tts_result:131 - TTS DB store done | chapter_id=2be1315f-c635-4c4d-ab28-0d5cd401641c | mode=full
2026-05-28 11:40:18.220 | INFO | logging:callHandlers:1762 - 10.16.37.205:43549 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:40:19.154 | INFO | app.services.workers.chapter_worker:process_chapter:139 - ✅ Chapter 1 READY | mode=full | segments=11
2026-05-28 11:40:22.579 | INFO | logging:callHandlers:1762 - 10.16.40.242:53946 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:40:23.178 | INFO | app.services.workers.book_pipeline:\_create_first_playable_notification_safely:123 - Content-ready first-playable event | book_id=0fb7d58f-9482-4903-8fee-6557072f61ea | mode=full | created=True
2026-05-28 11:40:23.400 | INFO | app.services.workers.chapter_worker:process_chapter:102 - Chapter processing start | chapter=2 | mode=full | title=Chương 5: Kết quả phân tích và so sánh | chars=16337 | estimated_tokens=7795 | estimated_audio_seconds=1612
2026-05-28 11:40:25.620 | INFO | app.services.workers.chapter_worker:process_chapter:130 - Chapter pipelines dispatch | chapter=2 | mode=full | rag=true | tts=true
2026-05-28 11:40:25.621 | INFO | app.services.workers.chapter_worker:process_chapter:102 - Chapter processing start | chapter=3 | mode=full | title=Chương 6: Bàn luận và Khuyến nghị | chars=14625 | estimated_tokens=6978 | estimated_audio_seconds=1420
2026-05-28 11:40:26.532 | INFO | logging:callHandlers:1762 - 10.16.47.7:7174 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:40:27.840 | INFO | app.services.workers.chapter_worker:process_chapter:130 - Chapter pipelines dispatch | chapter=3 | mode=full | rag=true | tts=true
2026-05-28 11:40:27.843 | INFO | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=2 | mode=full | title=Chương 5: Kết quả phân tích và so sánh | raw_chars=16337
2026-05-28 11:40:27.847 | INFO | app.services.llm_service:normalize_text_for_speech:227 - Normalize preflight | mode=full | title=Chương 5: Kết quả phân tích và so sánh | chars=16337 | estimated_tokens=7795 | estimated_audio_seconds=1612
2026-05-28 11:40:27.847 | INFO | app.services.llm_service:normalize_text_for_speech:236 - Normalize strategy | mode=full | strategy=single_call | title=Chương 5: Kết quả phân tích và so sánh
2026-05-28 11:40:27.848 | INFO | app.services.llm_service:\_call_normalize_llm:190 - LLM normalize start | mode=full | context=single | chars=16337 | attempt=1/2
2026-05-28 11:40:27.853 | INFO | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=3 | mode=full | title=Chương 6: Bàn luận và Khuyến nghị | raw_chars=14625
2026-05-28 11:40:27.858 | INFO | app.services.llm_service:normalize_text_for_speech:227 - Normalize preflight | mode=full | title=Chương 6: Bàn luận và Khuyến nghị | chars=14625 | estimated_tokens=6978 | estimated_audio_seconds=1420
2026-05-28 11:40:27.858 | INFO | app.services.llm_service:normalize_text_for_speech:236 - Normalize strategy | mode=full | strategy=single_call | title=Chương 6: Bàn luận và Khuyến nghị
2026-05-28 11:40:30.327 | INFO | logging:callHandlers:1762 - 10.16.37.205:45425 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:40:31.272 | INFO | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 16 vectors for chapter_id=9f035864-cf8d-46b9-a6b4-04252a843795
2026-05-28 11:40:32.438 | INFO | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 15 vectors for chapter_id=8790e3e7-e077-4282-ad71-414382964eed
2026-05-28 11:40:34.140 | INFO | logging:callHandlers:1762 - 10.16.40.242:62850 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:40:34.243 | INFO | logging:callHandlers:1762 - 10.16.40.242:31265 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/details HTTP/1.1" 200
2026-05-28 11:40:37.956 | INFO | logging:callHandlers:1762 - 10.16.47.7:13003 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:40:41.741 | INFO | logging:callHandlers:1762 - 10.16.3.80:2652 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:40:45.893 | INFO | logging:callHandlers:1762 - 10.16.3.80:33389 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:40:50.364 | INFO | logging:callHandlers:1762 - 10.16.37.205:16112 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:40:54.278 | INFO | logging:callHandlers:1762 - 10.16.37.205:1522 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:40:58.165 | INFO | logging:callHandlers:1762 - 10.16.40.242:42283 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
[2026-05-28 11:41:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-28 11:41:02.277 | INFO | logging:callHandlers:1762 - 10.16.3.80:47624 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
[2026-05-28 11:41:03,127: INFO/MainProcess] Task triam.notifications.scan_due[f083f56d-278f-448f-8e74-ba3c635d867c] received
2026-05-28 11:41:05.999 | INFO | logging:callHandlers:1762 - 10.16.40.242:15585 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:41:09.879 | INFO | logging:callHandlers:1762 - 10.16.40.242:32549 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:41:10.377 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=True
[2026-05-28 11:41:10,838: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f083f56d-278f-448f-8e74-ba3c635d867c] succeeded in 7.709248495288193s: None
[2026-05-28 11:41:11,489: INFO/MainProcess] Task triam.notifications.deliver_due[0ba119e5-0684-409f-97c6-f9a2885c3fec] received
2026-05-28 11:41:14.068 | INFO | logging:callHandlers:1762 - 10.16.3.80:63889 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:41:15.806 | INFO | app.tasks.notification_tasks:deliver_due_notifications_task:67 - Notification delivery batch done | worker_id=notification-worker:a8d7100e-d551-439d-9157-0b9f5a11f270 | delivered_attempts=1
[2026-05-28 11:41:15,806: INFO/ForkPoolWorker-1] Task triam.notifications.deliver_due[0ba119e5-0684-409f-97c6-f9a2885c3fec] succeeded in 4.315776558127254s: None
2026-05-28 11:41:16.742 | INFO | logging:callHandlers:1762 - 10.16.3.80:63889 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 200
2026-05-28 11:41:17.870 | INFO | logging:callHandlers:1762 - 10.16.47.7:17306 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:41:20.722 | INFO | logging:callHandlers:1762 - 10.16.3.80:64403 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 200
2026-05-28 11:41:22.085 | INFO | logging:callHandlers:1762 - 10.16.3.80:64403 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:41:26.136 | INFO | logging:callHandlers:1762 - 10.16.47.7:3373 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:41:26.318 | INFO | app.services.llm_service:\_call_normalize_llm:203 - LLM normalize done | mode=full | context=single | scripts=34 | review_chars=1035
2026-05-28 11:41:26.319 | INFO | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=2 | mode=full | main_scripts=34 | review_chars=1035
2026-05-28 11:41:26.320 | INFO | app.services.workers.tts_worker:\_generate_main_segments:46 - TTS main segments start | chapter=2 | mode=full | total_scripts=34
2026-05-28 11:41:26.320 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=1/34 | chars=476
2026-05-28 11:41:26.336 | INFO | app.services.llm_service:\_call_normalize_llm:190 - LLM normalize start | mode=full | context=single | chars=14625 | attempt=1/2
2026-05-28 11:41:30.099 | INFO | logging:callHandlers:1762 - 10.16.40.242:6898 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:41:33.861 | INFO | logging:callHandlers:1762 - 10.16.37.205:43486 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:41:34.301 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=1/34 | duration_ms=29232
2026-05-28 11:41:34.302 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=2/34 | chars=279
2026-05-28 11:41:37.645 | INFO | logging:callHandlers:1762 - 10.16.40.242:29459 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:41:38.508 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=2/34 | duration_ms=15456
2026-05-28 11:41:38.509 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=3/34 | chars=340
2026-05-28 11:41:41.510 | INFO | logging:callHandlers:1762 - 10.16.40.242:20123 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:41:41.805 | INFO | logging:callHandlers:1762 - 10.16.47.7:63351 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 200
2026-05-28 11:41:43.790 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=3/34 | duration_ms=21888
2026-05-28 11:41:43.791 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=4/34 | chars=547
2026-05-28 11:41:45.668 | INFO | logging:callHandlers:1762 - 10.16.40.242:57956 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:41:49.331 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=4/34 | duration_ms=30216
2026-05-28 11:41:49.331 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=5/34 | chars=618
2026-05-28 11:41:49.729 | INFO | logging:callHandlers:1762 - 10.16.37.205:46195 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:41:53.571 | INFO | logging:callHandlers:1762 - 10.16.47.7:57318 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:41:57.481 | INFO | logging:callHandlers:1762 - 10.16.37.205:53566 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:41:58.809 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=5/34 | duration_ms=35664
2026-05-28 11:41:58.810 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=6/34 | chars=419
2026-05-28 11:42:01.294 | INFO | logging:callHandlers:1762 - 10.16.47.7:57727 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:42:02.053 | INFO | logging:callHandlers:1762 - 10.16.40.242:1512 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 200
[2026-05-28 11:42:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:42:02,911: INFO/MainProcess] Task triam.notifications.scan_due[7212c1da-d887-4f8f-ac64-9cf807f874a3] received
2026-05-28 11:42:05.186 | INFO | logging:callHandlers:1762 - 10.16.47.7:20633 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:42:09.325 | INFO | logging:callHandlers:1762 - 10.16.3.80:63379 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:42:09.461 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=6/34 | duration_ms=25056
2026-05-28 11:42:09.462 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=7/34 | chars=430
2026-05-28 11:42:10.146 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:42:10,147: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7212c1da-d887-4f8f-ac64-9cf807f874a3] succeeded in 7.235163147095591s: None
2026-05-28 11:42:10.944 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=7/34 | duration_ms=23832
2026-05-28 11:42:10.944 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=8/34 | chars=361
2026-05-28 11:42:13.070 | INFO | logging:callHandlers:1762 - 10.16.40.242:48045 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:42:15.224 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=8/34 | duration_ms=21144
2026-05-28 11:42:15.224 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=9/34 | chars=475
2026-05-28 11:42:16.922 | INFO | logging:callHandlers:1762 - 10.16.37.205:6293 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:42:19.574 | INFO | app.services.llm_service:\_call_normalize_llm:203 - LLM normalize done | mode=full | context=single | scripts=37 | review_chars=1004
2026-05-28 11:42:19.575 | INFO | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=3 | mode=full | main_scripts=37 | review_chars=1004
2026-05-28 11:42:19.575 | INFO | app.services.workers.tts_worker:\_generate_main_segments:46 - TTS main segments start | chapter=3 | mode=full | total_scripts=37
2026-05-28 11:42:19.576 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=1/37 | chars=423
2026-05-28 11:42:20.739 | INFO | logging:callHandlers:1762 - 10.16.3.80:9264 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:42:20.997 | INFO | logging:callHandlers:1762 - 10.16.3.80:3975 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 200
2026-05-28 11:42:22.987 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=9/34 | duration_ms=26712
2026-05-28 11:42:22.987 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=10/34 | chars=445
2026-05-28 11:42:24.829 | INFO | logging:callHandlers:1762 - 10.16.47.7:58955 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:42:25.188 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=1/37 | duration_ms=24720
2026-05-28 11:42:25.189 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=2/37 | chars=537
2026-05-28 11:42:28.615 | INFO | logging:callHandlers:1762 - 10.16.3.80:61525 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:42:28.689 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=10/34 | duration_ms=25392
2026-05-28 11:42:28.690 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=11/34 | chars=385
2026-05-28 11:42:32.622 | INFO | logging:callHandlers:1762 - 10.16.3.80:21631 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:42:34.603 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=2/37 | duration_ms=30144
2026-05-28 11:42:34.604 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=3/37 | chars=311
2026-05-28 11:42:35.801 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=11/34 | duration_ms=22416
2026-05-28 11:42:35.801 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=12/34 | chars=689
2026-05-28 11:42:36.471 | INFO | logging:callHandlers:1762 - 10.16.37.205:50306 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:42:37.749 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=3/37 | duration_ms=2880
2026-05-28 11:42:37.749 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=4/37 | chars=458
2026-05-28 11:42:40.559 | INFO | logging:callHandlers:1762 - 10.16.3.80:50716 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:42:44.715 | INFO | logging:callHandlers:1762 - 10.16.40.242:19332 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:42:45.024 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=12/34 | duration_ms=39936
2026-05-28 11:42:45.024 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=13/34 | chars=494
2026-05-28 11:42:45.985 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=4/37 | duration_ms=25344
2026-05-28 11:42:45.985 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=5/37 | chars=503
2026-05-28 11:42:48.784 | INFO | logging:callHandlers:1762 - 10.16.47.7:55919 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:42:49.148 | INFO | logging:callHandlers:1762 - 10.16.37.205:53557 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 200
2026-05-28 11:42:52.664 | INFO | logging:callHandlers:1762 - 10.16.3.80:9031 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:42:54.229 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=13/34 | duration_ms=29112
2026-05-28 11:42:54.229 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=14/34 | chars=771
2026-05-28 11:42:54.820 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=5/37 | duration_ms=29328
2026-05-28 11:42:54.821 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=6/37 | chars=334
2026-05-28 11:42:56.666 | INFO | logging:callHandlers:1762 - 10.16.40.242:53778 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:42:59.227 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=6/37 | duration_ms=18576
2026-05-28 11:42:59.227 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=7/37 | chars=504
2026-05-28 11:43:00.465 | INFO | logging:callHandlers:1762 - 10.16.3.80:62401 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
[2026-05-28 11:43:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-28 11:43:03.002 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=14/34 | duration_ms=45024
2026-05-28 11:43:03.003 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=15/34 | chars=457
[2026-05-28 11:43:03,134: INFO/MainProcess] Task triam.notifications.scan_due[125fea1b-1f6f-4db1-ae1a-54b4d1a8d5b4] received
2026-05-28 11:43:04.352 | INFO | logging:callHandlers:1762 - 10.16.37.205:15288 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:43:06.295 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=7/37 | duration_ms=28104
2026-05-28 11:43:06.296 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=8/37 | chars=413
2026-05-28 11:43:08.302 | INFO | logging:callHandlers:1762 - 10.16.3.80:23461 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:43:09.321 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=15/34 | duration_ms=26808
2026-05-28 11:43:09.321 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=16/34 | chars=349
2026-05-28 11:43:11.564 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:43:11,565: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[125fea1b-1f6f-4db1-ae1a-54b4d1a8d5b4] succeeded in 8.430221023969352s: None
2026-05-28 11:43:11.729 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=8/37 | duration_ms=24600
2026-05-28 11:43:11.730 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=9/37 | chars=335
2026-05-28 11:43:12.249 | INFO | logging:callHandlers:1762 - 10.16.3.80:59775 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:43:14.446 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=16/34 | duration_ms=21720
2026-05-28 11:43:14.447 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=17/34 | chars=530
2026-05-28 11:43:15.042 | INFO | logging:callHandlers:1762 - 10.16.3.80:59775 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 200
2026-05-28 11:43:16.101 | INFO | logging:callHandlers:1762 - 10.16.37.205:22713 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:43:16.203 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=17/34 | duration_ms=31896
2026-05-28 11:43:16.204 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=18/34 | chars=451
2026-05-28 11:43:17.934 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=9/37 | duration_ms=18096
2026-05-28 11:43:17.934 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=10/37 | chars=372
2026-05-28 11:43:19.871 | INFO | logging:callHandlers:1762 - 10.16.3.80:2063 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:43:22.367 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=18/34 | duration_ms=27720
2026-05-28 11:43:22.368 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=19/34 | chars=537
2026-05-28 11:43:23.283 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=10/37 | duration_ms=21240
2026-05-28 11:43:23.284 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=11/37 | chars=296
2026-05-28 11:43:23.926 | INFO | logging:callHandlers:1762 - 10.16.3.80:15592 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:43:28.042 | INFO | logging:callHandlers:1762 - 10.16.3.80:42711 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:43:28.073 | INFO | logging:callHandlers:1762 - 10.16.3.80:49419 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 422
2026-05-28 11:43:29.303 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=11/37 | duration_ms=16367
2026-05-28 11:43:29.304 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=12/37 | chars=334
2026-05-28 11:43:29.937 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=19/34 | duration_ms=29952
2026-05-28 11:43:29.940 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=20/34 | chars=401
2026-05-28 11:43:32.119 | INFO | logging:callHandlers:1762 - 10.16.3.80:56925 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:43:32.344 | INFO | logging:callHandlers:1762 - 10.16.3.80:49419 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 200
2026-05-28 11:43:35.516 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=20/34 | duration_ms=23424
2026-05-28 11:43:35.517 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=21/34 | chars=519
2026-05-28 11:43:35.917 | INFO | logging:callHandlers:1762 - 10.16.3.80:49419 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:43:36.720 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=12/37 | duration_ms=21840
2026-05-28 11:43:36.720 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=13/37 | chars=445
2026-05-28 11:43:37.858 | INFO | logging:callHandlers:1762 - 10.16.37.205:55662 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-28 11:43:39.936 | INFO | logging:callHandlers:1762 - 10.16.40.242:24364 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:43:41.966 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=13/37 | duration_ms=25416
2026-05-28 11:43:41.966 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=14/37 | chars=373
2026-05-28 11:43:43.426 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=21/34 | duration_ms=31968
2026-05-28 11:43:43.426 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=22/34 | chars=685
2026-05-28 11:43:43.774 | INFO | logging:callHandlers:1762 - 10.16.40.242:36472 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:43:46.380 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=14/37 | duration_ms=21888
2026-05-28 11:43:46.381 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=15/37 | chars=354
2026-05-28 11:43:47.571 | INFO | logging:callHandlers:1762 - 10.16.47.7:61094 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:43:51.623 | INFO | logging:callHandlers:1762 - 10.16.40.242:28034 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:43:53.530 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=22/34 | duration_ms=39840
2026-05-28 11:43:53.530 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=23/34 | chars=542
2026-05-28 11:43:54.604 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=15/37 | duration_ms=21168
2026-05-28 11:43:54.605 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=16/37 | chars=319
2026-05-28 11:43:55.550 | INFO | logging:callHandlers:1762 - 10.16.37.205:33705 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:43:59.578 | INFO | logging:callHandlers:1762 - 10.16.37.205:38512 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:43:59.709 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=16/37 | duration_ms=17160
2026-05-28 11:43:59.709 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=17/37 | chars=337
2026-05-28 11:44:01.030 | INFO | logging:callHandlers:1762 - 10.16.47.7:45081 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 200
[2026-05-28 11:44:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:44:02,912: INFO/MainProcess] Task triam.notifications.scan_due[82ec0174-b173-4fb0-8a33-a05cad080398] received
2026-05-28 11:44:03.131 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=23/34 | duration_ms=31536
2026-05-28 11:44:03.131 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=24/34 | chars=362
2026-05-28 11:44:03.406 | INFO | logging:callHandlers:1762 - 10.16.3.80:28696 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:44:04.254 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=17/37 | duration_ms=20064
2026-05-28 11:44:04.255 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=18/37 | chars=410
2026-05-28 11:44:07.158 | INFO | logging:callHandlers:1762 - 10.16.3.80:40891 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:44:09.822 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=24/34 | duration_ms=21576
2026-05-28 11:44:09.823 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=25/34 | chars=693
2026-05-28 11:44:10.037 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:44:10,037: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[82ec0174-b173-4fb0-8a33-a05cad080398] succeeded in 7.124734275043011s: None
2026-05-28 11:44:11.024 | INFO | logging:callHandlers:1762 - 10.16.47.7:51886 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:44:12.999 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=18/37 | duration_ms=23664
2026-05-28 11:44:13.000 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=19/37 | chars=207
2026-05-28 11:44:13.884 | INFO | logging:callHandlers:1762 - 10.16.3.80:28632 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 422
2026-05-28 11:44:14.825 | INFO | logging:callHandlers:1762 - 10.16.47.7:41014 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:44:16.454 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=19/37 | duration_ms=11544
2026-05-28 11:44:16.455 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=20/37 | chars=437
2026-05-28 11:44:18.597 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=25/34 | duration_ms=38640
2026-05-28 11:44:18.597 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=26/34 | chars=527
2026-05-28 11:44:18.979 | INFO | logging:callHandlers:1762 - 10.16.40.242:49675 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:44:22.436 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=20/37 | duration_ms=24480
2026-05-28 11:44:22.437 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=21/37 | chars=481
2026-05-28 11:44:22.843 | INFO | logging:callHandlers:1762 - 10.16.3.80:37061 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:44:24.554 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=26/34 | duration_ms=28656
2026-05-28 11:44:24.554 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=27/34 | chars=329
2026-05-28 11:44:25.711 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=27/34 | duration_ms=17592
2026-05-28 11:44:25.711 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=28/34 | chars=516
2026-05-28 11:44:26.877 | INFO | logging:callHandlers:1762 - 10.16.40.242:35303 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:44:29.636 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=21/37 | duration_ms=29616
2026-05-28 11:44:29.637 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=22/37 | chars=535
2026-05-28 11:44:30.844 | INFO | logging:callHandlers:1762 - 10.16.40.242:15896 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:44:34.913 | INFO | logging:callHandlers:1762 - 10.16.3.80:30899 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:44:35.308 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=28/34 | duration_ms=30336
2026-05-28 11:44:35.308 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=29/34 | chars=374
2026-05-28 11:44:36.302 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=22/37 | duration_ms=32928
2026-05-28 11:44:36.303 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=23/37 | chars=452
2026-05-28 11:44:38.696 | INFO | logging:callHandlers:1762 - 10.16.40.242:40966 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:44:38.944 | INFO | logging:callHandlers:1762 - 10.16.40.242:33026 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 200
2026-05-28 11:44:40.987 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=29/34 | duration_ms=20856
2026-05-28 11:44:40.987 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=30/34 | chars=455
2026-05-28 11:44:42.441 | INFO | logging:callHandlers:1762 - 10.16.47.7:34597 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:44:42.920 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=23/37 | duration_ms=26640
2026-05-28 11:44:42.921 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=24/37 | chars=263
2026-05-28 11:44:45.823 | INFO | logging:callHandlers:1762 - 10.16.37.205:51908 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 422
2026-05-28 11:44:46.291 | INFO | logging:callHandlers:1762 - 10.16.3.80:6644 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:44:46.704 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=30/34 | duration_ms=25344
2026-05-28 11:44:46.704 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=31/34 | chars=281
2026-05-28 11:44:47.579 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=24/37 | duration_ms=16175
2026-05-28 11:44:47.579 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=25/37 | chars=398
2026-05-28 11:44:50.127 | INFO | logging:callHandlers:1762 - 10.16.47.7:42368 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:44:51.812 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=31/34 | duration_ms=16704
2026-05-28 11:44:51.812 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=32/34 | chars=446
2026-05-28 11:44:53.462 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=25/37 | duration_ms=23928
2026-05-28 11:44:53.463 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=26/37 | chars=411
2026-05-28 11:44:54.036 | INFO | logging:callHandlers:1762 - 10.16.47.7:5650 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:44:57.190 | INFO | logging:callHandlers:1762 - 10.16.3.80:54394 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 200
2026-05-28 11:44:57.876 | INFO | logging:callHandlers:1762 - 10.16.3.80:37235 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:44:58.787 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=32/34 | duration_ms=28584
2026-05-28 11:44:58.788 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=33/34 | chars=409
2026-05-28 11:45:01.978 | INFO | logging:callHandlers:1762 - 10.16.3.80:48470 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
[2026-05-28 11:45:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:45:03,126: INFO/MainProcess] Task triam.notifications.scan_due[6c144ff0-e1de-445a-a46a-6a7238c63632] received
2026-05-28 11:45:04.042 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=26/37 | duration_ms=22800
2026-05-28 11:45:04.043 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=27/37 | chars=411
2026-05-28 11:45:05.010 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=33/34 | duration_ms=23904
2026-05-28 11:45:05.010 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=34/34 | chars=603
2026-05-28 11:45:05.745 | INFO | logging:callHandlers:1762 - 10.16.3.80:16052 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:45:09.682 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=27/37 | duration_ms=24576
2026-05-28 11:45:09.682 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=28/37 | chars=562
2026-05-28 11:45:09.710 | INFO | logging:callHandlers:1762 - 10.16.3.80:1311 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:45:10.194 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:45:10,195: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[6c144ff0-e1de-445a-a46a-6a7238c63632] succeeded in 7.067821940872818s: None
2026-05-28 11:45:10.249 | INFO | logging:callHandlers:1762 - 10.16.47.7:50913 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 422
2026-05-28 11:45:11.205 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=28/37 | duration_ms=31032
2026-05-28 11:45:11.206 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=29/37 | chars=412
2026-05-28 11:45:13.444 | INFO | logging:callHandlers:1762 - 10.16.3.80:65315 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:45:13.819 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=34/34 | duration_ms=35400
2026-05-28 11:45:13.819 | INFO | app.services.workers.tts_worker:\_generate_main_segments:80 - TTS main segments done | chapter=2 | mode=full | created_segments=34/34
2026-05-28 11:45:13.820 | INFO | app.services.workers.tts_worker:\_generate_review_audio:99 - TTS review start | chapter=2 | mode=full | chars=1035
2026-05-28 11:45:17.082 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=29/37 | duration_ms=23784
2026-05-28 11:45:17.083 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=30/37 | chars=371
2026-05-28 11:45:17.382 | INFO | logging:callHandlers:1762 - 10.16.3.80:21850 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:45:21.162 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=30/37 | duration_ms=19584
2026-05-28 11:45:21.164 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=31/37 | chars=374
2026-05-28 11:45:21.223 | INFO | logging:callHandlers:1762 - 10.16.37.205:30172 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:45:25.079 | INFO | logging:callHandlers:1762 - 10.16.3.80:7489 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:45:25.837 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=31/37 | duration_ms=23328
2026-05-28 11:45:25.838 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=32/37 | chars=284
2026-05-28 11:45:28.272 | INFO | app.services.workers.tts_worker:\_generate_review_audio:103 - TTS review done | chapter=2 | mode=full
2026-05-28 11:45:28.272 | INFO | app.services.workers.tts_worker:\_store_tts_result:120 - TTS DB store start | chapter_id=9f035864-cf8d-46b9-a6b4-04252a843795 | mode=full | segments=34 | review_audio=True
2026-05-28 11:45:28.955 | INFO | logging:callHandlers:1762 - 10.16.37.205:37953 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:45:31.627 | INFO | app.services.workers.tts_worker:\_store_tts_result:131 - TTS DB store done | chapter_id=9f035864-cf8d-46b9-a6b4-04252a843795 | mode=full
2026-05-28 11:45:33.257 | INFO | logging:callHandlers:1762 - 10.16.40.242:18595 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:45:34.085 | INFO | app.services.workers.chapter_worker:process_chapter:139 - ✅ Chapter 2 READY | mode=full | segments=34
2026-05-28 11:45:37.157 | INFO | logging:callHandlers:1762 - 10.16.47.7:30902 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:45:37.383 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=32/37 | duration_ms=15816
2026-05-28 11:45:37.384 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=33/37 | chars=392
2026-05-28 11:45:38.528 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=33/37 | duration_ms=23400
2026-05-28 11:45:38.529 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=34/37 | chars=252
2026-05-28 11:45:39.466 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=34/37 | duration_ms=13368
2026-05-28 11:45:39.467 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=35/37 | chars=570
2026-05-28 11:45:41.307 | INFO | logging:callHandlers:1762 - 10.16.40.242:55363 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:45:45.079 | INFO | logging:callHandlers:1762 - 10.16.47.7:56255 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:45:45.248 | INFO | logging:callHandlers:1762 - 10.16.3.80:32721 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:45:47.786 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=35/37 | duration_ms=31848
2026-05-28 11:45:47.787 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=36/37 | chars=391
2026-05-28 11:45:48.830 | INFO | logging:callHandlers:1762 - 10.16.37.205:60757 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:45:52.663 | INFO | logging:callHandlers:1762 - 10.16.47.7:44222 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:45:52.788 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=36/37 | duration_ms=21768
2026-05-28 11:45:52.788 | INFO | app.services.workers.tts_worker:\_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=37/37 | chars=395
2026-05-28 11:45:56.515 | INFO | logging:callHandlers:1762 - 10.16.47.7:33242 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:45:58.100 | INFO | app.services.workers.tts_worker:\_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=37/37 | duration_ms=20712
2026-05-28 11:45:58.101 | INFO | app.services.workers.tts_worker:\_generate_main_segments:80 - TTS main segments done | chapter=3 | mode=full | created_segments=37/37
2026-05-28 11:45:58.101 | INFO | app.services.workers.tts_worker:\_generate_review_audio:99 - TTS review start | chapter=3 | mode=full | chars=1004
2026-05-28 11:46:00.470 | INFO | logging:callHandlers:1762 - 10.16.3.80:61064 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
[2026-05-28 11:46:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:46:03,126: INFO/MainProcess] Task triam.notifications.scan_due[028a6acb-e647-4116-bd8a-fcf67a9b3c74] received
2026-05-28 11:46:04.537 | INFO | logging:callHandlers:1762 - 10.16.47.7:61824 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:46:08.718 | INFO | logging:callHandlers:1762 - 10.16.37.205:16116 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:46:09.363 | INFO | app.services.workers.tts_worker:\_generate_review_audio:103 - TTS review done | chapter=3 | mode=full
2026-05-28 11:46:09.364 | INFO | app.services.workers.tts_worker:\_store_tts_result:120 - TTS DB store start | chapter_id=8790e3e7-e077-4282-ad71-414382964eed | mode=full | segments=37 | review_audio=True
2026-05-28 11:46:09.407 | INFO | logging:callHandlers:1762 - 10.16.3.80:42632 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-28 11:46:10.194 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:46:10,194: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[028a6acb-e647-4116-bd8a-fcf67a9b3c74] succeeded in 7.066730024293065s: None
2026-05-28 11:46:10.527 | INFO | logging:callHandlers:1762 - 10.16.3.80:42632 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-28 11:46:12.458 | INFO | logging:callHandlers:1762 - 10.16.47.7:17366 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:46:12.773 | INFO | app.services.workers.tts_worker:\_store_tts_result:131 - TTS DB store done | chapter_id=8790e3e7-e077-4282-ad71-414382964eed | mode=full
2026-05-28 11:46:15.238 | INFO | app.services.workers.chapter_worker:process_chapter:139 - ✅ Chapter 3 READY | mode=full | segments=37
2026-05-28 11:46:16.436 | INFO | logging:callHandlers:1762 - 10.16.3.80:35496 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:46:18.302 | INFO | logging:callHandlers:1762 - 10.16.37.205:46806 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:46:19.707 | INFO | app.services.workers.book_pipeline:\_create_book_ready_notification_safely:142 - Content-ready book-ready event | book_id=0fb7d58f-9482-4903-8fee-6557072f61ea | mode=full | created=True
2026-05-28 11:46:20.319 | INFO | logging:callHandlers:1762 - 10.16.37.205:46806 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:46:21.478 | INFO | app.services.workers.book_pipeline:run_background_processing:410 - 🎉 Book 0fb7d58f-9482-4903-8fee-6557072f61ea READY — tất cả chapters đã xử lý xong.
[2026-05-28 11:46:21,484: INFO/ForkPoolWorker-1] Task triam.books.process[4612f236-81cf-4493-8ee0-d8ff27bc19a9] succeeded in 471.3293173429556s: None
2026-05-28 11:46:24.238 | INFO | logging:callHandlers:1762 - 10.16.3.80:15072 - "GET /api/v1/jobs/573861f9-b10a-4428-87de-198119ca15e0 HTTP/1.1" 200
2026-05-28 11:46:59.662 | INFO | logging:callHandlers:1762 - 10.16.47.7:41094 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-28 11:47:01.280 | INFO | logging:callHandlers:1762 - 10.16.3.80:21212 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
[2026-05-28 11:47:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:47:02,909: INFO/MainProcess] Task triam.notifications.scan_due[202b486f-78f2-48af-a4d0-d0663a4457be] received
2026-05-28 11:47:10.237 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=True
[2026-05-28 11:47:10,699: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[202b486f-78f2-48af-a4d0-d0663a4457be] succeeded in 7.564122517127544s: None
[2026-05-28 11:47:11,351: INFO/MainProcess] Task triam.notifications.deliver_due[d9be61ec-75c7-4703-b029-9f7d5bfb86c9] received
2026-05-28 11:47:15.563 | INFO | app.tasks.notification_tasks:deliver_due_notifications_task:67 - Notification delivery batch done | worker_id=notification-worker:75943927-9839-48aa-a41d-b72d65d6cd2d | delivered_attempts=1
[2026-05-28 11:47:15,563: INFO/ForkPoolWorker-1] Task triam.notifications.deliver_due[d9be61ec-75c7-4703-b029-9f7d5bfb86c9] succeeded in 4.210030289832503s: None
2026-05-28 11:47:27.597 | INFO | logging:callHandlers:1762 - 10.16.40.242:65075 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:47:38.898 | INFO | logging:callHandlers:1762 - 10.16.40.242:54897 - "GET /api/v1/health HTTP/1.1" 200
2026-05-28 11:47:41.046 | INFO | logging:callHandlers:1762 - 10.16.37.205:23338 - "GET /api/v1/books HTTP/1.1" 200
2026-05-28 11:47:50.601 | INFO | logging:callHandlers:1762 - 10.16.47.7:16945 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 200
2026-05-28 11:47:52.861 | INFO | logging:callHandlers:1762 - 10.16.3.80:54278 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:48:01.308 | INFO | logging:callHandlers:1762 - 10.16.3.80:15498 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/content HTTP/1.1" 404
[2026-05-28 11:48:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-28 11:48:02.658 | INFO | logging:callHandlers:1762 - 10.16.3.80:15498 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 422
[2026-05-28 11:48:03,127: INFO/MainProcess] Task triam.notifications.scan_due[c75e1ba5-bf76-4041-b05e-7448a3ed91ae] received
2026-05-28 11:48:04.634 | INFO | logging:callHandlers:1762 - 10.16.40.242:48330 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/content HTTP/1.1" 404
2026-05-28 11:48:08.272 | INFO | logging:callHandlers:1762 - 10.16.37.205:36949 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/content HTTP/1.1" 404
2026-05-28 11:48:10.426 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:48:10,427: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c75e1ba5-bf76-4041-b05e-7448a3ed91ae] succeeded in 7.074722738005221s: None
[2026-05-28 11:49:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:49:02,907: INFO/MainProcess] Task triam.notifications.scan_due[828aa271-465e-4f72-99a1-1d512a7edca0] received
2026-05-28 11:49:09.983 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:49:09,985: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[828aa271-465e-4f72-99a1-1d512a7edca0] succeeded in 7.077037603594363s: None
2026-05-28 11:49:22.459 | INFO | logging:callHandlers:1762 - 10.16.3.80:64397 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 200
2026-05-28 11:49:32.661 | INFO | logging:callHandlers:1762 - 10.16.40.242:18599 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:34.488 | INFO | logging:callHandlers:1762 - 10.16.40.242:18599 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:40.821 | INFO | logging:callHandlers:1762 - 10.16.3.80:22625 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:41.482 | INFO | logging:callHandlers:1762 - 10.16.3.80:44612 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:43.602 | INFO | logging:callHandlers:1762 - 10.16.37.205:7867 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:43.606 | INFO | logging:callHandlers:1762 - 10.16.40.242:36665 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:43.610 | INFO | logging:callHandlers:1762 - 10.16.40.242:15240 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:43.623 | INFO | logging:callHandlers:1762 - 10.16.40.242:22545 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:43.634 | INFO | logging:callHandlers:1762 - 10.16.40.242:9013 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:43.637 | INFO | logging:callHandlers:1762 - 10.16.3.80:12834 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:43.641 | INFO | logging:callHandlers:1762 - 10.16.3.80:38522 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:45.016 | INFO | logging:callHandlers:1762 - 10.16.3.80:27511 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:45.021 | INFO | logging:callHandlers:1762 - 10.16.3.80:36660 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:45.027 | INFO | logging:callHandlers:1762 - 10.16.37.205:43927 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:45.029 | INFO | logging:callHandlers:1762 - 10.16.37.205:3491 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:45.557 | INFO | logging:callHandlers:1762 - 10.16.3.80:52675 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:45.559 | INFO | logging:callHandlers:1762 - 10.16.37.205:46309 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:45.560 | INFO | logging:callHandlers:1762 - 10.16.40.242:11046 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:46.064 | INFO | logging:callHandlers:1762 - 10.16.40.242:51465 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:46.319 | INFO | logging:callHandlers:1762 - 10.16.3.80:51406 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:46.399 | INFO | logging:callHandlers:1762 - 10.16.40.242:53408 - "PUT /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/chapters/2be1315f-c635-4c4d-ab28-0d5cd401641c/progress HTTP/1.1" 200
2026-05-28 11:49:46.406 | INFO | logging:callHandlers:1762 - 10.16.40.242:61918 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:46.407 | INFO | logging:callHandlers:1762 - 10.16.47.7:46463 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:46.408 | INFO | logging:callHandlers:1762 - 10.16.3.80:45265 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:46.409 | INFO | logging:callHandlers:1762 - 10.16.47.7:63023 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:46.410 | INFO | logging:callHandlers:1762 - 10.16.3.80:22625 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:49:46.413 | INFO | logging:callHandlers:1762 - 10.16.40.242:57132 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
[2026-05-28 11:50:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:50:03,125: INFO/MainProcess] Task triam.notifications.scan_due[a196c29d-5113-4b1e-b058-8fc12fb6122a] received
2026-05-28 11:50:13.645 | INFO | logging:callHandlers:1762 - 10.16.3.80:20812 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:13.648 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:13.709 | INFO | logging:callHandlers:1762 - 10.16.3.80:23430 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:13.711 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:13.730 | INFO | logging:callHandlers:1762 - 10.16.37.205:8907 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:13.732 | INFO | logging:callHandlers:1762 - 10.16.3.80:64890 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:13.734 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:13.737 | INFO | logging:callHandlers:1762 - 10.16.3.80:43691 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:13.737 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:13.745 | INFO | logging:callHandlers:1762 - 10.16.47.7:14486 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:13.890 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:13.892 | INFO | logging:callHandlers:1762 - 10.16.37.205:54598 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:13.893 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:16.412 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:16.414 | INFO | logging:callHandlers:1762 - 10.16.40.242:32298 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:16.416 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:16.423 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:16.427 | INFO | logging:callHandlers:1762 - 10.16.47.7:49402 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:16.428 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:16.431 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:16.434 | INFO | logging:callHandlers:1762 - 10.16.40.242:19027 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:16.434 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:16.437 | INFO | logging:callHandlers:1762 - 10.16.3.80:6605 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:17.493 | INFO | logging:callHandlers:1762 - 10.16.47.7:19545 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:17.495 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.499 | INFO | logging:callHandlers:1762 - 10.16.3.80:54855 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:17.500 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.503 | INFO | logging:callHandlers:1762 - 10.16.37.205:7083 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:17.509 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.512 | INFO | logging:callHandlers:1762 - 10.16.47.7:44215 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:17.513 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.517 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.519 | INFO | logging:callHandlers:1762 - 10.16.40.242:60651 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:17.520 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.524 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.526 | INFO | logging:callHandlers:1762 - 10.16.40.242:54165 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:17.526 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.527 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.529 | INFO | logging:callHandlers:1762 - 10.16.3.80:36568 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:17.529 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.530 | INFO | logging:callHandlers:1762 - 10.16.40.242:22657 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:17.532 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.534 | INFO | logging:callHandlers:1762 - 10.16.47.7:7807 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:17.534 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.565 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.568 | INFO | logging:callHandlers:1762 - 10.16.47.7:25198 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:17.569 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.694 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.696 | INFO | logging:callHandlers:1762 - 10.16.37.205:57881 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:17.696 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.703 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.706 | INFO | logging:callHandlers:1762 - 10.16.3.80:12106 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:17.706 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.721 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.724 | INFO | logging:callHandlers:1762 - 10.16.3.80:63366 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:17.724 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.726 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.728 | INFO | logging:callHandlers:1762 - 10.16.3.80:30223 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:17.728 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.730 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.732 | INFO | logging:callHandlers:1762 - 10.16.47.7:10540 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:17.732 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.734 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.735 | INFO | logging:callHandlers:1762 - 10.16.47.7:38514 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:17.736 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.738 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.739 | INFO | logging:callHandlers:1762 - 10.16.3.80:42911 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:17.740 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.742 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:17.743 | INFO | logging:callHandlers:1762 - 10.16.3.80:22765 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:17.744 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:18.642 | INFO | logging:callHandlers:1762 - 10.16.3.80:33999 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:18.643 | INFO | logging:callHandlers:1762 - 10.16.40.242:9194 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:18.644 | INFO | logging:callHandlers:1762 - 10.16.40.242:28386 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:18.645 | INFO | logging:callHandlers:1762 - 10.16.3.80:18783 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:18.646 | INFO | logging:callHandlers:1762 - 10.16.37.205:20504 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:18.647 | INFO | logging:callHandlers:1762 - 10.16.40.242:40812 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:18.649 | INFO | logging:callHandlers:1762 - 10.16.40.242:43943 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:18.650 | INFO | logging:callHandlers:1762 - 10.16.3.80:8900 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:19.908 | INFO | logging:callHandlers:1762 - 10.16.47.7:29428 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:19.910 | INFO | logging:callHandlers:1762 - 10.16.3.80:32475 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:19.912 | INFO | logging:callHandlers:1762 - 10.16.47.7:63203 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:19.913 | INFO | logging:callHandlers:1762 - 10.16.40.242:57480 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:21.018 | INFO | logging:callHandlers:1762 - 10.16.3.80:50889 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:21.065 | INFO | logging:callHandlers:1762 - 10.16.3.80:18288 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:21.067 | INFO | logging:callHandlers:1762 - 10.16.3.80:1615 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:22.252 | INFO | logging:callHandlers:1762 - 10.16.37.205:63156 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:22.253 | INFO | logging:callHandlers:1762 - 10.16.47.7:27905 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:22.254 | INFO | logging:callHandlers:1762 - 10.16.3.80:7517 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:22.255 | INFO | logging:callHandlers:1762 - 10.16.40.242:40624 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:22.256 | INFO | logging:callHandlers:1762 - 10.16.47.7:40135 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:22.257 | INFO | logging:callHandlers:1762 - 10.16.40.242:17062 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:22.258 | INFO | logging:callHandlers:1762 - 10.16.40.242:52959 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:22.261 | INFO | logging:callHandlers:1762 - 10.16.3.80:10777 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:23.425 | INFO | logging:callHandlers:1762 - 10.16.3.80:10777 - "GET /?logs=container HTTP/1.1" 200
2026-05-28 11:50:23.760 | INFO | logging:callHandlers:1762 - 10.16.47.7:40135 - "GET /?logs=container HTTP/1.1" 200
2026-05-28 11:50:25.783 | INFO | logging:callHandlers:1762 - 10.16.3.80:60500 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:25.786 | INFO | logging:callHandlers:1762 - 10.16.3.80:44612 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:25.792 | INFO | logging:callHandlers:1762 - 10.16.3.80:22140 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:25.795 | INFO | logging:callHandlers:1762 - 10.16.3.80:59352 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:25.797 | INFO | logging:callHandlers:1762 - 10.16.37.205:62890 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:25.799 | INFO | logging:callHandlers:1762 - 10.16.37.205:62160 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:25.803 | INFO | logging:callHandlers:1762 - 10.16.40.242:28816 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:25.804 | INFO | logging:callHandlers:1762 - 10.16.37.205:31159 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:26.927 | INFO | logging:callHandlers:1762 - 10.16.3.80:2453 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:26.930 | INFO | logging:callHandlers:1762 - 10.16.37.205:16299 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:26.931 | INFO | logging:callHandlers:1762 - 10.16.3.80:62344 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:26.933 | INFO | logging:callHandlers:1762 - 10.16.47.7:59385 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:26.936 | INFO | logging:callHandlers:1762 - 10.16.37.205:27664 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:26.939 | INFO | logging:callHandlers:1762 - 10.16.3.80:62934 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:26.940 | INFO | logging:callHandlers:1762 - 10.16.3.80:29983 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 200
2026-05-28 11:50:28.704 | INFO | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-28 11:50:28,704: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a196c29d-5113-4b1e-b058-8fc12fb6122a] succeeded in 25.579065847210586s: None
2026-05-28 11:50:48.620 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:48.623 | INFO | logging:callHandlers:1762 - 10.16.37.205:54500 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:48.624 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:55.793 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:55.795 | INFO | logging:callHandlers:1762 - 10.16.40.242:57132 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:55.796 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:55.803 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:55.808 | INFO | logging:callHandlers:1762 - 10.16.3.80:27511 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:55.809 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:55.818 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:55.822 | INFO | logging:callHandlers:1762 - 10.16.37.205:3491 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:55.828 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:55.832 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:55.834 | INFO | logging:callHandlers:1762 - 10.16.3.80:29398 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:55.835 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:55.837 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:55.840 | INFO | logging:callHandlers:1762 - 10.16.3.80:45265 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:55.840 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:55.981 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:55.986 | INFO | logging:callHandlers:1762 - 10.16.47.7:21345 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:55.987 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.009 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.013 | INFO | logging:callHandlers:1762 - 10.16.3.80:60925 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:56.017 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.026 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.030 | INFO | logging:callHandlers:1762 - 10.16.47.7:31856 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:56.031 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.034 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.037 | INFO | logging:callHandlers:1762 - 10.16.47.7:46463 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:56.040 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.885 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.889 | INFO | logging:callHandlers:1762 - 10.16.47.7:59374 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:56.891 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.897 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.901 | INFO | logging:callHandlers:1762 - 10.16.3.80:48099 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:56.902 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.918 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.921 | INFO | logging:callHandlers:1762 - 10.16.40.242:11046 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:56.923 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.925 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.930 | INFO | logging:callHandlers:1762 - 10.16.40.242:53408 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:56.932 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.939 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.943 | INFO | logging:callHandlers:1762 - 10.16.37.205:9186 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:56.945 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.953 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.961 | INFO | logging:callHandlers:1762 - 10.16.47.7:29035 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:56.962 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.966 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.969 | INFO | logging:callHandlers:1762 - 10.16.3.80:51406 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:56.970 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.977 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:56.981 | INFO | logging:callHandlers:1762 - 10.16.3.80:52675 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:56.983 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:58.015 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:58.018 | INFO | logging:callHandlers:1762 - 10.16.37.205:65386 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:58.018 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:58.049 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:58.052 | INFO | logging:callHandlers:1762 - 10.16.37.205:26048 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:58.053 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:58.056 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:58.060 | INFO | logging:callHandlers:1762 - 10.16.37.205:24911 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:58.061 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:58.064 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:58.067 | INFO | logging:callHandlers:1762 - 10.16.37.205:43696 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:58.068 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:58.073 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:58.076 | INFO | logging:callHandlers:1762 - 10.16.37.205:55363 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:58.079 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:58.087 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:58.092 | INFO | logging:callHandlers:1762 - 10.16.3.80:65510 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:58.096 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:58.106 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:58.113 | INFO | logging:callHandlers:1762 - 10.16.40.242:16038 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:58.115 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:59.555 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
2026-05-28 11:50:59.558 | INFO | logging:callHandlers:1762 - 10.16.40.242:56047 - "GET /api/v1/books/0fb7d58f-9482-4903-8fee-6557072f61ea/learning-progress?mode=full HTTP/1.1" 500
2026-05-28 11:50:59.559 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "/home/user/app/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in **call**
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 736, in app
await route.handle(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/routing.py", line 290, in handle
await self.app(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 53, in wrapped_app
raise exc
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/\_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 101, in app
response = await f(request)
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "/home/user/app/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, **values)
File "/home/user/app/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "/home/user/app/.venv/lib/python3.12/site-packages/anyio/\_backends/\_asyncio.py", line 986, in run
result = context.run(func, *args)
File "/home/user/app/app/api/v1/routers/learning_progress.py", line 49, in get_book_learning_progress_endpoint
return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
File "/home/user/app/app/services/learning_progress_service.py", line 284, in get_book_learning_progress
\_load_owned_book(session, user_id=user_id, book_id=book_id)
File "/home/user/app/app/services/learning_progress_service.py", line 35, in \_load_owned_book
book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlmodel/orm/session.py", line 75, in exec
results = super().execute(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2351, in execute
return self.\_execute_internal(
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2239, in \_execute_internal
conn = self.\_connection_for_bind(bind)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2108, in \_connection_for_bind
return trans.\_connection_for_bind(engine, execution_options)
File "<string>", line 2, in \_connection_for_bind
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 137, in \_go
ret_value = fn(self, *arg, **kw)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1187, in \_connection_for_bind
conn = bind.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
return self.\_connection_cls(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in **init**
self.\_dbapi_connection = engine.raw_connection()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
return self.pool.connect()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
return \_ConnectionFairy.\_checkout(self)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in \_checkout
fairy = \_ConnectionRecord.checkout(pool)
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
rec = pool.\_do_get()
File "/home/user/app/.venv/lib/python3.12/site-packages/sqlalchemy/pool/impl.py", line 166, in \_do_get
raise exc.TimeoutError(
sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 20 reached, connection timed out, timeout 30.00 (Background on this error at: https://sqlalche.me/e/20/3o7r)
[2026-05-28 11:51:02,240: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-28 11:51:03,125: INFO/MainProcess] Task triam.notifications.scan_due[0419a725-95f6-465a-a5a1-effe94f59790] received
