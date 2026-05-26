===== Application Startup at 2026-05-26 09:32:35 =====

Starting realtime voice agent...
Starting Celery document worker...
Starting Celery notification worker...
Starting Celery Beat...
Starting FastAPI on port 7860...
celery beat v5.6.3 (recovery) is starting.
2026-05-26 09:36:51.126 | INFO     | logging:callHandlers:1762 - starting worker
{"message": "starting worker", "level": "INFO", "name": "livekit.agents", "version": "1.5.8", "rtc-version": "1.1.7", "timestamp": "2026-05-26T09:36:51.125798+00:00"}
2026-05-26 09:36:51.132 | INFO     | logging:callHandlers:1762 - plugin registered
{"message": "plugin registered", "level": "INFO", "name": "livekit.agents", "plugin": "livekit.plugins.openai", "version": "1.5.8", "timestamp": "2026-05-26T09:36:51.129631+00:00"}
2026-05-26 09:36:51.133 | INFO     | logging:callHandlers:1762 - preloading plugins
{"message": "preloading plugins", "level": "INFO", "name": "livekit.agents", "packages": ["livekit.plugins.openai", "av"], "timestamp": "2026-05-26T09:36:51.133492+00:00"}
2026-05-26 09:36:51.199 | INFO     | logging:callHandlers:1762 - HTTP server listening on :8081
{"message": "HTTP server listening on :8081", "level": "INFO", "name": "livekit.agents", "timestamp": "2026-05-26T09:36:51.199579+00:00"}
2026-05-26 09:36:51.223 | INFO     | logging:callHandlers:1762 - initializing job runner
{"message": "initializing job runner", "level": "INFO", "name": "livekit.agents", "tid": 44, "timestamp": "2026-05-26T09:36:51.223339+00:00"}
2026-05-26 09:36:51.235 | INFO     | logging:callHandlers:1762 - job runner initialized
{"message": "job runner initialized", "level": "INFO", "name": "livekit.agents", "tid": 44, "elapsed_time": 0.0, "timestamp": "2026-05-26T09:36:51.235737+00:00"}
2026-05-26 09:36:51.331 | INFO     | logging:callHandlers:1762 - registered worker
{"message": "registered worker", "level": "INFO", "name": "livekit.agents", "agent_name": "triam-voice-agent", "id": "AW_k2xvFKRiCr2q", "url": "wss://tri-am-bmdl413w.livekit.cloud", "region": "US East B", "protocol": 17, "timestamp": "2026-05-26T09:36:51.331310+00:00"}
__    -    ... __   -        _
LocalTime -> 2026-05-26 09:37:49
Configuration ->
    . broker -> redis://default:**@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0
    . loader -> celery.loaders.app.AppLoader
    . scheduler -> celery.beat.PersistentScheduler
    . db -> celerybeat-schedule
    . logfile -> [stderr]@%INFO
    . maxinterval -> 5.00 minutes (300s)
[2026-05-26 09:37:49,205: INFO/MainProcess] beat: Starting...
2026-05-26 09:37:49.769 | INFO     | logging:callHandlers:1762 - Started server process [30]
2026-05-26 09:37:49.770 | INFO     | logging:callHandlers:1762 - Waiting for application startup.
2026-05-26 09:37:49.771 | INFO     | app.main:lifespan:16 - Khởi động hệ thống... (TRIAM)
2026-05-26 09:37:49.772 | INFO     | logging:callHandlers:1762 - Application startup complete.
2026-05-26 09:37:49.772 | INFO     | logging:callHandlers:1762 - Uvicorn running on http://0.0.0.0:7860 (Press CTRL+C to quit)
 
 -------------- celery@r-khoasinoo-tri-am-backend-se9j9qq2-26caf-ftdnb v5.6.3 (recovery)
--- ***** ----- 
-- ******* ---- Linux-6.12.83-113.160.amzn2023.x86_64-x86_64-with-glibc2.41 2026-05-26 09:37:49
- *** --- * --- 
- ** ---------- [config]
- ** ---------- .> app:         triam:0x7f95f839fb90
- ** ---------- .> transport:   redis://default:**@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0
- ** ---------- .> results:     disabled://
- *** --- * --- .> concurrency: 1 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** ----- 
 -------------- [queues]
                .> document         exchange=document(direct) key=document
                

[tasks]
  . triam.books.process
  . triam.books.switch_mode
  . triam.notifications.deliver_due
  . triam.notifications.scan_due

 
 -------------- celery@r-khoasinoo-tri-am-backend-se9j9qq2-26caf-ftdnb v5.6.3 (recovery)
--- ***** ----- 
-- ******* ---- Linux-6.12.83-113.160.amzn2023.x86_64-x86_64-with-glibc2.41 2026-05-26 09:37:50
- *** --- * --- 
- ** ---------- [config]
- ** ---------- .> app:         triam:0x7fc346fe5d30
- ** ---------- .> transport:   redis://default:**@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0
- ** ---------- .> results:     disabled://
- *** --- * --- .> concurrency: 1 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** ----- 
 -------------- [queues]
                .> maintenance      exchange=maintenance(direct) key=maintenance
                .> notification     exchange=notification(direct) key=notification

[tasks]
  . triam.books.process
  . triam.books.switch_mode
  . triam.notifications.deliver_due
  . triam.notifications.scan_due

[2026-05-26 09:37:53,384: INFO/MainProcess] Connected to redis://default:**@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0
[2026-05-26 09:37:53,618: INFO/MainProcess] Connected to redis://default:**@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0
[2026-05-26 09:37:54,490: INFO/MainProcess] mingle: searching for neighbors
[2026-05-26 09:37:56,791: INFO/MainProcess] mingle: searching for neighbors
[2026-05-26 09:38:05,729: INFO/MainProcess] mingle: all alone
[2026-05-26 09:38:07,909: INFO/MainProcess] mingle: all alone
[2026-05-26 09:38:12,468: INFO/MainProcess] celery@r-khoasinoo-tri-am-backend-se9j9qq2-26caf-ftdnb ready.
[2026-05-26 09:38:13,114: INFO/MainProcess] celery@r-khoasinoo-tri-am-backend-se9j9qq2-26caf-ftdnb ready.
[2026-05-26 09:38:50,364: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:38:52,367: INFO/MainProcess] Task triam.notifications.scan_due[30765b65-4b64-4d67-b23f-e5d0db2ac6ec] received
2026-05-26 09:39:02.355 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:39:02,358: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[30765b65-4b64-4d67-b23f-e5d0db2ac6ec] succeeded in 9.767691703978926s: None
[2026-05-26 09:39:49,266: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:39:50,104: INFO/MainProcess] Task triam.notifications.scan_due[f96dbf37-2371-4d68-9374-5db36c056020] received
2026-05-26 09:39:56.633 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:39:56,633: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f96dbf37-2371-4d68-9374-5db36c056020] succeeded in 6.310151038924232s: None
2026-05-26 09:40:00.432 | INFO     | logging:callHandlers:1762 - 10.16.46.186:12625 - "GET /?logs=container HTTP/1.1" 200
2026-05-26 09:40:07.703 | INFO     | logging:callHandlers:1762 - 10.16.25.130:60736 - "GET /?logs=container HTTP/1.1" 200
2026-05-26 09:40:08.104 | INFO     | logging:callHandlers:1762 - 10.16.20.36:47077 - "GET /?logs=container HTTP/1.1" 200
[2026-05-26 09:40:49,270: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:40:50,160: INFO/MainProcess] Task triam.notifications.scan_due[43289172-d0fd-401e-8af4-0632fe7aaeb5] received
2026-05-26 09:40:56.691 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:40:56,692: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[43289172-d0fd-401e-8af4-0632fe7aaeb5] succeeded in 6.306679108995013s: None
[2026-05-26 09:41:49,270: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:41:50,161: INFO/MainProcess] Task triam.notifications.scan_due[369e11e1-3162-4896-ac60-2e8cc1733113] received
2026-05-26 09:41:56.705 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:41:56,706: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[369e11e1-3162-4896-ac60-2e8cc1733113] succeeded in 6.329295847914182s: None
[2026-05-26 09:42:49,271: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:42:50,161: INFO/MainProcess] Task triam.notifications.scan_due[ed8c24b5-65d6-4b32-94a0-47a3d94f8bd2] received
2026-05-26 09:42:56.733 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:42:56,735: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ed8c24b5-65d6-4b32-94a0-47a3d94f8bd2] succeeded in 6.359278569929302s: None
[2026-05-26 09:43:49,271: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:43:50,253: INFO/MainProcess] Task triam.notifications.scan_due[5607fd0b-bfa7-4a54-bbb6-663382aad1f7] received
2026-05-26 09:43:56.755 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:43:56,756: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5607fd0b-bfa7-4a54-bbb6-663382aad1f7] succeeded in 6.50162906490732s: None
2026-05-26 09:44:18.216 | INFO     | logging:callHandlers:1762 - 10.16.20.36:54683 - "GET /api/v1/health HTTP/1.1" 200
[2026-05-26 09:44:49,271: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:44:49,921: INFO/MainProcess] Task triam.notifications.scan_due[1ec29a0f-84e2-402d-b5f6-b4cc8f2818be] received
2026-05-26 09:44:56.233 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:44:56,235: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1ec29a0f-84e2-402d-b5f6-b4cc8f2818be] succeeded in 6.311751359025948s: None
[2026-05-26 09:45:49,271: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:45:50,141: INFO/MainProcess] Task triam.notifications.scan_due[acd5feee-66c7-4366-8b47-35a9d582c175] received
2026-05-26 09:45:56.674 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:45:56,675: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[acd5feee-66c7-4366-8b47-35a9d582c175] succeeded in 6.317924848990515s: None
[2026-05-26 09:46:49,274: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:46:50,145: INFO/MainProcess] Task triam.notifications.scan_due[b00661b7-5b88-448b-bd3b-dc0adb11c517] received
2026-05-26 09:46:56.691 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:46:56,693: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b00661b7-5b88-448b-bd3b-dc0adb11c517] succeeded in 6.334368387004361s: None
[2026-05-26 09:47:49,276: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:47:50,151: INFO/MainProcess] Task triam.notifications.scan_due[1f13276e-88ee-4d43-a780-c782672f1ce0] received
2026-05-26 09:47:56.680 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:47:56,682: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1f13276e-88ee-4d43-a780-c782672f1ce0] succeeded in 6.313355035032146s: None
[2026-05-26 09:48:49,277: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:48:50,149: INFO/MainProcess] Task triam.notifications.scan_due[4d304d5a-81de-435f-a7e0-1ddd8f86db0e] received
2026-05-26 09:48:56.668 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:48:56,669: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4d304d5a-81de-435f-a7e0-1ddd8f86db0e] succeeded in 6.303482070099562s: None
[2026-05-26 09:49:49,277: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:49:49,929: INFO/MainProcess] Task triam.notifications.scan_due[4687e99b-e263-4810-af5c-6b72689056f3] received
2026-05-26 09:49:56.231 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:49:56,231: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4687e99b-e263-4810-af5c-6b72689056f3] succeeded in 6.3002697239862755s: None
2026-05-26 09:50:43.252 | INFO     | logging:callHandlers:1762 - 10.16.25.130:63782 - "GET / HTTP/1.1" 200
[2026-05-26 09:50:49,278: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:50:50,150: INFO/MainProcess] Task triam.notifications.scan_due[e10865e4-e477-47b8-96b2-acb5138b062c] received
2026-05-26 09:50:56.669 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:50:56,669: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e10865e4-e477-47b8-96b2-acb5138b062c] succeeded in 6.305865155998617s: None
[2026-05-26 09:51:49,278: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:51:50,146: INFO/MainProcess] Task triam.notifications.scan_due[c43ff585-86b5-4924-a720-fa3ac360db5c] received
2026-05-26 09:51:56.471 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:51:56,471: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c43ff585-86b5-4924-a720-fa3ac360db5c] succeeded in 6.3234690049430355s: None
[2026-05-26 09:52:49,278: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:52:50,151: INFO/MainProcess] Task triam.notifications.scan_due[551f387c-32bb-434f-a750-c50ace82bca4] received
2026-05-26 09:52:56.472 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:52:56,473: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[551f387c-32bb-434f-a750-c50ace82bca4] succeeded in 6.319570990046486s: None
[2026-05-26 09:53:49,279: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:53:50,151: INFO/MainProcess] Task triam.notifications.scan_due[7508dc77-3fae-4831-a9e3-4eb2debeea31] received
2026-05-26 09:53:56.686 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:53:56,687: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7508dc77-3fae-4831-a9e3-4eb2debeea31] succeeded in 6.322002541972324s: None
[2026-05-26 09:54:49,279: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:54:50,038: INFO/MainProcess] Task triam.notifications.scan_due[d194fe93-bd51-468e-aef0-520746aefc79] received
2026-05-26 09:54:56.475 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:54:56,476: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d194fe93-bd51-468e-aef0-520746aefc79] succeeded in 6.435982550028712s: None
[2026-05-26 09:55:49,279: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:55:50,257: INFO/MainProcess] Task triam.notifications.scan_due[1060a074-ea14-4b0e-80fd-4650167734dc] received
2026-05-26 09:55:56.794 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:55:56,795: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1060a074-ea14-4b0e-80fd-4650167734dc] succeeded in 6.319116914994083s: None
[2026-05-26 09:56:49,292: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:56:50,035: INFO/MainProcess] Task triam.notifications.scan_due[3bdf94f6-dc90-429a-95c0-03f4f2c22302] received
2026-05-26 09:56:56.348 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:56:56,349: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3bdf94f6-dc90-429a-95c0-03f4f2c22302] succeeded in 6.31243846192956s: None
[2026-05-26 09:57:49,293: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:57:50,164: INFO/MainProcess] Task triam.notifications.scan_due[f9aa569b-d0a5-4dd1-828b-bc38f7e0c1eb] received
2026-05-26 09:57:56.720 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:57:56,721: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f9aa569b-d0a5-4dd1-828b-bc38f7e0c1eb] succeeded in 6.342949196929112s: None
[2026-05-26 09:58:49,294: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:58:50,252: INFO/MainProcess] Task triam.notifications.scan_due[ce8775b1-40df-4bf9-b43d-3bb7ac94bf25] received
2026-05-26 09:58:56.782 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:58:56,784: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ce8775b1-40df-4bf9-b43d-3bb7ac94bf25] succeeded in 6.311859843903221s: None
[2026-05-26 09:59:49,294: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 09:59:49,945: INFO/MainProcess] Task triam.notifications.scan_due[ea0e578c-75b6-4141-975f-dbb43eb4351a] received
2026-05-26 09:59:56.251 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 09:59:56,252: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ea0e578c-75b6-4141-975f-dbb43eb4351a] succeeded in 6.305902153020725s: None
[2026-05-26 10:00:49,294: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:00:50,156: INFO/MainProcess] Task triam.notifications.scan_due[714088bd-9034-469b-bea4-1ab217999695] received
2026-05-26 10:00:56.485 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:00:56,486: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[714088bd-9034-469b-bea4-1ab217999695] succeeded in 6.328090050024912s: None
[2026-05-26 10:01:49,296: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:01:49,944: INFO/MainProcess] Task triam.notifications.scan_due[babb8031-f41b-4359-a588-378bedca4053] received
2026-05-26 10:01:56.260 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:01:56,262: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[babb8031-f41b-4359-a588-378bedca4053] succeeded in 6.315751592977904s: None
[2026-05-26 10:02:49,297: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:02:50,200: INFO/MainProcess] Task triam.notifications.scan_due[aea743b7-86a5-410f-8fc7-7cbbcfc0d513] received
2026-05-26 10:02:56.518 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:02:56,519: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[aea743b7-86a5-410f-8fc7-7cbbcfc0d513] succeeded in 6.316419436014257s: None
[2026-05-26 10:03:49,296: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:03:50,158: INFO/MainProcess] Task triam.notifications.scan_due[7adafab9-ee9b-4469-9d68-332b4415decd] received
2026-05-26 10:03:56.716 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:03:56,717: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7adafab9-ee9b-4469-9d68-332b4415decd] succeeded in 6.331911207991652s: None
[2026-05-26 10:04:49,297: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:04:49,948: INFO/MainProcess] Task triam.notifications.scan_due[3adb0dfc-264d-49a2-b1d7-40965897f45b] received
2026-05-26 10:04:56.300 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:04:56,303: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3adb0dfc-264d-49a2-b1d7-40965897f45b] succeeded in 6.353214205009863s: None
[2026-05-26 10:05:49,303: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:05:50,166: INFO/MainProcess] Task triam.notifications.scan_due[9872f9f3-e372-4c05-b027-d61369b8ca50] received
2026-05-26 10:05:56.629 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:05:56,631: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[9872f9f3-e372-4c05-b027-d61369b8ca50] succeeded in 6.461647677002475s: None
[2026-05-26 10:06:49,308: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:06:50,059: INFO/MainProcess] Task triam.notifications.scan_due[4af2eb0c-9a45-4f71-b96e-75e18d2eb205] received
2026-05-26 10:06:56.381 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:06:56,384: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4af2eb0c-9a45-4f71-b96e-75e18d2eb205] succeeded in 6.32372047600802s: None
[2026-05-26 10:07:49,310: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:07:50,365: INFO/MainProcess] Task triam.notifications.scan_due[fb677756-7a28-4c8c-8b4a-d0e902f191d2] received
2026-05-26 10:07:56.703 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:07:56,708: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[fb677756-7a28-4c8c-8b4a-d0e902f191d2] succeeded in 6.337857686914504s: None
[2026-05-26 10:08:49,310: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:08:50,170: INFO/MainProcess] Task triam.notifications.scan_due[00980999-2b52-4798-a933-328115dd68b1] received
2026-05-26 10:08:56.714 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:08:56,716: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[00980999-2b52-4798-a933-328115dd68b1] succeeded in 6.32187513099052s: None
[2026-05-26 10:09:49,315: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:09:49,964: INFO/MainProcess] Task triam.notifications.scan_due[3af29817-8358-4fa8-8c81-a097c6c140f2] received
2026-05-26 10:09:57.814 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:09:57,815: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3af29817-8358-4fa8-8c81-a097c6c140f2] succeeded in 7.8486489079659805s: None
[2026-05-26 10:10:49,316: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:10:50,177: INFO/MainProcess] Task triam.notifications.scan_due[2635ddad-1543-4d86-a393-b2cf441586f4] received
2026-05-26 10:10:56.686 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:10:56,686: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2635ddad-1543-4d86-a393-b2cf441586f4] succeeded in 6.5072741729673s: None
[2026-05-26 10:11:49,317: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:11:49,966: INFO/MainProcess] Task triam.notifications.scan_due[ceacd555-811e-4f73-b009-8731149d1fd4] received
2026-05-26 10:11:56.465 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:11:56,466: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ceacd555-811e-4f73-b009-8731149d1fd4] succeeded in 6.496554629993625s: None
[2026-05-26 10:12:49,317: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:12:50,356: INFO/MainProcess] Task triam.notifications.scan_due[7940d148-f05f-4d13-a203-80748426524b] received
2026-05-26 10:12:56.857 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:12:56,858: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7940d148-f05f-4d13-a203-80748426524b] succeeded in 6.500374756986275s: None
[2026-05-26 10:13:49,317: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:13:50,184: INFO/MainProcess] Task triam.notifications.scan_due[8f889178-4a85-4495-b800-cef2ba1ebbaa] received
2026-05-26 10:13:56.902 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:13:56,903: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8f889178-4a85-4495-b800-cef2ba1ebbaa] succeeded in 6.493284931988455s: None
[2026-05-26 10:14:49,317: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:14:50,251: INFO/MainProcess] Task triam.notifications.scan_due[253ea3ae-4caa-408d-b01d-cd84d89566fd] received
2026-05-26 10:14:57.705 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:14:57,705: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[253ea3ae-4caa-408d-b01d-cd84d89566fd] succeeded in 6.586613917024806s: None
[2026-05-26 10:15:49,318: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:15:50,185: INFO/MainProcess] Task triam.notifications.scan_due[98d71aab-ca66-4b24-ab31-b9d661720148] received
2026-05-26 10:15:56.694 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:15:56,695: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[98d71aab-ca66-4b24-ab31-b9d661720148] succeeded in 6.505491961026564s: None
[2026-05-26 10:16:49,319: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:16:50,009: INFO/MainProcess] Task triam.notifications.scan_due[4ea3e878-04d6-417c-b60a-458e16afa366] received
2026-05-26 10:16:56.355 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:16:56,357: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4ea3e878-04d6-417c-b60a-458e16afa366] succeeded in 6.3466458229813725s: None
[2026-05-26 10:17:49,319: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:17:50,288: INFO/MainProcess] Task triam.notifications.scan_due[89597071-2a3a-4b20-9d2d-dd9a77983090] received
2026-05-26 10:17:56.624 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:17:56,625: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[89597071-2a3a-4b20-9d2d-dd9a77983090] succeeded in 6.335975980968215s: None
[2026-05-26 10:18:49,319: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:18:50,189: INFO/MainProcess] Task triam.notifications.scan_due[58953e36-e55f-4237-999a-ba878c82890c] received
2026-05-26 10:18:56.517 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:18:56,519: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[58953e36-e55f-4237-999a-ba878c82890c] succeeded in 6.328348299022764s: None
[2026-05-26 10:19:49,319: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:19:50,185: INFO/MainProcess] Task triam.notifications.scan_due[cb28e446-9921-4c57-a107-7faa2441127f] received
2026-05-26 10:19:56.518 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:19:56,521: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[cb28e446-9921-4c57-a107-7faa2441127f] succeeded in 6.3336365529103205s: None
[2026-05-26 10:20:49,319: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:20:50,194: INFO/MainProcess] Task triam.notifications.scan_due[ecba53ec-4fb0-4398-86e9-8d8412c9b3dc] received
2026-05-26 10:20:56.532 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:20:56,533: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ecba53ec-4fb0-4398-86e9-8d8412c9b3dc] succeeded in 6.335130385006778s: None
[2026-05-26 10:21:49,319: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:21:50,010: INFO/MainProcess] Task triam.notifications.scan_due[ef067eca-cf23-4ae9-9b8b-64f3254bfec2] received
2026-05-26 10:21:56.351 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:21:56,352: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ef067eca-cf23-4ae9-9b8b-64f3254bfec2] succeeded in 6.34000761504285s: None
[2026-05-26 10:22:49,319: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:22:50,359: INFO/MainProcess] Task triam.notifications.scan_due[db67e9de-ea4e-4219-b7cf-124848598e9e] received
2026-05-26 10:22:56.716 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:22:56,717: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[db67e9de-ea4e-4219-b7cf-124848598e9e] succeeded in 6.3554171189898625s: None
[2026-05-26 10:23:49,320: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:23:50,187: INFO/MainProcess] Task triam.notifications.scan_due[87b9cfae-fe11-4fc4-94ec-100fa4c444ca] received
2026-05-26 10:23:56.658 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:23:56,659: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[87b9cfae-fe11-4fc4-94ec-100fa4c444ca] succeeded in 6.471628715982661s: None
[2026-05-26 10:24:49,320: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:24:50,187: INFO/MainProcess] Task triam.notifications.scan_due[ad26e265-f337-4515-b7c8-c58ae5370b60] received
2026-05-26 10:24:56.551 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:24:56,555: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ad26e265-f337-4515-b7c8-c58ae5370b60] succeeded in 6.366889013093896s: None
[2026-05-26 10:25:49,321: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:25:50,187: INFO/MainProcess] Task triam.notifications.scan_due[6e2aaa23-6082-4649-b3a9-16e7493ab01d] received
2026-05-26 10:25:56.529 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:25:56,530: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[6e2aaa23-6082-4649-b3a9-16e7493ab01d] succeeded in 6.342053264030255s: None
[2026-05-26 10:26:49,328: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:26:49,979: INFO/MainProcess] Task triam.notifications.scan_due[b199fe94-9854-4185-a9e1-1de0945ebaa1] received
2026-05-26 10:26:56.316 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:26:56,317: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b199fe94-9854-4185-a9e1-1de0945ebaa1] succeeded in 6.336650734068826s: None
[2026-05-26 10:27:49,332: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:27:50,311: INFO/MainProcess] Task triam.notifications.scan_due[85c81c9d-efff-42c0-90f9-15580c05b70e] received
2026-05-26 10:27:56.665 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:27:56,666: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[85c81c9d-efff-42c0-90f9-15580c05b70e] succeeded in 6.354458132991567s: None
[2026-05-26 10:28:49,328: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:28:50,200: INFO/MainProcess] Task triam.notifications.scan_due[bb5defb7-1fec-40b6-a10d-11d28abe9411] received
2026-05-26 10:28:56.532 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:28:56,533: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[bb5defb7-1fec-40b6-a10d-11d28abe9411] succeeded in 6.3320008009905s: None
[2026-05-26 10:29:49,329: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:29:50,205: INFO/MainProcess] Task triam.notifications.scan_due[e95df4d6-7293-4e01-9000-2ea1f553ac78] received
2026-05-26 10:29:56.552 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:29:56,553: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e95df4d6-7293-4e01-9000-2ea1f553ac78] succeeded in 6.341474713990465s: None
[2026-05-26 10:30:49,330: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:30:50,205: INFO/MainProcess] Task triam.notifications.scan_due[ece96c88-cd38-4296-81c7-b0b929126329] received
2026-05-26 10:30:56.579 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:30:56,580: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ece96c88-cd38-4296-81c7-b0b929126329] succeeded in 6.372506128973328s: None
[2026-05-26 10:31:49,332: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:31:49,988: INFO/MainProcess] Task triam.notifications.scan_due[d30796c4-ad17-452c-99fa-58d3d091a8a2] received
2026-05-26 10:31:56.482 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:31:56,483: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d30796c4-ad17-452c-99fa-58d3d091a8a2] succeeded in 6.492497676983476s: None
[2026-05-26 10:32:49,340: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:32:50,262: INFO/MainProcess] Task triam.notifications.scan_due[148b9ce9-3728-4662-9401-50019731009b] received
2026-05-26 10:32:56.602 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:32:56,602: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[148b9ce9-3728-4662-9401-50019731009b] succeeded in 6.33935409609694s: None
[2026-05-26 10:33:49,350: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:33:50,221: INFO/MainProcess] Task triam.notifications.scan_due[f497dd20-48c5-4d87-9022-bd0d016de3bb] received
2026-05-26 10:33:56.775 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:33:56,780: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f497dd20-48c5-4d87-9022-bd0d016de3bb] succeeded in 6.332352346042171s: None
[2026-05-26 10:34:49,350: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:34:50,231: INFO/MainProcess] Task triam.notifications.scan_due[cae94d99-9755-46aa-a936-8c41b7296c95] received
2026-05-26 10:34:56.612 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:34:56,613: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[cae94d99-9755-46aa-a936-8c41b7296c95] succeeded in 6.379523401032202s: None
[2026-05-26 10:35:49,363: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:35:50,236: INFO/MainProcess] Task triam.notifications.scan_due[ed96026a-e765-4974-af04-77c7285dc93d] received
2026-05-26 10:35:56.578 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:35:56,578: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ed96026a-e765-4974-af04-77c7285dc93d] succeeded in 6.339999156072736s: None
[2026-05-26 10:36:49,363: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:36:50,021: INFO/MainProcess] Task triam.notifications.scan_due[621f798d-017e-43ef-b2a1-db160f10a132] received
2026-05-26 10:36:56.344 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:36:56,345: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[621f798d-017e-43ef-b2a1-db160f10a132] succeeded in 6.3230582169489935s: None
[2026-05-26 10:37:49,364: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:37:50,242: INFO/MainProcess] Task triam.notifications.scan_due[22838c79-c655-4af6-b526-ad12f48cb0d0] received
2026-05-26 10:37:56.580 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:37:56,581: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[22838c79-c655-4af6-b526-ad12f48cb0d0] succeeded in 6.337017599027604s: None
[2026-05-26 10:38:49,370: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:38:50,037: INFO/MainProcess] Task triam.notifications.scan_due[306af2be-18d4-4a3b-a062-a9c7ff59d699] received
2026-05-26 10:38:56.380 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:38:56,380: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[306af2be-18d4-4a3b-a062-a9c7ff59d699] succeeded in 6.34223250602372s: None
[2026-05-26 10:39:49,371: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:39:50,251: INFO/MainProcess] Task triam.notifications.scan_due[1806157e-0bda-4f12-9c09-748c4b4bce4f] received
2026-05-26 10:39:57.711 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:39:57,712: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1806157e-0bda-4f12-9c09-748c4b4bce4f] succeeded in 7.457696477067657s: None
[2026-05-26 10:40:49,372: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:40:50,251: INFO/MainProcess] Task triam.notifications.scan_due[527fb145-d06e-45d6-a492-035e713d5351] received
2026-05-26 10:40:56.444 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:40:56,444: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[527fb145-d06e-45d6-a492-035e713d5351] succeeded in 6.1904882460366935s: None
[2026-05-26 10:41:49,373: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:41:50,114: INFO/MainProcess] Task triam.notifications.scan_due[f9058f66-23c4-4e1f-92cb-059f1d1933b9] received
2026-05-26 10:41:56.305 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:41:56,306: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f9058f66-23c4-4e1f-92cb-059f1d1933b9] succeeded in 6.189769034041092s: None
[2026-05-26 10:42:49,374: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:42:50,438: INFO/MainProcess] Task triam.notifications.scan_due[bb949883-aec6-4c15-aece-c98d60ad1131] received
2026-05-26 10:42:56.770 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:42:56,771: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[bb949883-aec6-4c15-aece-c98d60ad1131] succeeded in 6.329732595011592s: None
[2026-05-26 10:43:49,374: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:43:50,038: INFO/MainProcess] Task triam.notifications.scan_due[c38587b6-c2ca-4971-93fb-e4d29f27c51a] received
2026-05-26 10:43:56.227 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:43:56,228: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c38587b6-c2ca-4971-93fb-e4d29f27c51a] succeeded in 6.187697681016289s: None
[2026-05-26 10:44:49,374: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:44:50,245: INFO/MainProcess] Task triam.notifications.scan_due[88d5aa76-7164-4df7-bb74-d68f37693c3d] received
2026-05-26 10:44:56.429 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:44:56,430: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[88d5aa76-7164-4df7-bb74-d68f37693c3d] succeeded in 6.182388687971979s: None
[2026-05-26 10:45:49,377: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:45:50,286: INFO/MainProcess] Task triam.notifications.scan_due[011dc661-9276-4f23-8eb4-70a32ce046a2] received
2026-05-26 10:45:56.464 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:45:56,465: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[011dc661-9276-4f23-8eb4-70a32ce046a2] succeeded in 6.178467131918296s: None
[2026-05-26 10:46:49,377: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:46:50,082: INFO/MainProcess] Task triam.notifications.scan_due[c608a259-cea6-49d8-931b-efd925d43afb] received
2026-05-26 10:46:56.263 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:46:56,264: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c608a259-cea6-49d8-931b-efd925d43afb] succeeded in 6.178742119926028s: None
[2026-05-26 10:47:49,378: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:47:50,247: INFO/MainProcess] Task triam.notifications.scan_due[8a0bf6d0-3c80-4a51-9311-8d63b9edcd0b] received
2026-05-26 10:47:56.438 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:47:56,439: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8a0bf6d0-3c80-4a51-9311-8d63b9edcd0b] succeeded in 6.190470847999677s: None
[2026-05-26 10:48:49,379: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:48:50,034: INFO/MainProcess] Task triam.notifications.scan_due[1e7913cd-a10f-488e-ae27-db1e9bd347df] received
2026-05-26 10:48:56.216 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:48:56,217: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1e7913cd-a10f-488e-ae27-db1e9bd347df] succeeded in 6.181092952028848s: None
[2026-05-26 10:49:49,379: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:49:50,247: INFO/MainProcess] Task triam.notifications.scan_due[fb359605-3d39-4647-a38e-89f57c09d6e0] received
2026-05-26 10:49:56.659 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:49:56,661: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[fb359605-3d39-4647-a38e-89f57c09d6e0] succeeded in 6.18503359798342s: None
[2026-05-26 10:50:49,379: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:50:50,256: INFO/MainProcess] Task triam.notifications.scan_due[90d0e178-b6a6-4e63-bfce-eb5a3b427850] received
2026-05-26 10:50:56.435 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:50:56,437: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[90d0e178-b6a6-4e63-bfce-eb5a3b427850] succeeded in 6.175967965042219s: None
[2026-05-26 10:51:49,380: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:51:50,036: INFO/MainProcess] Task triam.notifications.scan_due[36118956-0e8c-4779-a23f-9d8bc508ad2f] received
2026-05-26 10:51:52.811 | INFO     | logging:callHandlers:1762 - 10.16.17.88:57859 - "GET /?logs=container HTTP/1.1" 200
2026-05-26 10:51:56.216 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:51:56,218: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[36118956-0e8c-4779-a23f-9d8bc508ad2f] succeeded in 6.181230786954984s: None
[2026-05-26 10:52:49,380: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:52:50,372: INFO/MainProcess] Task triam.notifications.scan_due[ac81662d-e5bc-4b76-8d99-0b38b641eaca] received
2026-05-26 10:52:56.550 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:52:56,551: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ac81662d-e5bc-4b76-8d99-0b38b641eaca] succeeded in 6.178046517074108s: None
[2026-05-26 10:53:49,380: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:53:50,035: INFO/MainProcess] Task triam.notifications.scan_due[b513904c-8a80-4270-956b-49c15885a37b] received
2026-05-26 10:53:56.211 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:53:56,213: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b513904c-8a80-4270-956b-49c15885a37b] succeeded in 6.176915928022936s: None
[2026-05-26 10:54:49,380: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:54:50,333: INFO/MainProcess] Task triam.notifications.scan_due[bcbc08e9-31af-4437-96de-f99c47b77f47] received
2026-05-26 10:54:56.629 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:54:56,630: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[bcbc08e9-31af-4437-96de-f99c47b77f47] succeeded in 6.294255431042984s: None
[2026-05-26 10:55:49,381: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:55:50,251: INFO/MainProcess] Task triam.notifications.scan_due[679f3427-deef-4bea-9cad-a2fd9d6ae6e2] received
2026-05-26 10:55:56.473 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:55:56,475: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[679f3427-deef-4bea-9cad-a2fd9d6ae6e2] succeeded in 6.2220997989643365s: None
[2026-05-26 10:56:49,380: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:56:50,226: INFO/MainProcess] Task triam.notifications.scan_due[de024b1c-dd8c-4491-8d71-528f4c9c42b1] received
2026-05-26 10:56:56.411 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:56:56,418: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[de024b1c-dd8c-4491-8d71-528f4c9c42b1] succeeded in 6.189254046999849s: None
[2026-05-26 10:57:49,380: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:57:50,336: INFO/MainProcess] Task triam.notifications.scan_due[8031039c-4492-4a50-bedb-405addde324c] received
2026-05-26 10:57:56.509 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:57:56,510: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8031039c-4492-4a50-bedb-405addde324c] succeeded in 6.1706773929763585s: None
[2026-05-26 10:58:49,380: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:58:50,034: INFO/MainProcess] Task triam.notifications.scan_due[b000304c-b33f-4b47-aafc-6ed0933b280c] received
2026-05-26 10:58:56.221 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:58:56,222: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b000304c-b33f-4b47-aafc-6ed0933b280c] succeeded in 6.187507270020433s: None
[2026-05-26 10:59:49,386: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 10:59:50,256: INFO/MainProcess] Task triam.notifications.scan_due[6f3a3248-0d6b-44aa-b606-e20ea34d83df] received
2026-05-26 10:59:56.455 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 10:59:56,457: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[6f3a3248-0d6b-44aa-b606-e20ea34d83df] succeeded in 6.198846654966474s: None
[2026-05-26 11:00:49,386: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:00:50,252: INFO/MainProcess] Task triam.notifications.scan_due[7c8e5c3e-335c-4e10-a829-2f454d7eded6] received
2026-05-26 11:00:56.443 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:00:56,444: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7c8e5c3e-335c-4e10-a829-2f454d7eded6] succeeded in 6.189067251980305s: None
[2026-05-26 11:01:49,386: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:01:50,373: INFO/MainProcess] Task triam.notifications.scan_due[4e7e1875-2f4b-444e-886b-b14729333314] received
2026-05-26 11:01:56.568 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:01:56,568: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4e7e1875-2f4b-444e-886b-b14729333314] succeeded in 6.19246692804154s: None
[2026-05-26 11:02:49,386: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:02:50,310: INFO/MainProcess] Task triam.notifications.scan_due[cbb455b9-61e8-4c66-8798-c15390a5d20f] received
2026-05-26 11:02:56.518 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:02:56,519: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[cbb455b9-61e8-4c66-8798-c15390a5d20f] succeeded in 6.207522559096105s: None
[2026-05-26 11:03:49,386: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:03:50,170: INFO/MainProcess] Task triam.notifications.scan_due[f004aa3a-07ce-4341-9fa8-03b66ba29939] received
2026-05-26 11:03:56.377 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:03:56,378: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f004aa3a-07ce-4341-9fa8-03b66ba29939] succeeded in 6.2076687649823725s: None
[2026-05-26 11:04:49,387: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:04:50,258: INFO/MainProcess] Task triam.notifications.scan_due[c1f6a2d9-e02d-4f72-9e17-f31e6c914f7e] received
2026-05-26 11:04:56.457 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:04:56,458: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c1f6a2d9-e02d-4f72-9e17-f31e6c914f7e] succeeded in 6.1930862159933895s: None
[2026-05-26 11:05:49,388: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:05:50,394: INFO/MainProcess] Task triam.notifications.scan_due[a45c56a9-71b8-463b-a343-3685f0529b28] received
2026-05-26 11:05:56.578 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:05:56,579: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a45c56a9-71b8-463b-a343-3685f0529b28] succeeded in 6.1828497420065105s: None
[2026-05-26 11:06:49,389: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:06:50,390: INFO/MainProcess] Task triam.notifications.scan_due[5832a164-11a6-49c9-8f10-ae8961777ddf] received
2026-05-26 11:06:56.578 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:06:56,579: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5832a164-11a6-49c9-8f10-ae8961777ddf] succeeded in 6.18781365104951s: None
[2026-05-26 11:07:49,390: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:07:50,536: INFO/MainProcess] Task triam.notifications.scan_due[51c4480c-0463-4c77-a565-164425e5db85] received
2026-05-26 11:07:56.746 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:07:56,747: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[51c4480c-0463-4c77-a565-164425e5db85] succeeded in 6.210467647993937s: None
[2026-05-26 11:08:49,391: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:08:50,196: INFO/MainProcess] Task triam.notifications.scan_due[d0e87d11-1fa7-41af-a38b-900e4ee609d0] received
2026-05-26 11:08:56.392 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:08:56,392: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d0e87d11-1fa7-41af-a38b-900e4ee609d0] succeeded in 6.193808116018772s: None
[2026-05-26 11:09:49,392: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:09:50,260: INFO/MainProcess] Task triam.notifications.scan_due[79275271-7771-4d8d-b4a3-f4bad5a96498] received
2026-05-26 11:09:58.110 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:09:58,111: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[79275271-7771-4d8d-b4a3-f4bad5a96498] succeeded in 7.846620702068321s: None
[2026-05-26 11:10:49,395: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:10:50,337: INFO/MainProcess] Task triam.notifications.scan_due[c59b7054-3baf-4e65-b7eb-f2e862f45f7c] received
2026-05-26 11:10:56.832 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:10:56,833: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c59b7054-3baf-4e65-b7eb-f2e862f45f7c] succeeded in 6.494513910030946s: None
[2026-05-26 11:11:49,395: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:11:50,264: INFO/MainProcess] Task triam.notifications.scan_due[5c0cfe9e-8e5c-44d6-b5a5-2cca16adfafc] received
2026-05-26 11:11:56.759 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:11:56,760: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5c0cfe9e-8e5c-44d6-b5a5-2cca16adfafc] succeeded in 6.495411600917578s: None
[2026-05-26 11:12:49,395: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:12:50,463: INFO/MainProcess] Task triam.notifications.scan_due[c45d28da-e3a7-4c58-8072-ced89eb1cd6f] received
2026-05-26 11:12:56.981 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:12:56,982: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c45d28da-e3a7-4c58-8072-ced89eb1cd6f] succeeded in 6.516584545024671s: None
[2026-05-26 11:13:49,395: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:13:50,049: INFO/MainProcess] Task triam.notifications.scan_due[0fb8952f-600b-4dfd-942c-303afc87c249] received
2026-05-26 11:13:56.681 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:13:56,683: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[0fb8952f-600b-4dfd-942c-303afc87c249] succeeded in 6.633190254913643s: None
[2026-05-26 11:14:49,395: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:14:50,444: INFO/MainProcess] Task triam.notifications.scan_due[0e8bef0b-ba4f-4591-9d50-61456e139115] received
2026-05-26 11:14:57.184 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:14:57,185: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[0e8bef0b-ba4f-4591-9d50-61456e139115] succeeded in 6.5165366410510615s: None
[2026-05-26 11:15:49,395: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:15:50,274: INFO/MainProcess] Task triam.notifications.scan_due[f07ecc02-638f-4112-a802-54e51f1627c3] received
2026-05-26 11:15:56.765 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:15:56,765: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f07ecc02-638f-4112-a802-54e51f1627c3] succeeded in 6.490213676006533s: None
[2026-05-26 11:16:49,395: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:16:50,268: INFO/MainProcess] Task triam.notifications.scan_due[df39d0bb-f08d-4a20-b952-e15517ec2c91] received
2026-05-26 11:16:56.770 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:16:56,772: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[df39d0bb-f08d-4a20-b952-e15517ec2c91] succeeded in 6.502763759926893s: None
[2026-05-26 11:17:49,396: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:17:50,394: INFO/MainProcess] Task triam.notifications.scan_due[37b9df33-8d83-4c93-9f6a-16e6951aa68e] received
2026-05-26 11:17:56.912 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:17:56,912: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[37b9df33-8d83-4c93-9f6a-16e6951aa68e] succeeded in 6.515926953055896s: None
[2026-05-26 11:18:49,396: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:18:50,051: INFO/MainProcess] Task triam.notifications.scan_due[8a6deab0-54a5-4d6d-8cac-b5fce47bb5be] received
2026-05-26 11:18:56.571 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:18:56,572: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8a6deab0-54a5-4d6d-8cac-b5fce47bb5be] succeeded in 6.517363862018101s: None
[2026-05-26 11:19:49,396: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:19:50,267: INFO/MainProcess] Task triam.notifications.scan_due[86a411a1-9f29-4587-b18b-e9fab2be465d] received
2026-05-26 11:19:56.770 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:19:56,770: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[86a411a1-9f29-4587-b18b-e9fab2be465d] succeeded in 6.500937739969231s: None
[2026-05-26 11:20:49,397: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:20:50,051: INFO/MainProcess] Task triam.notifications.scan_due[66fdfafe-e339-4066-b2cd-e1e449c0bc66] received
2026-05-26 11:20:56.552 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:20:56,554: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[66fdfafe-e339-4066-b2cd-e1e449c0bc66] succeeded in 6.5015078170690686s: None
[2026-05-26 11:21:49,397: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:21:50,266: INFO/MainProcess] Task triam.notifications.scan_due[614f9463-a137-4ff6-8244-937b90346edc] received
2026-05-26 11:21:56.890 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:21:56,892: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[614f9463-a137-4ff6-8244-937b90346edc] succeeded in 6.624280409072526s: None
[2026-05-26 11:22:49,398: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:22:50,265: INFO/MainProcess] Task triam.notifications.scan_due[5a680711-e183-44b7-8e97-5b9efd7d2056] received
2026-05-26 11:22:56.890 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:22:56,892: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5a680711-e183-44b7-8e97-5b9efd7d2056] succeeded in 6.620358576066792s: None
[2026-05-26 11:23:49,398: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:23:50,053: INFO/MainProcess] Task triam.notifications.scan_due[c0e79a8c-6ad2-4c7a-90d3-0af8bd5559f2] received
2026-05-26 11:23:56.664 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:23:56,666: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c0e79a8c-6ad2-4c7a-90d3-0af8bd5559f2] succeeded in 6.611763695022091s: None
[2026-05-26 11:24:49,399: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:24:50,269: INFO/MainProcess] Task triam.notifications.scan_due[e23d3274-c5b7-4876-8f91-e91564b266ed] received
2026-05-26 11:24:56.835 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:24:56,837: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e23d3274-c5b7-4876-8f91-e91564b266ed] succeeded in 6.556093383929692s: None
[2026-05-26 11:25:49,399: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:25:50,066: INFO/MainProcess] Task triam.notifications.scan_due[20863fcb-51f4-4a5c-b3e5-3fb718d519e6] received
2026-05-26 11:25:56.633 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:25:56,634: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[20863fcb-51f4-4a5c-b3e5-3fb718d519e6] succeeded in 6.566681983997114s: None
[2026-05-26 11:26:49,400: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:26:50,276: INFO/MainProcess] Task triam.notifications.scan_due[88959c63-0393-4851-bc7b-0e7f8cc1e129] received
2026-05-26 11:26:56.783 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:26:56,784: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[88959c63-0393-4851-bc7b-0e7f8cc1e129] succeeded in 6.506867783959024s: None
[2026-05-26 11:27:49,399: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:27:50,274: INFO/MainProcess] Task triam.notifications.scan_due[8dc8af83-79d0-431f-bdbc-2e85b7842a96] received
2026-05-26 11:27:56.767 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:27:56,770: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8dc8af83-79d0-431f-bdbc-2e85b7842a96] succeeded in 6.493023879011162s: None
[2026-05-26 11:28:49,399: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:28:50,058: INFO/MainProcess] Task triam.notifications.scan_due[cab1d98e-bf4e-4726-8a9a-f84018b0350c] received
2026-05-26 11:28:56.561 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:28:56,561: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[cab1d98e-bf4e-4726-8a9a-f84018b0350c] succeeded in 6.50135554804001s: None
2026-05-26 11:29:03.080 | INFO     | logging:callHandlers:1762 - 10.16.17.88:41048 - "GET /api/v1/books/a6cd35a5-75f9-492e-a554-684236567591/details HTTP/1.1" 401
[2026-05-26 11:29:49,400: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:29:50,272: INFO/MainProcess] Task triam.notifications.scan_due[8fddcf4f-3762-41e2-acac-601335c1f335] received
2026-05-26 11:29:56.787 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:29:56,788: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8fddcf4f-3762-41e2-acac-601335c1f335] succeeded in 6.5130113429622725s: None
[2026-05-26 11:30:49,404: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:30:50,065: INFO/MainProcess] Task triam.notifications.scan_due[e9330015-1beb-4ab1-9fba-c5b3c1ffde9f] received
2026-05-26 11:30:56.555 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:30:56,557: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e9330015-1beb-4ab1-9fba-c5b3c1ffde9f] succeeded in 6.490121591952629s: None
[2026-05-26 11:31:49,404: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:31:50,277: INFO/MainProcess] Task triam.notifications.scan_due[2ba54e30-1f6d-4cc7-bf98-9ce5d1706a9d] received
2026-05-26 11:31:56.788 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:31:56,789: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2ba54e30-1f6d-4cc7-bf98-9ce5d1706a9d] succeeded in 6.510271321050823s: None
[2026-05-26 11:32:49,404: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:32:50,277: INFO/MainProcess] Task triam.notifications.scan_due[a4031934-7267-476c-af97-0c3d1403e813] received
2026-05-26 11:32:56.780 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:32:56,781: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a4031934-7267-476c-af97-0c3d1403e813] succeeded in 6.502554666949436s: None
[2026-05-26 11:33:49,404: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:33:50,231: INFO/MainProcess] Task triam.notifications.scan_due[2a941a9c-b981-4b93-8141-2689393d3217] received
2026-05-26 11:33:51.185 | INFO     | logging:callHandlers:1762 - 10.16.17.88:56793 - "GET /api/v1/health HTTP/1.1" 200
2026-05-26 11:33:56.738 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:33:56,739: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2a941a9c-b981-4b93-8141-2689393d3217] succeeded in 6.507245371001773s: None
[2026-05-26 11:34:49,405: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:34:50,285: INFO/MainProcess] Task triam.notifications.scan_due[3b553373-2bac-4c5e-8628-88b148923b85] received
2026-05-26 11:34:56.787 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:34:56,788: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3b553373-2bac-4c5e-8628-88b148923b85] succeeded in 6.5006835559615865s: None
[2026-05-26 11:35:49,405: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:35:50,063: INFO/MainProcess] Task triam.notifications.scan_due[539e5425-463c-487e-9c2a-94e2afb7bc6a] received
2026-05-26 11:35:56.561 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:35:56,563: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[539e5425-463c-487e-9c2a-94e2afb7bc6a] succeeded in 6.498857847065665s: None
[2026-05-26 11:36:49,405: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:36:50,276: INFO/MainProcess] Task triam.notifications.scan_due[ebaa27ed-f575-4224-9777-6cf7c78888d3] received
2026-05-26 11:36:56.769 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:36:56,769: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ebaa27ed-f575-4224-9777-6cf7c78888d3] succeeded in 6.492245184024796s: None
[2026-05-26 11:37:49,406: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:37:50,276: INFO/MainProcess] Task triam.notifications.scan_due[bf626ac7-f242-400f-83ea-4ef23f5811e3] received
2026-05-26 11:37:56.777 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:37:56,781: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[bf626ac7-f242-400f-83ea-4ef23f5811e3] succeeded in 6.50259302998893s: None
[2026-05-26 11:38:49,406: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:38:50,069: INFO/MainProcess] Task triam.notifications.scan_due[72f88581-9016-4786-981a-65204552b8ff] received
2026-05-26 11:38:56.564 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:38:56,565: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[72f88581-9016-4786-981a-65204552b8ff] succeeded in 6.491599522065371s: None
[2026-05-26 11:39:49,406: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:39:50,280: INFO/MainProcess] Task triam.notifications.scan_due[a8d6fca5-b55a-4ec0-972f-19582a317f3e] received
2026-05-26 11:39:58.001 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:39:58,002: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a8d6fca5-b55a-4ec0-972f-19582a317f3e] succeeded in 7.507922039018013s: None
[2026-05-26 11:40:49,410: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:40:50,066: INFO/MainProcess] Task triam.notifications.scan_due[d477c909-7daa-4852-85cc-f73179a5bafd] received
2026-05-26 11:40:56.431 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:40:56,431: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d477c909-7daa-4852-85cc-f73179a5bafd] succeeded in 6.362735001021065s: None
[2026-05-26 11:41:49,411: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:41:50,282: INFO/MainProcess] Task triam.notifications.scan_due[6c13f635-39d0-4a14-b373-b57a9c8306bf] received
2026-05-26 11:41:56.688 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:41:56,689: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[6c13f635-39d0-4a14-b373-b57a9c8306bf] succeeded in 6.193576183984987s: None
[2026-05-26 11:42:49,411: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:42:50,289: INFO/MainProcess] Task triam.notifications.scan_due[8c2b3737-7eaf-4f9a-94b2-2c9c2cf96592] received
2026-05-26 11:42:56.706 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:42:56,707: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8c2b3737-7eaf-4f9a-94b2-2c9c2cf96592] succeeded in 6.20126264996361s: None
2026-05-26 11:43:02.341 | INFO     | logging:callHandlers:1762 - 10.16.17.88:57270 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 11:43:10.259 | INFO     | logging:callHandlers:1762 - 10.16.17.88:29610 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 11:43:16.467 | INFO     | logging:callHandlers:1762 - 10.16.5.171:48508 - "GET /api/v1/study-contexts HTTP/1.1" 200
[2026-05-26 11:43:49,415: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:43:50,288: INFO/MainProcess] Task triam.notifications.scan_due[0011880b-697e-43b6-ac68-789be35b55cb] received
2026-05-26 11:43:56.786 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:43:56,791: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[0011880b-697e-43b6-ac68-789be35b55cb] succeeded in 6.283238003030419s: None
[2026-05-26 11:44:49,416: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:44:50,291: INFO/MainProcess] Task triam.notifications.scan_due[f8736968-4256-4b8b-a747-614fc90269e2] received
2026-05-26 11:44:56.671 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:44:56,676: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f8736968-4256-4b8b-a747-614fc90269e2] succeeded in 6.165350834024139s: None
2026-05-26 11:45:41.725 | INFO     | app.services.upload_service:handle_upload_document:108 - ☁️  PDF uploaded to Storage: 1a2e51e4-4fca-454a-9071-9bd005ed13df/original.pdf
[2026-05-26 11:45:49,422: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:45:50,080: INFO/MainProcess] Task triam.notifications.scan_due[cc8ae603-3fc4-4bbb-b44d-ece7f8f7ffd7] received
2026-05-26 11:45:56.187 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:45:56,189: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[cc8ae603-3fc4-4bbb-b44d-ece7f8f7ffd7] succeeded in 6.106708178063855s: None
[2026-05-26 11:46:49,422: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:46:50,296: INFO/MainProcess] Task triam.notifications.scan_due[bf8c2b16-1d36-4d7b-8431-3c421bf1f0f0] received
2026-05-26 11:46:56.419 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:46:56,420: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[bf8c2b16-1d36-4d7b-8431-3c421bf1f0f0] succeeded in 6.121318334015086s: None
[2026-05-26 11:47:49,423: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:47:50,297: INFO/MainProcess] Task triam.notifications.scan_due[1343be92-f50b-4f1b-8381-1c0fa44c1fca] received
2026-05-26 11:47:56.435 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:47:56,437: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1343be92-f50b-4f1b-8381-1c0fa44c1fca] succeeded in 6.136855421005748s: None
2026-05-26 11:48:41.982 | INFO     | app.services.upload_service:handle_upload_document:139 - 📘 Created DRAFT book 1a2e51e4-4fca-454a-9071-9bd005ed13df | 210 chapters | file_url saved
2026-05-26 11:48:41.996 | INFO     | logging:callHandlers:1762 - 10.16.5.171:21038 - "POST /api/v1/upload HTTP/1.1" 200
2026-05-26 11:48:43.511 | INFO     | logging:callHandlers:1762 - 10.16.17.88:13510 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 11:48:44.806 | INFO     | logging:callHandlers:1762 - 10.16.5.171:49344 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 11:48:44.808 | INFO     | logging:callHandlers:1762 - 10.16.17.88:51004 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 11:48:44.875 | INFO     | logging:callHandlers:1762 - 10.16.17.88:21630 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 11:48:47.510 | INFO     | logging:callHandlers:1762 - 10.16.5.171:49344 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
[2026-05-26 11:48:49,423: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:48:50,295: INFO/MainProcess] Task triam.notifications.scan_due[e2aa86bd-4ef7-4fcf-aa98-74c1a8429efc] received
2026-05-26 11:48:56.433 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:48:56,434: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e2aa86bd-4ef7-4fcf-aa98-74c1a8429efc] succeeded in 6.1371368039399385s: None
[2026-05-26 11:49:49,424: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:49:50,297: INFO/MainProcess] Task triam.notifications.scan_due[129661c1-c8ab-4e69-916c-833f1d8a3db1] received
2026-05-26 11:49:56.440 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:49:56,441: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[129661c1-c8ab-4e69-916c-833f1d8a3db1] succeeded in 6.1410675450460985s: None
[2026-05-26 11:50:49,424: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:50:50,079: INFO/MainProcess] Task triam.notifications.scan_due[94d1820a-7b9e-4c44-bff0-fcd0235f2067] received
2026-05-26 11:50:56.197 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:50:56,198: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[94d1820a-7b9e-4c44-bff0-fcd0235f2067] succeeded in 6.117234667995945s: None
2026-05-26 11:51:44.937 | INFO     | logging:callHandlers:1762 - 10.16.25.130:36989 - "GET /api/v1/notifications/settings HTTP/1.1" 200
[2026-05-26 11:51:49,425: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:51:50,299: INFO/MainProcess] Task triam.notifications.scan_due[5a417bb0-57eb-478f-bfe7-cd106b386803] received
2026-05-26 11:51:56.641 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:51:56,642: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5a417bb0-57eb-478f-bfe7-cd106b386803] succeeded in 6.122620287002064s: None
2026-05-26 11:51:59.516 | INFO     | app.services.upload_service:handle_generate_plan:213 - 📋 ReadingPlan created for book 1a2e51e4-4fca-454a-9071-9bd005ed13df | mode=full | job=66d0dcf3-564e-4ff9-a794-ab1662af9ff3
2026-05-26 11:52:02.290 | INFO     | logging:callHandlers:1762 - 10.16.5.171:65332 - "POST /api/v1/generate-plan HTTP/1.1" 200
[2026-05-26 11:52:02,670: INFO/MainProcess] Task triam.books.process[e9358368-c8b6-49f2-8833-18ac7f2064d5] received
2026-05-26 11:52:02.686 | INFO     | app.tasks.book_tasks:process_book_task:23 - Celery process_book_task started | book_id=1a2e51e4-4fca-454a-9071-9bd005ed13df | mode=full | job_id=66d0dcf3-564e-4ff9-a794-ab1662af9ff3
2026-05-26 11:52:04.795 | INFO     | logging:callHandlers:1762 - 10.16.5.171:65332 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 11:52:04.802 | INFO     | logging:callHandlers:1762 - 10.16.25.130:55856 - "GET /api/v1/books/1a2e51e4-4fca-454a-9071-9bd005ed13df/details HTTP/1.1" 200
2026-05-26 11:52:06.702 | INFO     | logging:callHandlers:1762 - 10.16.17.88:9195 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:52:09.012 | INFO     | app.services.workers.book_pipeline:run_background_processing:306 - ⬇️  Downloading PDF from Storage: 1a2e51e4-4fca-454a-9071-9bd005ed13df/original.pdf
2026-05-26 11:52:10.809 | INFO     | logging:callHandlers:1762 - 10.16.46.186:8512 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:52:14.785 | INFO     | logging:callHandlers:1762 - 10.16.17.88:3286 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:52:18.864 | INFO     | logging:callHandlers:1762 - 10.16.17.88:39003 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:52:23.071 | INFO     | logging:callHandlers:1762 - 10.16.17.88:48843 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:52:27.123 | INFO     | logging:callHandlers:1762 - 10.16.17.88:55575 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:52:31.204 | INFO     | logging:callHandlers:1762 - 10.16.17.88:4713 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:52:35.189 | INFO     | logging:callHandlers:1762 - 10.16.25.130:21785 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:52:39.206 | INFO     | logging:callHandlers:1762 - 10.16.5.171:10881 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:52:43.465 | INFO     | logging:callHandlers:1762 - 10.16.25.130:52147 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:52:47.488 | INFO     | logging:callHandlers:1762 - 10.16.5.171:53124 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
[2026-05-26 11:52:49,428: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:52:50,312: INFO/MainProcess] Task triam.notifications.scan_due[ae91b213-5f60-46d8-93d3-617ea39fe829] received
2026-05-26 11:52:51.459 | INFO     | logging:callHandlers:1762 - 10.16.17.88:54700 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:52:55.471 | INFO     | logging:callHandlers:1762 - 10.16.5.171:48890 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:52:56.903 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:52:56,910: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ae91b213-5f60-46d8-93d3-617ea39fe829] succeeded in 6.37424399505835s: None
2026-05-26 11:52:59.929 | INFO     | logging:callHandlers:1762 - 10.16.46.186:31577 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:53:03.957 | INFO     | logging:callHandlers:1762 - 10.16.46.186:42510 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:53:07.968 | INFO     | logging:callHandlers:1762 - 10.16.25.130:56001 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:53:12.140 | INFO     | logging:callHandlers:1762 - 10.16.25.130:18204 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:53:16.138 | INFO     | logging:callHandlers:1762 - 10.16.25.130:45298 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:53:20.118 | INFO     | logging:callHandlers:1762 - 10.16.5.171:7753 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:53:24.121 | INFO     | logging:callHandlers:1762 - 10.16.17.88:29481 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:53:28.121 | INFO     | logging:callHandlers:1762 - 10.16.17.88:25952 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:53:32.106 | INFO     | logging:callHandlers:1762 - 10.16.17.88:12281 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:53:35.381 | INFO     | logging:callHandlers:1762 - 10.16.17.88:12281 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 11:53:36.012 | INFO     | logging:callHandlers:1762 - 10.16.17.88:61613 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:53:40.038 | INFO     | logging:callHandlers:1762 - 10.16.25.130:20258 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:53:44.101 | INFO     | logging:callHandlers:1762 - 10.16.25.130:47136 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:53:48.392 | INFO     | logging:callHandlers:1762 - 10.16.17.88:23703 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
[2026-05-26 11:53:49,441: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:53:50,322: INFO/MainProcess] Task triam.notifications.scan_due[7c745171-5278-4799-aa62-9ada6610b151] received
2026-05-26 11:53:54.788 | INFO     | app.services.upload_service:handle_upload_document:108 - ☁️  PDF uploaded to Storage: 9a64d766-eb7c-404f-a9e9-9073f11c0030/original.pdf
2026-05-26 11:53:56.577 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:53:56,581: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7c745171-5278-4799-aa62-9ada6610b151] succeeded in 6.256748429033905s: None
2026-05-26 11:53:57.880 | INFO     | app.services.upload_service:handle_upload_document:139 - 📘 Created DRAFT book 9a64d766-eb7c-404f-a9e9-9073f11c0030 | 2 chapters | file_url saved
2026-05-26 11:53:57.890 | INFO     | logging:callHandlers:1762 - 10.16.46.186:41148 - "POST /api/v1/upload HTTP/1.1" 200
2026-05-26 11:53:58.355 | INFO     | logging:callHandlers:1762 - 10.16.17.88:32629 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:54:00.233 | INFO     | logging:callHandlers:1762 - 10.16.46.186:41148 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 11:54:02.413 | INFO     | logging:callHandlers:1762 - 10.16.46.186:41148 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:54:06.563 | INFO     | logging:callHandlers:1762 - 10.16.17.88:45016 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:54:10.672 | INFO     | logging:callHandlers:1762 - 10.16.17.88:13132 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:54:11.346 | INFO     | logging:callHandlers:1762 - 10.16.17.88:21823 - "GET /api/v1/notifications/settings HTTP/1.1" 200
2026-05-26 11:54:14.606 | INFO     | logging:callHandlers:1762 - 10.16.17.88:21823 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:54:18.705 | INFO     | logging:callHandlers:1762 - 10.16.46.186:15826 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:54:22.687 | INFO     | logging:callHandlers:1762 - 10.16.5.171:9076 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:54:24.706 | WARNING  | app.main:app_exception_handler:36 - AppException: Lịch học này đang trùng với một sách khác. Hãy chọn ngày hoặc giờ khác. - Status Code: 409
2026-05-26 11:54:24.710 | INFO     | logging:callHandlers:1762 - 10.16.46.186:54367 - "POST /api/v1/generate-plan HTTP/1.1" 409
2026-05-26 11:54:26.584 | INFO     | logging:callHandlers:1762 - 10.16.17.88:7967 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:54:30.622 | INFO     | logging:callHandlers:1762 - 10.16.17.88:21078 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
2026-05-26 11:54:33.043 | INFO     | logging:callHandlers:1762 - 10.16.17.88:52663 - "GET /api/v1/notifications/settings HTTP/1.1" 200
2026-05-26 11:54:34.677 | INFO     | logging:callHandlers:1762 - 10.16.17.88:52663 - "GET /api/v1/jobs/66d0dcf3-564e-4ff9-a794-ab1662af9ff3 HTTP/1.1" 200
[2026-05-26 11:54:35,028: INFO/ForkPoolWorker-1] Task triam.books.process[e9358368-c8b6-49f2-8833-18ac7f2064d5] succeeded in 152.3427168210037s: None
2026-05-26 11:54:39.030 | WARNING  | app.main:app_exception_handler:36 - AppException: Lịch học này đang trùng với một sách khác. Hãy chọn ngày hoặc giờ khác. - Status Code: 409
2026-05-26 11:54:39.031 | INFO     | logging:callHandlers:1762 - 10.16.17.88:26156 - "POST /api/v1/generate-plan HTTP/1.1" 409
[2026-05-26 11:54:49,441: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:54:50,310: INFO/MainProcess] Task triam.notifications.scan_due[5faa9b62-b0c9-42ae-88af-6234c6349be8] received
2026-05-26 11:54:56.448 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:54:56,448: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5faa9b62-b0c9-42ae-88af-6234c6349be8] succeeded in 6.134473655023612s: None
2026-05-26 11:55:13.199 | INFO     | logging:callHandlers:1762 - 10.16.25.130:35051 - "GET /docs HTTP/1.1" 200
2026-05-26 11:55:14.274 | INFO     | logging:callHandlers:1762 - 10.16.25.130:35051 - "GET /openapi.json HTTP/1.1" 200
2026-05-26 11:55:25.874 | INFO     | logging:callHandlers:1762 - 10.16.25.130:62049 - "GET /api/v1/notifications/settings HTTP/1.1" 200
2026-05-26 11:55:34.707 | INFO     | app.services.upload_service:handle_generate_plan:213 - 📋 ReadingPlan created for book 9a64d766-eb7c-404f-a9e9-9073f11c0030 | mode=full | job=ba9bf6f6-b6fb-4825-8b6e-077fc9762258
2026-05-26 11:55:35.150 | INFO     | logging:callHandlers:1762 - 10.16.17.88:43350 - "POST /api/v1/generate-plan HTTP/1.1" 200
[2026-05-26 11:55:35,576: INFO/MainProcess] Task triam.books.process[72c1c02d-e8a2-4417-96b1-48ce1634d58d] received
2026-05-26 11:55:35.582 | INFO     | app.tasks.book_tasks:process_book_task:23 - Celery process_book_task started | book_id=9a64d766-eb7c-404f-a9e9-9073f11c0030 | mode=full | job_id=ba9bf6f6-b6fb-4825-8b6e-077fc9762258
2026-05-26 11:55:37.243 | INFO     | logging:callHandlers:1762 - 10.16.17.88:43350 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 11:55:37.870 | INFO     | app.services.workers.book_pipeline:run_background_processing:306 - ⬇️  Downloading PDF from Storage: 9a64d766-eb7c-404f-a9e9-9073f11c0030/original.pdf
2026-05-26 11:55:39.177 | INFO     | logging:callHandlers:1762 - 10.16.25.130:63009 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:55:43.173 | INFO     | logging:callHandlers:1762 - 10.16.5.171:64251 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:55:43.978 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=1 | mode=full | title=Tổng quan về logic | chars=1717 | estimated_tokens=858 | estimated_audio_seconds=166
2026-05-26 11:55:46.303 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=1 | mode=full | rag=true | tts=true
2026-05-26 11:55:47.161 | INFO     | logging:callHandlers:1762 - 10.16.46.186:51147 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:55:47.543 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=1 | mode=full | title=Tổng quan về logic | raw_chars=1717
2026-05-26 11:55:47.545 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Tổng quan về logic | chars=1717 | estimated_tokens=858 | estimated_audio_seconds=166
2026-05-26 11:55:47.547 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Tổng quan về logic
2026-05-26 11:55:47.548 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1717
[2026-05-26 11:55:49,441: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:55:50,096: INFO/MainProcess] Task triam.notifications.scan_due[9f67ecc6-aaaf-468b-a1d8-805cf91c6a9c] received
2026-05-26 11:55:50.101 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 2 vectors for chapter_id=ae4c9c22-c00d-4f4a-93cf-81146ef32cbf
2026-05-26 11:55:51.164 | INFO     | logging:callHandlers:1762 - 10.16.5.171:53281 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:55:55.142 | INFO     | logging:callHandlers:1762 - 10.16.25.130:18067 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:55:56.209 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:55:56,210: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[9f67ecc6-aaaf-468b-a1d8-805cf91c6a9c] succeeded in 6.112728183041327s: None
2026-05-26 11:55:59.143 | INFO     | logging:callHandlers:1762 - 10.16.17.88:49926 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:55:59.864 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=5 | review_chars=625
2026-05-26 11:55:59.864 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=1 | mode=full | main_scripts=5 | review_chars=625
2026-05-26 11:55:59.864 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=1 | mode=full | total_scripts=5
2026-05-26 11:55:59.865 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=1/5 | chars=285
2026-05-26 11:56:03.132 | INFO     | logging:callHandlers:1762 - 10.16.17.88:24046 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:56:04.260 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=1/5 | duration_ms=15984
2026-05-26 11:56:04.261 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=2/5 | chars=304
2026-05-26 11:56:07.138 | INFO     | logging:callHandlers:1762 - 10.16.25.130:51157 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:56:08.179 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=2/5 | duration_ms=18576
2026-05-26 11:56:08.180 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=3/5 | chars=448
2026-05-26 11:56:11.123 | INFO     | logging:callHandlers:1762 - 10.16.5.171:22466 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:56:13.949 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=3/5 | duration_ms=26064
2026-05-26 11:56:13.950 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=4/5 | chars=464
2026-05-26 11:56:15.265 | INFO     | logging:callHandlers:1762 - 10.16.25.130:4270 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:56:15.953 | INFO     | logging:callHandlers:1762 - 10.16.17.88:27223 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/details HTTP/1.1" 200
2026-05-26 11:56:19.328 | INFO     | logging:callHandlers:1762 - 10.16.17.88:27223 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:56:21.792 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=4/5 | duration_ms=26832
2026-05-26 11:56:21.795 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=5/5 | chars=459
2026-05-26 11:56:23.296 | INFO     | logging:callHandlers:1762 - 10.16.17.88:2443 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:56:27.706 | INFO     | logging:callHandlers:1762 - 10.16.5.171:25287 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:56:29.757 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=5/5 | duration_ms=28200
2026-05-26 11:56:29.758 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=1 | mode=full | created_segments=5/5
2026-05-26 11:56:29.760 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=1 | mode=full | chars=625
2026-05-26 11:56:31.713 | INFO     | logging:callHandlers:1762 - 10.16.46.186:28051 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:56:35.693 | INFO     | logging:callHandlers:1762 - 10.16.25.130:9719 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:56:39.612 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=1 | mode=full
2026-05-26 11:56:39.613 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=ae4c9c22-c00d-4f4a-93cf-81146ef32cbf | mode=full | segments=5 | review_audio=True
2026-05-26 11:56:39.688 | INFO     | logging:callHandlers:1762 - 10.16.46.186:4183 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:56:42.437 | WARNING  | app.main:app_exception_handler:36 - AppException: PDF không có bookmark/outline ẩn. Vui lòng upload PDF có mục lục chuẩn. - Status Code: 422
2026-05-26 11:56:42.440 | INFO     | logging:callHandlers:1762 - 10.16.25.130:51033 - "POST /api/v1/upload HTTP/1.1" 422
2026-05-26 11:56:42.851 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=ae4c9c22-c00d-4f4a-93cf-81146ef32cbf | mode=full
2026-05-26 11:56:43.446 | INFO     | logging:callHandlers:1762 - 10.16.17.88:41069 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:56:45.378 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 1 READY | mode=full | segments=5
2026-05-26 11:56:47.366 | INFO     | logging:callHandlers:1762 - 10.16.17.88:46480 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
[2026-05-26 11:56:49,442: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-26 11:56:49.539 | INFO     | app.services.workers.book_pipeline:_create_first_playable_notification_safely:123 - Content-ready first-playable event | book_id=9a64d766-eb7c-404f-a9e9-9073f11c0030 | mode=full | created=True
2026-05-26 11:56:49.767 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=2 | mode=full | title=Khái niệm | chars=5024 | estimated_tokens=2735 | estimated_audio_seconds=474
[2026-05-26 11:56:50,313: INFO/MainProcess] Task triam.notifications.scan_due[1efd6c1a-6468-4736-9fa6-6374d11e3455] received
2026-05-26 11:56:51.555 | INFO     | logging:callHandlers:1762 - 10.16.17.88:37546 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:56:52.059 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=2 | mode=full | rag=true | tts=true
2026-05-26 11:56:52.069 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=2 | mode=full | title=Khái niệm | raw_chars=5024
2026-05-26 11:56:52.078 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Khái niệm | chars=5024 | estimated_tokens=2735 | estimated_audio_seconds=474
2026-05-26 11:56:52.080 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Khái niệm
2026-05-26 11:56:52.081 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=5024
2026-05-26 11:56:55.275 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 5 vectors for chapter_id=42108346-ab9e-49fd-aff9-4879423487d1
2026-05-26 11:56:55.477 | INFO     | logging:callHandlers:1762 - 10.16.17.88:23266 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:56:56.652 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=True
[2026-05-26 11:56:59,307: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1efd6c1a-6468-4736-9fa6-6374d11e3455] succeeded in 8.992089433013462s: None
2026-05-26 11:56:59.463 | INFO     | logging:callHandlers:1762 - 10.16.46.186:1104 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
[2026-05-26 11:57:00,187: INFO/MainProcess] Task triam.notifications.deliver_due[f72512a7-8b39-4aa2-8121-e21cd17fcb41] received
2026-05-26 11:57:03.560 | INFO     | logging:callHandlers:1762 - 10.16.5.171:40664 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:57:04.276 | INFO     | app.tasks.notification_tasks:deliver_due_notifications_task:67 - Notification delivery batch done | worker_id=notification-worker:d0c70686-c863-4966-9d19-1a3f2a3d8194 | delivered_attempts=1
[2026-05-26 11:57:04,279: INFO/ForkPoolWorker-1] Task triam.notifications.deliver_due[f72512a7-8b39-4aa2-8121-e21cd17fcb41] succeeded in 4.087611838942394s: None
2026-05-26 11:57:07.554 | INFO     | logging:callHandlers:1762 - 10.16.5.171:56729 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:57:11.513 | INFO     | logging:callHandlers:1762 - 10.16.25.130:4121 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:57:15.538 | INFO     | logging:callHandlers:1762 - 10.16.5.171:63559 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:57:19.170 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=18 | review_chars=704
2026-05-26 11:57:19.171 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=2 | mode=full | main_scripts=18 | review_chars=704
2026-05-26 11:57:19.172 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=2 | mode=full | total_scripts=18
2026-05-26 11:57:19.173 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=1/18 | chars=411
2026-05-26 11:57:19.420 | INFO     | logging:callHandlers:1762 - 10.16.25.130:6160 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:57:22.398 | INFO     | logging:callHandlers:1762 - 10.16.5.171:61153 - "POST /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/switch-mode HTTP/1.1" 200
2026-05-26 11:57:23.474 | INFO     | logging:callHandlers:1762 - 10.16.5.171:61153 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:57:24.990 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=1/18 | duration_ms=24480
2026-05-26 11:57:24.992 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=2/18 | chars=459
2026-05-26 11:57:25.544 | INFO     | logging:callHandlers:1762 - 10.16.17.88:4948 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 11:57:27.597 | INFO     | logging:callHandlers:1762 - 10.16.17.88:4948 - "GET /api/v1/jobs/ca7d3c02-95e2-4f75-a51b-fae02779f608 HTTP/1.1" 200
2026-05-26 11:57:27.626 | INFO     | logging:callHandlers:1762 - 10.16.46.186:50883 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:57:31.734 | INFO     | logging:callHandlers:1762 - 10.16.17.88:38989 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:57:32.293 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=2/18 | duration_ms=27720
2026-05-26 11:57:32.295 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=3/18 | chars=366
2026-05-26 11:57:32.422 | INFO     | logging:callHandlers:1762 - 10.16.46.186:10265 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/details HTTP/1.1" 200
2026-05-26 11:57:35.689 | INFO     | logging:callHandlers:1762 - 10.16.17.88:37429 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:57:36.822 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=3/18 | duration_ms=21168
2026-05-26 11:57:36.823 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=4/18 | chars=179
2026-05-26 11:57:39.821 | INFO     | logging:callHandlers:1762 - 10.16.17.88:3029 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:57:40.459 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=4/18 | duration_ms=10464
2026-05-26 11:57:40.459 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=5/18 | chars=410
2026-05-26 11:57:43.996 | INFO     | logging:callHandlers:1762 - 10.16.25.130:44322 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:57:47.182 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=5/18 | duration_ms=23736
2026-05-26 11:57:47.185 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=6/18 | chars=429
2026-05-26 11:57:47.887 | INFO     | logging:callHandlers:1762 - 10.16.17.88:32577 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
[2026-05-26 11:57:49,443: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:57:50,313: INFO/MainProcess] Task triam.notifications.scan_due[74c6d385-309f-415e-89fc-893aa306d240] received
2026-05-26 11:57:51.877 | INFO     | logging:callHandlers:1762 - 10.16.17.88:8727 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:57:52.796 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=6/18 | duration_ms=24720
2026-05-26 11:57:52.799 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=7/18 | chars=457
2026-05-26 11:57:55.853 | INFO     | logging:callHandlers:1762 - 10.16.17.88:26109 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:57:56.667 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:57:56,671: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[74c6d385-309f-415e-89fc-893aa306d240] succeeded in 6.357202334096655s: None
2026-05-26 11:57:59.881 | INFO     | logging:callHandlers:1762 - 10.16.17.88:63453 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:58:02.749 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=7/18 | duration_ms=27792
2026-05-26 11:58:02.754 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=8/18 | chars=275
2026-05-26 11:58:03.880 | INFO     | logging:callHandlers:1762 - 10.16.17.88:4687 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:58:07.782 | INFO     | logging:callHandlers:1762 - 10.16.17.88:4453 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:58:09.376 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=8/18 | duration_ms=16104
2026-05-26 11:58:09.377 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=9/18 | chars=269
2026-05-26 11:58:11.747 | INFO     | logging:callHandlers:1762 - 10.16.46.186:31620 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:58:15.726 | INFO     | logging:callHandlers:1762 - 10.16.5.171:62995 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:58:15.817 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=9/18 | duration_ms=15888
2026-05-26 11:58:15.818 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=10/18 | chars=216
2026-05-26 11:58:19.750 | INFO     | logging:callHandlers:1762 - 10.16.25.130:13550 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:58:21.394 | INFO     | logging:callHandlers:1762 - 10.16.17.88:4493 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 11:58:21.685 | INFO     | logging:callHandlers:1762 - 10.16.46.186:60661 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 11:58:21.904 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=10/18 | duration_ms=12888
2026-05-26 11:58:21.906 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=11/18 | chars=262
2026-05-26 11:58:23.726 | INFO     | logging:callHandlers:1762 - 10.16.17.88:4493 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:58:26.229 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=11/18 | duration_ms=14352
2026-05-26 11:58:26.229 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=12/18 | chars=354
2026-05-26 11:58:27.805 | INFO     | logging:callHandlers:1762 - 10.16.25.130:58759 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:58:32.134 | INFO     | logging:callHandlers:1762 - 10.16.17.88:58875 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:58:34.288 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=12/18 | duration_ms=20832
2026-05-26 11:58:34.289 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=13/18 | chars=384
2026-05-26 11:58:36.122 | INFO     | logging:callHandlers:1762 - 10.16.17.88:50823 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:58:40.099 | INFO     | logging:callHandlers:1762 - 10.16.17.88:34456 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:58:42.159 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=13/18 | duration_ms=21336
2026-05-26 11:58:42.166 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=14/18 | chars=275
2026-05-26 11:58:44.118 | INFO     | logging:callHandlers:1762 - 10.16.17.88:22046 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:58:47.136 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=14/18 | duration_ms=16608
2026-05-26 11:58:47.138 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=15/18 | chars=251
2026-05-26 11:58:48.294 | INFO     | logging:callHandlers:1762 - 10.16.17.88:39946 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
[2026-05-26 11:58:49,444: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:58:50,318: INFO/MainProcess] Task triam.notifications.scan_due[09678d8a-e987-46d7-88e1-279c20d19314] received
2026-05-26 11:58:52.157 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=15/18 | duration_ms=14712
2026-05-26 11:58:52.158 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=16/18 | chars=249
2026-05-26 11:58:52.295 | INFO     | logging:callHandlers:1762 - 10.16.17.88:41330 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:58:56.314 | INFO     | logging:callHandlers:1762 - 10.16.46.186:46388 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:58:56.658 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 11:58:56,658: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[09678d8a-e987-46d7-88e1-279c20d19314] succeeded in 6.337829920928925s: None
2026-05-26 11:58:57.171 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=16/18 | duration_ms=13632
2026-05-26 11:58:57.171 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=17/18 | chars=511
2026-05-26 11:59:00.189 | INFO     | logging:callHandlers:1762 - 10.16.5.171:34619 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:59:04.160 | INFO     | logging:callHandlers:1762 - 10.16.17.88:57344 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:59:08.159 | INFO     | logging:callHandlers:1762 - 10.16.46.186:29134 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:59:08.338 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=17/18 | duration_ms=28368
2026-05-26 11:59:08.340 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=18/18 | chars=285
2026-05-26 11:59:12.061 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=18/18 | duration_ms=15888
2026-05-26 11:59:12.062 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=2 | mode=full | created_segments=18/18
2026-05-26 11:59:12.062 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=2 | mode=full | chars=704
2026-05-26 11:59:12.643 | INFO     | logging:callHandlers:1762 - 10.16.17.88:30552 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:59:16.778 | INFO     | logging:callHandlers:1762 - 10.16.25.130:62832 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:59:20.659 | INFO     | logging:callHandlers:1762 - 10.16.5.171:24455 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:59:24.593 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=2 | mode=full
2026-05-26 11:59:24.594 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=42108346-ab9e-49fd-aff9-4879423487d1 | mode=full | segments=18 | review_audio=True
2026-05-26 11:59:24.647 | INFO     | logging:callHandlers:1762 - 10.16.17.88:31274 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:59:27.820 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=42108346-ab9e-49fd-aff9-4879423487d1 | mode=full
2026-05-26 11:59:28.744 | INFO     | logging:callHandlers:1762 - 10.16.25.130:57639 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:59:30.354 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 2 READY | mode=full | segments=18
2026-05-26 11:59:32.976 | INFO     | logging:callHandlers:1762 - 10.16.17.88:60467 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
2026-05-26 11:59:34.946 | INFO     | app.services.workers.book_pipeline:_create_book_ready_notification_safely:142 - Content-ready book-ready event | book_id=9a64d766-eb7c-404f-a9e9-9073f11c0030 | mode=full | created=True
2026-05-26 11:59:36.774 | INFO     | app.services.workers.book_pipeline:run_background_processing:413 - 🎉 Book 9a64d766-eb7c-404f-a9e9-9073f11c0030 READY — tất cả chapters đã xử lý xong.
[2026-05-26 11:59:36,792: INFO/ForkPoolWorker-1] Task triam.books.process[72c1c02d-e8a2-4417-96b1-48ce1634d58d] succeeded in 241.21036757400725s: None
2026-05-26 11:59:36.931 | INFO     | logging:callHandlers:1762 - 10.16.25.130:54510 - "GET /api/v1/jobs/ba9bf6f6-b6fb-4825-8b6e-077fc9762258 HTTP/1.1" 200
[2026-05-26 11:59:37,674: INFO/MainProcess] Task triam.books.switch_mode[13591c74-dbdd-4ff0-bb8c-34a4cb959930] received
2026-05-26 11:59:37.679 | INFO     | app.tasks.book_tasks:switch_mode_task:43 - Celery switch_mode_task started | book_id=9a64d766-eb7c-404f-a9e9-9073f11c0030 | mode=pareto | job_id=ca7d3c02-95e2-4f75-a51b-fae02779f608
2026-05-26 11:59:39.966 | INFO     | app.services.workers.book_pipeline:run_switch_mode_processing:450 - ⬇️  Downloading PDF for switch mode: 9a64d766-eb7c-404f-a9e9-9073f11c0030/original.pdf
2026-05-26 11:59:45.487 | INFO     | app.services.workers.chapter_worker:process_switch_mode_chapter:150 - Switch-mode chapter start | chapter=1 | mode=pareto | chars=1717 | estimated_tokens=858 | estimated_audio_seconds=166
2026-05-26 11:59:47.322 | INFO     | app.services.workers.chapter_worker:process_switch_mode_chapter:175 - Switch-mode TTS dispatch | chapter=1 | mode=pareto
2026-05-26 11:59:47.322 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=1 | mode=pareto | title=(unknown) | raw_chars=1717
2026-05-26 11:59:47.326 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=pareto | title=(unknown) | chars=1717 | estimated_tokens=858 | estimated_audio_seconds=166
2026-05-26 11:59:47.327 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=pareto | strategy=single_call | title=(unknown)
2026-05-26 11:59:47.328 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=pareto | context=single | chars=1717
[2026-05-26 11:59:47,336: INFO/ForkPoolWorker-1] Retrying request to /chat/completions in 0.475952 seconds
[2026-05-26 11:59:49,444: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 11:59:50,313: INFO/MainProcess] Task triam.notifications.scan_due[8c5709fc-e45a-4a12-ba22-8595b02d9da7] received
2026-05-26 11:59:56.412 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=True
[2026-05-26 11:59:56,838: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8c5709fc-e45a-4a12-ba22-8595b02d9da7] succeeded in 6.522686509997584s: None
[2026-05-26 11:59:57,499: INFO/MainProcess] Task triam.notifications.deliver_due[efa35051-65a8-4aa1-b7f6-73ef9f9370cc] received
2026-05-26 12:00:01.019 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=pareto | context=single | scripts=5 | review_chars=563
2026-05-26 12:00:01.025 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=1 | mode=pareto | main_scripts=5 | review_chars=563
2026-05-26 12:00:01.028 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=1 | mode=pareto | total_scripts=5
2026-05-26 12:00:01.029 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=pareto | segment=1/5 | chars=242
2026-05-26 12:00:01.495 | INFO     | app.tasks.notification_tasks:deliver_due_notifications_task:67 - Notification delivery batch done | worker_id=notification-worker:bf25c781-d708-423e-9787-984b2b9325a2 | delivered_attempts=1
[2026-05-26 12:00:01,496: INFO/ForkPoolWorker-1] Task triam.notifications.deliver_due[efa35051-65a8-4aa1-b7f6-73ef9f9370cc] succeeded in 3.9949880350613967s: None
2026-05-26 12:00:06.169 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=pareto | segment=1/5 | duration_ms=13608
2026-05-26 12:00:06.171 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=pareto | segment=2/5 | chars=197
2026-05-26 12:00:09.735 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=pareto | segment=2/5 | duration_ms=12264
2026-05-26 12:00:09.739 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=pareto | segment=3/5 | chars=370
2026-05-26 12:00:14.186 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=pareto | segment=3/5 | duration_ms=22104
2026-05-26 12:00:14.188 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=pareto | segment=4/5 | chars=291
2026-05-26 12:00:19.213 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=pareto | segment=4/5 | duration_ms=17448
2026-05-26 12:00:19.215 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=pareto | segment=5/5 | chars=296
2026-05-26 12:00:25.940 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=pareto | segment=5/5 | duration_ms=19248
2026-05-26 12:00:25.941 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=1 | mode=pareto | created_segments=5/5
2026-05-26 12:00:25.941 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=1 | mode=pareto | chars=563
2026-05-26 12:00:35.876 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=1 | mode=pareto
2026-05-26 12:00:35.877 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=ae4c9c22-c00d-4f4a-93cf-81146ef32cbf | mode=pareto | segments=5 | review_audio=True
2026-05-26 12:00:39.085 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=ae4c9c22-c00d-4f4a-93cf-81146ef32cbf | mode=pareto
2026-05-26 12:00:40.694 | INFO     | app.services.workers.chapter_worker:process_switch_mode_chapter:179 - ✅ Chapter 1 switch mode 'pareto' READY | segments=5
2026-05-26 12:00:44.822 | INFO     | app.services.workers.book_pipeline:_create_first_playable_notification_safely:123 - Content-ready first-playable event | book_id=9a64d766-eb7c-404f-a9e9-9073f11c0030 | mode=pareto | created=True
2026-05-26 12:00:45.053 | INFO     | app.services.workers.chapter_worker:process_switch_mode_chapter:150 - Switch-mode chapter start | chapter=2 | mode=pareto | chars=5024 | estimated_tokens=2735 | estimated_audio_seconds=474
2026-05-26 12:00:46.884 | INFO     | app.services.workers.chapter_worker:process_switch_mode_chapter:175 - Switch-mode TTS dispatch | chapter=2 | mode=pareto
2026-05-26 12:00:46.885 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=2 | mode=pareto | title=(unknown) | raw_chars=5024
2026-05-26 12:00:46.891 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=pareto | title=(unknown) | chars=5024 | estimated_tokens=2735 | estimated_audio_seconds=474
2026-05-26 12:00:46.893 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=pareto | strategy=single_call | title=(unknown)
2026-05-26 12:00:46.895 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=pareto | context=single | chars=5024
[2026-05-26 12:00:49,446: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:00:50,103: INFO/MainProcess] Task triam.notifications.scan_due[80f90940-9e39-4379-b76d-cacd7e6dc474] received
2026-05-26 12:00:56.421 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=True
[2026-05-26 12:00:56,841: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[80f90940-9e39-4379-b76d-cacd7e6dc474] succeeded in 6.7359106939984486s: None
[2026-05-26 12:00:57,500: INFO/MainProcess] Task triam.notifications.deliver_due[c294fb1b-198a-4684-97ac-48d8252faa59] received
2026-05-26 12:01:01.709 | INFO     | app.tasks.notification_tasks:deliver_due_notifications_task:67 - Notification delivery batch done | worker_id=notification-worker:f19fcfaf-b1aa-4787-b03a-189f694f34ea | delivered_attempts=1
[2026-05-26 12:01:01,710: INFO/ForkPoolWorker-1] Task triam.notifications.deliver_due[c294fb1b-198a-4684-97ac-48d8252faa59] succeeded in 3.9881562480004504s: None
2026-05-26 12:01:04.768 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=pareto | context=single | scripts=11 | review_chars=657
2026-05-26 12:01:04.769 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=2 | mode=pareto | main_scripts=11 | review_chars=657
2026-05-26 12:01:04.769 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=2 | mode=pareto | total_scripts=11
2026-05-26 12:01:04.770 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=pareto | segment=1/11 | chars=365
2026-05-26 12:01:11.289 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=pareto | segment=1/11 | duration_ms=21600
2026-05-26 12:01:11.293 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=pareto | segment=2/11 | chars=316
2026-05-26 12:01:15.054 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=pareto | segment=2/11 | duration_ms=20664
2026-05-26 12:01:15.055 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=pareto | segment=3/11 | chars=307
2026-05-26 12:01:20.405 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=pareto | segment=3/11 | duration_ms=18528
2026-05-26 12:01:20.406 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=pareto | segment=4/11 | chars=233
2026-05-26 12:01:23.218 | INFO     | logging:callHandlers:1762 - 10.16.17.88:47516 - "GET /api/v1/study-contexts HTTP/1.1" 200
2026-05-26 12:01:23.648 | INFO     | logging:callHandlers:1762 - 10.16.17.88:15664 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 12:01:24.957 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=pareto | segment=4/11 | duration_ms=13752
2026-05-26 12:01:24.960 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=pareto | segment=5/11 | chars=467
2026-05-26 12:01:31.447 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=pareto | segment=5/11 | duration_ms=26520
2026-05-26 12:01:31.448 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=pareto | segment=6/11 | chars=487
2026-05-26 12:01:35.247 | INFO     | logging:callHandlers:1762 - 10.16.17.88:15636 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/processing-status HTTP/1.1" 200
2026-05-26 12:01:39.231 | INFO     | logging:callHandlers:1762 - 10.16.17.88:42540 - "GET /api/v1/jobs/ca7d3c02-95e2-4f75-a51b-fae02779f608 HTTP/1.1" 200
2026-05-26 12:01:41.585 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=pareto | segment=6/11 | duration_ms=28200
2026-05-26 12:01:41.586 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=pareto | segment=7/11 | chars=473
2026-05-26 12:01:43.699 | INFO     | logging:callHandlers:1762 - 10.16.5.171:10944 - "GET /api/v1/jobs/ca7d3c02-95e2-4f75-a51b-fae02779f608 HTTP/1.1" 200
2026-05-26 12:01:47.833 | INFO     | logging:callHandlers:1762 - 10.16.25.130:5221 - "GET /api/v1/study-contexts HTTP/1.1" 200
2026-05-26 12:01:48.277 | INFO     | logging:callHandlers:1762 - 10.16.17.88:1362 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 12:01:49.079 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=pareto | segment=7/11 | duration_ms=26376
2026-05-26 12:01:49.079 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=pareto | segment=8/11 | chars=590
[2026-05-26 12:01:49,446: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:01:50,317: INFO/MainProcess] Task triam.notifications.scan_due[f0c4385b-980b-4f96-847f-8994c9de2374] received
2026-05-26 12:01:56.649 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:01:56,650: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f0c4385b-980b-4f96-847f-8994c9de2374] succeeded in 6.331439552013762s: None
2026-05-26 12:01:57.828 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=pareto | segment=8/11 | duration_ms=32472
2026-05-26 12:01:57.831 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=pareto | segment=9/11 | chars=307
2026-05-26 12:02:02.638 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=pareto | segment=9/11 | duration_ms=17448
2026-05-26 12:02:02.639 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=pareto | segment=10/11 | chars=361
2026-05-26 12:02:09.756 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=pareto | segment=10/11 | duration_ms=20088
2026-05-26 12:02:09.757 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=pareto | segment=11/11 | chars=195
2026-05-26 12:02:12.902 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=pareto | segment=11/11 | duration_ms=10656
2026-05-26 12:02:12.903 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=2 | mode=pareto | created_segments=11/11
2026-05-26 12:02:12.903 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=2 | mode=pareto | chars=657
2026-05-26 12:02:19.906 | INFO     | logging:callHandlers:1762 - 10.16.5.171:6361 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 401
2026-05-26 12:02:20.915 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=2 | mode=pareto
2026-05-26 12:02:20.916 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=42108346-ab9e-49fd-aff9-4879423487d1 | mode=pareto | segments=11 | review_audio=True
2026-05-26 12:02:21.075 | INFO     | logging:callHandlers:1762 - 10.16.17.88:16086 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 401
2026-05-26 12:02:24.153 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=42108346-ab9e-49fd-aff9-4879423487d1 | mode=pareto
2026-05-26 12:02:25.754 | INFO     | app.services.workers.chapter_worker:process_switch_mode_chapter:179 - ✅ Chapter 2 switch mode 'pareto' READY | segments=11
2026-05-26 12:02:29.187 | INFO     | app.services.workers.book_pipeline:_create_book_ready_notification_safely:142 - Content-ready book-ready event | book_id=9a64d766-eb7c-404f-a9e9-9073f11c0030 | mode=pareto | created=False
2026-05-26 12:02:31.018 | INFO     | app.services.workers.book_pipeline:run_switch_mode_processing:556 - 🎉 Book 9a64d766-eb7c-404f-a9e9-9073f11c0030 đã gen xong audio cho mode: pareto.
[2026-05-26 12:02:31,024: INFO/ForkPoolWorker-1] Task triam.books.switch_mode[13591c74-dbdd-4ff0-bb8c-34a4cb959930] succeeded in 173.3448247150518s: None
2026-05-26 12:02:35.348 | INFO     | logging:callHandlers:1762 - 10.16.17.88:10759 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
[2026-05-26 12:02:49,446: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:02:50,102: INFO/MainProcess] Task triam.notifications.scan_due[0091e4c3-6294-42cb-a357-ecf1366d8d67] received
2026-05-26 12:02:56.474 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:02:56,475: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[0091e4c3-6294-42cb-a357-ecf1366d8d67] succeeded in 6.371086972998455s: None
2026-05-26 12:03:15.153 | INFO     | logging:callHandlers:1762 - 10.16.5.171:38877 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/details HTTP/1.1" 200
2026-05-26 12:03:18.138 | INFO     | logging:callHandlers:1762 - 10.16.17.88:35741 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=pareto HTTP/1.1" 200
2026-05-26 12:03:21.642 | INFO     | logging:callHandlers:1762 - 10.16.17.88:7554 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/ae4c9c22-c00d-4f4a-93cf-81146ef32cbf/progress HTTP/1.1" 422
2026-05-26 12:03:32.996 | INFO     | logging:callHandlers:1762 - 10.16.17.88:28831 - "GET /api/v1/health HTTP/1.1" 200
2026-05-26 12:03:36.015 | INFO     | logging:callHandlers:1762 - 10.16.5.171:48740 - "GET /api/v1/books HTTP/1.1" 200
2026-05-26 12:03:39.381 | INFO     | logging:callHandlers:1762 - 10.16.17.88:39245 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 12:03:48.704 | INFO     | logging:callHandlers:1762 - 10.16.17.88:26230 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=pareto HTTP/1.1" 200
[2026-05-26 12:03:49,447: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:03:50,324: INFO/MainProcess] Task triam.notifications.scan_due[70d251bf-151c-4aa3-9c75-7aa88e42edfd] received
2026-05-26 12:03:56.645 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:03:56,646: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[70d251bf-151c-4aa3-9c75-7aa88e42edfd] succeeded in 6.320764324977063s: None
[2026-05-26 12:04:49,449: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:04:50,481: INFO/MainProcess] Task triam.notifications.scan_due[465a82be-45b2-4118-b5e1-d6b6ab08fd3f] received
2026-05-26 12:04:55.324 | INFO     | logging:callHandlers:1762 - 10.16.17.88:46191 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=pareto HTTP/1.1" 200
2026-05-26 12:04:57.029 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:04:57,030: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[465a82be-45b2-4118-b5e1-d6b6ab08fd3f] succeeded in 6.3311390990857035s: None
2026-05-26 12:04:57.225 | INFO     | logging:callHandlers:1762 - 10.16.46.186:60280 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/ae4c9c22-c00d-4f4a-93cf-81146ef32cbf/progress HTTP/1.1" 422
2026-05-26 12:05:11.421 | INFO     | logging:callHandlers:1762 - 10.16.17.88:8423 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/ae4c9c22-c00d-4f4a-93cf-81146ef32cbf/progress HTTP/1.1" 422
2026-05-26 12:05:12.602 | INFO     | logging:callHandlers:1762 - 10.16.25.130:38994 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 12:05:24.208 | INFO     | logging:callHandlers:1762 - 10.16.5.171:57126 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/ae4c9c22-c00d-4f4a-93cf-81146ef32cbf/progress HTTP/1.1" 422
2026-05-26 12:05:39.637 | INFO     | logging:callHandlers:1762 - 10.16.5.171:60742 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/ae4c9c22-c00d-4f4a-93cf-81146ef32cbf/progress HTTP/1.1" 422
2026-05-26 12:05:47.799 | INFO     | logging:callHandlers:1762 - 10.16.17.88:20678 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/ae4c9c22-c00d-4f4a-93cf-81146ef32cbf/progress HTTP/1.1" 422
[2026-05-26 12:05:49,449: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:05:50,243: INFO/MainProcess] Task triam.notifications.scan_due[c1ec4a9e-9278-49f0-8519-e392a7039d15] received
2026-05-26 12:05:56.577 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:05:56,578: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c1ec4a9e-9278-49f0-8519-e392a7039d15] succeeded in 6.33242439199239s: None
2026-05-26 12:06:06.109 | INFO     | logging:callHandlers:1762 - 10.16.17.88:30254 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/ae4c9c22-c00d-4f4a-93cf-81146ef32cbf/progress HTTP/1.1" 422
2026-05-26 12:06:21.418 | INFO     | logging:callHandlers:1762 - 10.16.17.88:27130 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/ae4c9c22-c00d-4f4a-93cf-81146ef32cbf/progress HTTP/1.1" 422
2026-05-26 12:06:26.310 | INFO     | logging:callHandlers:1762 - 10.16.25.130:42733 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
2026-05-26 12:06:41.670 | INFO     | logging:callHandlers:1762 - 10.16.25.130:62347 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
2026-05-26 12:06:48.994 | INFO     | logging:callHandlers:1762 - 10.16.5.171:44666 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
[2026-05-26 12:06:49,450: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:06:50,323: INFO/MainProcess] Task triam.notifications.scan_due[ddfb8cce-c0db-4087-a55b-f58284158bea] received
2026-05-26 12:06:56.651 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:06:56,653: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ddfb8cce-c0db-4087-a55b-f58284158bea] succeeded in 6.326343602966517s: None
2026-05-26 12:07:03.922 | INFO     | logging:callHandlers:1762 - 10.16.25.130:13188 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
2026-05-26 12:07:11.361 | INFO     | logging:callHandlers:1762 - 10.16.25.130:45377 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
2026-05-26 12:07:30.049 | INFO     | logging:callHandlers:1762 - 10.16.46.186:58827 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
2026-05-26 12:07:45.581 | INFO     | logging:callHandlers:1762 - 10.16.17.88:15213 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
[2026-05-26 12:07:49,450: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:07:50,110: INFO/MainProcess] Task triam.notifications.scan_due[9fbd7bc6-6b42-42a1-8f36-4502bb7a5e2f] received
2026-05-26 12:07:56.433 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:07:56,434: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[9fbd7bc6-6b42-42a1-8f36-4502bb7a5e2f] succeeded in 6.317350917961448s: None
2026-05-26 12:08:00.039 | INFO     | logging:callHandlers:1762 - 10.16.46.186:63028 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
2026-05-26 12:08:12.967 | INFO     | logging:callHandlers:1762 - 10.16.5.171:49042 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
2026-05-26 12:08:41.761 | INFO     | logging:callHandlers:1762 - 10.16.5.171:47867 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
[2026-05-26 12:08:49,453: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:08:50,534: INFO/MainProcess] Task triam.notifications.scan_due[832cbfdc-46b9-4a67-936e-cd107ab5e7d3] received
2026-05-26 12:08:56.674 | INFO     | logging:callHandlers:1762 - 10.16.46.186:61555 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
2026-05-26 12:08:56.849 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:08:56,849: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[832cbfdc-46b9-4a67-936e-cd107ab5e7d3] succeeded in 6.3145842659287155s: None
2026-05-26 12:09:09.767 | INFO     | logging:callHandlers:1762 - 10.16.25.130:43764 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
2026-05-26 12:09:25.038 | INFO     | logging:callHandlers:1762 - 10.16.17.88:54397 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
2026-05-26 12:09:39.333 | INFO     | logging:callHandlers:1762 - 10.16.46.186:63995 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
2026-05-26 12:09:43.503 | INFO     | logging:callHandlers:1762 - 10.16.25.130:17669 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
[2026-05-26 12:09:49,453: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:09:50,328: INFO/MainProcess] Task triam.notifications.scan_due[b6eecd99-aed1-45d2-ab9e-5e4fcf671e85] received
2026-05-26 12:09:58.236 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:09:58,238: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b6eecd99-aed1-45d2-ab9e-5e4fcf671e85] succeeded in 7.909224836039357s: None
2026-05-26 12:09:58.391 | INFO     | logging:callHandlers:1762 - 10.16.46.186:43165 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
2026-05-26 12:10:01.221 | INFO     | logging:callHandlers:1762 - 10.16.46.186:43165 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
2026-05-26 12:10:23.114 | INFO     | logging:callHandlers:1762 - 10.16.17.88:12514 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
[2026-05-26 12:10:49,455: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:10:50,112: INFO/MainProcess] Task triam.notifications.scan_due[702178c9-cf59-48d5-8c28-cd3a8c502430] received
2026-05-26 12:10:56.725 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:10:56,726: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[702178c9-cf59-48d5-8c28-cd3a8c502430] succeeded in 6.609748009010218s: None
[2026-05-26 12:11:49,454: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:11:50,546: INFO/MainProcess] Task triam.notifications.scan_due[df87eec8-bfcf-46e9-91f5-53c217af1cdc] received
2026-05-26 12:11:57.345 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:11:57,345: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[df87eec8-bfcf-46e9-91f5-53c217af1cdc] succeeded in 6.577332974993624s: None
[2026-05-26 12:12:49,454: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:12:50,110: INFO/MainProcess] Task triam.notifications.scan_due[2d4ca3d0-d18b-43e1-8d96-95756d5d123e] received
2026-05-26 12:12:56.692 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:12:56,694: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2d4ca3d0-d18b-43e1-8d96-95756d5d123e] succeeded in 6.580541845993139s: None
[2026-05-26 12:13:49,455: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:13:50,326: INFO/MainProcess] Task triam.notifications.scan_due[544a62cb-a860-40bf-af88-76a88403830a] received
2026-05-26 12:13:57.133 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:13:57,134: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[544a62cb-a860-40bf-af88-76a88403830a] succeeded in 6.59006222395692s: None
2026-05-26 12:14:27.325 | INFO     | logging:callHandlers:1762 - 10.16.17.88:28434 - "GET /api/v1/threads/for-book/9a64d766-eb7c-404f-a9e9-9073f11c0030 HTTP/1.1" 200
2026-05-26 12:14:31.001 | INFO     | logging:callHandlers:1762 - 10.16.46.186:3741 - "GET /api/v1/live-token/thread/42a57333-9536-431c-9657-0e1e9c800b6b HTTP/1.1" 200
2026-05-26 12:14:33.292 | INFO     | logging:callHandlers:1762 - received job request
{"message": "received job request", "level": "INFO", "name": "livekit.agents", "job_id": "AJ_FJpSfdL6CVPy", "dispatch_id": "AD_yU5QWLaUGmbZ", "room": "triam_42a57333_999938", "room_id": "RM_izqNbmCRLM5G", "agent_name": "triam-voice-agent", "resuming": false, "enable_recording": false, "timestamp": "2026-05-26T12:14:33.292314+00:00"}
2026-05-26 12:14:33.381 | INFO     | logging:callHandlers:1762 - initializing job runner
{"message": "initializing job runner", "level": "INFO", "name": "livekit.agents", "tid": 85, "timestamp": "2026-05-26T12:14:33.381640+00:00"}
2026-05-26 12:14:33.385 | INFO     | logging:callHandlers:1762 - job runner initialized
{"message": "job runner initialized", "level": "INFO", "name": "livekit.agents", "tid": 85, "elapsed_time": 0.0, "timestamp": "2026-05-26T12:14:33.385209+00:00"}
2026-05-26 12:14:33.822 | INFO     | __main__:entrypoint:249 - ✅ Document IDs từ metadata: ['9a64d766-eb7c-404f-a9e9-9073f11c0030']
2026-05-26 12:14:33.824 | INFO     | __main__:entrypoint:250 - 🏠 Room Name (session): triam_42a57333_999938
2026-05-26 12:14:33.826 | INFO     | __main__:entrypoint:251 - Bat dau phien doc sach cho Thread ID: 42a57333-9536-431c-9657-0e1e9c800b6b
2026-05-26 12:14:33.855 | INFO     | __main__:entrypoint:554 - Starting realtime session with model: gpt-realtime, voice: cedar
2026-05-26 12:14:36.565 | INFO     | __main__:handle_data_input:433 - Data input from user_211294: tác giả tài liệu là ai
2026-05-26 12:14:38.736 | INFO     | __main__:flush:123 - Text output (2 chars): Ch
2026-05-26 12:14:38.848 | INFO     | __main__:_chat_naive_rag:337 - [Text Chat] Chế độ Naive RAG (web search TẮT)
2026-05-26 12:14:45.902 | INFO     | __main__:handle_data_input:454 - LLM Reply completed. Length: 336
[2026-05-26 12:14:49,455: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:14:50,462: INFO/MainProcess] Task triam.notifications.scan_due[38736668-dd23-4d3a-a846-b4e8ad1dcd81] received
2026-05-26 12:14:57.280 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:14:57,280: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[38736668-dd23-4d3a-a846-b4e8ad1dcd81] succeeded in 6.598636280046776s: None
2026-05-26 12:15:21.262 | INFO     | __main__:handle_data_input:433 - Data input from user_211294: trình bày các điểm chính mà tài liệu trình bày
2026-05-26 12:15:21.934 | INFO     | __main__:_chat_naive_rag:337 - [Text Chat] Chế độ Naive RAG (web search TẮT)
2026-05-26 12:15:32.753 | INFO     | __main__:handle_data_input:454 - LLM Reply completed. Length: 1495
[2026-05-26 12:15:49,457: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:15:50,114: INFO/MainProcess] Task triam.notifications.scan_due[72d605e8-9627-4e15-8935-d79d815d37e6] received
2026-05-26 12:15:56.707 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:15:56,708: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[72d605e8-9627-4e15-8935-d79d815d37e6] succeeded in 6.592760634957813s: None
2026-05-26 12:16:19.772 | INFO     | logging:callHandlers:1762 - closing agent session due to participant disconnect (disable via `RoomInputOptions.close_on_disconnect=False`)
{"message": "closing agent session due to participant disconnect (disable via `RoomInputOptions.close_on_disconnect=False`)", "level": "INFO", "name": "livekit.agents", "room": "triam_42a57333_999938", "participant": "user_211294", "reason": "CLIENT_INITIATED", "timestamp": "2026-05-26T12:16:19.772103+00:00"}
[2026-05-26 12:16:49,457: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:16:50,328: INFO/MainProcess] Task triam.notifications.scan_due[03b788c9-3484-4881-af04-ec9a48738bc9] received
2026-05-26 12:16:56.929 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:16:56,931: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[03b788c9-3484-4881-af04-ec9a48738bc9] succeeded in 6.600021409103647s: None
[2026-05-26 12:17:49,458: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:17:50,114: INFO/MainProcess] Task triam.notifications.scan_due[d755d247-c414-4796-98aa-a1d39e6dedda] received
2026-05-26 12:17:56.686 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:17:56,690: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d755d247-c414-4796-98aa-a1d39e6dedda] succeeded in 6.575033429078758s: None
[2026-05-26 12:18:49,458: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:18:50,330: INFO/MainProcess] Task triam.notifications.scan_due[441e25df-0312-43a0-bd40-4df993a4a8fd] received
2026-05-26 12:18:56.914 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:18:56,914: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[441e25df-0312-43a0-bd40-4df993a4a8fd] succeeded in 6.579014971968718s: None
[2026-05-26 12:19:49,458: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:19:50,329: INFO/MainProcess] Task triam.notifications.scan_due[d9e2eea6-225d-4b4d-ab7c-80257d46334e] received
2026-05-26 12:19:56.933 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:19:56,934: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d9e2eea6-225d-4b4d-ab7c-80257d46334e] succeeded in 6.603843575925566s: None
[2026-05-26 12:20:49,461: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:20:50,334: INFO/MainProcess] Task triam.notifications.scan_due[3a12a769-1881-4531-b5f5-e81cc25c4b1d] received
2026-05-26 12:20:57.039 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:20:57,040: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3a12a769-1881-4531-b5f5-e81cc25c4b1d] succeeded in 6.705060709035024s: None
[2026-05-26 12:21:49,461: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:21:50,335: INFO/MainProcess] Task triam.notifications.scan_due[46067bef-c253-4ceb-8efa-37f4bbb0e958] received
2026-05-26 12:21:57.015 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:21:57,015: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[46067bef-c253-4ceb-8efa-37f4bbb0e958] succeeded in 6.679096508072689s: None
2026-05-26 12:22:30.295 | INFO     | logging:callHandlers:1762 - 10.16.17.88:22519 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/42108346-ab9e-49fd-aff9-4879423487d1/progress HTTP/1.1" 422
2026-05-26 12:22:36.781 | INFO     | logging:callHandlers:1762 - 10.16.46.186:2419 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=pareto HTTP/1.1" 200
[2026-05-26 12:22:49,461: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:22:50,123: INFO/MainProcess] Task triam.notifications.scan_due[a00d88fb-2dc3-40f8-a507-29835356670c] received
2026-05-26 12:22:56.819 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:22:56,819: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a00d88fb-2dc3-40f8-a507-29835356670c] succeeded in 6.695149058010429s: None
2026-05-26 12:22:57.952 | INFO     | logging:callHandlers:1762 - 10.16.25.130:28361 - "GET /api/v1/books/2/details HTTP/1.1" 422
[2026-05-26 12:23:49,462: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:23:50,337: INFO/MainProcess] Task triam.notifications.scan_due[ce94cc2f-fdbb-46c9-9d55-f4ba957f0926] received
2026-05-26 12:23:57.037 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:23:57,038: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ce94cc2f-fdbb-46c9-9d55-f4ba957f0926] succeeded in 6.700759841944091s: None
[2026-05-26 12:24:49,462: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:24:50,342: INFO/MainProcess] Task triam.notifications.scan_due[cfeb4ac2-054d-49be-adf2-6121821540b1] received
2026-05-26 12:24:57.037 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:24:57,038: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[cfeb4ac2-054d-49be-adf2-6121821540b1] succeeded in 6.69521817995701s: None
[2026-05-26 12:25:49,462: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:25:50,337: INFO/MainProcess] Task triam.notifications.scan_due[8022781f-0099-483e-8553-d2b0c52c937d] received
2026-05-26 12:25:57.495 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:25:57,496: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8022781f-0099-483e-8553-d2b0c52c937d] succeeded in 7.157069737906568s: None
2026-05-26 12:26:26.166 | INFO     | logging:callHandlers:1762 - 10.16.17.88:54259 - "GET /api/v1/study-contexts HTTP/1.1" 200
[2026-05-26 12:26:49,463: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:26:50,334: INFO/MainProcess] Task triam.notifications.scan_due[ac37d0e0-2afe-4aa5-86fc-6db5ac108340] received
2026-05-26 12:26:57.026 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:26:57,027: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ac37d0e0-2afe-4aa5-86fc-6db5ac108340] succeeded in 6.691912446985953s: None
2026-05-26 12:27:23.587 | INFO     | logging:callHandlers:1762 - 10.16.17.88:35518 - "GET /api/v1/books/2/details HTTP/1.1" 422
2026-05-26 12:27:25.347 | INFO     | logging:callHandlers:1762 - 10.16.17.88:35518 - "GET /api/v1/books/2/details HTTP/1.1" 422
[2026-05-26 12:27:49,467: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:27:50,137: INFO/MainProcess] Task triam.notifications.scan_due[6625ddef-4cc2-4489-ab23-3c282e6d8192] received
2026-05-26 12:27:56.817 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:27:56,820: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[6625ddef-4cc2-4489-ab23-3c282e6d8192] succeeded in 6.6819950270000845s: None
[2026-05-26 12:28:49,467: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:28:50,336: INFO/MainProcess] Task triam.notifications.scan_due[08e27dda-1bbc-4dea-bf78-9699b523bc39] received
2026-05-26 12:28:56.969 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:28:56,971: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[08e27dda-1bbc-4dea-bf78-9699b523bc39] succeeded in 6.634069148101844s: None
[2026-05-26 12:29:49,467: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:29:50,337: INFO/MainProcess] Task triam.notifications.scan_due[99c0326e-e4ee-48e6-af93-3bfe354c125c] received
2026-05-26 12:29:56.972 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:29:56,973: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[99c0326e-e4ee-48e6-af93-3bfe354c125c] succeeded in 6.634632470086217s: None
[2026-05-26 12:30:49,467: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:30:50,341: INFO/MainProcess] Task triam.notifications.scan_due[9f791c1f-34fd-4f3e-bd80-b8bc6891c9a7] received
2026-05-26 12:30:56.982 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:30:56,984: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[9f791c1f-34fd-4f3e-bd80-b8bc6891c9a7] succeeded in 6.641989971045405s: None
[2026-05-26 12:31:49,467: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:31:50,443: INFO/MainProcess] Task triam.notifications.scan_due[4342c50a-8b4f-46c1-81ba-5dbd4bfd1b3b] received
2026-05-26 12:31:57.070 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:31:57,070: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4342c50a-8b4f-46c1-81ba-5dbd4bfd1b3b] succeeded in 6.625763631076552s: None
2026-05-26 12:32:21.860 | INFO     | logging:callHandlers:1762 - 10.16.17.88:59083 - "POST /api/v1/books/1a2e51e4-4fca-454a-9071-9bd005ed13df/switch-mode HTTP/1.1" 200
[2026-05-26 12:32:22,245: INFO/MainProcess] Task triam.books.switch_mode[5df7e81b-6217-49e2-8b30-7e60482d8e25] received
2026-05-26 12:32:22.247 | INFO     | app.tasks.book_tasks:switch_mode_task:43 - Celery switch_mode_task started | book_id=1a2e51e4-4fca-454a-9071-9bd005ed13df | mode=pareto | job_id=54fbb04f-8cb5-431b-8fb6-5327224a6666
2026-05-26 12:32:26.173 | INFO     | app.services.workers.book_pipeline:run_switch_mode_processing:450 - ⬇️  Downloading PDF for switch mode: 1a2e51e4-4fca-454a-9071-9bd005ed13df/original.pdf
2026-05-26 12:32:27.483 | INFO     | logging:callHandlers:1762 - 10.16.17.88:57779 - "GET /api/v1/jobs/54fbb04f-8cb5-431b-8fb6-5327224a6666 HTTP/1.1" 200
2026-05-26 12:32:32.970 | INFO     | logging:callHandlers:1762 - 10.16.5.171:9890 - "GET /api/v1/jobs/54fbb04f-8cb5-431b-8fb6-5327224a6666 HTTP/1.1" 200
2026-05-26 12:32:43.316 | INFO     | logging:callHandlers:1762 - 10.16.17.88:58928 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=pareto HTTP/1.1" 200
[2026-05-26 12:32:49,467: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:32:50,133: INFO/MainProcess] Task triam.notifications.scan_due[710d8d3c-c05a-4389-9998-f76141370ddf] received
2026-05-26 12:32:56.832 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:32:56,834: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[710d8d3c-c05a-4389-9998-f76141370ddf] succeeded in 6.700382314971648s: None
2026-05-26 12:33:33.554 | INFO     | logging:callHandlers:1762 - 10.16.17.88:43586 - "POST /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/switch-mode HTTP/1.1" 200
2026-05-26 12:33:36.745 | INFO     | logging:callHandlers:1762 - 10.16.5.171:62950 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/details HTTP/1.1" 200
2026-05-26 12:33:40.444 | INFO     | logging:callHandlers:1762 - 10.16.25.130:64262 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
[2026-05-26 12:33:49,468: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:33:50,477: INFO/MainProcess] Task triam.notifications.scan_due[dcfd5969-db43-419e-a0cf-24644f495733] received
2026-05-26 12:33:57.195 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:33:57,196: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[dcfd5969-db43-419e-a0cf-24644f495733] succeeded in 6.718015145044774s: None
2026-05-26 12:34:06.207 | INFO     | logging:callHandlers:1762 - 10.16.46.186:24954 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-26 12:34:13.547 | INFO     | logging:callHandlers:1762 - 10.16.17.88:1673 - "GET /api/v1/study-contexts HTTP/1.1" 200
2026-05-26 12:34:13.549 | INFO     | logging:callHandlers:1762 - 10.16.25.130:51363 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 12:34:35.199 | INFO     | app.repositories.audiobook_repo:delete_book_storage:93 - Đã xóa 1 files từ bucket: raw_books
[2026-05-26 12:34:37,879: INFO/ForkPoolWorker-1] Task triam.books.switch_mode[5df7e81b-6217-49e2-8b30-7e60482d8e25] succeeded in 135.63217112899292s: None
[2026-05-26 12:34:49,469: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:34:50,342: INFO/MainProcess] Task triam.notifications.scan_due[8fc6f21b-7297-4463-b9d9-fec39bca3b8c] received
2026-05-26 12:34:57.131 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:34:57,131: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8fc6f21b-7297-4463-b9d9-fec39bca3b8c] succeeded in 6.787418429041281s: None
[2026-05-26 12:35:49,469: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:35:50,339: INFO/MainProcess] Task triam.notifications.scan_due[4c3befcb-9966-40f0-9f1d-32b6f62476af] received
2026-05-26 12:35:56.978 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:35:56,979: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4c3befcb-9966-40f0-9f1d-32b6f62476af] succeeded in 6.638321901904419s: None
2026-05-26 12:36:07.446 | INFO     | app.repositories.audiobook_repo:delete_book_storage:97 - Đã dọn dẹp sạch sẽ database cho book: 1a2e51e4-4fca-454a-9071-9bd005ed13df
2026-05-26 12:36:07.448 | INFO     | logging:callHandlers:1762 - 10.16.46.186:10181 - "DELETE /api/v1/books/1a2e51e4-4fca-454a-9071-9bd005ed13df HTTP/1.1" 200
2026-05-26 12:36:09.041 | WARNING  | app.main:app_exception_handler:36 - AppException: PDF không có bookmark/outline ẩn. Vui lòng upload PDF có mục lục chuẩn. - Status Code: 422
2026-05-26 12:36:09.043 | INFO     | logging:callHandlers:1762 - 10.16.17.88:1155 - "POST /api/v1/upload HTTP/1.1" 422
2026-05-26 12:36:09.044 | WARNING  | app.main:app_exception_handler:36 - AppException: PDF không có bookmark/outline ẩn. Vui lòng upload PDF có mục lục chuẩn. - Status Code: 422
2026-05-26 12:36:09.045 | INFO     | logging:callHandlers:1762 - 10.16.5.171:63543 - "POST /api/v1/upload HTTP/1.1" 422
2026-05-26 12:36:09.084 | WARNING  | app.main:app_exception_handler:36 - AppException: Book not found. - Status Code: 404
2026-05-26 12:36:09.085 | INFO     | logging:callHandlers:1762 - 10.16.25.130:6824 - "DELETE /api/v1/books/1a2e51e4-4fca-454a-9071-9bd005ed13df HTTP/1.1" 404
[2026-05-26 12:36:49,470: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:36:50,339: INFO/MainProcess] Task triam.notifications.scan_due[3c3f3fb0-69be-48ac-a410-dca59e1f9898] received
2026-05-26 12:36:57.259 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:36:57,260: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3c3f3fb0-69be-48ac-a410-dca59e1f9898] succeeded in 6.704385485965759s: None
[2026-05-26 12:37:49,478: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:37:50,143: INFO/MainProcess] Task triam.notifications.scan_due[ba08d741-6caa-4fc3-a203-9cb7151908be] received
2026-05-26 12:37:56.864 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:37:56,865: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ba08d741-6caa-4fc3-a203-9cb7151908be] succeeded in 6.720394516014494s: None
[2026-05-26 12:38:49,481: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:38:50,348: INFO/MainProcess] Task triam.notifications.scan_due[c375a9e8-8d6f-4b68-a1cd-67de82d9e683] received
2026-05-26 12:38:54.860 | WARNING  | app.main:app_exception_handler:36 - AppException: DOCX không có Heading/mục lục hợp lệ. Vui lòng dùng Heading 1/Heading 2 cho tên chương. - Status Code: 422
2026-05-26 12:38:54.861 | INFO     | logging:callHandlers:1762 - 10.16.25.130:30469 - "POST /api/v1/upload HTTP/1.1" 422
2026-05-26 12:38:57.290 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:38:57,291: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c375a9e8-8d6f-4b68-a1cd-67de82d9e683] succeeded in 6.726011201972142s: None
[2026-05-26 12:39:49,482: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:39:50,138: INFO/MainProcess] Task triam.notifications.scan_due[5d2c74f3-2fc2-4797-8fbe-96d38a1bf497] received
2026-05-26 12:39:53.382 | INFO     | app.services.upload_service:handle_upload_document:108 - ☁️  DOCX uploaded to Storage: a9453a82-6e22-42c7-bc4a-c8bd9125c422/original.docx
2026-05-26 12:39:56.844 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:39:56,844: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5d2c74f3-2fc2-4797-8fbe-96d38a1bf497] succeeded in 6.6995503809303045s: None
2026-05-26 12:40:10.282 | INFO     | app.services.upload_service:handle_upload_document:139 - 📘 Created DRAFT book a9453a82-6e22-42c7-bc4a-c8bd9125c422 | 18 chapters | file_url saved
2026-05-26 12:40:10.286 | INFO     | logging:callHandlers:1762 - 10.16.46.186:16190 - "POST /api/v1/upload HTTP/1.1" 200
2026-05-26 12:40:12.471 | INFO     | logging:callHandlers:1762 - 10.16.17.88:16953 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 12:40:21.852 | INFO     | logging:callHandlers:1762 - 10.16.17.88:13653 - "GET /api/v1/notifications/settings HTTP/1.1" 200
2026-05-26 12:40:32.986 | INFO     | app.services.upload_service:handle_generate_plan:213 - 📋 ReadingPlan created for book a9453a82-6e22-42c7-bc4a-c8bd9125c422 | mode=pareto | job=d8bac78e-5601-4779-bc3e-5263b71e561c
2026-05-26 12:40:33.423 | INFO     | logging:callHandlers:1762 - 10.16.5.171:18602 - "POST /api/v1/generate-plan HTTP/1.1" 200
[2026-05-26 12:40:33,849: INFO/MainProcess] Task triam.books.process[7b8bd5cd-d07c-4c45-b083-a37fcffd042d] received
2026-05-26 12:40:33.850 | INFO     | app.tasks.book_tasks:process_book_task:23 - Celery process_book_task started | book_id=a9453a82-6e22-42c7-bc4a-c8bd9125c422 | mode=pareto | job_id=d8bac78e-5601-4779-bc3e-5263b71e561c
2026-05-26 12:40:36.001 | INFO     | logging:callHandlers:1762 - 10.16.25.130:8163 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 12:40:36.230 | INFO     | app.services.workers.book_pipeline:run_background_processing:306 - ⬇️  Downloading DOCX from Storage: a9453a82-6e22-42c7-bc4a-c8bd9125c422/original.docx
2026-05-26 12:40:37.485 | INFO     | logging:callHandlers:1762 - 10.16.46.186:7782 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:40:41.496 | INFO     | logging:callHandlers:1762 - 10.16.5.171:50641 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:40:42.191 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=1 | mode=pareto | title=LỜI MỞ ĐẦU | chars=2600 | estimated_tokens=1288 | estimated_audio_seconds=266
2026-05-26 12:40:44.536 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=1 | mode=pareto | rag=true | tts=true
[2026-05-26 12:40:44,542: INFO/ForkPoolWorker-1] Retrying request to /embeddings in 0.414969 seconds
2026-05-26 12:40:44.544 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=1 | mode=pareto | title=LỜI MỞ ĐẦU | raw_chars=2600
2026-05-26 12:40:44.548 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=pareto | title=LỜI MỞ ĐẦU | chars=2600 | estimated_tokens=1288 | estimated_audio_seconds=266
2026-05-26 12:40:44.549 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=pareto | strategy=single_call | title=LỜI MỞ ĐẦU
2026-05-26 12:40:44.550 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=pareto | context=single | chars=2600
[2026-05-26 12:40:44,555: INFO/ForkPoolWorker-1] Retrying request to /chat/completions in 0.451608 seconds
2026-05-26 12:40:45.413 | INFO     | logging:callHandlers:1762 - 10.16.25.130:50387 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:40:47.184 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 3 vectors for chapter_id=f8631a49-0e4c-4092-8b3f-c14cc075626e
[2026-05-26 12:40:49,482: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-26 12:40:49.527 | INFO     | logging:callHandlers:1762 - 10.16.5.171:12995 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
[2026-05-26 12:40:50,350: INFO/MainProcess] Task triam.notifications.scan_due[f1b9cdd3-0d78-4f83-8cd1-2db0eb8f7e52] received
2026-05-26 12:40:53.491 | INFO     | logging:callHandlers:1762 - 10.16.46.186:10934 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:40:57.462 | INFO     | logging:callHandlers:1762 - 10.16.17.88:34613 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:40:57.644 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=pareto | context=single | scripts=5 | review_chars=537
2026-05-26 12:40:57.646 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=1 | mode=pareto | main_scripts=5 | review_chars=537
2026-05-26 12:40:57.647 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=1 | mode=pareto | total_scripts=5
2026-05-26 12:40:57.648 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=pareto | segment=1/5 | chars=314
2026-05-26 12:40:58.750 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:40:58,751: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f1b9cdd3-0d78-4f83-8cd1-2db0eb8f7e52] succeeded in 8.182348555070348s: None
2026-05-26 12:41:01.472 | INFO     | logging:callHandlers:1762 - 10.16.17.88:15556 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:41:05.341 | INFO     | logging:callHandlers:1762 - 10.16.17.88:58479 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:41:08.294 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=pareto | segment=1/5 | duration_ms=17640
2026-05-26 12:41:08.295 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=pareto | segment=2/5 | chars=406
2026-05-26 12:41:09.364 | INFO     | logging:callHandlers:1762 - 10.16.46.186:27294 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:41:13.216 | INFO     | logging:callHandlers:1762 - 10.16.5.171:5908 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:41:15.891 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=pareto | segment=2/5 | duration_ms=22032
2026-05-26 12:41:15.891 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=pareto | segment=3/5 | chars=385
2026-05-26 12:41:17.030 | INFO     | logging:callHandlers:1762 - 10.16.46.186:57737 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:41:21.011 | INFO     | logging:callHandlers:1762 - 10.16.25.130:53754 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:41:22.402 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=pareto | segment=3/5 | duration_ms=22296
2026-05-26 12:41:22.403 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=pareto | segment=4/5 | chars=425
2026-05-26 12:41:24.989 | INFO     | logging:callHandlers:1762 - 10.16.17.88:29131 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:41:29.211 | INFO     | logging:callHandlers:1762 - 10.16.25.130:49843 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:41:33.224 | INFO     | logging:callHandlers:1762 - 10.16.17.88:22865 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:41:33.370 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=pareto | segment=4/5 | duration_ms=24048
2026-05-26 12:41:33.371 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=pareto | segment=5/5 | chars=290
2026-05-26 12:41:37.173 | INFO     | logging:callHandlers:1762 - 10.16.17.88:4719 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:41:40.013 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=pareto | segment=5/5 | duration_ms=15576
2026-05-26 12:41:40.014 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=1 | mode=pareto | created_segments=5/5
2026-05-26 12:41:40.014 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=1 | mode=pareto | chars=537
2026-05-26 12:41:41.184 | INFO     | logging:callHandlers:1762 - 10.16.5.171:35491 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:41:45.083 | INFO     | logging:callHandlers:1762 - 10.16.17.88:7954 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:41:47.500 | WARNING  | app.services.storage_service:upload_file_to_supabase:57 - Upload failed (attempt 1/3), retrying in 1s...
2026-05-26 12:41:49.062 | INFO     | logging:callHandlers:1762 - 10.16.17.88:14728 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
[2026-05-26 12:41:49,482: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-26 12:41:49.762 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=1 | mode=pareto
2026-05-26 12:41:49.763 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=f8631a49-0e4c-4092-8b3f-c14cc075626e | mode=pareto | segments=5 | review_audio=True
[2026-05-26 12:41:50,353: INFO/MainProcess] Task triam.notifications.scan_due[86bcc162-47b0-4523-b32b-48f3dd62cdbe] received
2026-05-26 12:41:53.044 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=f8631a49-0e4c-4092-8b3f-c14cc075626e | mode=pareto
2026-05-26 12:41:53.451 | INFO     | logging:callHandlers:1762 - 10.16.17.88:25925 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:41:55.602 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 1 READY | mode=pareto | segments=5
2026-05-26 12:41:57.184 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:41:57,185: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[86bcc162-47b0-4523-b32b-48f3dd62cdbe] succeeded in 6.830852318089455s: None
2026-05-26 12:41:57.241 | INFO     | logging:callHandlers:1762 - 10.16.46.186:3137 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:41:58.842 | INFO     | app.services.workers.book_pipeline:_create_first_playable_notification_safely:123 - Content-ready first-playable event | book_id=a9453a82-6e22-42c7-bc4a-c8bd9125c422 | mode=pareto | created=False
2026-05-26 12:41:59.073 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=2 | mode=pareto | title=1.1 Giới thiệu | chars=387 | estimated_tokens=174 | estimated_audio_seconds=38
2026-05-26 12:42:01.045 | INFO     | logging:callHandlers:1762 - 10.16.17.88:5177 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:42:01.385 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=2 | mode=pareto | rag=true | tts=true
2026-05-26 12:42:01.391 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=3 | mode=pareto | title=1.2 Tính cấp thiết dự án | chars=4744 | estimated_tokens=2335 | estimated_audio_seconds=482
2026-05-26 12:42:03.697 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=3 | mode=pareto | rag=true | tts=true
2026-05-26 12:42:03.708 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=2 | mode=pareto | title=1.1 Giới thiệu | raw_chars=387
2026-05-26 12:42:03.710 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=pareto | title=1.1 Giới thiệu | chars=387 | estimated_tokens=174 | estimated_audio_seconds=38
2026-05-26 12:42:03.713 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=pareto | strategy=single_call | title=1.1 Giới thiệu
2026-05-26 12:42:03.714 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=pareto | context=single | chars=387
2026-05-26 12:42:03.722 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=3 | mode=pareto | title=1.2 Tính cấp thiết dự án | raw_chars=4744
2026-05-26 12:42:03.727 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=pareto | title=1.2 Tính cấp thiết dự án | chars=4744 | estimated_tokens=2335 | estimated_audio_seconds=482
2026-05-26 12:42:03.728 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=pareto | strategy=single_call | title=1.2 Tính cấp thiết dự án
2026-05-26 12:42:04.858 | INFO     | logging:callHandlers:1762 - 10.16.17.88:57215 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:42:05.688 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 6 vectors for chapter_id=bf20abc7-caf4-4ca9-8eb0-49383a5787a9
2026-05-26 12:42:06.387 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=f5e2c035-0761-4a4a-bb04-f1f727570ac7
2026-05-26 12:42:06.625 | INFO     | logging:callHandlers:1762 - 10.16.25.130:59530 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 12:42:06.626 | INFO     | logging:callHandlers:1762 - 10.16.46.186:62633 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 12:42:09.075 | INFO     | logging:callHandlers:1762 - 10.16.17.88:57134 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:42:12.905 | INFO     | logging:callHandlers:1762 - 10.16.17.88:35948 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:42:15.132 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=pareto | context=single | chars=4744
2026-05-26 12:42:15.145 | ERROR    | app.services.workers.chapter_worker:process_chapter:118 - ❌ Chapter 2 thất bại: LLM response không phải JSON hợp lệ.
2026-05-26 12:42:16.791 | INFO     | logging:callHandlers:1762 - 10.16.17.88:24674 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:42:19.531 | INFO     | app.services.workers.chapter_worker:process_chapter:125 - 🧹 Cleaned failed side effects for chapter 2.
2026-05-26 12:42:19.533 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=4 | mode=pareto | title=1.3.1. Mục tiêu chung | chars=428 | estimated_tokens=211 | estimated_audio_seconds=43
2026-05-26 12:42:20.548 | INFO     | logging:callHandlers:1762 - 10.16.5.171:6351 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:42:21.828 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=4 | mode=pareto | rag=true | tts=true
2026-05-26 12:42:21.840 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=4 | mode=pareto | title=1.3.1. Mục tiêu chung | raw_chars=428
2026-05-26 12:42:21.843 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=pareto | title=1.3.1. Mục tiêu chung | chars=428 | estimated_tokens=211 | estimated_audio_seconds=43
2026-05-26 12:42:21.846 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=pareto | strategy=single_call | title=1.3.1. Mục tiêu chung
2026-05-26 12:42:24.305 | INFO     | logging:callHandlers:1762 - 10.16.25.130:64862 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
2026-05-26 12:42:26.008 | ERROR    | app.services.workers.book_pipeline:run_background_processing:418 - ❌ LỖI XỬ LÝ SÁCH a9453a82-6e22-42c7-bc4a-c8bd9125c422: LLM response không phải JSON hợp lệ.
[2026-05-26 12:42:26,012: INFO/ForkPoolWorker-1] Task triam.books.process[7b8bd5cd-d07c-4c45-b083-a37fcffd042d] succeeded in 112.1625805409858s: None
2026-05-26 12:42:28.147 | INFO     | logging:callHandlers:1762 - 10.16.5.171:1563 - "GET /api/v1/jobs/d8bac78e-5601-4779-bc3e-5263b71e561c HTTP/1.1" 200
[2026-05-26 12:42:49,485: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:42:50,138: INFO/MainProcess] Task triam.notifications.scan_due[eae40548-de18-4693-b43c-97b08e2ca01d] received
2026-05-26 12:42:56.963 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:42:56,964: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[eae40548-de18-4693-b43c-97b08e2ca01d] succeeded in 6.82614288199693s: None
[2026-05-26 12:43:49,484: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:43:50,353: INFO/MainProcess] Task triam.notifications.scan_due[8a9c8a0e-a5b7-47ec-9976-eb9638f4e4d7] received
2026-05-26 12:43:57.163 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:43:57,165: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8a9c8a0e-a5b7-47ec-9976-eb9638f4e4d7] succeeded in 6.809661546954885s: None
[2026-05-26 12:44:49,484: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:44:50,136: INFO/MainProcess] Task triam.notifications.scan_due[4861c58a-af70-4a26-ac70-ee253bbd892e] received
2026-05-26 12:44:57.091 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:44:57,091: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4861c58a-af70-4a26-ac70-ee253bbd892e] succeeded in 6.953528438927606s: None
[2026-05-26 12:45:49,486: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:45:50,356: INFO/MainProcess] Task triam.notifications.scan_due[72c42677-1592-4216-8b87-9e117660330e] received
2026-05-26 12:45:57.373 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:45:57,374: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[72c42677-1592-4216-8b87-9e117660330e] succeeded in 6.7999428058974445s: None
[2026-05-26 12:46:49,485: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:46:50,356: INFO/MainProcess] Task triam.notifications.scan_due[ac362bb9-751f-461f-929f-98594816f930] received
2026-05-26 12:46:57.402 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:46:57,404: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ac362bb9-751f-461f-929f-98594816f930] succeeded in 6.829610027023591s: None
[2026-05-26 12:47:49,485: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:47:50,139: INFO/MainProcess] Task triam.notifications.scan_due[627bb154-ec86-4b37-85e4-5d2004b0a13a] received
2026-05-26 12:47:56.960 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:47:56,961: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[627bb154-ec86-4b37-85e4-5d2004b0a13a] succeeded in 6.8204277330078185s: None
[2026-05-26 12:48:49,486: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:48:50,354: INFO/MainProcess] Task triam.notifications.scan_due[7329163e-91a1-433c-bad1-3b01564661d6] received
2026-05-26 12:48:57.396 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:48:57,396: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7329163e-91a1-433c-bad1-3b01564661d6] succeeded in 6.822617442929186s: None
[2026-05-26 12:49:49,487: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:49:50,141: INFO/MainProcess] Task triam.notifications.scan_due[5904d831-8159-422f-b28f-d012b5cace42] received
2026-05-26 12:49:56.980 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:49:56,984: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5904d831-8159-422f-b28f-d012b5cace42] succeeded in 6.84159384702798s: None
[2026-05-26 12:50:49,485: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:50:50,365: INFO/MainProcess] Task triam.notifications.scan_due[b224585c-e79f-4e11-a57b-876507bfcbf9] received
2026-05-26 12:50:57.193 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:50:57,194: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b224585c-e79f-4e11-a57b-876507bfcbf9] succeeded in 6.828401717939414s: None
[2026-05-26 12:51:49,486: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:51:50,353: INFO/MainProcess] Task triam.notifications.scan_due[447b96e9-0475-4cfc-aa62-037d082e2b2f] received
2026-05-26 12:51:57.401 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:51:57,407: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[447b96e9-0475-4cfc-aa62-037d082e2b2f] succeeded in 6.834720361977816s: None
[2026-05-26 12:52:49,487: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:52:50,141: INFO/MainProcess] Task triam.notifications.scan_due[1d592b17-1c11-4be8-b5cf-5d039179a81d] received
2026-05-26 12:52:56.984 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:52:56,986: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1d592b17-1c11-4be8-b5cf-5d039179a81d] succeeded in 6.843663585023023s: None
[2026-05-26 12:53:49,487: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:53:50,354: INFO/MainProcess] Task triam.notifications.scan_due[3b7fd12e-3f05-4bfd-81d0-64c2f69dfdea] received
2026-05-26 12:53:57.560 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:53:57,561: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3b7fd12e-3f05-4bfd-81d0-64c2f69dfdea] succeeded in 6.988140466040932s: None
[2026-05-26 12:54:49,488: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:54:50,145: INFO/MainProcess] Task triam.notifications.scan_due[940257f4-3020-4b0c-bbf4-494513f229af] received
2026-05-26 12:54:57.079 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:54:57,081: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[940257f4-3020-4b0c-bbf4-494513f229af] succeeded in 6.934983821003698s: None
[2026-05-26 12:55:49,488: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:55:50,359: INFO/MainProcess] Task triam.notifications.scan_due[af7fea74-da57-46ad-8711-46317522d8bd] received
2026-05-26 12:55:57.406 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:55:57,406: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[af7fea74-da57-46ad-8711-46317522d8bd] succeeded in 6.8265673130517825s: None
[2026-05-26 12:56:49,488: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:56:50,357: INFO/MainProcess] Task triam.notifications.scan_due[8386214e-ad6d-4f61-8bec-57ee77c407ee] received
2026-05-26 12:56:57.405 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:56:57,406: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8386214e-ad6d-4f61-8bec-57ee77c407ee] succeeded in 6.827617777045816s: None
[2026-05-26 12:57:49,490: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:57:50,359: INFO/MainProcess] Task triam.notifications.scan_due[163926c9-1ff5-49ab-8dba-45f149e24f7c] received
2026-05-26 12:57:58.052 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:57:58,052: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[163926c9-1ff5-49ab-8dba-45f149e24f7c] succeeded in 6.827676424989477s: None
[2026-05-26 12:58:49,490: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:58:50,359: INFO/MainProcess] Task triam.notifications.scan_due[03dff077-f468-48b9-88c9-3b4fd302406a] received
2026-05-26 12:58:57.409 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:58:57,411: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[03dff077-f468-48b9-88c9-3b4fd302406a] succeeded in 6.836284340010025s: None
[2026-05-26 12:59:49,490: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 12:59:50,146: INFO/MainProcess] Task triam.notifications.scan_due[d0a36d82-2e19-4bd4-932d-c8ba935e375f] received
2026-05-26 12:59:56.970 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 12:59:56,971: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d0a36d82-2e19-4bd4-932d-c8ba935e375f] succeeded in 6.822706156061031s: None
[2026-05-26 13:00:49,490: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:00:50,358: INFO/MainProcess] Task triam.notifications.scan_due[4b546bc1-e12f-47c3-92e2-5970a963a51b] received
2026-05-26 13:01:08.474 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=2 | recovered=0 | should_deliver=True
[2026-05-26 13:01:08,900: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4b546bc1-e12f-47c3-92e2-5970a963a51b] succeeded in 18.325294847018085s: None
[2026-05-26 13:01:09,557: INFO/MainProcess] Task triam.notifications.deliver_due[b2d3ecc7-bdec-4626-99d6-a00101a2c5dc] received
2026-05-26 13:01:16.869 | INFO     | app.tasks.notification_tasks:deliver_due_notifications_task:67 - Notification delivery batch done | worker_id=notification-worker:a577449b-07ee-4e76-b20e-c285aa1be21b | delivered_attempts=2
[2026-05-26 13:01:16,871: INFO/ForkPoolWorker-1] Task triam.notifications.deliver_due[b2d3ecc7-bdec-4626-99d6-a00101a2c5dc] succeeded in 7.311582383932546s: None
[2026-05-26 13:01:49,491: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:01:50,363: INFO/MainProcess] Task triam.notifications.scan_due[8f83495e-0014-4d56-b7d1-8ea3060b25a0] received
2026-05-26 13:01:58.049 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:01:58,052: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8f83495e-0014-4d56-b7d1-8ea3060b25a0] succeeded in 7.686969886068255s: None
[2026-05-26 13:02:49,502: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:02:50,372: INFO/MainProcess] Task triam.notifications.scan_due[3c053873-0c05-4a85-aa0b-7c9cd7ea8881] received
2026-05-26 13:02:58.106 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:02:58,107: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3c053873-0c05-4a85-aa0b-7c9cd7ea8881] succeeded in 7.516267177998088s: None
[2026-05-26 13:03:49,502: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:03:50,375: INFO/MainProcess] Task triam.notifications.scan_due[4f3b3fe7-bde4-4cda-a914-dfe19a0b5afa] received
2026-05-26 13:03:58.099 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:03:58,100: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4f3b3fe7-bde4-4cda-a914-dfe19a0b5afa] succeeded in 7.505151638062671s: None
[2026-05-26 13:04:49,503: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:04:50,155: INFO/MainProcess] Task triam.notifications.scan_due[ea00d6e5-52ae-440d-befb-314f1fe629c2] received
2026-05-26 13:04:57.671 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:04:57,672: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ea00d6e5-52ae-440d-befb-314f1fe629c2] succeeded in 7.516100551001728s: None
[2026-05-26 13:05:49,506: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:05:50,377: INFO/MainProcess] Task triam.notifications.scan_due[6f059c7f-1bcb-43ad-81ba-fb636403cc6e] received
2026-05-26 13:05:58.121 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:05:58,123: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[6f059c7f-1bcb-43ad-81ba-fb636403cc6e] succeeded in 7.527265665004961s: None
[2026-05-26 13:06:49,507: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:06:50,376: INFO/MainProcess] Task triam.notifications.scan_due[715c6938-566b-4870-b145-ec6b3dcbc5dd] received
2026-05-26 13:06:58.096 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:06:58,097: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[715c6938-566b-4870-b145-ec6b3dcbc5dd] succeeded in 7.503184242057614s: None
[2026-05-26 13:07:49,506: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:07:50,380: INFO/MainProcess] Task triam.notifications.scan_due[2f9e9e2e-d344-4026-abe1-cd21ed9f2c16] received
2026-05-26 13:07:58.109 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:07:58,110: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2f9e9e2e-d344-4026-abe1-cd21ed9f2c16] succeeded in 7.5123544880189s: None
[2026-05-26 13:08:49,509: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:08:50,394: INFO/MainProcess] Task triam.notifications.scan_due[35d07073-38cf-4c8b-bb7f-8cbc2f37fbeb] received
2026-05-26 13:08:58.149 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:08:58,150: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[35d07073-38cf-4c8b-bb7f-8cbc2f37fbeb] succeeded in 7.536290050018579s: None
[2026-05-26 13:09:49,510: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:09:50,167: INFO/MainProcess] Task triam.notifications.scan_due[83cb8f1c-c803-4f88-b2eb-c7ba19050b6c] received
2026-05-26 13:09:57.679 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:09:57,681: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[83cb8f1c-c803-4f88-b2eb-c7ba19050b6c] succeeded in 7.511467156931758s: None
[2026-05-26 13:10:49,510: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:10:50,379: INFO/MainProcess] Task triam.notifications.scan_due[17528a75-bd93-4511-a4fa-a23989f140db] received
2026-05-26 13:10:59.207 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:10:59,209: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[17528a75-bd93-4511-a4fa-a23989f140db] succeeded in 8.829082143027335s: None
[2026-05-26 13:11:49,510: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:11:50,379: INFO/MainProcess] Task triam.notifications.scan_due[424bde81-5252-4e2f-82e5-b18f22fab6fb] received
2026-05-26 13:11:57.794 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:11:57,795: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[424bde81-5252-4e2f-82e5-b18f22fab6fb] succeeded in 7.414503006031737s: None
[2026-05-26 13:12:49,510: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:12:50,379: INFO/MainProcess] Task triam.notifications.scan_due[2aefcf59-5d08-45b0-8cb0-51349329fc65] received
2026-05-26 13:12:57.951 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:12:57,952: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2aefcf59-5d08-45b0-8cb0-51349329fc65] succeeded in 7.351059162989259s: None
[2026-05-26 13:13:49,510: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:13:50,379: INFO/MainProcess] Task triam.notifications.scan_due[bb264189-3ca5-4243-b999-376e56855228] received
2026-05-26 13:13:57.953 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:13:57,954: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[bb264189-3ca5-4243-b999-376e56855228] succeeded in 7.356695175985806s: None
[2026-05-26 13:14:49,511: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:14:50,183: INFO/MainProcess] Task triam.notifications.scan_due[1698bd2a-2651-4f6a-87b6-dfc7f70d28b0] received
2026-05-26 13:14:57.548 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:14:57,549: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1698bd2a-2651-4f6a-87b6-dfc7f70d28b0] succeeded in 7.364819190930575s: None
[2026-05-26 13:15:49,511: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:15:50,469: INFO/MainProcess] Task triam.notifications.scan_due[c269fa7a-4873-455f-8c4c-b25ae6580f74] received
2026-05-26 13:15:57.823 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:15:57,824: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c269fa7a-4873-455f-8c4c-b25ae6580f74] succeeded in 7.35368003800977s: None
[2026-05-26 13:16:49,512: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:16:50,278: INFO/MainProcess] Task triam.notifications.scan_due[62c72ad2-3676-4019-9212-b36bfc9e939e] received
2026-05-26 13:16:57.673 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:16:57,675: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[62c72ad2-3676-4019-9212-b36bfc9e939e] succeeded in 7.395883381948806s: None
[2026-05-26 13:17:49,515: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:17:50,516: INFO/MainProcess] Task triam.notifications.scan_due[53704bc8-b439-43b9-bb6b-aaae58d49bc9] received
2026-05-26 13:17:58.164 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:17:58,164: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[53704bc8-b439-43b9-bb6b-aaae58d49bc9] succeeded in 7.424902867991477s: None
[2026-05-26 13:18:49,516: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:18:50,387: INFO/MainProcess] Task triam.notifications.scan_due[0872210b-9d4b-4ddc-a0fb-af15d363cac4] received
2026-05-26 13:18:57.796 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:18:57,799: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[0872210b-9d4b-4ddc-a0fb-af15d363cac4] succeeded in 7.40954599599354s: None
2026-05-26 13:19:14.865 | INFO     | logging:callHandlers:1762 - 10.16.5.171:42594 - "GET /api/v1/books/a9453a82-6e22-42c7-bc4a-c8bd9125c422/processing-status HTTP/1.1" 200
2026-05-26 13:19:17.969 | INFO     | logging:callHandlers:1762 - 10.16.5.171:42594 - "GET /api/v1/books/a9453a82-6e22-42c7-bc4a-c8bd9125c422/details HTTP/1.1" 200
2026-05-26 13:19:22.722 | INFO     | logging:callHandlers:1762 - 10.16.5.171:42594 - "GET /api/v1/books/a9453a82-6e22-42c7-bc4a-c8bd9125c422/learning-progress?mode=pareto HTTP/1.1" 200
2026-05-26 13:19:46.350 | INFO     | logging:callHandlers:1762 - 10.16.17.88:37955 - "GET /api/v1/books/a9453a82-6e22-42c7-bc4a-c8bd9125c422/learning-progress?mode=pareto HTTP/1.1" 200
[2026-05-26 13:19:49,518: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:19:50,175: INFO/MainProcess] Task triam.notifications.scan_due[493616df-fa48-46e4-a2f3-2e5c33ad5461] received
2026-05-26 13:19:57.581 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:19:57,582: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[493616df-fa48-46e4-a2f3-2e5c33ad5461] succeeded in 7.401796672958881s: None
2026-05-26 13:20:04.005 | INFO     | logging:callHandlers:1762 - 10.16.5.171:27151 - "GET /api/v1/books/a9453a82-6e22-42c7-bc4a-c8bd9125c422/learning-progress?mode=pareto HTTP/1.1" 200
[2026-05-26 13:20:49,516: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:20:50,385: INFO/MainProcess] Task triam.notifications.scan_due[0d8113aa-8366-4c59-bfc8-29ee350d4b93] received
2026-05-26 13:20:57.785 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:20:57,786: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[0d8113aa-8366-4c59-bfc8-29ee350d4b93] succeeded in 7.397187571972609s: None
[2026-05-26 13:21:49,516: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:21:50,171: INFO/MainProcess] Task triam.notifications.scan_due[2b9ad8a3-6f31-48b2-9e58-e5b4fb495da5] received
2026-05-26 13:21:57.567 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:21:57,568: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2b9ad8a3-6f31-48b2-9e58-e5b4fb495da5] succeeded in 7.3939640478929505s: None
2026-05-26 13:22:47.712 | INFO     | logging:callHandlers:1762 - 10.16.25.130:49758 - "GET /api/v1/books/a9453a82-6e22-42c7-bc4a-c8bd9125c422/learning-progress?mode=pareto HTTP/1.1" 200
[2026-05-26 13:22:49,517: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:22:50,384: INFO/MainProcess] Task triam.notifications.scan_due[030e22f8-a925-42f0-965c-c8c771408fd5] received
2026-05-26 13:22:57.826 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:22:57,826: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[030e22f8-a925-42f0-965c-c8c771408fd5] succeeded in 7.441034896997735s: None
[2026-05-26 13:23:49,517: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:23:50,387: INFO/MainProcess] Task triam.notifications.scan_due[c98aa9ec-9eb7-461c-9efb-7ef49c55260d] received
2026-05-26 13:23:57.764 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:23:57,765: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c98aa9ec-9eb7-461c-9efb-7ef49c55260d] succeeded in 7.377213858067989s: None
[2026-05-26 13:24:49,517: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:24:50,171: INFO/MainProcess] Task triam.notifications.scan_due[4c6a023a-1b7f-497d-8a98-77ae9fa0cc5d] received
2026-05-26 13:24:57.536 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:24:57,537: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4c6a023a-1b7f-497d-8a98-77ae9fa0cc5d] succeeded in 7.3650136379292235s: None
[2026-05-26 13:25:49,517: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:25:50,383: INFO/MainProcess] Task triam.notifications.scan_due[6989a65c-3f81-4a05-ae6d-29a46b211df3] received
2026-05-26 13:25:57.783 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:25:57,784: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[6989a65c-3f81-4a05-ae6d-29a46b211df3] succeeded in 7.39820543397218s: None
[2026-05-26 13:26:49,518: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:26:50,169: INFO/MainProcess] Task triam.notifications.scan_due[3aaecab0-f4cf-4ad4-b0ff-6429a366f996] received
2026-05-26 13:26:57.556 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:26:57,557: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3aaecab0-f4cf-4ad4-b0ff-6429a366f996] succeeded in 7.386332824011333s: None
[2026-05-26 13:27:49,519: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:27:50,389: INFO/MainProcess] Task triam.notifications.scan_due[61f97d13-7c26-4722-844f-7a8e92d9e11c] received
2026-05-26 13:27:57.780 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:27:57,780: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[61f97d13-7c26-4722-844f-7a8e92d9e11c] succeeded in 7.3891925669740885s: None
2026-05-26 13:28:23.077 | INFO     | logging:callHandlers:1762 - 10.16.17.88:1114 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 401
2026-05-26 13:28:24.232 | INFO     | logging:callHandlers:1762 - 10.16.25.130:6769 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 401
[2026-05-26 13:28:49,519: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:28:50,390: INFO/MainProcess] Task triam.notifications.scan_due[e1e78a73-6fe6-41c4-8964-d153d19d149e] received
2026-05-26 13:28:57.782 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:28:57,783: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e1e78a73-6fe6-41c4-8964-d153d19d149e] succeeded in 7.3894757479429245s: None
[2026-05-26 13:29:49,521: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:29:50,177: INFO/MainProcess] Task triam.notifications.scan_due[810d911f-8fde-4a33-9fb0-570935952b29] received
2026-05-26 13:29:57.582 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:29:57,583: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[810d911f-8fde-4a33-9fb0-570935952b29] succeeded in 7.402942453976721s: None
[2026-05-26 13:30:49,523: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:30:50,383: INFO/MainProcess] Task triam.notifications.scan_due[d550b621-d8e7-4f28-adab-d110d4ecb3e9] received
2026-05-26 13:30:58.002 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:30:58,003: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d550b621-d8e7-4f28-adab-d110d4ecb3e9] succeeded in 7.399284646962769s: None
2026-05-26 13:31:47.929 | INFO     | logging:callHandlers:1762 - 10.16.46.186:41510 - "GET /api/v1/health HTTP/1.1" 200
[2026-05-26 13:31:49,522: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:31:50,168: INFO/MainProcess] Task triam.notifications.scan_due[384218b2-565d-4876-bcc4-bada0321d201] received
2026-05-26 13:31:50.427 | INFO     | logging:callHandlers:1762 - 10.16.17.88:4738 - "GET /api/v1/books HTTP/1.1" 200
2026-05-26 13:31:54.270 | INFO     | logging:callHandlers:1762 - 10.16.5.171:17580 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 13:31:57.711 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:31:57,712: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[384218b2-565d-4876-bcc4-bada0321d201] succeeded in 7.541155082988553s: None
[2026-05-26 13:32:49,540: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:32:50,400: INFO/MainProcess] Task triam.notifications.scan_due[bd1b1a83-7665-419f-8457-2309d538cf9e] received
2026-05-26 13:32:58.124 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:32:58,125: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[bd1b1a83-7665-419f-8457-2309d538cf9e] succeeded in 7.510688024922274s: None
[2026-05-26 13:33:49,541: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:33:50,402: INFO/MainProcess] Task triam.notifications.scan_due[c1f1acc2-abaf-45b6-a4e4-1c01f948d8e9] received
2026-05-26 13:33:58.003 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:33:58,005: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c1f1acc2-abaf-45b6-a4e4-1c01f948d8e9] succeeded in 7.388712621992454s: None
[2026-05-26 13:34:49,543: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:34:50,187: INFO/MainProcess] Task triam.notifications.scan_due[0cc0501c-cad6-4b37-8785-1977a1da4f5e] received
2026-05-26 13:34:57.785 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:34:57,787: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[0cc0501c-cad6-4b37-8785-1977a1da4f5e] succeeded in 7.387072687968612s: None
[2026-05-26 13:35:49,543: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:35:50,596: INFO/MainProcess] Task triam.notifications.scan_due[39b4ce44-3125-4057-b11e-8ca255e3197d] received
2026-05-26 13:35:57.996 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:35:57,998: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[39b4ce44-3125-4057-b11e-8ca255e3197d] succeeded in 7.39947373198811s: None
[2026-05-26 13:36:49,543: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:36:50,190: INFO/MainProcess] Task triam.notifications.scan_due[f651a9f2-8417-4053-b1da-16d65171df33] received
2026-05-26 13:36:57.568 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:36:57,569: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f651a9f2-8417-4053-b1da-16d65171df33] succeeded in 7.378243271028623s: None
[2026-05-26 13:37:49,543: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:37:50,403: INFO/MainProcess] Task triam.notifications.scan_due[3bb0fd48-acf7-4de4-880f-a6d08c5b73e3] received
2026-05-26 13:37:57.806 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:37:57,808: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3bb0fd48-acf7-4de4-880f-a6d08c5b73e3] succeeded in 7.402825741097331s: None
[2026-05-26 13:38:49,545: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:38:50,422: INFO/MainProcess] Task triam.notifications.scan_due[4c9d110f-969c-4647-88d7-5a5c14116733] received
2026-05-26 13:38:57.833 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:38:57,834: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4c9d110f-969c-4647-88d7-5a5c14116733] succeeded in 7.410989166004583s: None
[2026-05-26 13:39:49,545: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:39:50,416: INFO/MainProcess] Task triam.notifications.scan_due[8eced009-41f9-408f-864d-544e4b0c5fd8] received
2026-05-26 13:39:57.803 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:39:57,804: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8eced009-41f9-408f-864d-544e4b0c5fd8] succeeded in 7.386035869014449s: None
[2026-05-26 13:40:49,545: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:40:50,417: INFO/MainProcess] Task triam.notifications.scan_due[81599db5-938f-4487-9e9e-887c5d1a577c] received
2026-05-26 13:40:59.190 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:40:59,191: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[81599db5-938f-4487-9e9e-887c5d1a577c] succeeded in 8.770726443035528s: None
[2026-05-26 13:41:49,545: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:41:50,205: INFO/MainProcess] Task triam.notifications.scan_due[fca13500-6c3a-4d36-b13a-3167d5bbf507] received
2026-05-26 13:41:57.742 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:41:57,744: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[fca13500-6c3a-4d36-b13a-3167d5bbf507] succeeded in 7.534258660976775s: None
[2026-05-26 13:42:49,547: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:42:50,418: INFO/MainProcess] Task triam.notifications.scan_due[0b01f782-0bdb-4dcc-ba7e-54ce6e2be578] received
2026-05-26 13:42:57.796 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:42:57,799: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[0b01f782-0bdb-4dcc-ba7e-54ce6e2be578] succeeded in 7.376219591940753s: None
[2026-05-26 13:43:49,547: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:43:50,419: INFO/MainProcess] Task triam.notifications.scan_due[d00a9e27-1a9d-4c09-aea8-d9ead126921d] received
2026-05-26 13:43:57.818 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:43:57,824: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d00a9e27-1a9d-4c09-aea8-d9ead126921d] succeeded in 7.404063623049296s: None
[2026-05-26 13:44:49,547: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:44:50,421: INFO/MainProcess] Task triam.notifications.scan_due[549e3e51-0e71-47f8-a1a8-093f22c7a3da] received
2026-05-26 13:44:58.124 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:44:58,126: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[549e3e51-0e71-47f8-a1a8-093f22c7a3da] succeeded in 7.702750870957971s: None
[2026-05-26 13:45:49,553: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:45:50,428: INFO/MainProcess] Task triam.notifications.scan_due[ed600320-b33c-400a-bdb2-4c732455a1ab] received
2026-05-26 13:45:58.127 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:45:58,128: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ed600320-b33c-400a-bdb2-4c732455a1ab] succeeded in 7.696584296994843s: None
[2026-05-26 13:46:49,553: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:46:50,211: INFO/MainProcess] Task triam.notifications.scan_due[8b76a58f-0535-4dbd-bfd4-836e1257e7ba] received
2026-05-26 13:46:57.896 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:46:57,900: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8b76a58f-0535-4dbd-bfd4-836e1257e7ba] succeeded in 7.687136917957105s: None
[2026-05-26 13:47:49,554: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:47:50,436: INFO/MainProcess] Task triam.notifications.scan_due[a33c2f75-5537-4c7b-81a6-8e98d6925b38] received
2026-05-26 13:47:58.345 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:47:58,346: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a33c2f75-5537-4c7b-81a6-8e98d6925b38] succeeded in 7.694723671069369s: None
[2026-05-26 13:48:49,554: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:48:50,424: INFO/MainProcess] Task triam.notifications.scan_due[d15ad92f-e4ef-4d7a-a7c8-ca40206ca74d] received
2026-05-26 13:48:58.317 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:48:58,318: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d15ad92f-e4ef-4d7a-a7c8-ca40206ca74d] succeeded in 7.6822140630101785s: None
[2026-05-26 13:49:49,555: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:49:50,424: INFO/MainProcess] Task triam.notifications.scan_due[636440df-f702-42d8-8693-cc99b15b48b9] received
2026-05-26 13:49:58.328 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:49:58,330: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[636440df-f702-42d8-8693-cc99b15b48b9] succeeded in 7.692686562077142s: None
2026-05-26 13:50:33.817 | INFO     | logging:callHandlers:1762 - 10.16.17.88:44904 - "GET /api/v1/health HTTP/1.1" 200
2026-05-26 13:50:38.286 | INFO     | logging:callHandlers:1762 - 10.16.46.186:6779 - "GET /api/v1/books HTTP/1.1" 200
2026-05-26 13:50:43.354 | INFO     | logging:callHandlers:1762 - 10.16.17.88:17225 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
[2026-05-26 13:50:49,555: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:50:50,427: INFO/MainProcess] Task triam.notifications.scan_due[be11f7e8-2993-4375-af83-fa8b99c7d40a] received
2026-05-26 13:50:58.120 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:50:58,124: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[be11f7e8-2993-4375-af83-fa8b99c7d40a] succeeded in 7.696134926052764s: None
[2026-05-26 13:51:49,557: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:51:50,210: INFO/MainProcess] Task triam.notifications.scan_due[c74c30a2-17a7-4726-aa03-01d332507fcf] received
2026-05-26 13:51:57.906 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:51:57,907: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c74c30a2-17a7-4726-aa03-01d332507fcf] succeeded in 7.694315399043262s: None
[2026-05-26 13:52:49,557: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:52:50,425: INFO/MainProcess] Task triam.notifications.scan_due[42ba0e63-12c5-47f7-a6d0-cef34562da7e] received
2026-05-26 13:52:58.324 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:52:58,324: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[42ba0e63-12c5-47f7-a6d0-cef34562da7e] succeeded in 7.686805866891518s: None
[2026-05-26 13:53:49,558: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:53:50,426: INFO/MainProcess] Task triam.notifications.scan_due[e427dba3-2e3c-4771-b69f-9bc9f4c8feb9] received
2026-05-26 13:53:58.337 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:53:58,340: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e427dba3-2e3c-4771-b69f-9bc9f4c8feb9] succeeded in 7.7013784979935735s: None
[2026-05-26 13:54:49,559: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:54:50,429: INFO/MainProcess] Task triam.notifications.scan_due[17e23af2-5167-45fe-afbc-7a04b373774f] received
2026-05-26 13:54:58.377 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:54:58,378: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[17e23af2-5167-45fe-afbc-7a04b373774f] succeeded in 7.734267416992225s: None
[2026-05-26 13:55:49,560: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:55:50,430: INFO/MainProcess] Task triam.notifications.scan_due[223fb891-95c9-471b-9291-0c9af62a1cb2] received
2026-05-26 13:55:58.334 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:55:58,337: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[223fb891-95c9-471b-9291-0c9af62a1cb2] succeeded in 7.6894465199438855s: None
[2026-05-26 13:56:49,561: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:56:50,214: INFO/MainProcess] Task triam.notifications.scan_due[2a9e5abd-3901-4a17-81fd-09d163f0e8ca] received
2026-05-26 13:56:57.911 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:56:57,914: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2a9e5abd-3901-4a17-81fd-09d163f0e8ca] succeeded in 7.697633103001863s: None
[2026-05-26 13:57:49,560: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:57:50,432: INFO/MainProcess] Task triam.notifications.scan_due[d5f8a377-2392-4bca-89b3-147402be9de8] received
2026-05-26 13:57:58.328 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:57:58,330: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d5f8a377-2392-4bca-89b3-147402be9de8] succeeded in 7.682437523966655s: None
[2026-05-26 13:58:49,561: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:58:50,216: INFO/MainProcess] Task triam.notifications.scan_due[80155cd5-0472-41dd-b436-682269f62ccb] received
2026-05-26 13:58:58.116 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:58:58,117: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[80155cd5-0472-41dd-b436-682269f62ccb] succeeded in 7.687422760063782s: None
[2026-05-26 13:59:49,561: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 13:59:50,622: INFO/MainProcess] Task triam.notifications.scan_due[93fb0fa7-eba1-43f5-aa9b-17a874d18c10] received
2026-05-26 13:59:58.315 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 13:59:58,316: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[93fb0fa7-eba1-43f5-aa9b-17a874d18c10] succeeded in 7.686567886965349s: None
[2026-05-26 14:00:49,563: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:00:50,434: INFO/MainProcess] Task triam.notifications.scan_due[b1f03646-451c-42fc-a895-a9214f99ec49] received
2026-05-26 14:00:58.159 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:00:58,161: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b1f03646-451c-42fc-a895-a9214f99ec49] succeeded in 7.721405986929312s: None
[2026-05-26 14:01:49,564: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:01:50,214: INFO/MainProcess] Task triam.notifications.scan_due[6bef45a1-bcb5-4a71-98ad-c76831edd7f0] received
2026-05-26 14:01:57.905 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:01:57,906: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[6bef45a1-bcb5-4a71-98ad-c76831edd7f0] succeeded in 7.690114865079522s: None
[2026-05-26 14:02:49,564: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:02:50,434: INFO/MainProcess] Task triam.notifications.scan_due[e5ea3e50-783c-4e60-8055-4b441c51b572] received
2026-05-26 14:02:58.132 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:02:58,133: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e5ea3e50-783c-4e60-8055-4b441c51b572] succeeded in 7.696667405078188s: None
[2026-05-26 14:03:49,564: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:03:50,219: INFO/MainProcess] Task triam.notifications.scan_due[8db45ea2-6563-4c8c-b09b-132dd1a12dc8] received
2026-05-26 14:03:57.934 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:03:57,936: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8db45ea2-6563-4c8c-b09b-132dd1a12dc8] succeeded in 7.71441978495568s: None
[2026-05-26 14:04:49,565: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:04:50,437: INFO/MainProcess] Task triam.notifications.scan_due[f15e65d6-1951-4258-9030-44b91a3deb8d] received
2026-05-26 14:04:58.128 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:04:58,129: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f15e65d6-1951-4258-9030-44b91a3deb8d] succeeded in 7.690040969988331s: None
[2026-05-26 14:05:49,565: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:05:50,435: INFO/MainProcess] Task triam.notifications.scan_due[4bdd76bd-ef5c-4841-9bd6-3942d402df5c] received
2026-05-26 14:05:58.125 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:05:58,128: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4bdd76bd-ef5c-4841-9bd6-3942d402df5c] succeeded in 7.691502621979453s: None
2026-05-26 14:06:26.627 | INFO     | logging:callHandlers:1762 - 10.16.25.130:46160 - "GET /api/v1/study-contexts HTTP/1.1" 200
[2026-05-26 14:06:49,565: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:06:50,220: INFO/MainProcess] Task triam.notifications.scan_due[1c168aba-c0e4-4b8e-8604-a6be8c206975] received
2026-05-26 14:06:57.910 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:06:57,911: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1c168aba-c0e4-4b8e-8604-a6be8c206975] succeeded in 7.688202842022292s: None
[2026-05-26 14:07:49,565: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:07:50,435: INFO/MainProcess] Task triam.notifications.scan_due[5a0b5d7a-9b88-4274-9a6d-991a345c2e9b] received
2026-05-26 14:07:58.140 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:07:58,140: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5a0b5d7a-9b88-4274-9a6d-991a345c2e9b] succeeded in 7.703256967943162s: None
[2026-05-26 14:08:49,565: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:08:50,218: INFO/MainProcess] Task triam.notifications.scan_due[8530b1fa-02e6-4ea7-9300-f97c45da67f4] received
2026-05-26 14:08:57.921 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:08:57,922: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8530b1fa-02e6-4ea7-9300-f97c45da67f4] succeeded in 7.701752649969421s: None
[2026-05-26 14:09:49,567: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:09:50,440: INFO/MainProcess] Task triam.notifications.scan_due[b1a5e8ce-7df1-455b-919b-c3a63e7e0795] received
2026-05-26 14:09:58.151 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:09:58,152: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b1a5e8ce-7df1-455b-919b-c3a63e7e0795] succeeded in 7.709880898008123s: None
[2026-05-26 14:10:49,567: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:10:50,435: INFO/MainProcess] Task triam.notifications.scan_due[440d231f-6b5e-403b-b478-0102b5c402d6] received
2026-05-26 14:10:59.222 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:10:59,223: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[440d231f-6b5e-403b-b478-0102b5c402d6] succeeded in 8.573310988023877s: None
[2026-05-26 14:11:49,568: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:11:50,222: INFO/MainProcess] Task triam.notifications.scan_due[e2f67271-408a-43ee-857a-38135f451919] received
2026-05-26 14:11:57.442 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:11:57,444: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e2f67271-408a-43ee-857a-38135f451919] succeeded in 7.217698102002032s: None
[2026-05-26 14:12:49,569: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:12:50,438: INFO/MainProcess] Task triam.notifications.scan_due[3d51e13e-70e1-4149-8fb9-58bdd17521f8] received
2026-05-26 14:12:57.931 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:12:57,935: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3d51e13e-70e1-4149-8fb9-58bdd17521f8] succeeded in 7.282313463045284s: None
[2026-05-26 14:13:49,569: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:13:50,278: INFO/MainProcess] Task triam.notifications.scan_due[f1cb38d3-17c2-43fc-a611-7ee0255f90e9] received
2026-05-26 14:13:57.475 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:13:57,477: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f1cb38d3-17c2-43fc-a611-7ee0255f90e9] succeeded in 7.198129934957251s: None
[2026-05-26 14:14:49,569: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:14:50,437: INFO/MainProcess] Task triam.notifications.scan_due[0255b98f-b31a-4e28-8312-887054a9cbbd] received
2026-05-26 14:14:57.850 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:14:57,851: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[0255b98f-b31a-4e28-8312-887054a9cbbd] succeeded in 7.201258028042503s: None
[2026-05-26 14:15:49,569: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:15:50,436: INFO/MainProcess] Task triam.notifications.scan_due[bd12ca0d-55c5-4b3e-b8d4-d21015cdf096] received
2026-05-26 14:15:57.864 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:15:57,865: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[bd12ca0d-55c5-4b3e-b8d4-d21015cdf096] succeeded in 7.21546772995498s: None
2026-05-26 14:16:45.947 | INFO     | logging:callHandlers:1762 - 10.16.25.130:26719 - "GET /api/v1/books/a9453a82-6e22-42c7-bc4a-c8bd9125c422 HTTP/1.1" 200
[2026-05-26 14:16:49,569: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:16:50,438: INFO/MainProcess] Task triam.notifications.scan_due[8eb2ed99-98be-4857-bb1e-f7a3d78356d4] received
2026-05-26 14:16:57.869 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:16:57,870: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8eb2ed99-98be-4857-bb1e-f7a3d78356d4] succeeded in 7.219441259978339s: None
[2026-05-26 14:17:49,569: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:17:50,438: INFO/MainProcess] Task triam.notifications.scan_due[ca3c4f00-044d-4b2e-bb28-23bbad4417df] received
2026-05-26 14:17:59.384 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:17:59,385: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ca3c4f00-044d-4b2e-bb28-23bbad4417df] succeeded in 8.734629945014603s: None
[2026-05-26 14:18:49,570: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:18:50,222: INFO/MainProcess] Task triam.notifications.scan_due[8fb53140-f3c4-46f7-a081-18a4d7ce1002] received
2026-05-26 14:18:57.636 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:18:57,637: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8fb53140-f3c4-46f7-a081-18a4d7ce1002] succeeded in 7.412211283924989s: None
[2026-05-26 14:19:49,570: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:19:50,443: INFO/MainProcess] Task triam.notifications.scan_due[067db63b-3dad-49f0-bc6c-7da2766ea99f] received
2026-05-26 14:19:57.860 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:19:57,861: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[067db63b-3dad-49f0-bc6c-7da2766ea99f] succeeded in 7.205409962916747s: None
[2026-05-26 14:20:49,574: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:20:50,448: INFO/MainProcess] Task triam.notifications.scan_due[1b12689d-d9f9-4a09-a0d4-52fb7f6338a8] received
2026-05-26 14:20:57.865 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:20:57,866: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1b12689d-d9f9-4a09-a0d4-52fb7f6338a8] succeeded in 7.205304262926802s: None
2026-05-26 14:21:20.710 | INFO     | logging:callHandlers:1762 - 10.16.46.186:47121 - "GET /api/v1/health HTTP/1.1" 200
2026-05-26 14:21:24.893 | INFO     | logging:callHandlers:1762 - 10.16.46.186:47121 - "GET /api/v1/books HTTP/1.1" 200
2026-05-26 14:21:29.969 | INFO     | logging:callHandlers:1762 - 10.16.17.88:6575 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 14:21:47.552 | INFO     | logging:callHandlers:1762 - 10.16.46.186:6744 - "GET /api/v1/study-contexts HTTP/1.1" 200
[2026-05-26 14:21:49,574: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:21:50,447: INFO/MainProcess] Task triam.notifications.scan_due[3824b6ec-fe94-40ca-9388-af39b4dd6df3] received
2026-05-26 14:21:51.886 | INFO     | logging:callHandlers:1762 - 10.16.17.88:27985 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/details HTTP/1.1" 200
2026-05-26 14:21:56.219 | INFO     | logging:callHandlers:1762 - 10.16.5.171:30650 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-26 14:21:57.977 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:21:57,980: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3824b6ec-fe94-40ca-9388-af39b4dd6df3] succeeded in 7.318101948010735s: None
2026-05-26 14:22:08.969 | INFO     | logging:callHandlers:1762 - 10.16.46.186:20179 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/ae4c9c22-c00d-4f4a-93cf-81146ef32cbf/progress HTTP/1.1" 422
2026-05-26 14:22:23.813 | INFO     | logging:callHandlers:1762 - 10.16.5.171:6541 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/ae4c9c22-c00d-4f4a-93cf-81146ef32cbf/progress HTTP/1.1" 422
2026-05-26 14:22:25.726 | INFO     | logging:callHandlers:1762 - 10.16.25.130:48563 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/ae4c9c22-c00d-4f4a-93cf-81146ef32cbf/progress HTTP/1.1" 422
2026-05-26 14:22:41.106 | INFO     | logging:callHandlers:1762 - 10.16.46.186:46865 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/ae4c9c22-c00d-4f4a-93cf-81146ef32cbf/progress HTTP/1.1" 422
2026-05-26 14:22:42.240 | INFO     | logging:callHandlers:1762 - 10.16.25.130:17709 - "GET /api/v1/books/a9453a82-6e22-42c7-bc4a-c8bd9125c422/details HTTP/1.1" 200
2026-05-26 14:22:44.980 | INFO     | logging:callHandlers:1762 - 10.16.17.88:3399 - "PUT /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/chapters/ae4c9c22-c00d-4f4a-93cf-81146ef32cbf/progress HTTP/1.1" 422
[2026-05-26 14:22:49,574: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:22:50,451: INFO/MainProcess] Task triam.notifications.scan_due[42c7d1b8-7c5a-4473-ba39-91459be587d4] received
2026-05-26 14:22:57.313 | INFO     | logging:callHandlers:1762 - 10.16.5.171:3685 - "GET /api/v1/books/a9453a82-6e22-42c7-bc4a-c8bd9125c422/content HTTP/1.1" 404
2026-05-26 14:22:57.865 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:22:57,866: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[42c7d1b8-7c5a-4473-ba39-91459be587d4] succeeded in 7.201448632054962s: None
2026-05-26 14:23:00.365 | INFO     | logging:callHandlers:1762 - 10.16.5.171:4270 - "GET /api/v1/books/a9453a82-6e22-42c7-bc4a-c8bd9125c422/content HTTP/1.1" 404
[2026-05-26 14:23:49,575: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:23:50,235: INFO/MainProcess] Task triam.notifications.scan_due[730e2237-e971-4032-aa85-79bcf0cf5a14] received
2026-05-26 14:23:57.539 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:23:57,539: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[730e2237-e971-4032-aa85-79bcf0cf5a14] succeeded in 7.302515876945108s: None
[2026-05-26 14:24:49,575: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:24:50,453: INFO/MainProcess] Task triam.notifications.scan_due[5fac8b71-e006-48fe-9a29-588e8673886d] received
2026-05-26 14:24:57.730 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:24:57,731: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5fac8b71-e006-48fe-9a29-588e8673886d] succeeded in 7.276188210002147s: None
2026-05-26 14:25:28.602 | WARNING  | app.main:app_exception_handler:36 - AppException: PDF không có bookmark/outline ẩn. Vui lòng upload PDF có mục lục chuẩn. - Status Code: 422
2026-05-26 14:25:28.604 | INFO     | logging:callHandlers:1762 - 10.16.17.88:34449 - "POST /api/v1/upload HTTP/1.1" 422
2026-05-26 14:25:31.315 | INFO     | logging:callHandlers:1762 - 10.16.17.88:34449 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 14:25:37.117 | INFO     | logging:callHandlers:1762 - 10.16.17.88:35827 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
[2026-05-26 14:25:49,576: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:25:50,456: INFO/MainProcess] Task triam.notifications.scan_due[e8252b81-ddde-4048-a63d-f81c2e895c55] received
2026-05-26 14:25:57.660 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:25:57,660: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e8252b81-ddde-4048-a63d-f81c2e895c55] succeeded in 7.2037868309998885s: None
2026-05-26 14:26:06.939 | INFO     | logging:callHandlers:1762 - 10.16.46.186:7705 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
[2026-05-26 14:26:49,576: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:26:50,448: INFO/MainProcess] Task triam.notifications.scan_due[b7e2f328-2cad-42d3-b018-817a6e53c300] received
2026-05-26 14:26:57.659 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:26:57,660: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b7e2f328-2cad-42d3-b018-817a6e53c300] succeeded in 7.20943808008451s: None
2026-05-26 14:27:07.913 | INFO     | logging:callHandlers:1762 - 10.16.17.88:39703 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 14:27:40.717 | INFO     | app.services.upload_service:handle_upload_document:108 - ☁️  DOCX uploaded to Storage: 4ef0ad48-0e8f-457d-b278-3d3fe3da0905/original.docx
[2026-05-26 14:27:49,577: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:27:50,455: INFO/MainProcess] Task triam.notifications.scan_due[9b0db05b-b705-489e-b6c2-ad55f6903c28] received
2026-05-26 14:27:57.919 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:27:57,919: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[9b0db05b-b705-489e-b6c2-ad55f6903c28] succeeded in 7.251293933950365s: None
[2026-05-26 14:28:49,578: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:28:50,235: INFO/MainProcess] Task triam.notifications.scan_due[274a7811-dcc4-4c7a-9819-aa04699caaa3] received
2026-05-26 14:28:57.644 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:28:57,645: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[274a7811-dcc4-4c7a-9819-aa04699caaa3] succeeded in 7.19800839596428s: None
2026-05-26 14:29:04.184 | INFO     | app.services.upload_service:handle_upload_document:139 - 📘 Created DRAFT book 4ef0ad48-0e8f-457d-b278-3d3fe3da0905 | 93 chapters | file_url saved
2026-05-26 14:29:04.193 | INFO     | logging:callHandlers:1762 - 10.16.17.88:53138 - "POST /api/v1/upload HTTP/1.1" 200
2026-05-26 14:29:24.980 | INFO     | logging:callHandlers:1762 - 10.16.17.88:31222 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
[2026-05-26 14:29:49,579: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:29:50,658: INFO/MainProcess] Task triam.notifications.scan_due[f45bf9ce-4220-4af7-80ec-5e75ae33ef68] received
2026-05-26 14:29:56.897 | INFO     | logging:callHandlers:1762 - 10.16.17.88:60668 - "GET /api/v1/notifications/settings HTTP/1.1" 200
2026-05-26 14:29:57.845 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:29:57,846: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f45bf9ce-4220-4af7-80ec-5e75ae33ef68] succeeded in 7.185965579003096s: None
2026-05-26 14:30:05.289 | INFO     | app.services.upload_service:handle_generate_plan:213 - 📋 ReadingPlan created for book 4ef0ad48-0e8f-457d-b278-3d3fe3da0905 | mode=full | job=541e7dc7-79d0-43c7-99c4-59c1bb1b354e
2026-05-26 14:30:05.726 | INFO     | logging:callHandlers:1762 - 10.16.17.88:18436 - "POST /api/v1/generate-plan HTTP/1.1" 200
[2026-05-26 14:30:06,153: INFO/MainProcess] Task triam.books.process[0ae58bba-c2fe-4d4b-829b-fe77c8aeadb6] received
2026-05-26 14:30:06.160 | INFO     | app.tasks.book_tasks:process_book_task:23 - Celery process_book_task started | book_id=4ef0ad48-0e8f-457d-b278-3d3fe3da0905 | mode=full | job_id=541e7dc7-79d0-43c7-99c4-59c1bb1b354e
2026-05-26 14:30:08.140 | INFO     | logging:callHandlers:1762 - 10.16.5.171:55440 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 14:30:09.769 | INFO     | logging:callHandlers:1762 - 10.16.25.130:3249 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:30:09.883 | INFO     | app.services.workers.book_pipeline:run_background_processing:306 - ⬇️  Downloading DOCX from Storage: 4ef0ad48-0e8f-457d-b278-3d3fe3da0905/original.docx
2026-05-26 14:30:13.752 | INFO     | logging:callHandlers:1762 - 10.16.17.88:44020 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:30:17.774 | INFO     | logging:callHandlers:1762 - 10.16.25.130:63199 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:30:21.839 | INFO     | logging:callHandlers:1762 - 10.16.5.171:48811 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:30:22.393 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=1 | mode=full | title=Khái niệm mệnh đề và chân trị | chars=1198 | estimated_tokens=610 | estimated_audio_seconds=133
2026-05-26 14:30:24.699 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=1 | mode=full | rag=true | tts=true
2026-05-26 14:30:24.710 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=1 | mode=full | title=Khái niệm mệnh đề và chân trị | raw_chars=1198
2026-05-26 14:30:24.712 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Khái niệm mệnh đề và chân trị | chars=1198 | estimated_tokens=610 | estimated_audio_seconds=133
2026-05-26 14:30:24.714 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Khái niệm mệnh đề và chân trị
2026-05-26 14:30:24.716 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1198
2026-05-26 14:30:26.367 | INFO     | logging:callHandlers:1762 - 10.16.46.186:56346 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:30:27.300 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=c0085c32-0274-4444-b2cc-f7eafe1f4d09
2026-05-26 14:30:30.538 | INFO     | logging:callHandlers:1762 - 10.16.46.186:2150 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:30:34.984 | INFO     | logging:callHandlers:1762 - 10.16.5.171:21692 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:30:39.066 | INFO     | logging:callHandlers:1762 - 10.16.25.130:38344 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:30:42.142 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=7 | review_chars=715
2026-05-26 14:30:42.142 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=1 | mode=full | main_scripts=7 | review_chars=715
2026-05-26 14:30:42.143 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=1 | mode=full | total_scripts=7
2026-05-26 14:30:42.144 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=1/7 | chars=349
2026-05-26 14:30:43.161 | INFO     | logging:callHandlers:1762 - 10.16.17.88:25872 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:30:47.238 | INFO     | logging:callHandlers:1762 - 10.16.17.88:58493 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
[2026-05-26 14:30:49,579: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:30:50,527: INFO/MainProcess] Task triam.notifications.scan_due[dc4ec866-e489-4784-b59e-ec2d222fec21] received
2026-05-26 14:30:51.223 | INFO     | logging:callHandlers:1762 - 10.16.17.88:27909 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:30:53.012 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=1/7 | duration_ms=20376
2026-05-26 14:30:53.013 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=2/7 | chars=238
2026-05-26 14:30:55.234 | INFO     | logging:callHandlers:1762 - 10.16.25.130:46015 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:30:57.734 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:30:57,734: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[dc4ec866-e489-4784-b59e-ec2d222fec21] succeeded in 7.204821845982224s: None
2026-05-26 14:30:59.347 | INFO     | logging:callHandlers:1762 - 10.16.25.130:62607 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:31:01.975 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=2/7 | duration_ms=14688
2026-05-26 14:31:01.976 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=3/7 | chars=268
2026-05-26 14:31:02.712 | INFO     | logging:callHandlers:1762 - 10.16.46.186:49576 - "GET /api/v1/books/4ef0ad48-0e8f-457d-b278-3d3fe3da0905/details HTTP/1.1" 200
2026-05-26 14:31:03.391 | INFO     | logging:callHandlers:1762 - 10.16.17.88:30572 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:31:07.438 | INFO     | logging:callHandlers:1762 - 10.16.17.88:12211 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:31:11.516 | INFO     | logging:callHandlers:1762 - 10.16.17.88:38756 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:31:14.272 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=3/7 | duration_ms=16968
2026-05-26 14:31:14.274 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=4/7 | chars=224
2026-05-26 14:31:15.601 | INFO     | logging:callHandlers:1762 - 10.16.17.88:25204 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:31:19.590 | INFO     | logging:callHandlers:1762 - 10.16.46.186:63120 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:31:23.702 | INFO     | logging:callHandlers:1762 - 10.16.17.88:1746 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:31:27.335 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=4/7 | duration_ms=14832
2026-05-26 14:31:27.337 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=5/7 | chars=299
2026-05-26 14:31:28.206 | INFO     | logging:callHandlers:1762 - 10.16.25.130:13670 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:31:32.268 | INFO     | logging:callHandlers:1762 - 10.16.25.130:48830 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:31:35.559 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=5/7 | duration_ms=18120
2026-05-26 14:31:35.564 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=6/7 | chars=259
2026-05-26 14:31:36.270 | INFO     | logging:callHandlers:1762 - 10.16.25.130:40319 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:31:40.273 | INFO     | logging:callHandlers:1762 - 10.16.25.130:49665 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:31:44.290 | INFO     | logging:callHandlers:1762 - 10.16.25.130:29200 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:31:44.589 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=6/7 | duration_ms=16512
2026-05-26 14:31:44.593 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=1 | mode=full | segment=7/7 | chars=326
2026-05-26 14:31:48.441 | INFO     | logging:callHandlers:1762 - 10.16.5.171:29499 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
[2026-05-26 14:31:49,579: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:31:50,461: INFO/MainProcess] Task triam.notifications.scan_due[660aca1b-1a45-49f8-8b7d-a6e404684ce4] received
2026-05-26 14:31:52.455 | INFO     | logging:callHandlers:1762 - 10.16.46.186:25997 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:31:52.547 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=1 | mode=full | segment=7/7 | duration_ms=22320
2026-05-26 14:31:52.547 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=1 | mode=full | created_segments=7/7
2026-05-26 14:31:52.548 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=1 | mode=full | chars=715
2026-05-26 14:31:56.475 | INFO     | logging:callHandlers:1762 - 10.16.17.88:27364 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:31:57.662 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:31:57,662: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[660aca1b-1a45-49f8-8b7d-a6e404684ce4] succeeded in 7.199795946013182s: None
2026-05-26 14:32:00.599 | INFO     | logging:callHandlers:1762 - 10.16.25.130:15816 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:32:04.651 | INFO     | logging:callHandlers:1762 - 10.16.5.171:24204 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:32:08.876 | INFO     | logging:callHandlers:1762 - 10.16.46.186:18028 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:32:12.962 | INFO     | logging:callHandlers:1762 - 10.16.46.186:31025 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:32:13.468 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=1 | mode=full
2026-05-26 14:32:13.469 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=c0085c32-0274-4444-b2cc-f7eafe1f4d09 | mode=full | segments=7 | review_audio=True
2026-05-26 14:32:16.788 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=c0085c32-0274-4444-b2cc-f7eafe1f4d09 | mode=full
2026-05-26 14:32:17.200 | INFO     | logging:callHandlers:1762 - 10.16.25.130:16725 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:32:19.443 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 1 READY | mode=full | segments=7
2026-05-26 14:32:21.242 | INFO     | logging:callHandlers:1762 - 10.16.46.186:37451 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:32:22.687 | INFO     | app.services.workers.book_pipeline:_create_first_playable_notification_safely:123 - Content-ready first-playable event | book_id=4ef0ad48-0e8f-457d-b278-3d3fe3da0905 | mode=full | created=False
2026-05-26 14:32:22.921 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=2 | mode=full | title=Phân loại | chars=642 | estimated_tokens=309 | estimated_audio_seconds=66
2026-05-26 14:32:25.254 | INFO     | logging:callHandlers:1762 - 10.16.5.171:54602 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:32:25.261 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=2 | mode=full | rag=true | tts=true
2026-05-26 14:32:25.262 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=3 | mode=full | title=Các phép toán mệnh đề | chars=1562 | estimated_tokens=800 | estimated_audio_seconds=169
2026-05-26 14:32:27.549 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=3 | mode=full | rag=true | tts=true
2026-05-26 14:32:27.561 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=2 | mode=full | title=Phân loại | raw_chars=642
2026-05-26 14:32:27.568 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Phân loại | chars=642 | estimated_tokens=309 | estimated_audio_seconds=66
2026-05-26 14:32:27.570 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Phân loại
2026-05-26 14:32:27.571 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=642
2026-05-26 14:32:27.581 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=3 | mode=full | title=Các phép toán mệnh đề | raw_chars=1562
2026-05-26 14:32:27.591 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Các phép toán mệnh đề | chars=1562 | estimated_tokens=800 | estimated_audio_seconds=169
2026-05-26 14:32:27.593 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Các phép toán mệnh đề
2026-05-26 14:32:29.161 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=028dd483-48c2-4496-adf5-5ea1073b6ba7
2026-05-26 14:32:30.119 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 2 vectors for chapter_id=fc2f3451-4957-453f-bcd1-09436cb627e8
2026-05-26 14:32:30.355 | INFO     | logging:callHandlers:1762 - 10.16.17.88:65424 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:32:34.366 | INFO     | logging:callHandlers:1762 - 10.16.17.88:45287 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:32:38.127 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=4 | review_chars=548
2026-05-26 14:32:38.129 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=2 | mode=full | main_scripts=4 | review_chars=548
2026-05-26 14:32:38.130 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=2 | mode=full | total_scripts=4
2026-05-26 14:32:38.132 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=1/4 | chars=274
2026-05-26 14:32:38.171 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1562
2026-05-26 14:32:38.437 | INFO     | logging:callHandlers:1762 - 10.16.5.171:54763 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:32:42.456 | INFO     | logging:callHandlers:1762 - 10.16.25.130:63786 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:32:46.532 | INFO     | logging:callHandlers:1762 - 10.16.25.130:37691 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:32:47.635 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=1/4 | duration_ms=17184
2026-05-26 14:32:47.636 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=2/4 | chars=209
[2026-05-26 14:32:49,580: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:32:50,453: INFO/MainProcess] Task triam.notifications.scan_due[46fc4377-76b1-4cc7-b052-2ceff5604619] received
2026-05-26 14:32:50.731 | INFO     | logging:callHandlers:1762 - 10.16.17.88:4592 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:32:54.736 | INFO     | logging:callHandlers:1762 - 10.16.17.88:8591 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:32:56.955 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=2/4 | duration_ms=12792
2026-05-26 14:32:56.956 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=3/4 | chars=144
2026-05-26 14:32:57.313 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=9 | review_chars=667
2026-05-26 14:32:57.314 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=3 | mode=full | main_scripts=9 | review_chars=667
2026-05-26 14:32:57.316 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=3 | mode=full | total_scripts=9
2026-05-26 14:32:57.316 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=1/9 | chars=162
2026-05-26 14:32:57.903 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:32:57,904: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[46fc4377-76b1-4cc7-b052-2ceff5604619] succeeded in 7.450071622035466s: None
2026-05-26 14:32:58.911 | INFO     | logging:callHandlers:1762 - 10.16.25.130:55051 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:33:01.818 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=1/9 | duration_ms=9432
2026-05-26 14:33:01.820 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=2/9 | chars=267
2026-05-26 14:33:02.919 | INFO     | logging:callHandlers:1762 - 10.16.46.186:27923 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:33:04.995 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=3/4 | duration_ms=10680
2026-05-26 14:33:05.001 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=2 | mode=full | segment=4/4 | chars=302
2026-05-26 14:33:06.925 | INFO     | logging:callHandlers:1762 - 10.16.25.130:26175 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:33:08.838 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=2/9 | duration_ms=17376
2026-05-26 14:33:08.839 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=3/9 | chars=168
2026-05-26 14:33:10.979 | INFO     | logging:callHandlers:1762 - 10.16.17.88:21481 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:33:11.781 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=3/9 | duration_ms=9864
2026-05-26 14:33:11.786 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=4/9 | chars=356
2026-05-26 14:33:14.980 | INFO     | logging:callHandlers:1762 - 10.16.17.88:1047 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:33:18.839 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=2 | mode=full | segment=4/4 | duration_ms=18504
2026-05-26 14:33:18.841 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=2 | mode=full | created_segments=4/4
2026-05-26 14:33:18.841 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=2 | mode=full | chars=548
2026-05-26 14:33:18.996 | INFO     | logging:callHandlers:1762 - 10.16.46.186:35579 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:33:20.014 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=4/9 | duration_ms=21312
2026-05-26 14:33:20.015 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=5/9 | chars=640
2026-05-26 14:33:22.994 | INFO     | logging:callHandlers:1762 - 10.16.46.186:23445 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:33:26.996 | INFO     | logging:callHandlers:1762 - 10.16.17.88:24838 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:33:31.286 | INFO     | logging:callHandlers:1762 - 10.16.17.88:23323 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:33:35.276 | INFO     | logging:callHandlers:1762 - 10.16.17.88:59772 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:33:35.832 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=2 | mode=full
2026-05-26 14:33:35.841 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=028dd483-48c2-4496-adf5-5ea1073b6ba7 | mode=full | segments=4 | review_audio=True
2026-05-26 14:33:39.038 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=028dd483-48c2-4496-adf5-5ea1073b6ba7 | mode=full
2026-05-26 14:33:39.274 | INFO     | logging:callHandlers:1762 - 10.16.17.88:11385 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:33:41.514 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 2 READY | mode=full | segments=4
2026-05-26 14:33:41.519 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=4 | mode=full | title=Phép tuyển () | chars=401 | estimated_tokens=207 | estimated_audio_seconds=43
2026-05-26 14:33:43.337 | INFO     | logging:callHandlers:1762 - 10.16.46.186:31453 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:33:43.767 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=4 | mode=full | rag=true | tts=true
2026-05-26 14:33:43.776 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=4 | mode=full | title=Phép tuyển () | raw_chars=401
2026-05-26 14:33:43.777 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Phép tuyển () | chars=401 | estimated_tokens=207 | estimated_audio_seconds=43
2026-05-26 14:33:43.778 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Phép tuyển ()
2026-05-26 14:33:43.779 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=401
2026-05-26 14:33:47.370 | INFO     | logging:callHandlers:1762 - 10.16.25.130:47564 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:33:47.519 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=5/9 | duration_ms=43176
2026-05-26 14:33:47.519 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=6/9 | chars=175
2026-05-26 14:33:48.501 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=dd482d9f-e9e2-493e-82ab-d76f9e224580
[2026-05-26 14:33:49,581: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:33:50,236: INFO/MainProcess] Task triam.notifications.scan_due[83bba441-1f81-4d61-abf8-caca2a50eaf8] received
2026-05-26 14:33:51.673 | INFO     | logging:callHandlers:1762 - 10.16.17.88:49922 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:33:55.292 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=6/9 | duration_ms=12888
2026-05-26 14:33:55.293 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=7/9 | chars=140
2026-05-26 14:33:55.768 | INFO     | logging:callHandlers:1762 - 10.16.5.171:4479 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:33:57.674 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:33:57,677: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[83bba441-1f81-4d61-abf8-caca2a50eaf8] succeeded in 7.435526393936016s: None
2026-05-26 14:33:59.821 | INFO     | logging:callHandlers:1762 - 10.16.5.171:16388 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:34:00.394 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=7/9 | duration_ms=7992
2026-05-26 14:34:00.396 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=8/9 | chars=389
2026-05-26 14:34:03.833 | INFO     | logging:callHandlers:1762 - 10.16.17.88:31007 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:34:07.832 | INFO     | logging:callHandlers:1762 - 10.16.25.130:39074 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:34:08.042 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=8/9 | duration_ms=28344
2026-05-26 14:34:08.043 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=3 | mode=full | segment=9/9 | chars=382
2026-05-26 14:34:11.933 | INFO     | logging:callHandlers:1762 - 10.16.17.88:47496 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:34:11.955 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=5 | review_chars=533
2026-05-26 14:34:11.955 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=4 | mode=full | main_scripts=5 | review_chars=533
2026-05-26 14:34:11.955 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=4 | mode=full | total_scripts=5
2026-05-26 14:34:11.956 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=4 | mode=full | segment=1/5 | chars=132
2026-05-26 14:34:15.787 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=4 | mode=full | segment=1/5 | duration_ms=9600
2026-05-26 14:34:15.789 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=4 | mode=full | segment=2/5 | chars=136
2026-05-26 14:34:16.624 | INFO     | logging:callHandlers:1762 - 10.16.25.130:28909 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:34:17.078 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=3 | mode=full | segment=9/9 | duration_ms=25752
2026-05-26 14:34:17.082 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=3 | mode=full | created_segments=9/9
2026-05-26 14:34:17.088 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=3 | mode=full | chars=667
2026-05-26 14:34:17.294 | WARNING  | app.services.tts_service:generate_audio_and_get_duration:98 - TTS attempt 1/6 failed (667 chars): No audio was received. Please verify that your parameters are correct.. Retry in 3s...
2026-05-26 14:34:19.227 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=4 | mode=full | segment=2/5 | duration_ms=8856
2026-05-26 14:34:19.228 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=4 | mode=full | segment=3/5 | chars=106
2026-05-26 14:34:20.624 | INFO     | logging:callHandlers:1762 - 10.16.17.88:37206 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:34:21.687 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=4 | mode=full | segment=3/5 | duration_ms=6816
2026-05-26 14:34:21.689 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=4 | mode=full | segment=4/5 | chars=146
2026-05-26 14:34:24.627 | INFO     | logging:callHandlers:1762 - 10.16.17.88:42353 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:34:25.376 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=4 | mode=full | segment=4/5 | duration_ms=10392
2026-05-26 14:34:25.384 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=4 | mode=full | segment=5/5 | chars=102
2026-05-26 14:34:28.635 | INFO     | logging:callHandlers:1762 - 10.16.46.186:44993 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:34:32.667 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=4 | mode=full | segment=5/5 | duration_ms=8064
2026-05-26 14:34:32.668 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=4 | mode=full | created_segments=5/5
2026-05-26 14:34:32.669 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=4 | mode=full | chars=533
2026-05-26 14:34:32.809 | INFO     | logging:callHandlers:1762 - 10.16.17.88:41227 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:34:36.848 | INFO     | logging:callHandlers:1762 - 10.16.17.88:3943 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:34:40.924 | INFO     | logging:callHandlers:1762 - 10.16.17.88:41763 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:34:42.656 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=3 | mode=full
2026-05-26 14:34:42.660 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=fc2f3451-4957-453f-bcd1-09436cb627e8 | mode=full | segments=9 | review_audio=True
2026-05-26 14:34:45.007 | INFO     | logging:callHandlers:1762 - 10.16.17.88:44107 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:34:45.819 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=fc2f3451-4957-453f-bcd1-09436cb627e8 | mode=full
2026-05-26 14:34:48.283 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 3 READY | mode=full | segments=9
2026-05-26 14:34:48.286 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=5 | mode=full | title=Phép hoặc () | chars=329 | estimated_tokens=177 | estimated_audio_seconds=36
2026-05-26 14:34:49.187 | INFO     | logging:callHandlers:1762 - 10.16.17.88:51878 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
[2026-05-26 14:34:49,581: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:34:50,495: INFO/MainProcess] Task triam.notifications.scan_due[1941cab8-599e-48e9-b38e-a36cca1e745e] received
2026-05-26 14:34:50.533 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=5 | mode=full | rag=true | tts=true
2026-05-26 14:34:50.537 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=5 | mode=full | title=Phép hoặc () | raw_chars=329
2026-05-26 14:34:50.538 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Phép hoặc () | chars=329 | estimated_tokens=177 | estimated_audio_seconds=36
2026-05-26 14:34:50.539 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Phép hoặc ()
2026-05-26 14:34:50.539 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=329
2026-05-26 14:34:53.285 | INFO     | logging:callHandlers:1762 - 10.16.25.130:55280 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:34:53.731 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=4 | mode=full
2026-05-26 14:34:53.732 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=dd482d9f-e9e2-493e-82ab-d76f9e224580 | mode=full | segments=5 | review_audio=True
2026-05-26 14:34:56.887 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=dd482d9f-e9e2-493e-82ab-d76f9e224580 | mode=full
2026-05-26 14:34:57.283 | INFO     | logging:callHandlers:1762 - 10.16.25.130:51206 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:34:57.918 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:34:57,920: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1941cab8-599e-48e9-b38e-a36cca1e745e] succeeded in 7.422001559985802s: None
2026-05-26 14:34:59.377 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 4 READY | mode=full | segments=5
2026-05-26 14:34:59.395 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=6 | mode=full | title=Phép kéo theo() | chars=773 | estimated_tokens=411 | estimated_audio_seconds=84
2026-05-26 14:35:01.303 | INFO     | logging:callHandlers:1762 - 10.16.25.130:35329 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:35:01.652 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=6 | mode=full | rag=true | tts=true
2026-05-26 14:35:01.657 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=6 | mode=full | title=Phép kéo theo() | raw_chars=773
2026-05-26 14:35:01.658 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Phép kéo theo() | chars=773 | estimated_tokens=411 | estimated_audio_seconds=84
2026-05-26 14:35:01.659 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Phép kéo theo()
2026-05-26 14:35:05.055 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=086f1a41-3685-451a-8e4c-5f7c1017f157
2026-05-26 14:35:05.492 | INFO     | logging:callHandlers:1762 - 10.16.17.88:57387 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:35:05.753 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=e3c16e18-28a3-4a4c-baa8-9f80b7af3074
2026-05-26 14:35:09.491 | INFO     | logging:callHandlers:1762 - 10.16.46.186:17101 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:35:11.524 | INFO     | logging:callHandlers:1762 - 10.16.25.130:36105 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 14:35:13.470 | INFO     | logging:callHandlers:1762 - 10.16.17.88:61483 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:35:17.436 | INFO     | logging:callHandlers:1762 - 10.16.17.88:14881 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:35:17.462 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=2 | review_chars=424
2026-05-26 14:35:17.467 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=5 | mode=full | main_scripts=2 | review_chars=424
2026-05-26 14:35:17.469 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=5 | mode=full | total_scripts=2
2026-05-26 14:35:17.471 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=5 | mode=full | segment=1/2 | chars=138
2026-05-26 14:35:17.504 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=773
2026-05-26 14:35:21.449 | INFO     | logging:callHandlers:1762 - 10.16.25.130:43665 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:35:22.148 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=5 | mode=full | segment=1/2 | duration_ms=9024
2026-05-26 14:35:22.149 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=5 | mode=full | segment=2/2 | chars=210
2026-05-26 14:35:25.461 | INFO     | logging:callHandlers:1762 - 10.16.25.130:50883 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:35:27.434 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=5 | mode=full | segment=2/2 | duration_ms=16056
2026-05-26 14:35:27.435 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=5 | mode=full | created_segments=2/2
2026-05-26 14:35:27.436 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=5 | mode=full | chars=424
2026-05-26 14:35:28.583 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=4 | review_chars=548
2026-05-26 14:35:28.584 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=6 | mode=full | main_scripts=4 | review_chars=548
2026-05-26 14:35:28.586 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=6 | mode=full | total_scripts=4
2026-05-26 14:35:28.587 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=6 | mode=full | segment=1/4 | chars=360
2026-05-26 14:35:29.464 | INFO     | logging:callHandlers:1762 - 10.16.17.88:16563 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:35:33.842 | INFO     | logging:callHandlers:1762 - 10.16.17.88:24822 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:35:37.844 | INFO     | logging:callHandlers:1762 - 10.16.25.130:15456 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:35:38.242 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=5 | mode=full
2026-05-26 14:35:38.242 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=e3c16e18-28a3-4a4c-baa8-9f80b7af3074 | mode=full | segments=2 | review_audio=True
2026-05-26 14:35:41.400 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=e3c16e18-28a3-4a4c-baa8-9f80b7af3074 | mode=full
2026-05-26 14:35:41.852 | INFO     | logging:callHandlers:1762 - 10.16.5.171:49973 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:35:43.894 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 5 READY | mode=full | segments=2
2026-05-26 14:35:43.897 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=7 | mode=full | title=Phép kéo theo hai chiều hay tương đương () | chars=348 | estimated_tokens=177 | estimated_audio_seconds=39
2026-05-26 14:35:45.854 | INFO     | logging:callHandlers:1762 - 10.16.17.88:41809 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:35:46.143 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=7 | mode=full | rag=true | tts=true
2026-05-26 14:35:46.147 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=7 | mode=full | title=Phép kéo theo hai chiều hay tương đương () | raw_chars=348
2026-05-26 14:35:46.158 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Phép kéo theo hai chiều hay tương đương () | chars=348 | estimated_tokens=177 | estimated_audio_seconds=39
2026-05-26 14:35:46.160 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Phép kéo theo hai chiều hay tương đương ()
2026-05-26 14:35:46.162 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=348
2026-05-26 14:35:49.392 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=6 | mode=full | segment=1/4 | duration_ms=24168
2026-05-26 14:35:49.393 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=6 | mode=full | segment=2/4 | chars=253
[2026-05-26 14:35:49,581: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-26 14:35:50.065 | INFO     | logging:callHandlers:1762 - 10.16.46.186:56656 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
[2026-05-26 14:35:50,242: INFO/MainProcess] Task triam.notifications.scan_due[e6fa1b8f-fa5b-44f7-a0fd-555f293296eb] received
2026-05-26 14:35:50.538 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=6894608a-e589-4739-9ec0-d6c2294a9aaa
2026-05-26 14:35:54.044 | INFO     | logging:callHandlers:1762 - 10.16.46.186:27241 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:35:55.563 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=6 | mode=full | segment=2/4 | duration_ms=14448
2026-05-26 14:35:55.564 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=6 | mode=full | segment=3/4 | chars=411
2026-05-26 14:35:57.680 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:35:57,681: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e6fa1b8f-fa5b-44f7-a0fd-555f293296eb] succeeded in 7.436725032981485s: None
2026-05-26 14:35:58.002 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=3 | review_chars=481
2026-05-26 14:35:58.007 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=7 | mode=full | main_scripts=3 | review_chars=481
2026-05-26 14:35:58.009 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=7 | mode=full | total_scripts=3
2026-05-26 14:35:58.012 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=7 | mode=full | segment=1/3 | chars=158
2026-05-26 14:35:58.115 | INFO     | logging:callHandlers:1762 - 10.16.25.130:37049 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:36:02.120 | INFO     | logging:callHandlers:1762 - 10.16.17.88:17538 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:36:02.972 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=7 | mode=full | segment=1/3 | duration_ms=10680
2026-05-26 14:36:02.973 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=7 | mode=full | segment=2/3 | chars=172
2026-05-26 14:36:06.137 | INFO     | logging:callHandlers:1762 - 10.16.5.171:8501 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:36:07.796 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=7 | mode=full | segment=2/3 | duration_ms=11232
2026-05-26 14:36:07.796 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=7 | mode=full | segment=3/3 | chars=155
2026-05-26 14:36:10.100 | INFO     | logging:callHandlers:1762 - 10.16.17.88:24381 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:36:11.005 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=6 | mode=full | segment=3/4 | duration_ms=25584
2026-05-26 14:36:11.005 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=6 | mode=full | segment=4/4 | chars=264
2026-05-26 14:36:11.891 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=7 | mode=full | segment=3/3 | duration_ms=9288
2026-05-26 14:36:11.893 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=7 | mode=full | created_segments=3/3
2026-05-26 14:36:11.898 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=7 | mode=full | chars=481
2026-05-26 14:36:14.320 | INFO     | logging:callHandlers:1762 - 10.16.25.130:41969 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:36:18.554 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=6 | mode=full | segment=4/4 | duration_ms=15960
2026-05-26 14:36:18.555 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=6 | mode=full | created_segments=4/4
2026-05-26 14:36:18.559 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=6 | mode=full | chars=548
2026-05-26 14:36:23.196 | INFO     | logging:callHandlers:1762 - 10.16.5.171:38102 - "GET /api/v1/health HTTP/1.1" 200
2026-05-26 14:36:23.845 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=7 | mode=full
2026-05-26 14:36:23.848 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=6894608a-e589-4739-9ec0-d6c2294a9aaa | mode=full | segments=3 | review_audio=True
2026-05-26 14:36:27.047 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=6894608a-e589-4739-9ec0-d6c2294a9aaa | mode=full
2026-05-26 14:36:27.374 | INFO     | logging:callHandlers:1762 - 10.16.25.130:43013 - "GET /api/v1/books HTTP/1.1" 200
2026-05-26 14:36:29.588 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 7 READY | mode=full | segments=3
2026-05-26 14:36:29.592 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=8 | mode=full | title=Khái niệm | chars=154 | estimated_tokens=78 | estimated_audio_seconds=16
2026-05-26 14:36:31.854 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=8 | mode=full | rag=true | tts=true
2026-05-26 14:36:31.869 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=8 | mode=full | title=Khái niệm | raw_chars=154
2026-05-26 14:36:31.874 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Khái niệm | chars=154 | estimated_tokens=78 | estimated_audio_seconds=16
2026-05-26 14:36:31.877 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Khái niệm
2026-05-26 14:36:31.883 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=154
2026-05-26 14:36:35.397 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=6 | mode=full
2026-05-26 14:36:35.397 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=086f1a41-3685-451a-8e4c-5f7c1017f157 | mode=full | segments=4 | review_audio=True
2026-05-26 14:36:38.595 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=086f1a41-3685-451a-8e4c-5f7c1017f157 | mode=full
2026-05-26 14:36:41.058 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 6 READY | mode=full | segments=4
2026-05-26 14:36:41.063 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=9 | mode=full | title=Các ví dụ | chars=161 | estimated_tokens=89 | estimated_audio_seconds=13
2026-05-26 14:36:43.274 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=9 | mode=full | rag=true | tts=true
2026-05-26 14:36:44.170 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=e70d5d69-644a-4ea5-bcc3-f20b5f84fc01
2026-05-26 14:36:44.176 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=9 | mode=full | title=Các ví dụ | raw_chars=161
2026-05-26 14:36:44.180 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Các ví dụ | chars=161 | estimated_tokens=89 | estimated_audio_seconds=13
2026-05-26 14:36:44.181 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Các ví dụ
2026-05-26 14:36:46.394 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=1 | review_chars=446
2026-05-26 14:36:46.400 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=8 | mode=full | main_scripts=1 | review_chars=446
2026-05-26 14:36:46.401 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=8 | mode=full | total_scripts=1
2026-05-26 14:36:46.402 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=8 | mode=full | segment=1/1 | chars=576
2026-05-26 14:36:46.438 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=161
2026-05-26 14:36:47.747 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=80175285-f7a2-4b4c-b5c1-002ada637f05
[2026-05-26 14:36:49,591: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:36:50,462: INFO/MainProcess] Task triam.notifications.scan_due[8a593e8a-50e5-41b3-99a2-59d42a9a854b] received
2026-05-26 14:36:57.622 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:36:57,624: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8a593e8a-50e5-41b3-99a2-59d42a9a854b] succeeded in 7.158157097990625s: None
2026-05-26 14:37:02.541 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=8 | mode=full | segment=1/1 | duration_ms=37608
2026-05-26 14:37:02.541 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=8 | mode=full | created_segments=1/1
2026-05-26 14:37:02.541 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=8 | mode=full | chars=446
2026-05-26 14:37:04.184 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=4 | review_chars=565
2026-05-26 14:37:04.186 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=9 | mode=full | main_scripts=4 | review_chars=565
2026-05-26 14:37:04.188 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=9 | mode=full | total_scripts=4
2026-05-26 14:37:04.191 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=9 | mode=full | segment=1/4 | chars=279
2026-05-26 14:37:13.943 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=9 | mode=full | segment=1/4 | duration_ms=17952
2026-05-26 14:37:13.944 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=9 | mode=full | segment=2/4 | chars=375
2026-05-26 14:37:18.266 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=8 | mode=full
2026-05-26 14:37:18.268 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=e70d5d69-644a-4ea5-bcc3-f20b5f84fc01 | mode=full | segments=1 | review_audio=True
2026-05-26 14:37:21.365 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=e70d5d69-644a-4ea5-bcc3-f20b5f84fc01 | mode=full
2026-05-26 14:37:23.801 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 8 READY | mode=full | segments=1
2026-05-26 14:37:23.805 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=10 | mode=full | title=Sự tương đương logic | chars=431 | estimated_tokens=215 | estimated_audio_seconds=47
2026-05-26 14:37:26.027 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=10 | mode=full | rag=true | tts=true
2026-05-26 14:37:26.033 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=10 | mode=full | title=Sự tương đương logic | raw_chars=431
2026-05-26 14:37:26.036 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Sự tương đương logic | chars=431 | estimated_tokens=215 | estimated_audio_seconds=47
2026-05-26 14:37:26.038 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Sự tương đương logic
2026-05-26 14:37:26.039 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=431
2026-05-26 14:37:29.476 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=41ca8144-e54f-4cd6-9819-254946a26bcf
2026-05-26 14:37:34.224 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=9 | mode=full | segment=2/4 | duration_ms=26688
2026-05-26 14:37:34.225 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=9 | mode=full | segment=3/4 | chars=342
2026-05-26 14:37:38.712 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=4 | review_chars=494
2026-05-26 14:37:38.713 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=10 | mode=full | main_scripts=4 | review_chars=494
2026-05-26 14:37:38.714 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=10 | mode=full | total_scripts=4
2026-05-26 14:37:38.715 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=10 | mode=full | segment=1/4 | chars=277
2026-05-26 14:37:46.679 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=9 | mode=full | segment=3/4 | duration_ms=23112
2026-05-26 14:37:46.682 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=9 | mode=full | segment=4/4 | chars=372
2026-05-26 14:37:48.392 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=10 | mode=full | segment=1/4 | duration_ms=16271
2026-05-26 14:37:48.394 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=10 | mode=full | segment=2/4 | chars=346
[2026-05-26 14:37:49,592: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:37:50,462: INFO/MainProcess] Task triam.notifications.scan_due[f66c57f6-33e1-4107-b4fd-a5ebc72e901e] received
2026-05-26 14:37:55.871 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=9 | mode=full | segment=4/4 | duration_ms=23232
2026-05-26 14:37:55.873 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=9 | mode=full | created_segments=4/4
2026-05-26 14:37:55.874 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=9 | mode=full | chars=565
2026-05-26 14:37:57.554 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:37:57,555: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f66c57f6-33e1-4107-b4fd-a5ebc72e901e] succeeded in 7.091966398991644s: None
2026-05-26 14:37:58.806 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=10 | mode=full | segment=2/4 | duration_ms=21048
2026-05-26 14:37:58.806 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=10 | mode=full | segment=3/4 | chars=208
2026-05-26 14:38:05.698 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=10 | mode=full | segment=3/4 | duration_ms=12048
2026-05-26 14:38:05.698 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=10 | mode=full | segment=4/4 | chars=291
2026-05-26 14:38:08.797 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=9 | mode=full
2026-05-26 14:38:08.798 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=80175285-f7a2-4b4c-b5c1-002ada637f05 | mode=full | segments=4 | review_audio=True
2026-05-26 14:38:11.893 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=80175285-f7a2-4b4c-b5c1-002ada637f05 | mode=full
2026-05-26 14:38:14.319 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 9 READY | mode=full | segments=4
2026-05-26 14:38:14.323 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=11 | mode=full | title=Các luật logic thông dụng | chars=711 | estimated_tokens=421 | estimated_audio_seconds=78
2026-05-26 14:38:16.534 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=11 | mode=full | rag=true | tts=true
2026-05-26 14:38:16.537 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=11 | mode=full | title=Các luật logic thông dụng | raw_chars=711
2026-05-26 14:38:16.538 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Các luật logic thông dụng | chars=711 | estimated_tokens=421 | estimated_audio_seconds=78
2026-05-26 14:38:16.538 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Các luật logic thông dụng
2026-05-26 14:38:16.538 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=711
2026-05-26 14:38:19.500 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=10 | mode=full | segment=4/4 | duration_ms=17088
2026-05-26 14:38:19.502 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=10 | mode=full | created_segments=4/4
2026-05-26 14:38:19.503 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=10 | mode=full | chars=494
2026-05-26 14:38:20.600 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=474f4ced-4010-4219-a123-958ddbf93753
2026-05-26 14:38:35.583 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=10 | mode=full
2026-05-26 14:38:35.586 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=41ca8144-e54f-4cd6-9819-254946a26bcf | mode=full | segments=4 | review_audio=True
2026-05-26 14:38:38.701 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=41ca8144-e54f-4cd6-9819-254946a26bcf | mode=full
2026-05-26 14:38:41.132 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 10 READY | mode=full | segments=4
2026-05-26 14:38:41.133 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=12 | mode=full | title=Các qui tắc thay thế | chars=314 | estimated_tokens=159 | estimated_audio_seconds=33
2026-05-26 14:38:43.341 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=12 | mode=full | rag=true | tts=true
2026-05-26 14:38:43.348 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=12 | mode=full | title=Các qui tắc thay thế | raw_chars=314
2026-05-26 14:38:43.351 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Các qui tắc thay thế | chars=314 | estimated_tokens=159 | estimated_audio_seconds=33
2026-05-26 14:38:43.353 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Các qui tắc thay thế
2026-05-26 14:38:45.566 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=11 | review_chars=742
2026-05-26 14:38:45.571 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=11 | mode=full | main_scripts=11 | review_chars=742
2026-05-26 14:38:45.571 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=11 | mode=full | total_scripts=11
2026-05-26 14:38:45.575 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=11 | mode=full | segment=1/11 | chars=210
2026-05-26 14:38:45.608 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=314
2026-05-26 14:38:46.728 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=e3ff0c72-a872-4898-9443-ac399796b0ef
[2026-05-26 14:38:49,592: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:38:50,246: INFO/MainProcess] Task triam.notifications.scan_due[3de4dd3d-6221-44e1-aa82-16166cf7dd61] received
2026-05-26 14:38:53.158 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=2 | review_chars=491
2026-05-26 14:38:53.160 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=12 | mode=full | main_scripts=2 | review_chars=491
2026-05-26 14:38:53.160 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=12 | mode=full | total_scripts=2
2026-05-26 14:38:53.163 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=12 | mode=full | segment=1/2 | chars=254
2026-05-26 14:38:55.145 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=11 | mode=full | segment=1/11 | duration_ms=12312
2026-05-26 14:38:55.146 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=11 | mode=full | segment=2/11 | chars=142
2026-05-26 14:38:57.349 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:38:57,350: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3de4dd3d-6221-44e1-aa82-16166cf7dd61] succeeded in 7.102588271023706s: None
2026-05-26 14:39:01.157 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=12 | mode=full | segment=1/2 | duration_ms=13656
2026-05-26 14:39:01.160 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=12 | mode=full | segment=2/2 | chars=265
2026-05-26 14:39:05.417 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=11 | mode=full | segment=2/11 | duration_ms=9336
2026-05-26 14:39:05.418 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=11 | mode=full | segment=3/11 | chars=192
2026-05-26 14:39:13.090 | INFO     | logging:callHandlers:1762 - 10.16.46.186:7320 - "GET /api/v1/study-contexts HTTP/1.1" 200
2026-05-26 14:39:14.766 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=12 | mode=full | segment=2/2 | duration_ms=15480
2026-05-26 14:39:14.768 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=12 | mode=full | created_segments=2/2
2026-05-26 14:39:14.771 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=12 | mode=full | chars=491
2026-05-26 14:39:15.147 | INFO     | logging:callHandlers:1762 - 10.16.46.186:7320 - "GET /api/v1/books/4ef0ad48-0e8f-457d-b278-3d3fe3da0905/processing-status HTTP/1.1" 200
2026-05-26 14:39:15.483 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=11 | mode=full | segment=3/11 | duration_ms=16271
2026-05-26 14:39:15.489 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=11 | mode=full | segment=4/11 | chars=178
2026-05-26 14:39:18.288 | INFO     | logging:callHandlers:1762 - 10.16.46.186:7320 - "GET /api/v1/books/4ef0ad48-0e8f-457d-b278-3d3fe3da0905/details HTTP/1.1" 200
2026-05-26 14:39:19.610 | INFO     | logging:callHandlers:1762 - 10.16.25.130:12412 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:39:21.540 | INFO     | logging:callHandlers:1762 - 10.16.46.186:7320 - "GET /api/v1/books?limit=50&offset=0 HTTP/1.1" 200
2026-05-26 14:39:21.769 | INFO     | logging:callHandlers:1762 - 10.16.25.130:12412 - "GET /api/v1/books/4ef0ad48-0e8f-457d-b278-3d3fe3da0905/learning-progress?mode=full HTTP/1.1" 200
2026-05-26 14:39:24.086 | INFO     | logging:callHandlers:1762 - 10.16.46.186:7320 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:39:26.878 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=11 | mode=full | segment=4/11 | duration_ms=17592
2026-05-26 14:39:26.880 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=11 | mode=full | segment=5/11 | chars=202
2026-05-26 14:39:28.201 | INFO     | logging:callHandlers:1762 - 10.16.17.88:29760 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:39:31.450 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=12 | mode=full
2026-05-26 14:39:31.451 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=e3ff0c72-a872-4898-9443-ac399796b0ef | mode=full | segments=2 | review_audio=True
2026-05-26 14:39:32.172 | INFO     | logging:callHandlers:1762 - 10.16.25.130:52611 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:39:34.542 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=e3ff0c72-a872-4898-9443-ac399796b0ef | mode=full
2026-05-26 14:39:36.266 | INFO     | logging:callHandlers:1762 - 10.16.17.88:24154 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:39:36.974 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 12 READY | mode=full | segments=2
2026-05-26 14:39:36.981 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=13 | mode=full | title=Các ví dụ | chars=1114 | estimated_tokens=598 | estimated_audio_seconds=92
2026-05-26 14:39:39.195 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=13 | mode=full | rag=true | tts=true
2026-05-26 14:39:39.203 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=13 | mode=full | title=Các ví dụ | raw_chars=1114
2026-05-26 14:39:39.205 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Các ví dụ | chars=1114 | estimated_tokens=598 | estimated_audio_seconds=92
2026-05-26 14:39:39.206 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Các ví dụ
2026-05-26 14:39:39.208 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1114
2026-05-26 14:39:40.369 | INFO     | logging:callHandlers:1762 - 10.16.17.88:30162 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:39:42.133 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=11 | mode=full | segment=5/11 | duration_ms=16704
2026-05-26 14:39:42.134 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=11 | mode=full | segment=6/11 | chars=122
2026-05-26 14:39:43.315 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=6aed16f5-2800-499b-b174-28cd7bbe5084
2026-05-26 14:39:44.463 | INFO     | logging:callHandlers:1762 - 10.16.17.88:34225 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:39:48.542 | INFO     | logging:callHandlers:1762 - 10.16.46.186:7398 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:39:48.716 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=11 | mode=full | segment=6/11 | duration_ms=10032
2026-05-26 14:39:48.717 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=11 | mode=full | segment=7/11 | chars=208
[2026-05-26 14:39:49,592: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:39:50,628: INFO/MainProcess] Task triam.notifications.scan_due[d6a13cf8-65c9-42df-a719-17fd085111fd] received
2026-05-26 14:39:53.113 | INFO     | logging:callHandlers:1762 - 10.16.46.186:61151 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:39:57.096 | INFO     | logging:callHandlers:1762 - 10.16.25.130:9375 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:39:57.755 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:39:57,756: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d6a13cf8-65c9-42df-a719-17fd085111fd] succeeded in 7.1255518780089915s: None
2026-05-26 14:39:58.347 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=11 | mode=full | segment=7/11 | duration_ms=14064
2026-05-26 14:39:58.347 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=11 | mode=full | segment=8/11 | chars=216
2026-05-26 14:40:01.060 | INFO     | logging:callHandlers:1762 - 10.16.46.186:46689 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:40:05.101 | INFO     | logging:callHandlers:1762 - 10.16.17.88:65309 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:40:09.113 | INFO     | logging:callHandlers:1762 - 10.16.17.88:40061 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:40:13.202 | INFO     | logging:callHandlers:1762 - 10.16.17.88:48099 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:40:17.239 | INFO     | logging:callHandlers:1762 - 10.16.25.130:36452 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:40:18.172 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=11 | mode=full | segment=8/11 | duration_ms=17328
2026-05-26 14:40:18.175 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=11 | mode=full | segment=9/11 | chars=236
2026-05-26 14:40:21.338 | INFO     | logging:callHandlers:1762 - 10.16.25.130:10031 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:40:26.042 | INFO     | logging:callHandlers:1762 - 10.16.46.186:56981 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:40:29.770 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=11 | mode=full | segment=9/11 | duration_ms=15984
2026-05-26 14:40:29.773 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=11 | mode=full | segment=10/11 | chars=184
2026-05-26 14:40:30.122 | INFO     | logging:callHandlers:1762 - 10.16.5.171:58924 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:40:34.214 | INFO     | logging:callHandlers:1762 - 10.16.17.88:60841 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:40:38.293 | INFO     | logging:callHandlers:1762 - 10.16.46.186:21513 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:40:41.828 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=11 | mode=full | segment=10/11 | duration_ms=12504
2026-05-26 14:40:41.828 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=11 | mode=full | segment=11/11 | chars=314
2026-05-26 14:40:42.304 | INFO     | logging:callHandlers:1762 - 10.16.46.186:21242 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:40:46.318 | INFO     | logging:callHandlers:1762 - 10.16.17.88:16579 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
[2026-05-26 14:40:49,593: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:40:50,247: INFO/MainProcess] Task triam.notifications.scan_due[df4c5315-1c0f-4e6f-b746-9664db8b855c] received
2026-05-26 14:40:50.502 | INFO     | logging:callHandlers:1762 - 10.16.25.130:23343 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:40:54.578 | INFO     | logging:callHandlers:1762 - 10.16.17.88:17039 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:40:57.350 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:40:57,352: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[df4c5315-1c0f-4e6f-b746-9664db8b855c] succeeded in 7.101813599001616s: None
2026-05-26 14:40:58.563 | INFO     | logging:callHandlers:1762 - 10.16.25.130:27867 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:41:02.595 | INFO     | logging:callHandlers:1762 - 10.16.5.171:8284 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:41:05.467 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=11 | mode=full | segment=11/11 | duration_ms=26736
2026-05-26 14:41:05.469 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=11 | mode=full | created_segments=11/11
2026-05-26 14:41:05.471 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=11 | mode=full | chars=742
2026-05-26 14:41:06.696 | INFO     | logging:callHandlers:1762 - 10.16.5.171:47399 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:41:10.769 | INFO     | logging:callHandlers:1762 - 10.16.5.171:32399 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:41:15.479 | INFO     | logging:callHandlers:1762 - 10.16.46.186:30321 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:41:19.574 | INFO     | logging:callHandlers:1762 - 10.16.17.88:40753 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:41:23.785 | INFO     | logging:callHandlers:1762 - 10.16.5.171:22036 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:41:27.860 | INFO     | logging:callHandlers:1762 - 10.16.25.130:11894 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:41:31.839 | INFO     | logging:callHandlers:1762 - 10.16.25.130:22270 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:41:35.847 | INFO     | logging:callHandlers:1762 - 10.16.17.88:59436 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:41:39.856 | INFO     | logging:callHandlers:1762 - 10.16.17.88:63398 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:41:43.007 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=11 | mode=full
2026-05-26 14:41:43.008 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=474f4ced-4010-4219-a123-958ddbf93753 | mode=full | segments=11 | review_audio=True
2026-05-26 14:41:43.929 | INFO     | logging:callHandlers:1762 - 10.16.17.88:34984 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:41:46.102 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=474f4ced-4010-4219-a123-958ddbf93753 | mode=full
2026-05-26 14:41:47.930 | INFO     | logging:callHandlers:1762 - 10.16.17.88:27515 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:41:48.525 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 11 READY | mode=full | segments=11
2026-05-26 14:41:48.526 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=14 | mode=full | title=Các Dạng Chính Tắc | chars=781 | estimated_tokens=421 | estimated_audio_seconds=78
[2026-05-26 14:41:49,592: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:41:50,465: INFO/MainProcess] Task triam.notifications.scan_due[6faf5d15-f193-42b1-80ca-2428251e2162] received
2026-05-26 14:41:50.726 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=14 | mode=full | rag=true | tts=true
2026-05-26 14:41:50.730 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=14 | mode=full | title=Các Dạng Chính Tắc | raw_chars=781
2026-05-26 14:41:50.735 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Các Dạng Chính Tắc | chars=781 | estimated_tokens=421 | estimated_audio_seconds=78
2026-05-26 14:41:50.735 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Các Dạng Chính Tắc
2026-05-26 14:41:51.926 | INFO     | logging:callHandlers:1762 - 10.16.17.88:7076 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:41:54.436 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=25ef0df6-afe2-4b59-8769-fb4d717318e9
2026-05-26 14:41:55.934 | INFO     | logging:callHandlers:1762 - 10.16.17.88:49773 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:41:59.632 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:41:59,633: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[6faf5d15-f193-42b1-80ca-2428251e2162] succeeded in 8.955304911010899s: None
2026-05-26 14:42:00.010 | INFO     | logging:callHandlers:1762 - 10.16.17.88:14134 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:42:04.135 | INFO     | logging:callHandlers:1762 - 10.16.46.186:6306 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
[2026-05-26 14:42:49,595: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:42:50,464: INFO/MainProcess] Task triam.notifications.scan_due[cbd610ef-a909-449b-a30d-4b21c87cef3b] received
2026-05-26 14:42:58.239 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:42:58,241: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[cbd610ef-a909-449b-a30d-4b21c87cef3b] succeeded in 7.561801022966392s: None
2026-05-26 14:43:13.497 | INFO     | logging:callHandlers:1762 - 10.16.46.186:31487 - "GET /api/v1/books/4ef0ad48-0e8f-457d-b278-3d3fe3da0905/processing-status HTTP/1.1" 200
2026-05-26 14:43:17.522 | INFO     | logging:callHandlers:1762 - 10.16.17.88:17731 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:43:21.595 | INFO     | logging:callHandlers:1762 - 10.16.17.88:14342 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:43:25.591 | INFO     | logging:callHandlers:1762 - 10.16.25.130:11222 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:43:29.602 | INFO     | logging:callHandlers:1762 - 10.16.5.171:33852 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:43:33.610 | INFO     | logging:callHandlers:1762 - 10.16.46.186:37246 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:43:38.292 | INFO     | logging:callHandlers:1762 - 10.16.25.130:18746 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:43:42.275 | INFO     | logging:callHandlers:1762 - 10.16.5.171:22863 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
2026-05-26 14:43:46.281 | INFO     | logging:callHandlers:1762 - 10.16.25.130:22655 - "GET /api/v1/jobs/541e7dc7-79d0-43c7-99c4-59c1bb1b354e HTTP/1.1" 200
[2026-05-26 14:43:49,597: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:43:50,252: INFO/MainProcess] Task triam.notifications.scan_due[28bc0f63-b870-436c-933f-a114f9b1d651] received
2026-05-26 14:43:56.091 | INFO     | logging:callHandlers:1762 - 10.16.17.88:2892 - "GET /api/v1/health HTTP/1.1" 200
2026-05-26 14:43:57.796 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:43:57,796: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[28bc0f63-b870-436c-933f-a114f9b1d651] succeeded in 7.542238277033903s: None
2026-05-26 14:43:58.644 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=17 | review_chars=465
2026-05-26 14:43:58.656 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=13 | mode=full | main_scripts=17 | review_chars=465
2026-05-26 14:43:58.656 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=13 | mode=full | total_scripts=17
2026-05-26 14:43:58.656 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=13 | mode=full | segment=1/17 | chars=253
2026-05-26 14:43:58.692 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=781
2026-05-26 14:43:58.877 | INFO     | logging:callHandlers:1762 - 10.16.17.88:2892 - "GET /api/v1/books HTTP/1.1" 200
2026-05-26 14:44:06.215 | INFO     | logging:callHandlers:1762 - 10.16.46.186:31528 - "GET /api/v1/books/4ef0ad48-0e8f-457d-b278-3d3fe3da0905/learning-progress?mode=full HTTP/1.1" 200
2026-05-26 14:44:06.669 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=13 | mode=full | segment=1/17 | duration_ms=17184
2026-05-26 14:44:06.671 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=13 | mode=full | segment=2/17 | chars=217
2026-05-26 14:44:19.126 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=13 | mode=full | segment=2/17 | duration_ms=15840
2026-05-26 14:44:19.132 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=13 | mode=full | segment=3/17 | chars=216
2026-05-26 14:44:26.346 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=3 | review_chars=616
2026-05-26 14:44:26.346 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=14 | mode=full | main_scripts=3 | review_chars=616
2026-05-26 14:44:26.346 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=14 | mode=full | total_scripts=3
2026-05-26 14:44:26.347 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=14 | mode=full | segment=1/3 | chars=369
2026-05-26 14:44:31.013 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=13 | mode=full | segment=3/17 | duration_ms=14400
2026-05-26 14:44:31.014 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=13 | mode=full | segment=4/17 | chars=234
2026-05-26 14:44:40.026 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=13 | mode=full | segment=4/17 | duration_ms=16175
2026-05-26 14:44:40.029 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=13 | mode=full | segment=5/17 | chars=274
2026-05-26 14:44:49.003 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=13 | mode=full | segment=5/17 | duration_ms=18048
2026-05-26 14:44:49.004 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=13 | mode=full | segment=6/17 | chars=229
[2026-05-26 14:44:49,598: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:44:50,472: INFO/MainProcess] Task triam.notifications.scan_due[fe9aa819-11f8-4d9d-9250-ab0450161b43] received
2026-05-26 14:44:52.015 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=14 | mode=full | segment=1/3 | duration_ms=26880
2026-05-26 14:44:52.016 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=14 | mode=full | segment=2/3 | chars=378
2026-05-26 14:44:58.289 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:44:58,292: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[fe9aa819-11f8-4d9d-9250-ab0450161b43] succeeded in 7.6029328210279346s: None
2026-05-26 14:44:58.453 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=13 | mode=full | segment=6/17 | duration_ms=14496
2026-05-26 14:44:58.455 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=13 | mode=full | segment=7/17 | chars=300
2026-05-26 14:45:07.967 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=14 | mode=full | segment=2/3 | duration_ms=27264
2026-05-26 14:45:07.968 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=14 | mode=full | segment=3/3 | chars=476
2026-05-26 14:45:09.763 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=13 | mode=full | segment=7/17 | duration_ms=18768
2026-05-26 14:45:09.764 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=13 | mode=full | segment=8/17 | chars=381
2026-05-26 14:45:20.352 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=13 | mode=full | segment=8/17 | duration_ms=22656
2026-05-26 14:45:20.356 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=13 | mode=full | segment=9/17 | chars=396
2026-05-26 14:45:22.049 | INFO     | logging:callHandlers:1762 - 10.16.46.186:22494 - "GET /api/v1/books/4ef0ad48-0e8f-457d-b278-3d3fe3da0905/details HTTP/1.1" 200
2026-05-26 14:45:25.606 | INFO     | logging:callHandlers:1762 - 10.16.46.186:22494 - "GET /api/v1/books/4ef0ad48-0e8f-457d-b278-3d3fe3da0905/learning-progress?mode=full HTTP/1.1" 200
2026-05-26 14:45:27.570 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=14 | mode=full | segment=3/3 | duration_ms=44880
2026-05-26 14:45:27.572 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=14 | mode=full | created_segments=3/3
2026-05-26 14:45:27.576 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=14 | mode=full | chars=616
2026-05-26 14:45:30.901 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=13 | mode=full | segment=9/17 | duration_ms=22224
2026-05-26 14:45:30.902 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=13 | mode=full | segment=10/17 | chars=166
2026-05-26 14:45:36.245 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=13 | mode=full | segment=10/17 | duration_ms=10968
2026-05-26 14:45:36.247 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=13 | mode=full | segment=11/17 | chars=181
2026-05-26 14:45:43.375 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=13 | mode=full | segment=11/17 | duration_ms=11640
2026-05-26 14:45:43.378 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=13 | mode=full | segment=12/17 | chars=321
[2026-05-26 14:45:49,598: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-26 14:45:50.254 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=14 | mode=full
2026-05-26 14:45:50.255 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=25ef0df6-afe2-4b59-8769-fb4d717318e9 | mode=full | segments=3 | review_audio=True
[2026-05-26 14:45:50,253: INFO/MainProcess] Task triam.notifications.scan_due[48e25c9d-0a55-4157-bc62-2b8abe7ab669] received
2026-05-26 14:45:53.374 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=25ef0df6-afe2-4b59-8769-fb4d717318e9 | mode=full
2026-05-26 14:45:55.810 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 14 READY | mode=full | segments=3
2026-05-26 14:45:55.811 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=15 | mode=full | title=Khái niệm vị từ | chars=585 | estimated_tokens=283 | estimated_audio_seconds=62
2026-05-26 14:45:58.027 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=15 | mode=full | rag=true | tts=true
2026-05-26 14:45:58.039 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=15 | mode=full | title=Khái niệm vị từ | raw_chars=585
2026-05-26 14:45:58.043 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Khái niệm vị từ | chars=585 | estimated_tokens=283 | estimated_audio_seconds=62
2026-05-26 14:45:58.047 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Khái niệm vị từ
2026-05-26 14:45:58.048 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=585
2026-05-26 14:45:58.154 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:45:58,155: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[48e25c9d-0a55-4157-bc62-2b8abe7ab669] succeeded in 7.686491621076129s: None
2026-05-26 14:46:01.015 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=13 | mode=full | segment=12/17 | duration_ms=20184
2026-05-26 14:46:01.016 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=13 | mode=full | segment=13/17 | chars=249
2026-05-26 14:46:02.486 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=bcaea8c9-5ffb-4659-bae4-cfc6591565e4
2026-05-26 14:46:09.968 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=13 | mode=full | segment=13/17 | duration_ms=16104
2026-05-26 14:46:09.981 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=13 | mode=full | segment=14/17 | chars=241
2026-05-26 14:46:11.930 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=2 | review_chars=615
2026-05-26 14:46:11.931 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=15 | mode=full | main_scripts=2 | review_chars=615
2026-05-26 14:46:11.932 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=15 | mode=full | total_scripts=2
2026-05-26 14:46:11.933 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=15 | mode=full | segment=1/2 | chars=391
2026-05-26 14:46:20.613 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=13 | mode=full | segment=14/17 | duration_ms=15624
2026-05-26 14:46:20.618 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=13 | mode=full | segment=15/17 | chars=219
2026-05-26 14:46:31.680 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=13 | mode=full | segment=15/17 | duration_ms=14760
2026-05-26 14:46:31.681 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=13 | mode=full | segment=16/17 | chars=193
2026-05-26 14:46:33.087 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=15 | mode=full | segment=1/2 | duration_ms=29928
2026-05-26 14:46:33.088 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=15 | mode=full | segment=2/2 | chars=658
2026-05-26 14:46:39.575 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=13 | mode=full | segment=16/17 | duration_ms=12912
2026-05-26 14:46:39.576 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=13 | mode=full | segment=17/17 | chars=192
[2026-05-26 14:46:49,598: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:46:50,668: INFO/MainProcess] Task triam.notifications.scan_due[22103a52-3773-417d-8d7f-66bdb14d8904] received
2026-05-26 14:46:51.644 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=15 | mode=full | segment=2/2 | duration_ms=43896
2026-05-26 14:46:51.644 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=15 | mode=full | created_segments=2/2
2026-05-26 14:46:51.648 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=15 | mode=full | chars=615
2026-05-26 14:46:54.629 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=13 | mode=full | segment=17/17 | duration_ms=13536
2026-05-26 14:46:54.631 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=13 | mode=full | created_segments=17/17
2026-05-26 14:46:54.633 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=13 | mode=full | chars=465
2026-05-26 14:46:58.257 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:46:58,258: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[22103a52-3773-417d-8d7f-66bdb14d8904] succeeded in 7.583332702983171s: None
2026-05-26 14:47:08.254 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=13 | mode=full
2026-05-26 14:47:08.256 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=6aed16f5-2800-499b-b174-28cd7bbe5084 | mode=full | segments=17 | review_audio=True
2026-05-26 14:47:11.368 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=6aed16f5-2800-499b-b174-28cd7bbe5084 | mode=full
2026-05-26 14:47:13.798 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 13 READY | mode=full | segments=17
2026-05-26 14:47:13.804 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=16 | mode=full | title=Các phép toán trên vị từ | chars=330 | estimated_tokens=165 | estimated_audio_seconds=31
2026-05-26 14:47:16.015 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=16 | mode=full | rag=true | tts=true
2026-05-26 14:47:16.020 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=16 | mode=full | title=Các phép toán trên vị từ | raw_chars=330
2026-05-26 14:47:16.021 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Các phép toán trên vị từ | chars=330 | estimated_tokens=165 | estimated_audio_seconds=31
2026-05-26 14:47:16.023 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Các phép toán trên vị từ
2026-05-26 14:47:16.027 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=330
2026-05-26 14:47:19.446 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=65ea66b3-2875-48e7-9b3f-0d1c7d7ca98b
2026-05-26 14:47:29.619 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=15 | mode=full
2026-05-26 14:47:29.620 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=bcaea8c9-5ffb-4659-bae4-cfc6591565e4 | mode=full | segments=2 | review_audio=True
2026-05-26 14:47:32.716 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=bcaea8c9-5ffb-4659-bae4-cfc6591565e4 | mode=full
2026-05-26 14:47:35.148 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 15 READY | mode=full | segments=2
2026-05-26 14:47:35.151 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=17 | mode=full | title=Qui tắc phủ định ( DeMorgan). | chars=36 | estimated_tokens=23 | estimated_audio_seconds=3
2026-05-26 14:47:37.364 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=17 | mode=full | rag=true | tts=true
2026-05-26 14:47:37.366 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=6 | review_chars=379
2026-05-26 14:47:37.367 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=16 | mode=full | main_scripts=6 | review_chars=379
2026-05-26 14:47:37.369 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=16 | mode=full | total_scripts=6
2026-05-26 14:47:37.370 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=16 | mode=full | segment=1/6 | chars=164
2026-05-26 14:47:37.396 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=17 | mode=full | title=Qui tắc phủ định ( DeMorgan). | raw_chars=36
2026-05-26 14:47:37.397 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Qui tắc phủ định ( DeMorgan). | chars=36 | estimated_tokens=23 | estimated_audio_seconds=3
2026-05-26 14:47:37.399 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Qui tắc phủ định ( DeMorgan).
2026-05-26 14:47:37.400 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=36
2026-05-26 14:47:41.808 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=21800da4-23fe-4b6c-9fb5-036195e6c7d4
2026-05-26 14:47:48.530 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=16 | mode=full | segment=1/6 | duration_ms=13320
2026-05-26 14:47:48.534 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=16 | mode=full | segment=2/6 | chars=183
[2026-05-26 14:47:49,598: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:47:50,469: INFO/MainProcess] Task triam.notifications.scan_due[bdac10e1-d428-4bd1-b92f-733cd2370649] received
2026-05-26 14:47:55.093 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=4 | review_chars=388
2026-05-26 14:47:55.094 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=17 | mode=full | main_scripts=4 | review_chars=388
2026-05-26 14:47:55.094 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=17 | mode=full | total_scripts=4
2026-05-26 14:47:55.094 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=17 | mode=full | segment=1/4 | chars=51
2026-05-26 14:47:56.600 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=16 | mode=full | segment=2/6 | duration_ms=14904
2026-05-26 14:47:56.601 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=16 | mode=full | segment=3/6 | chars=220
2026-05-26 14:47:57.200 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=17 | mode=full | segment=1/4 | duration_ms=3480
2026-05-26 14:47:57.201 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=17 | mode=full | segment=2/4 | chars=55
2026-05-26 14:47:58.067 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:47:58,069: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[bdac10e1-d428-4bd1-b92f-733cd2370649] succeeded in 7.596973198000342s: None
2026-05-26 14:47:59.847 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=17 | mode=full | segment=2/4 | duration_ms=3456
2026-05-26 14:47:59.848 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=17 | mode=full | segment=3/4 | chars=55
2026-05-26 14:48:03.719 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=17 | mode=full | segment=3/4 | duration_ms=4104
2026-05-26 14:48:03.720 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=17 | mode=full | segment=4/4 | chars=67
2026-05-26 14:48:05.808 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=16 | mode=full | segment=3/6 | duration_ms=19968
2026-05-26 14:48:05.810 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=16 | mode=full | segment=4/6 | chars=222
2026-05-26 14:48:07.197 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=17 | mode=full | segment=4/4 | duration_ms=3888
2026-05-26 14:48:07.203 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=17 | mode=full | created_segments=4/4
2026-05-26 14:48:07.204 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=17 | mode=full | chars=388
2026-05-26 14:48:19.398 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=16 | mode=full | segment=4/6 | duration_ms=19776
2026-05-26 14:48:19.399 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=16 | mode=full | segment=5/6 | chars=208
2026-05-26 14:48:21.008 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=17 | mode=full
2026-05-26 14:48:21.009 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=21800da4-23fe-4b6c-9fb5-036195e6c7d4 | mode=full | segments=4 | review_audio=True
2026-05-26 14:48:24.129 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=21800da4-23fe-4b6c-9fb5-036195e6c7d4 | mode=full
2026-05-26 14:48:26.554 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 17 READY | mode=full | segments=4
2026-05-26 14:48:26.557 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=18 | mode=full | title=Qui tắc thay đổi thứ tự lượng từ hoá 2 biến. | chars=78 | estimated_tokens=49 | estimated_audio_seconds=10
2026-05-26 14:48:28.772 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=18 | mode=full | rag=true | tts=true
2026-05-26 14:48:28.781 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=18 | mode=full | title=Qui tắc thay đổi thứ tự lượng từ hoá 2 biến. | raw_chars=78
2026-05-26 14:48:28.783 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Qui tắc thay đổi thứ tự lượng từ hoá 2 biến. | chars=78 | estimated_tokens=49 | estimated_audio_seconds=10
2026-05-26 14:48:28.784 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Qui tắc thay đổi thứ tự lượng từ hoá 2 biến.
2026-05-26 14:48:28.785 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=78
2026-05-26 14:48:32.155 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=16 | mode=full | segment=5/6 | duration_ms=16968
2026-05-26 14:48:32.158 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=16 | mode=full | segment=6/6 | chars=222
2026-05-26 14:48:34.424 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=beea2633-45a8-4ed5-acf6-b6f30d42f626
2026-05-26 14:48:39.713 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=16 | mode=full | segment=6/6 | duration_ms=16152
2026-05-26 14:48:39.716 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=16 | mode=full | created_segments=6/6
2026-05-26 14:48:39.717 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=16 | mode=full | chars=379
2026-05-26 14:48:43.835 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=3 | review_chars=250
2026-05-26 14:48:43.836 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=18 | mode=full | main_scripts=3 | review_chars=250
2026-05-26 14:48:43.837 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=18 | mode=full | total_scripts=3
2026-05-26 14:48:43.838 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=18 | mode=full | segment=1/3 | chars=25
2026-05-26 14:48:46.769 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=18 | mode=full | segment=1/3 | duration_ms=5304
2026-05-26 14:48:46.770 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=18 | mode=full | segment=2/3 | chars=25
2026-05-26 14:48:48.013 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=18 | mode=full | segment=2/3 | duration_ms=5304
2026-05-26 14:48:48.014 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=18 | mode=full | segment=3/3 | chars=25
2026-05-26 14:48:48.626 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=18 | mode=full | segment=3/3 | duration_ms=5304
2026-05-26 14:48:48.631 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=18 | mode=full | created_segments=3/3
2026-05-26 14:48:48.631 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=18 | mode=full | chars=250
[2026-05-26 14:48:49,598: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-26 14:48:49.601 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=16 | mode=full
2026-05-26 14:48:49.603 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=65ea66b3-2875-48e7-9b3f-0d1c7d7ca98b | mode=full | segments=6 | review_audio=True
[2026-05-26 14:48:50,255: INFO/MainProcess] Task triam.notifications.scan_due[1d7f5b6a-151a-4dc7-be2e-880eff5b7d45] received
2026-05-26 14:48:52.731 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=65ea66b3-2875-48e7-9b3f-0d1c7d7ca98b | mode=full
2026-05-26 14:48:55.178 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 16 READY | mode=full | segments=6
2026-05-26 14:48:55.182 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=19 | mode=full | title=Qui tắc kéo theo. | chars=16 | estimated_tokens=11 | estimated_audio_seconds=1
2026-05-26 14:48:57.394 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=19 | mode=full | rag=true | tts=true
2026-05-26 14:48:57.402 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=19 | mode=full | title=Qui tắc kéo theo. | raw_chars=16
2026-05-26 14:48:57.403 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Qui tắc kéo theo. | chars=16 | estimated_tokens=11 | estimated_audio_seconds=1
2026-05-26 14:48:57.405 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Qui tắc kéo theo.
2026-05-26 14:48:57.405 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=16
2026-05-26 14:48:57.845 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:48:57,846: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[1d7f5b6a-151a-4dc7-be2e-880eff5b7d45] succeeded in 7.590241148951463s: None
2026-05-26 14:49:01.008 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=2243ceeb-c72c-4a6a-8e0a-037297033318
2026-05-26 14:49:05.148 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=18 | mode=full
2026-05-26 14:49:05.149 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=beea2633-45a8-4ed5-acf6-b6f30d42f626 | mode=full | segments=3 | review_audio=True
2026-05-26 14:49:08.248 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=beea2633-45a8-4ed5-acf6-b6f30d42f626 | mode=full
2026-05-26 14:49:10.680 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 18 READY | mode=full | segments=3
2026-05-26 14:49:10.681 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=20 | mode=full | title=Qui tắc đặc biệt hoá phổ dụng. | chars=59 | estimated_tokens=35 | estimated_audio_seconds=6
2026-05-26 14:49:12.887 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=20 | mode=full | rag=true | tts=true
2026-05-26 14:49:12.891 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=20 | mode=full | title=Qui tắc đặc biệt hoá phổ dụng. | raw_chars=59
2026-05-26 14:49:12.895 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Qui tắc đặc biệt hoá phổ dụng. | chars=59 | estimated_tokens=35 | estimated_audio_seconds=6
2026-05-26 14:49:12.897 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Qui tắc đặc biệt hoá phổ dụng.
2026-05-26 14:49:15.112 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=1 | review_chars=78
2026-05-26 14:49:15.115 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=19 | mode=full | main_scripts=1 | review_chars=78
2026-05-26 14:49:15.118 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=19 | mode=full | total_scripts=1
2026-05-26 14:49:15.120 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=19 | mode=full | segment=1/1 | chars=39
2026-05-26 14:49:15.164 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=59
2026-05-26 14:49:16.338 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=1e0eb3f5-3e6e-43d8-a495-b04a3f41717b
2026-05-26 14:49:17.752 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=19 | mode=full | segment=1/1 | duration_ms=3144
2026-05-26 14:49:17.752 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=19 | mode=full | created_segments=1/1
2026-05-26 14:49:17.754 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=19 | mode=full | chars=78
2026-05-26 14:49:20.244 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=19 | mode=full
2026-05-26 14:49:20.245 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=2243ceeb-c72c-4a6a-8e0a-037297033318 | mode=full | segments=1 | review_audio=True
2026-05-26 14:49:23.193 | INFO     | logging:callHandlers:1762 - 10.16.46.186:5911 - "GET /api/v1/books/4ef0ad48-0e8f-457d-b278-3d3fe3da0905/learning-progress?mode=full HTTP/1.1" 200
2026-05-26 14:49:23.332 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=2243ceeb-c72c-4a6a-8e0a-037297033318 | mode=full
2026-05-26 14:49:25.770 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 19 READY | mode=full | segments=1
2026-05-26 14:49:25.773 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=21 | mode=full | title=Qui tắc tổng quát hoá phổ dụng. | chars=83 | estimated_tokens=47 | estimated_audio_seconds=9
2026-05-26 14:49:27.983 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=21 | mode=full | rag=true | tts=true
2026-05-26 14:49:27.986 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=1 | review_chars=450
2026-05-26 14:49:27.987 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=20 | mode=full | main_scripts=1 | review_chars=450
2026-05-26 14:49:27.987 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=20 | mode=full | total_scripts=1
2026-05-26 14:49:27.988 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=20 | mode=full | segment=1/1 | chars=121
2026-05-26 14:49:28.041 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=21 | mode=full | title=Qui tắc tổng quát hoá phổ dụng. | raw_chars=83
2026-05-26 14:49:28.042 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Qui tắc tổng quát hoá phổ dụng. | chars=83 | estimated_tokens=47 | estimated_audio_seconds=9
2026-05-26 14:49:28.044 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Qui tắc tổng quát hoá phổ dụng.
2026-05-26 14:49:28.044 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=83
2026-05-26 14:49:31.363 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=ec35ab6f-f1c9-4f34-9114-b6f637dbde5c
2026-05-26 14:49:33.282 | INFO     | logging:callHandlers:1762 - 10.16.25.130:28917 - "GET /api/v1/study-contexts HTTP/1.1" 200
2026-05-26 14:49:35.102 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=20 | mode=full | segment=1/1 | duration_ms=9456
2026-05-26 14:49:35.102 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=20 | mode=full | created_segments=1/1
2026-05-26 14:49:35.102 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=20 | mode=full | chars=450
2026-05-26 14:49:37.571 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=1 | review_chars=350
2026-05-26 14:49:37.571 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=21 | mode=full | main_scripts=1 | review_chars=350
2026-05-26 14:49:37.571 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=21 | mode=full | total_scripts=1
2026-05-26 14:49:37.575 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=21 | mode=full | segment=1/1 | chars=125
2026-05-26 14:49:43.879 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=21 | mode=full | segment=1/1 | duration_ms=10224
2026-05-26 14:49:43.880 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=21 | mode=full | created_segments=1/1
2026-05-26 14:49:43.881 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=21 | mode=full | chars=350
[2026-05-26 14:49:49,598: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:49:50,690: INFO/MainProcess] Task triam.notifications.scan_due[5c3703fd-970a-4cf9-af7c-b2ef9a143730] received
2026-05-26 14:49:51.512 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=20 | mode=full
2026-05-26 14:49:51.512 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=1e0eb3f5-3e6e-43d8-a495-b04a3f41717b | mode=full | segments=1 | review_audio=True
2026-05-26 14:49:54.615 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=1e0eb3f5-3e6e-43d8-a495-b04a3f41717b | mode=full
2026-05-26 14:49:57.044 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 20 READY | mode=full | segments=1
2026-05-26 14:49:57.051 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=22 | mode=full | title=Các ví dụ | chars=1954 | estimated_tokens=1152 | estimated_audio_seconds=245
2026-05-26 14:49:58.290 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:49:58,291: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5c3703fd-970a-4cf9-af7c-b2ef9a143730] succeeded in 7.599124344997108s: None
2026-05-26 14:49:59.253 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=22 | mode=full | rag=true | tts=true
2026-05-26 14:49:59.262 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=22 | mode=full | title=Các ví dụ | raw_chars=1954
2026-05-26 14:49:59.265 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Các ví dụ | chars=1954 | estimated_tokens=1152 | estimated_audio_seconds=245
2026-05-26 14:49:59.266 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Các ví dụ
2026-05-26 14:49:59.268 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1954
2026-05-26 14:50:03.140 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=21 | mode=full
2026-05-26 14:50:03.141 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=ec35ab6f-f1c9-4f34-9114-b6f637dbde5c | mode=full | segments=1 | review_audio=True
2026-05-26 14:50:06.238 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=ec35ab6f-f1c9-4f34-9114-b6f637dbde5c | mode=full
2026-05-26 14:50:08.674 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 21 READY | mode=full | segments=1
2026-05-26 14:50:08.676 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=23 | mode=full | title=Ví dụ: | chars=199 | estimated_tokens=113 | estimated_audio_seconds=20
2026-05-26 14:50:10.897 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=23 | mode=full | rag=true | tts=true
2026-05-26 14:50:10.905 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=23 | mode=full | title=Ví dụ: | raw_chars=199
2026-05-26 14:50:10.906 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Ví dụ: | chars=199 | estimated_tokens=113 | estimated_audio_seconds=20
2026-05-26 14:50:10.906 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Ví dụ:
[2026-05-26 14:50:13,124: INFO/ForkPoolWorker-1] Retrying request to /chat/completions in 0.437045 seconds
[2026-05-26 14:50:13,125: INFO/ForkPoolWorker-1] Retrying request to /embeddings in 0.414472 seconds
2026-05-26 14:50:14.337 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=38b37054-3289-4fd7-a11b-f53cd1f03504
2026-05-26 14:50:15.925 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 2 vectors for chapter_id=e4c8823d-4dbf-4c73-bc4b-6fa062507ed8
2026-05-26 14:50:36.486 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=14 | review_chars=581
2026-05-26 14:50:36.490 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=22 | mode=full | main_scripts=14 | review_chars=581
2026-05-26 14:50:36.494 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=22 | mode=full | total_scripts=14
2026-05-26 14:50:36.494 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=22 | mode=full | segment=1/14 | chars=243
2026-05-26 14:50:36.533 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=199
2026-05-26 14:50:42.960 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=2 | review_chars=515
2026-05-26 14:50:42.961 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=23 | mode=full | main_scripts=2 | review_chars=515
2026-05-26 14:50:42.962 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=23 | mode=full | total_scripts=2
2026-05-26 14:50:42.962 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=23 | mode=full | segment=1/2 | chars=198
[2026-05-26 14:50:49,598: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:50:50,255: INFO/MainProcess] Task triam.notifications.scan_due[5ab587b2-bc55-4db5-a5b7-b1e60e2743cc] received
2026-05-26 14:50:51.582 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=22 | mode=full | segment=1/14 | duration_ms=21696
2026-05-26 14:50:51.582 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=22 | mode=full | segment=2/14 | chars=225
2026-05-26 14:50:56.749 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=23 | mode=full | segment=1/2 | duration_ms=15984
2026-05-26 14:50:56.750 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=23 | mode=full | segment=2/2 | chars=177
2026-05-26 14:50:57.858 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:50:57,860: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[5ab587b2-bc55-4db5-a5b7-b1e60e2743cc] succeeded in 7.602214802056551s: None
2026-05-26 14:51:01.607 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=22 | mode=full | segment=2/14 | duration_ms=20088
2026-05-26 14:51:01.609 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=22 | mode=full | segment=3/14 | chars=296
2026-05-26 14:51:07.979 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=23 | mode=full | segment=2/2 | duration_ms=15144
2026-05-26 14:51:07.979 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=23 | mode=full | created_segments=2/2
2026-05-26 14:51:07.985 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=23 | mode=full | chars=515
2026-05-26 14:51:14.819 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=22 | mode=full | segment=3/14 | duration_ms=23232
2026-05-26 14:51:14.831 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=22 | mode=full | segment=4/14 | chars=319
2026-05-26 14:51:28.001 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=23 | mode=full
2026-05-26 14:51:28.004 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=38b37054-3289-4fd7-a11b-f53cd1f03504 | mode=full | segments=2 | review_audio=True
2026-05-26 14:51:31.102 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=38b37054-3289-4fd7-a11b-f53cd1f03504 | mode=full
2026-05-26 14:51:33.528 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 23 READY | mode=full | segments=2
2026-05-26 14:51:33.531 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=24 | mode=full | title=Khái niệm lượng từ | chars=560 | estimated_tokens=295 | estimated_audio_seconds=62
2026-05-26 14:51:35.745 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=24 | mode=full | rag=true | tts=true
2026-05-26 14:51:35.754 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=24 | mode=full | title=Khái niệm lượng từ | raw_chars=560
2026-05-26 14:51:35.757 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Khái niệm lượng từ | chars=560 | estimated_tokens=295 | estimated_audio_seconds=62
2026-05-26 14:51:35.758 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Khái niệm lượng từ
2026-05-26 14:51:35.761 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=560
2026-05-26 14:51:39.382 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=22 | mode=full | segment=4/14 | duration_ms=27960
2026-05-26 14:51:39.383 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=22 | mode=full | segment=5/14 | chars=159
2026-05-26 14:51:40.335 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=bbf4a797-6647-4682-a64c-87556be423d1
2026-05-26 14:51:48.507 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=22 | mode=full | segment=5/14 | duration_ms=13176
2026-05-26 14:51:48.509 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=22 | mode=full | segment=6/14 | chars=340
[2026-05-26 14:51:49,598: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:51:50,472: INFO/MainProcess] Task triam.notifications.scan_due[b272818e-fa7d-4ebd-bffc-983ca051b32d] received
2026-05-26 14:51:52.748 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=7 | review_chars=680
2026-05-26 14:51:52.749 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=24 | mode=full | main_scripts=7 | review_chars=680
2026-05-26 14:51:52.749 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=24 | mode=full | total_scripts=7
2026-05-26 14:51:52.749 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=24 | mode=full | segment=1/7 | chars=155
2026-05-26 14:51:58.078 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:51:58,080: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b272818e-fa7d-4ebd-bffc-983ca051b32d] succeeded in 7.606571862939745s: None
2026-05-26 14:51:58.565 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=24 | mode=full | segment=1/7 | duration_ms=11232
2026-05-26 14:51:58.565 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=24 | mode=full | segment=2/7 | chars=169
2026-05-26 14:52:02.158 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=22 | mode=full | segment=6/14 | duration_ms=24432
2026-05-26 14:52:02.161 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=22 | mode=full | segment=7/14 | chars=473
2026-05-26 14:52:05.177 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=24 | mode=full | segment=2/7 | duration_ms=12480
2026-05-26 14:52:05.178 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=24 | mode=full | segment=3/7 | chars=152
2026-05-26 14:52:11.203 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=24 | mode=full | segment=3/7 | duration_ms=11880
2026-05-26 14:52:11.203 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=24 | mode=full | segment=4/7 | chars=92
2026-05-26 14:52:16.773 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=24 | mode=full | segment=4/7 | duration_ms=6528
2026-05-26 14:52:16.774 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=24 | mode=full | segment=5/7 | chars=155
2026-05-26 14:52:20.641 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=22 | mode=full | segment=7/14 | duration_ms=34512
2026-05-26 14:52:20.642 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=22 | mode=full | segment=8/14 | chars=193
2026-05-26 14:52:23.302 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=24 | mode=full | segment=5/7 | duration_ms=12912
2026-05-26 14:52:23.306 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=24 | mode=full | segment=6/7 | chars=194
2026-05-26 14:52:30.857 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=22 | mode=full | segment=8/14 | duration_ms=13944
2026-05-26 14:52:30.861 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=22 | mode=full | segment=9/14 | chars=229
2026-05-26 14:52:31.983 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=24 | mode=full | segment=6/7 | duration_ms=15768
2026-05-26 14:52:31.986 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=24 | mode=full | segment=7/7 | chars=276
2026-05-26 14:52:41.753 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=22 | mode=full | segment=9/14 | duration_ms=15456
2026-05-26 14:52:41.756 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=22 | mode=full | segment=10/14 | chars=313
2026-05-26 14:52:44.246 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=24 | mode=full | segment=7/7 | duration_ms=19824
2026-05-26 14:52:44.247 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=24 | mode=full | created_segments=7/7
2026-05-26 14:52:44.247 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=24 | mode=full | chars=680
[2026-05-26 14:52:49,600: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:52:50,469: INFO/MainProcess] Task triam.notifications.scan_due[df3cb826-a862-4449-a7fa-d17a05020489] received
2026-05-26 14:52:53.614 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=22 | mode=full | segment=10/14 | duration_ms=22320
2026-05-26 14:52:53.615 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=22 | mode=full | segment=11/14 | chars=311
2026-05-26 14:52:58.058 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:52:58,058: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[df3cb826-a862-4449-a7fa-d17a05020489] succeeded in 7.584396003047004s: None
2026-05-26 14:53:02.737 | INFO     | logging:callHandlers:1762 - 10.16.21.47:27194 - "GET /api/v1/health HTTP/1.1" 200
2026-05-26 14:53:04.566 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=22 | mode=full | segment=11/14 | duration_ms=21936
2026-05-26 14:53:04.567 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=22 | mode=full | segment=12/14 | chars=236
2026-05-26 14:53:07.665 | INFO     | logging:callHandlers:1762 - 10.16.5.171:33112 - "GET /api/v1/books HTTP/1.1" 200
2026-05-26 14:53:09.975 | INFO     | logging:callHandlers:1762 - 10.16.25.130:52913 - "GET /api/v1/study-contexts HTTP/1.1" 200
2026-05-26 14:53:13.628 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=22 | mode=full | segment=12/14 | duration_ms=16752
2026-05-26 14:53:13.629 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=22 | mode=full | segment=13/14 | chars=289
2026-05-26 14:53:18.204 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=24 | mode=full
2026-05-26 14:53:18.204 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=bbf4a797-6647-4682-a64c-87556be423d1 | mode=full | segments=7 | review_audio=True
2026-05-26 14:53:21.375 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=bbf4a797-6647-4682-a64c-87556be423d1 | mode=full
2026-05-26 14:53:23.825 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 24 READY | mode=full | segments=7
2026-05-26 14:53:23.830 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=25 | mode=full | title=Khái niệm | chars=581 | estimated_tokens=314 | estimated_audio_seconds=60
2026-05-26 14:53:25.990 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=25 | mode=full | rag=true | tts=true
2026-05-26 14:53:25.998 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=25 | mode=full | title=Khái niệm | raw_chars=581
2026-05-26 14:53:25.999 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Khái niệm | chars=581 | estimated_tokens=314 | estimated_audio_seconds=60
2026-05-26 14:53:26.000 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Khái niệm
2026-05-26 14:53:26.001 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=581
2026-05-26 14:53:29.320 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=e4680889-17f9-430a-8eac-5e4d0f514f19
2026-05-26 14:53:33.673 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=22 | mode=full | segment=13/14 | duration_ms=21744
2026-05-26 14:53:33.674 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=22 | mode=full | segment=14/14 | chars=271
2026-05-26 14:53:39.640 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=5 | review_chars=544
2026-05-26 14:53:39.642 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=25 | mode=full | main_scripts=5 | review_chars=544
2026-05-26 14:53:39.643 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=25 | mode=full | total_scripts=5
2026-05-26 14:53:39.644 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=25 | mode=full | segment=1/5 | chars=159
2026-05-26 14:53:43.603 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=25 | mode=full | segment=1/5 | duration_ms=8832
2026-05-26 14:53:43.606 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=25 | mode=full | segment=2/5 | chars=199
2026-05-26 14:53:48.867 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=22 | mode=full | segment=14/14 | duration_ms=20136
2026-05-26 14:53:48.868 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=22 | mode=full | created_segments=14/14
2026-05-26 14:53:48.869 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=22 | mode=full | chars=581
[2026-05-26 14:53:49,600: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:53:50,478: INFO/MainProcess] Task triam.notifications.scan_due[79331290-e753-4fab-9745-54daeafdfac8] received
2026-05-26 14:53:52.363 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=25 | mode=full | segment=2/5 | duration_ms=13440
2026-05-26 14:53:52.364 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=25 | mode=full | segment=3/5 | chars=301
2026-05-26 14:53:57.062 | INFO     | logging:callHandlers:1762 - 10.16.46.186:44872 - "GET /api/v1/notifications?limit=5&unread_only=false HTTP/1.1" 200
2026-05-26 14:53:58.130 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:53:58,133: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[79331290-e753-4fab-9745-54daeafdfac8] succeeded in 7.651154111023061s: None
2026-05-26 14:53:58.551 | INFO     | logging:callHandlers:1762 - 10.16.17.88:9293 - "GET /api/v1/notifications/settings HTTP/1.1" 200
2026-05-26 14:54:00.456 | INFO     | logging:callHandlers:1762 - 10.16.5.171:21566 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/details HTTP/1.1" 200
2026-05-26 14:54:02.467 | INFO     | logging:callHandlers:1762 - 10.16.46.186:53487 - "GET /api/v1/books/9a64d766-eb7c-404f-a9e9-9073f11c0030/learning-progress?mode=full HTTP/1.1" 200
2026-05-26 14:54:04.266 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=25 | mode=full | segment=3/5 | duration_ms=19488
2026-05-26 14:54:04.269 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=25 | mode=full | segment=4/5 | chars=81
2026-05-26 14:54:05.244 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=22 | mode=full
2026-05-26 14:54:05.246 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=e4c8823d-4dbf-4c73-bc4b-6fa062507ed8 | mode=full | segments=14 | review_audio=True
2026-05-26 14:54:08.227 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=e4c8823d-4dbf-4c73-bc4b-6fa062507ed8 | mode=full
2026-05-26 14:54:10.570 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 22 READY | mode=full | segments=14
2026-05-26 14:54:10.572 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=26 | mode=full | title=Các phương pháp kiểm tra một luật suy diễn. | chars=163 | estimated_tokens=71 | estimated_audio_seconds=15
2026-05-26 14:54:12.698 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=26 | mode=full | rag=true | tts=true
2026-05-26 14:54:12.708 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=26 | mode=full | title=Các phương pháp kiểm tra một luật suy diễn. | raw_chars=163
2026-05-26 14:54:12.709 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Các phương pháp kiểm tra một luật suy diễn. | chars=163 | estimated_tokens=71 | estimated_audio_seconds=15
2026-05-26 14:54:12.709 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Các phương pháp kiểm tra một luật suy diễn.
2026-05-26 14:54:12.709 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=163
2026-05-26 14:54:15.920 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=b9a25faf-b603-45ee-a0df-f2dc0d046899
2026-05-26 14:54:17.830 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=25 | mode=full | segment=4/5 | duration_ms=6744
2026-05-26 14:54:17.833 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=25 | mode=full | segment=5/5 | chars=135
2026-05-26 14:54:20.552 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=1 | review_chars=497
2026-05-26 14:54:20.553 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=26 | mode=full | main_scripts=1 | review_chars=497
2026-05-26 14:54:20.554 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=26 | mode=full | total_scripts=1
2026-05-26 14:54:20.555 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=26 | mode=full | segment=1/1 | chars=443
2026-05-26 14:54:24.922 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=25 | mode=full | segment=5/5 | duration_ms=10728
2026-05-26 14:54:24.924 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=25 | mode=full | created_segments=5/5
2026-05-26 14:54:24.926 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=25 | mode=full | chars=544
2026-05-26 14:54:31.744 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=26 | mode=full | segment=1/1 | duration_ms=25080
2026-05-26 14:54:31.746 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=26 | mode=full | created_segments=1/1
2026-05-26 14:54:31.748 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=26 | mode=full | chars=497
2026-05-26 14:54:38.364 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=25 | mode=full
2026-05-26 14:54:38.364 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=e4680889-17f9-430a-8eac-5e4d0f514f19 | mode=full | segments=5 | review_audio=True
2026-05-26 14:54:41.338 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=e4680889-17f9-430a-8eac-5e4d0f514f19 | mode=full
2026-05-26 14:54:43.674 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 25 READY | mode=full | segments=5
2026-05-26 14:54:43.675 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=27 | mode=full | title=Các qui tắc suy diễn cơ bản | chars=315 | estimated_tokens=174 | estimated_audio_seconds=28
2026-05-26 14:54:45.803 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=27 | mode=full | rag=true | tts=true
2026-05-26 14:54:45.806 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=27 | mode=full | title=Các qui tắc suy diễn cơ bản | raw_chars=315
2026-05-26 14:54:45.807 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Các qui tắc suy diễn cơ bản | chars=315 | estimated_tokens=174 | estimated_audio_seconds=28
2026-05-26 14:54:45.807 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Các qui tắc suy diễn cơ bản
2026-05-26 14:54:45.807 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=315
2026-05-26 14:54:49.290 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=26 | mode=full
2026-05-26 14:54:49.296 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=b9a25faf-b603-45ee-a0df-f2dc0d046899 | mode=full | segments=1 | review_audio=True
[2026-05-26 14:54:49,601: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:54:50,496: INFO/MainProcess] Task triam.notifications.scan_due[ac5ebca2-903d-43c1-9b9e-036dfb7478cf] received
2026-05-26 14:54:52.278 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=b9a25faf-b603-45ee-a0df-f2dc0d046899 | mode=full
2026-05-26 14:54:54.617 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 26 READY | mode=full | segments=1
2026-05-26 14:54:54.625 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=28 | mode=full | title=Khái niệm: | chars=215 | estimated_tokens=102 | estimated_audio_seconds=22
2026-05-26 14:54:56.749 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=28 | mode=full | rag=true | tts=true
2026-05-26 14:54:57.611 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=48c48c97-a07e-4d46-bb17-cabf4806fdb1
2026-05-26 14:54:57.618 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=28 | mode=full | title=Khái niệm: | raw_chars=215
2026-05-26 14:54:57.621 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Khái niệm: | chars=215 | estimated_tokens=102 | estimated_audio_seconds=22
2026-05-26 14:54:57.624 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Khái niệm:
2026-05-26 14:54:58.106 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:54:58,109: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ac5ebca2-903d-43c1-9b9e-036dfb7478cf] succeeded in 7.610231240047142s: None
2026-05-26 14:55:01.013 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=8aca2f21-443e-4f86-a7ab-bb88e0930f56
2026-05-26 14:55:13.283 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=8 | review_chars=405
2026-05-26 14:55:13.290 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=27 | mode=full | main_scripts=8 | review_chars=405
2026-05-26 14:55:13.291 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=27 | mode=full | total_scripts=8
2026-05-26 14:55:13.292 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=27 | mode=full | segment=1/8 | chars=150
2026-05-26 14:55:13.324 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=215
2026-05-26 14:55:19.173 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=1 | review_chars=416
2026-05-26 14:55:19.174 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=28 | mode=full | main_scripts=1 | review_chars=416
2026-05-26 14:55:19.177 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=28 | mode=full | total_scripts=1
2026-05-26 14:55:19.178 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=28 | mode=full | segment=1/1 | chars=275
2026-05-26 14:55:22.303 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=28 | mode=full | segment=1/1 | duration_ms=240
2026-05-26 14:55:22.303 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=28 | mode=full | created_segments=1/1
2026-05-26 14:55:22.307 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=28 | mode=full | chars=416
2026-05-26 14:55:23.486 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=27 | mode=full | segment=1/8 | duration_ms=11112
2026-05-26 14:55:23.487 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=27 | mode=full | segment=2/8 | chars=161
2026-05-26 14:55:34.254 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=27 | mode=full | segment=2/8 | duration_ms=11688
2026-05-26 14:55:34.254 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=27 | mode=full | segment=3/8 | chars=150
2026-05-26 14:55:40.434 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=27 | mode=full | segment=3/8 | duration_ms=11400
2026-05-26 14:55:40.437 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=27 | mode=full | segment=4/8 | chars=138
2026-05-26 14:55:41.169 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=28 | mode=full
2026-05-26 14:55:41.171 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=8aca2f21-443e-4f86-a7ab-bb88e0930f56 | mode=full | segments=1 | review_audio=True
2026-05-26 14:55:44.149 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=8aca2f21-443e-4f86-a7ab-bb88e0930f56 | mode=full
2026-05-26 14:55:46.494 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 28 READY | mode=full | segments=1
2026-05-26 14:55:46.495 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=29 | mode=full | title=Các ví dụ | chars=2294 | estimated_tokens=1235 | estimated_audio_seconds=228
2026-05-26 14:55:48.620 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=29 | mode=full | rag=true | tts=true
2026-05-26 14:55:48.626 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=29 | mode=full | title=Các ví dụ | raw_chars=2294
2026-05-26 14:55:48.633 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Các ví dụ | chars=2294 | estimated_tokens=1235 | estimated_audio_seconds=228
2026-05-26 14:55:48.635 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Các ví dụ
2026-05-26 14:55:48.636 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=2294
[2026-05-26 14:55:49,601: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:55:50,260: INFO/MainProcess] Task triam.notifications.scan_due[768daca5-a170-4691-ac3f-288458b3776d] received
2026-05-26 14:55:52.150 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 3 vectors for chapter_id=bfe41d68-c13f-415f-86f9-60f3f9da95a2
2026-05-26 14:55:56.630 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=27 | mode=full | segment=4/8 | duration_ms=9792
2026-05-26 14:55:56.633 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=27 | mode=full | segment=5/8 | chars=85
2026-05-26 14:55:57.856 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:55:57,857: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[768daca5-a170-4691-ac3f-288458b3776d] succeeded in 7.582091904012486s: None
2026-05-26 14:56:00.925 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=27 | mode=full | segment=5/8 | duration_ms=6792
2026-05-26 14:56:00.928 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=27 | mode=full | segment=6/8 | chars=95
2026-05-26 14:56:06.354 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=27 | mode=full | segment=6/8 | duration_ms=6744
2026-05-26 14:56:06.355 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=27 | mode=full | segment=7/8 | chars=123
2026-05-26 14:56:11.394 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=27 | mode=full | segment=7/8 | duration_ms=9288
2026-05-26 14:56:11.394 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=27 | mode=full | segment=8/8 | chars=219
2026-05-26 14:56:22.962 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=27 | mode=full | segment=8/8 | duration_ms=15480
2026-05-26 14:56:22.963 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=27 | mode=full | created_segments=8/8
2026-05-26 14:56:22.965 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=27 | mode=full | chars=405
2026-05-26 14:56:25.489 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=11 | review_chars=735
2026-05-26 14:56:25.490 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=29 | mode=full | main_scripts=11 | review_chars=735
2026-05-26 14:56:25.490 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=29 | mode=full | total_scripts=11
2026-05-26 14:56:25.490 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=29 | mode=full | segment=1/11 | chars=283
2026-05-26 14:56:35.317 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=29 | mode=full | segment=1/11 | duration_ms=19080
2026-05-26 14:56:35.320 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=29 | mode=full | segment=2/11 | chars=424
2026-05-26 14:56:36.367 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=27 | mode=full
2026-05-26 14:56:36.369 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=48c48c97-a07e-4d46-bb17-cabf4806fdb1 | mode=full | segments=8 | review_audio=True
2026-05-26 14:56:39.468 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=48c48c97-a07e-4d46-bb17-cabf4806fdb1 | mode=full
2026-05-26 14:56:41.913 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 27 READY | mode=full | segments=8
2026-05-26 14:56:41.914 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=30 | mode=full | title=Nguyên lý qui nạp | chars=3809 | estimated_tokens=2136 | estimated_audio_seconds=375
2026-05-26 14:56:44.104 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=30 | mode=full | rag=true | tts=true
2026-05-26 14:56:44.108 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=30 | mode=full | title=Nguyên lý qui nạp | raw_chars=3809
2026-05-26 14:56:44.113 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Nguyên lý qui nạp | chars=3809 | estimated_tokens=2136 | estimated_audio_seconds=375
2026-05-26 14:56:44.114 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Nguyên lý qui nạp
2026-05-26 14:56:44.115 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=3809
2026-05-26 14:56:48.150 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 4 vectors for chapter_id=6f6ff074-c012-409a-beb8-cce6b0d424f9
[2026-05-26 14:56:49,605: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:56:50,482: INFO/MainProcess] Task triam.notifications.scan_due[47674ec9-e331-4b87-bc6d-c92fa36059f3] received
2026-05-26 14:56:53.474 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=29 | mode=full | segment=2/11 | duration_ms=27984
2026-05-26 14:56:53.476 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=29 | mode=full | segment=3/11 | chars=525
2026-05-26 14:56:58.085 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:56:58,085: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[47674ec9-e331-4b87-bc6d-c92fa36059f3] succeeded in 7.602916734991595s: None
2026-05-26 14:57:11.566 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=29 | mode=full | segment=3/11 | duration_ms=33096
2026-05-26 14:57:11.568 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=29 | mode=full | segment=4/11 | chars=414
2026-05-26 14:57:27.078 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=29 | mode=full | segment=4/11 | duration_ms=23328
2026-05-26 14:57:27.078 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=29 | mode=full | segment=5/11 | chars=463
2026-05-26 14:57:42.471 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=29 | mode=full | segment=5/11 | duration_ms=27144
2026-05-26 14:57:42.473 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=29 | mode=full | segment=6/11 | chars=631
2026-05-26 14:57:44.743 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=22 | review_chars=731
2026-05-26 14:57:44.744 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=30 | mode=full | main_scripts=22 | review_chars=731
2026-05-26 14:57:44.745 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=30 | mode=full | total_scripts=22
2026-05-26 14:57:44.746 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=1/22 | chars=306
[2026-05-26 14:57:49,605: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:57:50,659: INFO/MainProcess] Task triam.notifications.scan_due[0dbda4d9-ef03-4576-aa73-794a542c7f6c] received
2026-05-26 14:57:58.256 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:57:58,257: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[0dbda4d9-ef03-4576-aa73-794a542c7f6c] succeeded in 7.593539273948409s: None
2026-05-26 14:57:59.154 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=1/22 | duration_ms=22536
2026-05-26 14:57:59.157 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=2/22 | chars=221
2026-05-26 14:58:06.925 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=2/22 | duration_ms=13680
2026-05-26 14:58:06.926 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=3/22 | chars=250
2026-05-26 14:58:12.716 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=29 | mode=full | segment=6/11 | duration_ms=40848
2026-05-26 14:58:12.716 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=29 | mode=full | segment=7/11 | chars=360
2026-05-26 14:58:17.122 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=3/22 | duration_ms=15240
2026-05-26 14:58:17.128 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=4/22 | chars=318
2026-05-26 14:58:27.320 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=4/22 | duration_ms=21432
2026-05-26 14:58:27.323 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=5/22 | chars=322
2026-05-26 14:58:30.458 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=29 | mode=full | segment=7/11 | duration_ms=24144
2026-05-26 14:58:30.461 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=29 | mode=full | segment=8/11 | chars=624
2026-05-26 14:58:38.475 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=5/22 | duration_ms=20472
2026-05-26 14:58:38.476 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=6/22 | chars=501
2026-05-26 14:58:44.217 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=29 | mode=full | segment=8/11 | duration_ms=37824
2026-05-26 14:58:44.218 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=29 | mode=full | segment=9/11 | chars=839
[2026-05-26 14:58:49,605: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:58:50,481: INFO/MainProcess] Task triam.notifications.scan_due[f8f8a137-2d11-433f-ade0-e939b52353f5] received
2026-05-26 14:58:54.543 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=6/22 | duration_ms=29832
2026-05-26 14:58:54.548 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=7/22 | chars=596
2026-05-26 14:58:58.073 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:58:58,073: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f8f8a137-2d11-433f-ade0-e939b52353f5] succeeded in 7.590816008974798s: None
2026-05-26 14:59:03.968 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=29 | mode=full | segment=9/11 | duration_ms=53832
2026-05-26 14:59:03.968 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=29 | mode=full | segment=10/11 | chars=519
2026-05-26 14:59:13.039 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=7/22 | duration_ms=34464
2026-05-26 14:59:13.039 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=8/22 | chars=427
2026-05-26 14:59:23.255 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=8/22 | duration_ms=27024
2026-05-26 14:59:23.258 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=9/22 | chars=790
2026-05-26 14:59:26.091 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=29 | mode=full | segment=10/11 | duration_ms=35208
2026-05-26 14:59:26.093 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=29 | mode=full | segment=11/11 | chars=671
2026-05-26 14:59:46.836 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=29 | mode=full | segment=11/11 | duration_ms=44712
2026-05-26 14:59:46.839 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=29 | mode=full | created_segments=11/11
2026-05-26 14:59:46.839 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=29 | mode=full | chars=735
2026-05-26 14:59:47.935 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=9/22 | duration_ms=48576
2026-05-26 14:59:47.938 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=10/22 | chars=245
[2026-05-26 14:59:49,609: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 14:59:50,487: INFO/MainProcess] Task triam.notifications.scan_due[c88b207f-4583-4d9c-a10e-4630463749fc] received
2026-05-26 14:59:57.561 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=10/22 | duration_ms=17136
2026-05-26 14:59:57.562 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=11/22 | chars=638
2026-05-26 14:59:58.316 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 14:59:58,316: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c88b207f-4583-4d9c-a10e-4630463749fc] succeeded in 7.60875934897922s: None
2026-05-26 15:00:05.374 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=29 | mode=full
2026-05-26 15:00:05.375 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=bfe41d68-c13f-415f-86f9-60f3f9da95a2 | mode=full | segments=11 | review_audio=True
2026-05-26 15:00:09.770 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=bfe41d68-c13f-415f-86f9-60f3f9da95a2 | mode=full
2026-05-26 15:00:12.187 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 29 READY | mode=full | segments=11
2026-05-26 15:00:12.193 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=31 | mode=full | title=C: "Tôi vô tội" | chars=1740 | estimated_tokens=961 | estimated_audio_seconds=186
2026-05-26 15:00:14.397 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=31 | mode=full | rag=true | tts=true
2026-05-26 15:00:14.406 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=31 | mode=full | title=C: "Tôi vô tội" | raw_chars=1740
2026-05-26 15:00:14.408 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=C: "Tôi vô tội" | chars=1740 | estimated_tokens=961 | estimated_audio_seconds=186
2026-05-26 15:00:14.410 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=C: "Tôi vô tội"
2026-05-26 15:00:14.411 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1740
2026-05-26 15:00:18.298 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 2 vectors for chapter_id=db3ff3dc-b632-4c27-8c8d-d03ff74f5cf9
2026-05-26 15:00:41.171 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=11/22 | duration_ms=42648
2026-05-26 15:00:41.172 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=12/22 | chars=334
2026-05-26 15:00:49.189 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=15 | review_chars=818
2026-05-26 15:00:49.191 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=31 | mode=full | main_scripts=15 | review_chars=818
2026-05-26 15:00:49.194 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=31 | mode=full | total_scripts=15
2026-05-26 15:00:49.195 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=31 | mode=full | segment=1/15 | chars=301
[2026-05-26 15:00:49,610: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:00:50,271: INFO/MainProcess] Task triam.notifications.scan_due[53aebfe0-25eb-44a8-bfbc-f707a8673867] received
2026-05-26 15:00:57.544 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=12/22 | duration_ms=20520
2026-05-26 15:00:57.545 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=13/22 | chars=430
2026-05-26 15:00:57.862 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:00:57,866: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[53aebfe0-25eb-44a8-bfbc-f707a8673867] succeeded in 7.592853487934917s: None
2026-05-26 15:01:05.932 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=31 | mode=full | segment=1/15 | duration_ms=20448
2026-05-26 15:01:05.933 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=31 | mode=full | segment=2/15 | chars=366
2026-05-26 15:01:10.950 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=13/22 | duration_ms=27336
2026-05-26 15:01:10.959 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=14/22 | chars=424
2026-05-26 15:01:20.385 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=31 | mode=full | segment=2/15 | duration_ms=22440
2026-05-26 15:01:20.391 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=31 | mode=full | segment=3/15 | chars=497
2026-05-26 15:01:33.541 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=14/22 | duration_ms=27168
2026-05-26 15:01:33.541 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=15/22 | chars=419
[2026-05-26 15:01:49,611: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-26 15:01:49.921 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=15/22 | duration_ms=26664
2026-05-26 15:01:49.923 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=16/22 | chars=348
[2026-05-26 15:01:50,784: INFO/MainProcess] Task triam.notifications.scan_due[57f2401a-8e6e-44b4-9cc7-741c3971618b] received
2026-05-26 15:01:50.925 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=31 | mode=full | segment=3/15 | duration_ms=34200
2026-05-26 15:01:50.925 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=31 | mode=full | segment=4/15 | chars=464
2026-05-26 15:01:58.367 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:01:58,369: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[57f2401a-8e6e-44b4-9cc7-741c3971618b] succeeded in 7.583695937064476s: None
2026-05-26 15:01:59.728 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=16/22 | duration_ms=22248
2026-05-26 15:01:59.729 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=17/22 | chars=733
2026-05-26 15:02:03.806 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=31 | mode=full | segment=4/15 | duration_ms=30624
2026-05-26 15:02:03.808 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=31 | mode=full | segment=5/15 | chars=435
2026-05-26 15:02:16.810 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=31 | mode=full | segment=5/15 | duration_ms=30576
2026-05-26 15:02:16.813 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=31 | mode=full | segment=6/15 | chars=248
2026-05-26 15:02:24.214 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=31 | mode=full | segment=6/15 | duration_ms=18792
2026-05-26 15:02:24.214 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=31 | mode=full | segment=7/15 | chars=434
2026-05-26 15:02:27.172 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=17/22 | duration_ms=51936
2026-05-26 15:02:27.172 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=18/22 | chars=403
2026-05-26 15:02:41.129 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=31 | mode=full | segment=7/15 | duration_ms=29640
2026-05-26 15:02:41.131 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=31 | mode=full | segment=8/15 | chars=431
2026-05-26 15:02:42.218 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=18/22 | duration_ms=25584
2026-05-26 15:02:42.221 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=19/22 | chars=524
[2026-05-26 15:02:49,611: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:02:50,536: INFO/MainProcess] Task triam.notifications.scan_due[a8b7ce2e-29d4-443a-9054-bdfe73da788d] received
2026-05-26 15:02:54.261 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=31 | mode=full | segment=8/15 | duration_ms=32472
2026-05-26 15:02:54.261 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=31 | mode=full | segment=9/15 | chars=455
2026-05-26 15:02:56.592 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=19/22 | duration_ms=31608
2026-05-26 15:02:56.593 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=20/22 | chars=276
2026-05-26 15:02:58.156 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:02:58,157: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a8b7ce2e-29d4-443a-9054-bdfe73da788d] succeeded in 7.619557828991674s: None
2026-05-26 15:03:09.184 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=31 | mode=full | segment=9/15 | duration_ms=32856
2026-05-26 15:03:09.186 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=31 | mode=full | segment=10/15 | chars=331
2026-05-26 15:03:11.053 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=20/22 | duration_ms=19584
2026-05-26 15:03:11.056 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=21/22 | chars=538
2026-05-26 15:03:22.244 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=31 | mode=full | segment=10/15 | duration_ms=22464
2026-05-26 15:03:22.250 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=31 | mode=full | segment=11/15 | chars=284
2026-05-26 15:03:30.659 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=31 | mode=full | segment=11/15 | duration_ms=17784
2026-05-26 15:03:30.663 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=31 | mode=full | segment=12/15 | chars=469
2026-05-26 15:03:32.687 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=21/22 | duration_ms=36336
2026-05-26 15:03:32.688 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=30 | mode=full | segment=22/22 | chars=210
2026-05-26 15:03:41.238 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=30 | mode=full | segment=22/22 | duration_ms=15456
2026-05-26 15:03:41.240 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=30 | mode=full | created_segments=22/22
2026-05-26 15:03:41.240 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=30 | mode=full | chars=731
[2026-05-26 15:03:49,612: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:03:50,494: INFO/MainProcess] Task triam.notifications.scan_due[30746776-e083-4452-bfdc-ace8d6ad28e0] received
2026-05-26 15:03:54.005 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=31 | mode=full | segment=12/15 | duration_ms=32208
2026-05-26 15:03:54.006 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=31 | mode=full | segment=13/15 | chars=365
2026-05-26 15:03:58.093 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:03:58,094: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[30746776-e083-4452-bfdc-ace8d6ad28e0] succeeded in 7.59932580194436s: None
2026-05-26 15:04:04.012 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=30 | mode=full
2026-05-26 15:04:04.013 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=6f6ff074-c012-409a-beb8-cce6b0d424f9 | mode=full | segments=22 | review_audio=True
2026-05-26 15:04:07.327 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=6f6ff074-c012-409a-beb8-cce6b0d424f9 | mode=full
2026-05-26 15:04:09.741 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 30 READY | mode=full | segments=22
2026-05-26 15:04:09.745 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=32 | mode=full | title=Ví dụ | chars=74 | estimated_tokens=41 | estimated_audio_seconds=8
2026-05-26 15:04:11.934 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=32 | mode=full | rag=true | tts=true
2026-05-26 15:04:11.941 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=32 | mode=full | title=Ví dụ | raw_chars=74
2026-05-26 15:04:11.944 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Ví dụ | chars=74 | estimated_tokens=41 | estimated_audio_seconds=8
2026-05-26 15:04:11.944 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Ví dụ
2026-05-26 15:04:11.946 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=74
2026-05-26 15:04:15.442 | WARNING  | app.services.storage_service:upload_file_to_supabase:57 - Upload failed (attempt 1/3), retrying in 1s...
2026-05-26 15:04:16.340 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=018153a2-69c0-4b13-a651-98cefe6bfd52
2026-05-26 15:04:17.896 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=31 | mode=full | segment=13/15 | duration_ms=24432
2026-05-26 15:04:17.897 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=31 | mode=full | segment=14/15 | chars=288
2026-05-26 15:04:22.875 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=1 | review_chars=272
2026-05-26 15:04:22.876 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=32 | mode=full | main_scripts=1 | review_chars=272
2026-05-26 15:04:22.876 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=32 | mode=full | total_scripts=1
2026-05-26 15:04:22.881 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=32 | mode=full | segment=1/1 | chars=254
2026-05-26 15:04:25.803 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=31 | mode=full | segment=14/15 | duration_ms=20016
2026-05-26 15:04:25.803 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=31 | mode=full | segment=15/15 | chars=326
2026-05-26 15:04:35.119 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=31 | mode=full | segment=15/15 | duration_ms=22776
2026-05-26 15:04:35.120 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=31 | mode=full | created_segments=15/15
2026-05-26 15:04:35.122 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=31 | mode=full | chars=818
2026-05-26 15:04:46.170 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=32 | mode=full | segment=1/1 | duration_ms=18288
2026-05-26 15:04:46.172 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=32 | mode=full | created_segments=1/1
2026-05-26 15:04:46.173 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=32 | mode=full | chars=272
[2026-05-26 15:04:49,613: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:04:50,494: INFO/MainProcess] Task triam.notifications.scan_due[d115dadf-5fa1-49db-b22b-d5cf25395cc1] received
2026-05-26 15:04:57.346 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=32 | mode=full
2026-05-26 15:04:57.347 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=018153a2-69c0-4b13-a651-98cefe6bfd52 | mode=full | segments=1 | review_audio=True
2026-05-26 15:04:58.091 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:04:58,093: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d115dadf-5fa1-49db-b22b-d5cf25395cc1] succeeded in 7.595947634079494s: None
2026-05-26 15:05:00.450 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=018153a2-69c0-4b13-a651-98cefe6bfd52 | mode=full
2026-05-26 15:05:02.986 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 32 READY | mode=full | segments=1
2026-05-26 15:05:02.991 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=33 | mode=full | title=Cộng | chars=156 | estimated_tokens=91 | estimated_audio_seconds=13
2026-05-26 15:05:05.192 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=33 | mode=full | rag=true | tts=true
2026-05-26 15:05:05.200 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=33 | mode=full | title=Cộng | raw_chars=156
2026-05-26 15:05:05.201 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Cộng | chars=156 | estimated_tokens=91 | estimated_audio_seconds=13
2026-05-26 15:05:05.202 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Cộng
2026-05-26 15:05:05.202 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=156
2026-05-26 15:05:08.791 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=31 | mode=full
2026-05-26 15:05:08.793 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=db3ff3dc-b632-4c27-8c8d-d03ff74f5cf9 | mode=full | segments=15 | review_audio=True
2026-05-26 15:05:11.888 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=db3ff3dc-b632-4c27-8c8d-d03ff74f5cf9 | mode=full
2026-05-26 15:05:14.300 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 31 READY | mode=full | segments=15
2026-05-26 15:05:14.306 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=34 | mode=full | title=Nhân | chars=408 | estimated_tokens=232 | estimated_audio_seconds=38
2026-05-26 15:05:16.497 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=34 | mode=full | rag=true | tts=true
2026-05-26 15:05:16.502 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=34 | mode=full | title=Nhân | raw_chars=408
2026-05-26 15:05:16.505 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Nhân | chars=408 | estimated_tokens=232 | estimated_audio_seconds=38
2026-05-26 15:05:16.506 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Nhân
[2026-05-26 15:05:18,706: INFO/ForkPoolWorker-1] Retrying request to /chat/completions in 0.401850 seconds
2026-05-26 15:05:19.850 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=57a9925c-95be-4938-80e5-8af26a0b305f
2026-05-26 15:05:20.532 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=0faed9da-5a32-45b6-93f3-0b602a31f4df
2026-05-26 15:05:28.622 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=3 | review_chars=507
2026-05-26 15:05:28.623 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=33 | mode=full | main_scripts=3 | review_chars=507
2026-05-26 15:05:28.624 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=33 | mode=full | total_scripts=3
2026-05-26 15:05:28.624 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=33 | mode=full | segment=1/3 | chars=254
2026-05-26 15:05:28.653 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=408
2026-05-26 15:05:37.045 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=33 | mode=full | segment=1/3 | duration_ms=15936
2026-05-26 15:05:37.046 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=33 | mode=full | segment=2/3 | chars=397
2026-05-26 15:05:40.371 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=4 | review_chars=526
2026-05-26 15:05:40.372 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=34 | mode=full | main_scripts=4 | review_chars=526
2026-05-26 15:05:40.374 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=34 | mode=full | total_scripts=4
2026-05-26 15:05:40.375 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=34 | mode=full | segment=1/4 | chars=216
2026-05-26 15:05:45.911 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=34 | mode=full | segment=1/4 | duration_ms=13296
2026-05-26 15:05:45.912 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=34 | mode=full | segment=2/4 | chars=368
[2026-05-26 15:05:49,615: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:05:50,277: INFO/MainProcess] Task triam.notifications.scan_due[9022c9bc-764e-4e3b-8fc9-3090808562f0] received
2026-05-26 15:05:51.074 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=33 | mode=full | segment=2/3 | duration_ms=27000
2026-05-26 15:05:51.075 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=33 | mode=full | segment=3/3 | chars=227
2026-05-26 15:05:57.936 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:05:57,937: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[9022c9bc-764e-4e3b-8fc9-3090808562f0] succeeded in 7.659269573981874s: None
2026-05-26 15:06:00.065 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=34 | mode=full | segment=2/4 | duration_ms=23856
2026-05-26 15:06:00.066 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=34 | mode=full | segment=3/4 | chars=482
2026-05-26 15:06:02.189 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=33 | mode=full | segment=3/3 | duration_ms=14376
2026-05-26 15:06:02.192 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=33 | mode=full | created_segments=3/3
2026-05-26 15:06:02.193 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=33 | mode=full | chars=507
2026-05-26 15:06:11.576 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=34 | mode=full | segment=3/4 | duration_ms=27792
2026-05-26 15:06:11.576 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=34 | mode=full | segment=4/4 | chars=293
2026-05-26 15:06:15.498 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=33 | mode=full
2026-05-26 15:06:15.499 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=0faed9da-5a32-45b6-93f3-0b602a31f4df | mode=full | segments=3 | review_audio=True
2026-05-26 15:06:18.606 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=0faed9da-5a32-45b6-93f3-0b602a31f4df | mode=full
2026-05-26 15:06:21.032 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 33 READY | mode=full | segments=3
2026-05-26 15:06:21.039 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=35 | mode=full | title=Định nghĩa | chars=240 | estimated_tokens=124 | estimated_audio_seconds=28
2026-05-26 15:06:23.232 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=35 | mode=full | rag=true | tts=true
2026-05-26 15:06:23.235 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=35 | mode=full | title=Định nghĩa | raw_chars=240
2026-05-26 15:06:23.237 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Định nghĩa | chars=240 | estimated_tokens=124 | estimated_audio_seconds=28
2026-05-26 15:06:23.239 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Định nghĩa
2026-05-26 15:06:23.240 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=240
2026-05-26 15:06:26.177 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=34 | mode=full | segment=4/4 | duration_ms=19368
2026-05-26 15:06:26.177 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=34 | mode=full | created_segments=4/4
2026-05-26 15:06:26.178 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=34 | mode=full | chars=526
2026-05-26 15:06:27.135 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=5102f772-3145-4f58-93eb-4094dfef1ee7
2026-05-26 15:06:36.142 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=3 | review_chars=534
2026-05-26 15:06:36.144 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=35 | mode=full | main_scripts=3 | review_chars=534
2026-05-26 15:06:36.145 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=35 | mode=full | total_scripts=3
2026-05-26 15:06:36.145 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=35 | mode=full | segment=1/3 | chars=229
2026-05-26 15:06:39.412 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=34 | mode=full
2026-05-26 15:06:39.413 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=57a9925c-95be-4938-80e5-8af26a0b305f | mode=full | segments=4 | review_audio=True
2026-05-26 15:06:42.486 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=57a9925c-95be-4938-80e5-8af26a0b305f | mode=full
2026-05-26 15:06:44.910 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 34 READY | mode=full | segments=4
2026-05-26 15:06:44.915 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=36 | mode=full | title=Các khái niệm về tính chất (phép toán 2 ngôi). | chars=683 | estimated_tokens=384 | estimated_audio_seconds=70
2026-05-26 15:06:47.106 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=36 | mode=full | rag=true | tts=true
2026-05-26 15:06:47.120 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=36 | mode=full | title=Các khái niệm về tính chất (phép toán 2 ngôi). | raw_chars=683
2026-05-26 15:06:47.132 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Các khái niệm về tính chất (phép toán 2 ngôi). | chars=683 | estimated_tokens=384 | estimated_audio_seconds=70
2026-05-26 15:06:47.134 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Các khái niệm về tính chất (phép toán 2 ngôi).
2026-05-26 15:06:47.134 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=683
[2026-05-26 15:06:49,616: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-26 15:06:50.436 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=35 | mode=full | segment=1/3 | duration_ms=15624
2026-05-26 15:06:50.436 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=35 | mode=full | segment=2/3 | chars=216
[2026-05-26 15:06:50,493: INFO/MainProcess] Task triam.notifications.scan_due[660092e0-eb8d-424f-9cb0-18c1e2ff8876] received
2026-05-26 15:06:51.894 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=425feba5-11ae-44b5-b5b8-054cca885677
2026-05-26 15:06:58.099 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:06:58,102: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[660092e0-eb8d-424f-9cb0-18c1e2ff8876] succeeded in 7.605812317924574s: None
2026-05-26 15:07:00.289 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=35 | mode=full | segment=2/3 | duration_ms=16704
2026-05-26 15:07:00.292 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=35 | mode=full | segment=3/3 | chars=247
2026-05-26 15:07:01.479 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=5 | review_chars=681
2026-05-26 15:07:01.481 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=36 | mode=full | main_scripts=5 | review_chars=681
2026-05-26 15:07:01.482 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=36 | mode=full | total_scripts=5
2026-05-26 15:07:01.484 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=36 | mode=full | segment=1/5 | chars=262
2026-05-26 15:07:10.054 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=36 | mode=full | segment=1/5 | duration_ms=16032
2026-05-26 15:07:10.055 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=36 | mode=full | segment=2/5 | chars=210
2026-05-26 15:07:13.110 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=35 | mode=full | segment=3/3 | duration_ms=20376
2026-05-26 15:07:13.112 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=35 | mode=full | created_segments=3/3
2026-05-26 15:07:13.113 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=35 | mode=full | chars=534
2026-05-26 15:07:15.949 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=36 | mode=full | segment=2/5 | duration_ms=13680
2026-05-26 15:07:15.951 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=36 | mode=full | segment=3/5 | chars=328
2026-05-26 15:07:26.870 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=35 | mode=full
2026-05-26 15:07:26.871 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=5102f772-3145-4f58-93eb-4094dfef1ee7 | mode=full | segments=3 | review_audio=True
2026-05-26 15:07:29.945 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=5102f772-3145-4f58-93eb-4094dfef1ee7 | mode=full
2026-05-26 15:07:32.364 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 35 READY | mode=full | segments=3
2026-05-26 15:07:32.368 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=37 | mode=full | title=Khái niệm đại số | chars=93 | estimated_tokens=50 | estimated_audio_seconds=10
2026-05-26 15:07:34.562 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=37 | mode=full | rag=true | tts=true
2026-05-26 15:07:34.569 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=37 | mode=full | title=Khái niệm đại số | raw_chars=93
2026-05-26 15:07:34.571 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Khái niệm đại số | chars=93 | estimated_tokens=50 | estimated_audio_seconds=10
2026-05-26 15:07:34.572 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Khái niệm đại số
2026-05-26 15:07:34.572 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=93
2026-05-26 15:07:37.756 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=36 | mode=full | segment=3/5 | duration_ms=19176
2026-05-26 15:07:37.762 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=36 | mode=full | segment=4/5 | chars=340
2026-05-26 15:07:38.953 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=3beeda57-7be1-4f01-b377-5a09fe5615a0
2026-05-26 15:07:44.738 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=1 | review_chars=469
2026-05-26 15:07:44.744 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=37 | mode=full | main_scripts=1 | review_chars=469
2026-05-26 15:07:44.751 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=37 | mode=full | total_scripts=1
2026-05-26 15:07:44.752 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=37 | mode=full | segment=1/1 | chars=198
2026-05-26 15:07:47.081 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=36 | mode=full | segment=4/5 | duration_ms=22632
2026-05-26 15:07:47.084 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=36 | mode=full | segment=5/5 | chars=301
[2026-05-26 15:07:49,629: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:07:50,504: INFO/MainProcess] Task triam.notifications.scan_due[b301e994-53fb-49ee-a6ff-2514129e4fd3] received
2026-05-26 15:07:52.736 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=37 | mode=full | segment=1/1 | duration_ms=13776
2026-05-26 15:07:52.737 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=37 | mode=full | created_segments=1/1
2026-05-26 15:07:52.739 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=37 | mode=full | chars=469
2026-05-26 15:07:58.106 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:07:58,108: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b301e994-53fb-49ee-a6ff-2514129e4fd3] succeeded in 7.601255182991736s: None
2026-05-26 15:08:01.220 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=36 | mode=full | segment=5/5 | duration_ms=22920
2026-05-26 15:08:01.221 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=36 | mode=full | created_segments=5/5
2026-05-26 15:08:01.221 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=36 | mode=full | chars=681
2026-05-26 15:08:07.585 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=37 | mode=full
2026-05-26 15:08:07.586 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=3beeda57-7be1-4f01-b377-5a09fe5615a0 | mode=full | segments=1 | review_audio=True
2026-05-26 15:08:10.655 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=3beeda57-7be1-4f01-b377-5a09fe5615a0 | mode=full
2026-05-26 15:08:13.069 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 37 READY | mode=full | segments=1
2026-05-26 15:08:13.072 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=38 | mode=full | title=Một số ví dụ | chars=784 | estimated_tokens=440 | estimated_audio_seconds=83
2026-05-26 15:08:15.260 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=38 | mode=full | rag=true | tts=true
2026-05-26 15:08:15.264 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=38 | mode=full | title=Một số ví dụ | raw_chars=784
2026-05-26 15:08:15.281 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Một số ví dụ | chars=784 | estimated_tokens=440 | estimated_audio_seconds=83
2026-05-26 15:08:15.282 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Một số ví dụ
2026-05-26 15:08:15.282 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=784
2026-05-26 15:08:18.989 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=36 | mode=full
2026-05-26 15:08:18.989 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=425feba5-11ae-44b5-b5b8-054cca885677 | mode=full | segments=5 | review_audio=True
2026-05-26 15:08:22.063 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=425feba5-11ae-44b5-b5b8-054cca885677 | mode=full
2026-05-26 15:08:24.473 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 36 READY | mode=full | segments=5
2026-05-26 15:08:24.483 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=39 | mode=full | title=Định nghĩa | chars=365 | estimated_tokens=205 | estimated_audio_seconds=39
2026-05-26 15:08:26.676 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=39 | mode=full | rag=true | tts=true
2026-05-26 15:08:27.565 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=3f4cf89e-5fd9-4aae-8de1-0a1f936b9dfb
2026-05-26 15:08:27.567 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=39 | mode=full | title=Định nghĩa | raw_chars=365
2026-05-26 15:08:27.568 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Định nghĩa | chars=365 | estimated_tokens=205 | estimated_audio_seconds=39
2026-05-26 15:08:27.569 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Định nghĩa
2026-05-26 15:08:30.592 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=b252ff81-5981-41b8-b4ee-c19449e4af69
2026-05-26 15:08:31.696 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=6 | review_chars=645
2026-05-26 15:08:31.697 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=38 | mode=full | main_scripts=6 | review_chars=645
2026-05-26 15:08:31.698 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=38 | mode=full | total_scripts=6
2026-05-26 15:08:31.699 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=38 | mode=full | segment=1/6 | chars=366
2026-05-26 15:08:31.732 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=365
2026-05-26 15:08:44.029 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=38 | mode=full | segment=1/6 | duration_ms=24528
2026-05-26 15:08:44.033 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=38 | mode=full | segment=2/6 | chars=128
2026-05-26 15:08:47.411 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=6 | review_chars=515
2026-05-26 15:08:47.411 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=39 | mode=full | main_scripts=6 | review_chars=515
2026-05-26 15:08:47.412 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=39 | mode=full | total_scripts=6
2026-05-26 15:08:47.412 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=39 | mode=full | segment=1/6 | chars=300
2026-05-26 15:08:48.203 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=38 | mode=full | segment=2/6 | duration_ms=8256
2026-05-26 15:08:48.211 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=38 | mode=full | segment=3/6 | chars=423
[2026-05-26 15:08:49,629: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:08:50,504: INFO/MainProcess] Task triam.notifications.scan_due[e630cbbf-be2c-4fc1-a437-94cc1f993b61] received
2026-05-26 15:08:56.421 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=39 | mode=full | segment=1/6 | duration_ms=20256
2026-05-26 15:08:56.421 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=39 | mode=full | segment=2/6 | chars=260
2026-05-26 15:08:58.077 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:08:58,078: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e630cbbf-be2c-4fc1-a437-94cc1f993b61] succeeded in 7.573038544971496s: None
2026-05-26 15:09:02.703 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=38 | mode=full | segment=3/6 | duration_ms=32088
2026-05-26 15:09:02.711 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=38 | mode=full | segment=4/6 | chars=387
2026-05-26 15:09:05.858 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=39 | mode=full | segment=2/6 | duration_ms=18600
2026-05-26 15:09:05.860 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=39 | mode=full | segment=3/6 | chars=342
2026-05-26 15:09:16.815 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=39 | mode=full | segment=3/6 | duration_ms=20112
2026-05-26 15:09:16.818 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=39 | mode=full | segment=4/6 | chars=421
2026-05-26 15:09:21.419 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=38 | mode=full | segment=4/6 | duration_ms=27888
2026-05-26 15:09:21.420 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=38 | mode=full | segment=5/6 | chars=337
2026-05-26 15:09:30.299 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=39 | mode=full | segment=4/6 | duration_ms=25056
2026-05-26 15:09:30.299 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=39 | mode=full | segment=5/6 | chars=162
2026-05-26 15:09:31.058 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=38 | mode=full | segment=5/6 | duration_ms=25008
2026-05-26 15:09:31.059 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=38 | mode=full | segment=6/6 | chars=347
2026-05-26 15:09:38.676 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=39 | mode=full | segment=5/6 | duration_ms=12336
2026-05-26 15:09:38.678 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=39 | mode=full | segment=6/6 | chars=218
2026-05-26 15:09:46.186 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=38 | mode=full | segment=6/6 | duration_ms=27240
2026-05-26 15:09:46.187 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=38 | mode=full | created_segments=6/6
2026-05-26 15:09:46.188 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=38 | mode=full | chars=645
2026-05-26 15:09:47.100 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=39 | mode=full | segment=6/6 | duration_ms=15336
2026-05-26 15:09:47.102 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=39 | mode=full | created_segments=6/6
2026-05-26 15:09:47.102 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=39 | mode=full | chars=515
[2026-05-26 15:09:49,629: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:09:50,510: INFO/MainProcess] Task triam.notifications.scan_due[2dbeba64-a78e-4166-8d8e-2c6044df7993] received
2026-05-26 15:09:58.097 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:09:58,097: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2dbeba64-a78e-4166-8d8e-2c6044df7993] succeeded in 7.586309195961803s: None
2026-05-26 15:09:58.289 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=39 | mode=full
2026-05-26 15:09:58.290 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=b252ff81-5981-41b8-b4ee-c19449e4af69 | mode=full | segments=6 | review_audio=True
2026-05-26 15:10:01.361 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=b252ff81-5981-41b8-b4ee-c19449e4af69 | mode=full
2026-05-26 15:10:03.778 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 39 READY | mode=full | segments=6
2026-05-26 15:10:03.786 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=40 | mode=full | title=Các tính chất đại số Boole | chars=536 | estimated_tokens=304 | estimated_audio_seconds=62
2026-05-26 15:10:05.974 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=40 | mode=full | rag=true | tts=true
2026-05-26 15:10:05.982 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=40 | mode=full | title=Các tính chất đại số Boole | raw_chars=536
2026-05-26 15:10:05.984 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Các tính chất đại số Boole | chars=536 | estimated_tokens=304 | estimated_audio_seconds=62
2026-05-26 15:10:05.986 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Các tính chất đại số Boole
2026-05-26 15:10:05.987 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=536
2026-05-26 15:10:09.545 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=38 | mode=full
2026-05-26 15:10:09.546 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=3f4cf89e-5fd9-4aae-8de1-0a1f936b9dfb | mode=full | segments=6 | review_audio=True
2026-05-26 15:10:12.621 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=3f4cf89e-5fd9-4aae-8de1-0a1f936b9dfb | mode=full
2026-05-26 15:10:15.038 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 38 READY | mode=full | segments=6
2026-05-26 15:10:15.039 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=41 | mode=full | title=Định nghĩa đẳng cấu Boole | chars=167 | estimated_tokens=87 | estimated_audio_seconds=18
2026-05-26 15:10:17.227 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=41 | mode=full | rag=true | tts=true
2026-05-26 15:10:17.232 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=41 | mode=full | title=Định nghĩa đẳng cấu Boole | raw_chars=167
2026-05-26 15:10:17.233 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Định nghĩa đẳng cấu Boole | chars=167 | estimated_tokens=87 | estimated_audio_seconds=18
2026-05-26 15:10:17.234 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Định nghĩa đẳng cấu Boole
[2026-05-26 15:10:19,432: INFO/ForkPoolWorker-1] Retrying request to /embeddings in 0.481164 seconds
[2026-05-26 15:10:19,438: INFO/ForkPoolWorker-1] Retrying request to /chat/completions in 0.476237 seconds
2026-05-26 15:10:20.649 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=07e49f52-540f-4132-9c7d-6f2171836052
2026-05-26 15:10:21.491 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=adee4bba-449f-4d9f-ad9b-06969d2746bd
2026-05-26 15:10:42.531 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=6 | review_chars=512
2026-05-26 15:10:42.533 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=40 | mode=full | main_scripts=6 | review_chars=512
2026-05-26 15:10:42.533 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=40 | mode=full | total_scripts=6
2026-05-26 15:10:42.534 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=40 | mode=full | segment=1/6 | chars=149
2026-05-26 15:10:42.557 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=167
2026-05-26 15:10:49.571 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=40 | mode=full | segment=1/6 | duration_ms=9960
2026-05-26 15:10:49.580 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=40 | mode=full | segment=2/6 | chars=224
[2026-05-26 15:10:49,630: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:10:50,295: INFO/MainProcess] Task triam.notifications.scan_due[ccf5feb4-8b43-435b-a645-d8491816d27c] received
2026-05-26 15:10:53.693 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=1 | review_chars=491
2026-05-26 15:10:53.694 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=41 | mode=full | main_scripts=1 | review_chars=491
2026-05-26 15:10:53.695 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=41 | mode=full | total_scripts=1
2026-05-26 15:10:53.696 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=41 | mode=full | segment=1/1 | chars=314
2026-05-26 15:10:57.875 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:10:57,875: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ccf5feb4-8b43-435b-a645-d8491816d27c] succeeded in 7.577993602026254s: None
2026-05-26 15:10:58.593 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=40 | mode=full | segment=2/6 | duration_ms=15192
2026-05-26 15:10:58.597 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=40 | mode=full | segment=3/6 | chars=147
2026-05-26 15:11:04.602 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=40 | mode=full | segment=3/6 | duration_ms=9384
2026-05-26 15:11:04.603 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=40 | mode=full | segment=4/6 | chars=249
2026-05-26 15:11:08.652 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=41 | mode=full | segment=1/1 | duration_ms=20880
2026-05-26 15:11:08.661 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=41 | mode=full | created_segments=1/1
2026-05-26 15:11:08.662 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=41 | mode=full | chars=491
2026-05-26 15:11:12.361 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=40 | mode=full | segment=4/6 | duration_ms=14448
2026-05-26 15:11:12.365 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=40 | mode=full | segment=5/6 | chars=399
2026-05-26 15:11:22.774 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=41 | mode=full
2026-05-26 15:11:22.775 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=07e49f52-540f-4132-9c7d-6f2171836052 | mode=full | segments=1 | review_audio=True
2026-05-26 15:11:25.849 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=07e49f52-540f-4132-9c7d-6f2171836052 | mode=full
2026-05-26 15:11:28.261 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 41 READY | mode=full | segments=1
2026-05-26 15:11:28.263 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=42 | mode=full | title=Định lý Stone (định lý biểu diễn). | chars=39 | estimated_tokens=24 | estimated_audio_seconds=4
2026-05-26 15:11:30.455 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=42 | mode=full | rag=true | tts=true
2026-05-26 15:11:30.462 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=42 | mode=full | title=Định lý Stone (định lý biểu diễn). | raw_chars=39
2026-05-26 15:11:30.472 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Định lý Stone (định lý biểu diễn). | chars=39 | estimated_tokens=24 | estimated_audio_seconds=4
2026-05-26 15:11:30.472 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Định lý Stone (định lý biểu diễn).
2026-05-26 15:11:30.473 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=39
2026-05-26 15:11:33.605 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=40 | mode=full | segment=5/6 | duration_ms=25728
2026-05-26 15:11:33.606 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=40 | mode=full | segment=6/6 | chars=238
2026-05-26 15:11:35.036 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=4896fb29-3309-4044-a7a5-ce9c04ae8c54
2026-05-26 15:11:43.959 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=1 | review_chars=718
2026-05-26 15:11:43.959 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=42 | mode=full | main_scripts=1 | review_chars=718
2026-05-26 15:11:43.960 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=42 | mode=full | total_scripts=1
2026-05-26 15:11:43.961 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=42 | mode=full | segment=1/1 | chars=40
2026-05-26 15:11:44.916 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=40 | mode=full | segment=6/6 | duration_ms=14496
2026-05-26 15:11:44.917 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=40 | mode=full | created_segments=6/6
2026-05-26 15:11:44.918 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=40 | mode=full | chars=512
2026-05-26 15:11:46.288 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=42 | mode=full | segment=1/1 | duration_ms=2856
2026-05-26 15:11:46.289 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=42 | mode=full | created_segments=1/1
2026-05-26 15:11:46.289 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=42 | mode=full | chars=718
[2026-05-26 15:11:49,630: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:11:50,507: INFO/MainProcess] Task triam.notifications.scan_due[bda254d2-1eb2-4817-b838-f6084613baa5] received
2026-05-26 15:11:59.354 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:11:59,355: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[bda254d2-1eb2-4817-b838-f6084613baa5] succeeded in 8.84739982697647s: None
2026-05-26 15:12:06.508 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=40 | mode=full
2026-05-26 15:12:06.510 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=adee4bba-449f-4d9f-ad9b-06969d2746bd | mode=full | segments=6 | review_audio=True
2026-05-26 15:12:09.590 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=adee4bba-449f-4d9f-ad9b-06969d2746bd | mode=full
2026-05-26 15:12:12.011 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 40 READY | mode=full | segments=6
2026-05-26 15:12:12.016 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=43 | mode=full | title=Khái niệm nguyên tử. | chars=405 | estimated_tokens=227 | estimated_audio_seconds=47
2026-05-26 15:12:14.211 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=43 | mode=full | rag=true | tts=true
2026-05-26 15:12:14.226 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=43 | mode=full | title=Khái niệm nguyên tử. | raw_chars=405
2026-05-26 15:12:14.230 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Khái niệm nguyên tử. | chars=405 | estimated_tokens=227 | estimated_audio_seconds=47
2026-05-26 15:12:14.233 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Khái niệm nguyên tử.
2026-05-26 15:12:14.233 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=405
2026-05-26 15:12:17.939 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=42 | mode=full
2026-05-26 15:12:17.940 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=4896fb29-3309-4044-a7a5-ce9c04ae8c54 | mode=full | segments=1 | review_audio=True
2026-05-26 15:12:21.008 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=4896fb29-3309-4044-a7a5-ce9c04ae8c54 | mode=full
2026-05-26 15:12:23.420 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 42 READY | mode=full | segments=1
2026-05-26 15:12:23.425 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=44 | mode=full | title=. Định nghĩa hàm Boole | chars=407 | estimated_tokens=212 | estimated_audio_seconds=39
2026-05-26 15:12:25.622 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=44 | mode=full | rag=true | tts=true
2026-05-26 15:12:25.630 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=44 | mode=full | title=. Định nghĩa hàm Boole | raw_chars=407
2026-05-26 15:12:25.633 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=. Định nghĩa hàm Boole | chars=407 | estimated_tokens=212 | estimated_audio_seconds=39
2026-05-26 15:12:25.634 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=. Định nghĩa hàm Boole
[2026-05-26 15:12:27,825: INFO/ForkPoolWorker-1] Retrying request to /embeddings in 0.430009 seconds
[2026-05-26 15:12:27,829: INFO/ForkPoolWorker-1] Retrying request to /chat/completions in 0.498011 seconds
2026-05-26 15:12:29.376 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=a283fe82-bd6f-43aa-b0d5-9e039486c9ac
2026-05-26 15:12:30.049 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=57eb2d11-0bf5-4f24-b3c3-506bfa843f29
2026-05-26 15:12:35.938 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=3 | review_chars=499
2026-05-26 15:12:35.938 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=43 | mode=full | main_scripts=3 | review_chars=499
2026-05-26 15:12:35.938 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=43 | mode=full | total_scripts=3
2026-05-26 15:12:35.938 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=43 | mode=full | segment=1/3 | chars=220
2026-05-26 15:12:35.971 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=407
2026-05-26 15:12:41.207 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=43 | mode=full | segment=1/3 | duration_ms=14136
2026-05-26 15:12:41.208 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=43 | mode=full | segment=2/3 | chars=219
2026-05-26 15:12:47.297 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=43 | mode=full | segment=2/3 | duration_ms=17640
2026-05-26 15:12:47.300 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=43 | mode=full | segment=3/3 | chars=276
[2026-05-26 15:12:49,633: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:12:50,292: INFO/MainProcess] Task triam.notifications.scan_due[63e7fd70-5a1d-427f-b8ed-9a6351d3e2bc] received
2026-05-26 15:12:53.782 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=3 | review_chars=490
2026-05-26 15:12:53.783 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=44 | mode=full | main_scripts=3 | review_chars=490
2026-05-26 15:12:53.783 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=44 | mode=full | total_scripts=3
2026-05-26 15:12:53.784 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=44 | mode=full | segment=1/3 | chars=247
2026-05-26 15:12:57.802 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:12:57,803: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[63e7fd70-5a1d-427f-b8ed-9a6351d3e2bc] succeeded in 7.508741489960812s: None
2026-05-26 15:12:58.062 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=43 | mode=full | segment=3/3 | duration_ms=19776
2026-05-26 15:12:58.065 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=43 | mode=full | created_segments=3/3
2026-05-26 15:12:58.066 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=43 | mode=full | chars=499
2026-05-26 15:13:01.923 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=44 | mode=full | segment=1/3 | duration_ms=18576
2026-05-26 15:13:01.928 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=44 | mode=full | segment=2/3 | chars=308
2026-05-26 15:13:09.540 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=43 | mode=full
2026-05-26 15:13:09.540 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=a283fe82-bd6f-43aa-b0d5-9e039486c9ac | mode=full | segments=3 | review_audio=True
2026-05-26 15:13:12.605 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=a283fe82-bd6f-43aa-b0d5-9e039486c9ac | mode=full
2026-05-26 15:13:15.020 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 43 READY | mode=full | segments=3
2026-05-26 15:13:15.023 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=45 | mode=full | title=Định nghĩa 1 | chars=437 | estimated_tokens=246 | estimated_audio_seconds=42
2026-05-26 15:13:17.213 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=45 | mode=full | rag=true | tts=true
2026-05-26 15:13:17.217 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=45 | mode=full | title=Định nghĩa 1 | raw_chars=437
2026-05-26 15:13:17.218 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Định nghĩa 1 | chars=437 | estimated_tokens=246 | estimated_audio_seconds=42
2026-05-26 15:13:17.218 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Định nghĩa 1
2026-05-26 15:13:17.218 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=437
2026-05-26 15:13:20.702 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=44 | mode=full | segment=2/3 | duration_ms=18696
2026-05-26 15:13:20.704 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=44 | mode=full | segment=3/3 | chars=248
2026-05-26 15:13:21.819 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=c772a322-7f67-42a2-88d4-61480d3d3b06
2026-05-26 15:13:33.222 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=44 | mode=full | segment=3/3 | duration_ms=18576
2026-05-26 15:13:33.223 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=44 | mode=full | created_segments=3/3
2026-05-26 15:13:33.223 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=44 | mode=full | chars=490
2026-05-26 15:13:39.441 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=4 | review_chars=511
2026-05-26 15:13:39.444 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=45 | mode=full | main_scripts=4 | review_chars=511
2026-05-26 15:13:39.444 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=45 | mode=full | total_scripts=4
2026-05-26 15:13:39.445 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=45 | mode=full | segment=1/4 | chars=197
2026-05-26 15:13:45.860 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=44 | mode=full
2026-05-26 15:13:45.863 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=57eb2d11-0bf5-4f24-b3c3-506bfa843f29 | mode=full | segments=3 | review_audio=True
2026-05-26 15:13:48.964 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=57eb2d11-0bf5-4f24-b3c3-506bfa843f29 | mode=full
[2026-05-26 15:13:49,638: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:13:50,520: INFO/MainProcess] Task triam.notifications.scan_due[599c181b-44f0-4a65-9143-fe9f57aabb85] received
2026-05-26 15:13:51.388 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 44 READY | mode=full | segments=3
2026-05-26 15:13:51.396 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=46 | mode=full | title=Định nghĩa 2 | chars=410 | estimated_tokens=220 | estimated_audio_seconds=42
2026-05-26 15:13:53.638 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=46 | mode=full | rag=true | tts=true
2026-05-26 15:13:53.642 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=46 | mode=full | title=Định nghĩa 2 | raw_chars=410
2026-05-26 15:13:53.645 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Định nghĩa 2 | chars=410 | estimated_tokens=220 | estimated_audio_seconds=42
2026-05-26 15:13:53.648 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Định nghĩa 2
2026-05-26 15:13:53.651 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=410
2026-05-26 15:13:56.978 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=45 | mode=full | segment=1/4 | duration_ms=13392
2026-05-26 15:13:56.980 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=45 | mode=full | segment=2/4 | chars=228
2026-05-26 15:13:58.328 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=6a0f7c39-99b3-40b1-a0c5-08973dfff077
2026-05-26 15:13:58.378 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:13:58,382: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[599c181b-44f0-4a65-9143-fe9f57aabb85] succeeded in 7.644872587989084s: None
2026-05-26 15:14:05.476 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=45 | mode=full | segment=2/4 | duration_ms=15240
2026-05-26 15:14:05.477 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=45 | mode=full | segment=3/4 | chars=162
2026-05-26 15:14:07.134 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=4 | review_chars=486
2026-05-26 15:14:07.136 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=46 | mode=full | main_scripts=4 | review_chars=486
2026-05-26 15:14:07.138 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=46 | mode=full | total_scripts=4
2026-05-26 15:14:07.141 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=46 | mode=full | segment=1/4 | chars=96
2026-05-26 15:14:09.441 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=45 | mode=full | segment=3/4 | duration_ms=9408
2026-05-26 15:14:09.442 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=45 | mode=full | segment=4/4 | chars=291
2026-05-26 15:14:10.018 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=46 | mode=full | segment=1/4 | duration_ms=6312
2026-05-26 15:14:10.021 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=46 | mode=full | segment=2/4 | chars=171
2026-05-26 15:14:14.262 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=46 | mode=full | segment=2/4 | duration_ms=10488
2026-05-26 15:14:14.263 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=46 | mode=full | segment=3/4 | chars=137
2026-05-26 15:14:16.545 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=45 | mode=full | segment=4/4 | duration_ms=17712
2026-05-26 15:14:16.547 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=45 | mode=full | created_segments=4/4
2026-05-26 15:14:16.548 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=45 | mode=full | chars=511
2026-05-26 15:14:19.143 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=46 | mode=full | segment=3/4 | duration_ms=8496
2026-05-26 15:14:19.146 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=46 | mode=full | segment=4/4 | chars=300
2026-05-26 15:14:26.328 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=46 | mode=full | segment=4/4 | duration_ms=17352
2026-05-26 15:14:26.328 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=46 | mode=full | created_segments=4/4
2026-05-26 15:14:26.330 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=46 | mode=full | chars=486
2026-05-26 15:14:29.181 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=45 | mode=full
2026-05-26 15:14:29.184 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=c772a322-7f67-42a2-88d4-61480d3d3b06 | mode=full | segments=4 | review_audio=True
2026-05-26 15:14:32.257 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=c772a322-7f67-42a2-88d4-61480d3d3b06 | mode=full
2026-05-26 15:14:34.682 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 45 READY | mode=full | segments=4
2026-05-26 15:14:34.688 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=47 | mode=full | title=Cổng logic | chars=311 | estimated_tokens=153 | estimated_audio_seconds=31
2026-05-26 15:14:36.884 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=47 | mode=full | rag=true | tts=true
2026-05-26 15:14:36.892 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=47 | mode=full | title=Cổng logic | raw_chars=311
2026-05-26 15:14:36.894 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Cổng logic | chars=311 | estimated_tokens=153 | estimated_audio_seconds=31
2026-05-26 15:14:36.897 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Cổng logic
2026-05-26 15:14:36.899 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=311
2026-05-26 15:14:40.481 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=f62e7374-3ae8-4de1-ad03-5d3c8ec66812
2026-05-26 15:14:47.185 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=4 | review_chars=417
2026-05-26 15:14:47.186 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=47 | mode=full | main_scripts=4 | review_chars=417
2026-05-26 15:14:47.186 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=47 | mode=full | total_scripts=4
2026-05-26 15:14:47.186 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=47 | mode=full | segment=1/4 | chars=154
[2026-05-26 15:14:49,637: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:14:50,519: INFO/MainProcess] Task triam.notifications.scan_due[73c9a297-c9ba-4038-b0ff-303b65c35e7a] received
2026-05-26 15:14:50.541 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=46 | mode=full
2026-05-26 15:14:50.541 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=6a0f7c39-99b3-40b1-a0c5-08973dfff077 | mode=full | segments=4 | review_audio=True
2026-05-26 15:14:53.622 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=6a0f7c39-99b3-40b1-a0c5-08973dfff077 | mode=full
2026-05-26 15:14:56.044 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 46 READY | mode=full | segments=4
2026-05-26 15:14:56.050 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=48 | mode=full | title=Tối ưu hóa | chars=417 | estimated_tokens=222 | estimated_audio_seconds=43
2026-05-26 15:14:58.056 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:14:58,057: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[73c9a297-c9ba-4038-b0ff-303b65c35e7a] succeeded in 7.536710441927426s: None
2026-05-26 15:14:58.236 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=48 | mode=full | rag=true | tts=true
2026-05-26 15:14:58.242 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=48 | mode=full | title=Tối ưu hóa | raw_chars=417
2026-05-26 15:14:58.248 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Tối ưu hóa | chars=417 | estimated_tokens=222 | estimated_audio_seconds=43
2026-05-26 15:14:58.250 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Tối ưu hóa
2026-05-26 15:14:58.254 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=417
2026-05-26 15:15:01.610 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=47 | mode=full | segment=1/4 | duration_ms=9216
2026-05-26 15:15:01.612 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=47 | mode=full | segment=2/4 | chars=193
2026-05-26 15:15:02.721 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=bea7796f-57ef-4887-b585-2a3f8f3f34ae
2026-05-26 15:15:09.676 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=47 | mode=full | segment=2/4 | duration_ms=12720
2026-05-26 15:15:09.677 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=47 | mode=full | segment=3/4 | chars=137
2026-05-26 15:15:15.436 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=4 | review_chars=531
2026-05-26 15:15:15.436 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=48 | mode=full | main_scripts=4 | review_chars=531
2026-05-26 15:15:15.437 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=48 | mode=full | total_scripts=4
2026-05-26 15:15:15.437 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=48 | mode=full | segment=1/4 | chars=257
2026-05-26 15:15:16.650 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=47 | mode=full | segment=3/4 | duration_ms=8784
2026-05-26 15:15:16.651 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=47 | mode=full | segment=4/4 | chars=223
2026-05-26 15:15:25.886 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=47 | mode=full | segment=4/4 | duration_ms=12480
2026-05-26 15:15:25.886 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=47 | mode=full | created_segments=4/4
2026-05-26 15:15:25.887 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=47 | mode=full | chars=417
2026-05-26 15:15:26.811 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=48 | mode=full | segment=1/4 | duration_ms=14304
2026-05-26 15:15:26.812 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=48 | mode=full | segment=2/4 | chars=179
2026-05-26 15:15:33.437 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=48 | mode=full | segment=2/4 | duration_ms=10704
2026-05-26 15:15:33.437 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=48 | mode=full | segment=3/4 | chars=237
2026-05-26 15:15:40.471 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=47 | mode=full
2026-05-26 15:15:40.473 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=f62e7374-3ae8-4de1-ad03-5d3c8ec66812 | mode=full | segments=4 | review_audio=True
2026-05-26 15:15:43.544 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=f62e7374-3ae8-4de1-ad03-5d3c8ec66812 | mode=full
2026-05-26 15:15:45.959 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 47 READY | mode=full | segments=4
2026-05-26 15:15:45.961 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=49 | mode=full | title=Biểu diễn tích cơ bản | chars=52 | estimated_tokens=25 | estimated_audio_seconds=6
2026-05-26 15:15:48.151 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=49 | mode=full | rag=true | tts=true
2026-05-26 15:15:48.155 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=49 | mode=full | title=Biểu diễn tích cơ bản | raw_chars=52
2026-05-26 15:15:48.155 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Biểu diễn tích cơ bản | chars=52 | estimated_tokens=25 | estimated_audio_seconds=6
2026-05-26 15:15:48.155 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Biểu diễn tích cơ bản
2026-05-26 15:15:48.156 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=52
[2026-05-26 15:15:49,647: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:15:50,307: INFO/MainProcess] Task triam.notifications.scan_due[4709dd10-8754-4d7c-b085-a75fcee8f73f] received
2026-05-26 15:15:51.561 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=48 | mode=full | segment=3/4 | duration_ms=14904
2026-05-26 15:15:51.561 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=48 | mode=full | segment=4/4 | chars=574
2026-05-26 15:15:52.800 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=75971ef9-9584-4f19-8e90-0be67a44be67
2026-05-26 15:15:58.033 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:15:58,033: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4709dd10-8754-4d7c-b085-a75fcee8f73f] succeeded in 7.506449922104366s: None
2026-05-26 15:15:59.979 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=3 | review_chars=98
2026-05-26 15:15:59.980 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=49 | mode=full | main_scripts=3 | review_chars=98
2026-05-26 15:15:59.981 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=49 | mode=full | total_scripts=3
2026-05-26 15:15:59.982 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=49 | mode=full | segment=1/3 | chars=16
2026-05-26 15:16:01.634 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=49 | mode=full | segment=1/3 | duration_ms=1752
2026-05-26 15:16:01.634 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=49 | mode=full | segment=2/3 | chars=16
2026-05-26 15:16:03.986 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=49 | mode=full | segment=2/3 | duration_ms=1752
2026-05-26 15:16:03.987 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=49 | mode=full | segment=3/3 | chars=16
2026-05-26 15:16:06.731 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=48 | mode=full | segment=4/4 | duration_ms=36984
2026-05-26 15:16:06.733 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=48 | mode=full | created_segments=4/4
2026-05-26 15:16:06.735 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=48 | mode=full | chars=531
2026-05-26 15:16:07.189 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=49 | mode=full | segment=3/3 | duration_ms=1848
2026-05-26 15:16:07.191 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=49 | mode=full | created_segments=3/3
2026-05-26 15:16:07.194 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=49 | mode=full | chars=98
2026-05-26 15:16:10.545 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=49 | mode=full
2026-05-26 15:16:10.545 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=75971ef9-9584-4f19-8e90-0be67a44be67 | mode=full | segments=3 | review_audio=True
2026-05-26 15:16:13.649 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=75971ef9-9584-4f19-8e90-0be67a44be67 | mode=full
2026-05-26 15:16:16.064 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 49 READY | mode=full | segments=3
2026-05-26 15:16:16.065 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=50 | mode=full | title=Tính chất biểu đồ Karnaugh | chars=67 | estimated_tokens=34 | estimated_audio_seconds=4
2026-05-26 15:16:18.250 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=50 | mode=full | rag=true | tts=true
2026-05-26 15:16:18.253 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=50 | mode=full | title=Tính chất biểu đồ Karnaugh | raw_chars=67
2026-05-26 15:16:18.254 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Tính chất biểu đồ Karnaugh | chars=67 | estimated_tokens=34 | estimated_audio_seconds=4
2026-05-26 15:16:18.254 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Tính chất biểu đồ Karnaugh
2026-05-26 15:16:18.254 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=67
2026-05-26 15:16:21.745 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=ab56bf3a-6c93-401b-98db-48379ecba677
2026-05-26 15:16:23.168 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=48 | mode=full
2026-05-26 15:16:23.169 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=bea7796f-57ef-4887-b585-2a3f8f3f34ae | mode=full | segments=4 | review_audio=True
2026-05-26 15:16:26.245 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=bea7796f-57ef-4887-b585-2a3f8f3f34ae | mode=full
2026-05-26 15:16:28.653 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 48 READY | mode=full | segments=4
2026-05-26 15:16:28.654 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=51 | mode=full | title=Khái niệm tế bào lớn | chars=33 | estimated_tokens=18 | estimated_audio_seconds=3
2026-05-26 15:16:30.840 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=51 | mode=full | rag=true | tts=true
2026-05-26 15:16:30.843 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=51 | mode=full | title=Khái niệm tế bào lớn | raw_chars=33
2026-05-26 15:16:30.847 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Khái niệm tế bào lớn | chars=33 | estimated_tokens=18 | estimated_audio_seconds=3
2026-05-26 15:16:30.850 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Khái niệm tế bào lớn
2026-05-26 15:16:33.052 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=3 | review_chars=512
2026-05-26 15:16:33.053 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=50 | mode=full | main_scripts=3 | review_chars=512
2026-05-26 15:16:33.054 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=50 | mode=full | total_scripts=3
2026-05-26 15:16:33.054 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=50 | mode=full | segment=1/3 | chars=256
2026-05-26 15:16:33.093 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=33
2026-05-26 15:16:34.210 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=d4d5ef99-901b-4360-807b-de47f1b03f70
2026-05-26 15:16:42.016 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=1 | review_chars=242
2026-05-26 15:16:42.017 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=51 | mode=full | main_scripts=1 | review_chars=242
2026-05-26 15:16:42.020 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=51 | mode=full | total_scripts=1
2026-05-26 15:16:42.024 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=51 | mode=full | segment=1/1 | chars=33
2026-05-26 15:16:45.521 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=51 | mode=full | segment=1/1 | duration_ms=4848
2026-05-26 15:16:45.522 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=51 | mode=full | created_segments=1/1
2026-05-26 15:16:45.523 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=51 | mode=full | chars=242
[2026-05-26 15:16:49,647: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-26 15:16:49.821 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=50 | mode=full | segment=1/3 | duration_ms=15552
2026-05-26 15:16:49.824 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=50 | mode=full | segment=2/3 | chars=204
[2026-05-26 15:16:50,706: INFO/MainProcess] Task triam.notifications.scan_due[ac538794-72c8-4e95-968a-989826ef9eab] received
2026-05-26 15:16:53.118 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=51 | mode=full
2026-05-26 15:16:53.121 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=d4d5ef99-901b-4360-807b-de47f1b03f70 | mode=full | segments=1 | review_audio=True
2026-05-26 15:16:56.299 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=d4d5ef99-901b-4360-807b-de47f1b03f70 | mode=full
2026-05-26 15:16:58.191 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:16:58,192: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ac538794-72c8-4e95-968a-989826ef9eab] succeeded in 7.483195805922151s: None
2026-05-26 15:16:58.712 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 51 READY | mode=full | segments=1
2026-05-26 15:16:58.714 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=52 | mode=full | title=Thuật toán Karnaugh | chars=1903 | estimated_tokens=1035 | estimated_audio_seconds=223
2026-05-26 15:17:00.901 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=52 | mode=full | rag=true | tts=true
2026-05-26 15:17:00.907 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=52 | mode=full | title=Thuật toán Karnaugh | raw_chars=1903
2026-05-26 15:17:00.911 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Thuật toán Karnaugh | chars=1903 | estimated_tokens=1035 | estimated_audio_seconds=223
2026-05-26 15:17:00.913 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Thuật toán Karnaugh
2026-05-26 15:17:00.914 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1903
2026-05-26 15:17:04.272 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=50 | mode=full | segment=2/3 | duration_ms=12432
2026-05-26 15:17:04.277 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=50 | mode=full | segment=3/3 | chars=275
2026-05-26 15:17:05.454 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 2 vectors for chapter_id=ceb620d9-ac0e-4254-b317-2cf0ad39b080
2026-05-26 15:17:15.234 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=50 | mode=full | segment=3/3 | duration_ms=15912
2026-05-26 15:17:15.235 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=50 | mode=full | created_segments=3/3
2026-05-26 15:17:15.235 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=50 | mode=full | chars=512
2026-05-26 15:17:35.653 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=50 | mode=full
2026-05-26 15:17:35.654 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=ab56bf3a-6c93-401b-98db-48379ecba677 | mode=full | segments=3 | review_audio=True
2026-05-26 15:17:38.737 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=ab56bf3a-6c93-401b-98db-48379ecba677 | mode=full
2026-05-26 15:17:41.171 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 50 READY | mode=full | segments=3
2026-05-26 15:17:41.172 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=53 | mode=full | title=Khái niệm tập hợp | chars=1567 | estimated_tokens=827 | estimated_audio_seconds=174
2026-05-26 15:17:43.357 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=53 | mode=full | rag=true | tts=true
2026-05-26 15:17:43.359 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=53 | mode=full | title=Khái niệm tập hợp | raw_chars=1567
2026-05-26 15:17:43.364 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Khái niệm tập hợp | chars=1567 | estimated_tokens=827 | estimated_audio_seconds=174
2026-05-26 15:17:43.367 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Khái niệm tập hợp
2026-05-26 15:17:45.555 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=22 | review_chars=643
2026-05-26 15:17:45.556 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=52 | mode=full | main_scripts=22 | review_chars=643
2026-05-26 15:17:45.556 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=52 | mode=full | total_scripts=22
2026-05-26 15:17:45.557 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=1/22 | chars=207
2026-05-26 15:17:45.596 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1567
2026-05-26 15:17:47.190 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 2 vectors for chapter_id=b37f863a-536d-4264-94d4-59faf369a739
[2026-05-26 15:17:49,647: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:17:50,306: INFO/MainProcess] Task triam.notifications.scan_due[2dda9dcb-665b-45ca-bbbe-a4b4622b510d] received
2026-05-26 15:17:52.740 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=1/22 | duration_ms=13224
2026-05-26 15:17:52.742 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=2/22 | chars=107
2026-05-26 15:17:56.589 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=2/22 | duration_ms=6816
2026-05-26 15:17:56.590 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=3/22 | chars=187
2026-05-26 15:17:58.005 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:17:58,008: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2dda9dcb-665b-45ca-bbbe-a4b4622b510d] succeeded in 7.487189544946887s: None
2026-05-26 15:18:01.960 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=3/22 | duration_ms=11184
2026-05-26 15:18:01.963 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=4/22 | chars=214
2026-05-26 15:18:04.301 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=7 | review_chars=624
2026-05-26 15:18:04.302 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=53 | mode=full | main_scripts=7 | review_chars=624
2026-05-26 15:18:04.302 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=53 | mode=full | total_scripts=7
2026-05-26 15:18:04.302 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=53 | mode=full | segment=1/7 | chars=180
2026-05-26 15:18:10.010 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=53 | mode=full | segment=1/7 | duration_ms=10512
2026-05-26 15:18:10.011 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=53 | mode=full | segment=2/7 | chars=253
2026-05-26 15:18:11.917 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=4/22 | duration_ms=14808
2026-05-26 15:18:11.918 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=5/22 | chars=182
2026-05-26 15:18:21.520 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=53 | mode=full | segment=2/7 | duration_ms=14472
2026-05-26 15:18:21.520 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=53 | mode=full | segment=3/7 | chars=379
2026-05-26 15:18:24.475 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=5/22 | duration_ms=14496
2026-05-26 15:18:24.475 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=6/22 | chars=120
2026-05-26 15:18:29.867 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=6/22 | duration_ms=8448
2026-05-26 15:18:29.869 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=7/22 | chars=305
2026-05-26 15:18:33.807 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=53 | mode=full | segment=3/7 | duration_ms=26592
2026-05-26 15:18:33.811 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=53 | mode=full | segment=4/7 | chars=516
2026-05-26 15:18:43.768 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=7/22 | duration_ms=23280
2026-05-26 15:18:43.769 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=8/22 | chars=116
2026-05-26 15:18:48.291 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=8/22 | duration_ms=7296
2026-05-26 15:18:48.292 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=9/22 | chars=199
[2026-05-26 15:18:49,647: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-26 15:18:50.216 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=53 | mode=full | segment=4/7 | duration_ms=31008
2026-05-26 15:18:50.217 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=53 | mode=full | segment=5/7 | chars=283
[2026-05-26 15:18:50,713: INFO/MainProcess] Task triam.notifications.scan_due[a6b04cf8-7aa5-4fbe-9538-bf3848894d00] received
2026-05-26 15:18:56.331 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=9/22 | duration_ms=15000
2026-05-26 15:18:56.334 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=10/22 | chars=166
2026-05-26 15:18:58.231 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:18:58,231: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a6b04cf8-7aa5-4fbe-9538-bf3848894d00] succeeded in 7.51667085592635s: None
2026-05-26 15:19:05.744 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=10/22 | duration_ms=13464
2026-05-26 15:19:05.745 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=11/22 | chars=184
2026-05-26 15:19:08.027 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=53 | mode=full | segment=5/7 | duration_ms=20400
2026-05-26 15:19:08.029 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=53 | mode=full | segment=6/7 | chars=518
2026-05-26 15:19:12.141 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=11/22 | duration_ms=13848
2026-05-26 15:19:12.142 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=12/22 | chars=178
2026-05-26 15:19:19.249 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=12/22 | duration_ms=12096
2026-05-26 15:19:19.250 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=13/22 | chars=145
2026-05-26 15:19:29.583 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=53 | mode=full | segment=6/7 | duration_ms=32784
2026-05-26 15:19:29.584 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=53 | mode=full | segment=7/7 | chars=110
2026-05-26 15:19:30.294 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=13/22 | duration_ms=11568
2026-05-26 15:19:30.300 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=14/22 | chars=229
2026-05-26 15:19:34.909 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=53 | mode=full | segment=7/7 | duration_ms=7488
2026-05-26 15:19:34.909 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=53 | mode=full | created_segments=7/7
2026-05-26 15:19:34.910 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=53 | mode=full | chars=624
2026-05-26 15:19:40.385 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=14/22 | duration_ms=14664
2026-05-26 15:19:40.386 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=15/22 | chars=157
2026-05-26 15:19:49.345 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=15/22 | duration_ms=11304
2026-05-26 15:19:49.346 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=16/22 | chars=227
[2026-05-26 15:19:49,649: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:19:50,689: INFO/MainProcess] Task triam.notifications.scan_due[718fdfe5-62ac-4efc-b680-7bfdba0b1ce4] received
2026-05-26 15:19:57.314 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=16/22 | duration_ms=14016
2026-05-26 15:19:57.316 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=17/22 | chars=241
2026-05-26 15:19:58.205 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:19:58,206: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[718fdfe5-62ac-4efc-b680-7bfdba0b1ce4] succeeded in 7.5155079460237175s: None
2026-05-26 15:20:02.073 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=53 | mode=full
2026-05-26 15:20:02.074 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=b37f863a-536d-4264-94d4-59faf369a739 | mode=full | segments=7 | review_audio=True
2026-05-26 15:20:05.152 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=b37f863a-536d-4264-94d4-59faf369a739 | mode=full
2026-05-26 15:20:07.586 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 53 READY | mode=full | segments=7
2026-05-26 15:20:07.589 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=54 | mode=full | title=Quan hệ bao hàm và tập con | chars=236 | estimated_tokens=123 | estimated_audio_seconds=30
2026-05-26 15:20:09.781 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=54 | mode=full | rag=true | tts=true
2026-05-26 15:20:09.790 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=54 | mode=full | title=Quan hệ bao hàm và tập con | raw_chars=236
2026-05-26 15:20:09.792 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Quan hệ bao hàm và tập con | chars=236 | estimated_tokens=123 | estimated_audio_seconds=30
2026-05-26 15:20:09.794 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Quan hệ bao hàm và tập con
2026-05-26 15:20:09.795 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=236
2026-05-26 15:20:13.172 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=17/22 | duration_ms=15744
2026-05-26 15:20:13.174 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=18/22 | chars=167
2026-05-26 15:20:14.608 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=16631dd1-5af1-42f3-942d-d206b317027c
2026-05-26 15:20:19.031 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=18/22 | duration_ms=10584
2026-05-26 15:20:19.033 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=19/22 | chars=189
2026-05-26 15:20:19.077 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=1 | review_chars=280
2026-05-26 15:20:19.078 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=54 | mode=full | main_scripts=1 | review_chars=280
2026-05-26 15:20:19.078 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=54 | mode=full | total_scripts=1
2026-05-26 15:20:19.080 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=54 | mode=full | segment=1/1 | chars=479
2026-05-26 15:20:28.310 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=19/22 | duration_ms=12384
2026-05-26 15:20:28.311 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=20/22 | chars=73
2026-05-26 15:20:32.244 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=20/22 | duration_ms=5640
2026-05-26 15:20:32.247 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=21/22 | chars=188
2026-05-26 15:20:34.312 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=54 | mode=full | segment=1/1 | duration_ms=28488
2026-05-26 15:20:34.315 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=54 | mode=full | created_segments=1/1
2026-05-26 15:20:34.316 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=54 | mode=full | chars=280
2026-05-26 15:20:37.042 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=21/22 | duration_ms=12840
2026-05-26 15:20:37.044 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=52 | mode=full | segment=22/22 | chars=49
2026-05-26 15:20:39.917 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=52 | mode=full | segment=22/22 | duration_ms=4008
2026-05-26 15:20:39.920 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=52 | mode=full | created_segments=22/22
2026-05-26 15:20:39.921 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=52 | mode=full | chars=643
2026-05-26 15:20:45.218 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=54 | mode=full
2026-05-26 15:20:45.219 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=16631dd1-5af1-42f3-942d-d206b317027c | mode=full | segments=1 | review_audio=True
2026-05-26 15:20:48.290 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=16631dd1-5af1-42f3-942d-d206b317027c | mode=full
[2026-05-26 15:20:49,649: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:20:50,577: INFO/MainProcess] Task triam.notifications.scan_due[926f2452-13b3-4bc4-b168-bdd23aa32b90] received
2026-05-26 15:20:50.699 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 54 READY | mode=full | segments=1
2026-05-26 15:20:50.702 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=55 | mode=full | title=Quan hệ bằng nhau | chars=475 | estimated_tokens=234 | estimated_audio_seconds=55
2026-05-26 15:20:52.911 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=55 | mode=full | rag=true | tts=true
2026-05-26 15:20:52.916 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=55 | mode=full | title=Quan hệ bằng nhau | raw_chars=475
2026-05-26 15:20:52.917 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Quan hệ bằng nhau | chars=475 | estimated_tokens=234 | estimated_audio_seconds=55
2026-05-26 15:20:52.918 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Quan hệ bằng nhau
2026-05-26 15:20:52.919 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=475
2026-05-26 15:20:56.548 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=83190ca5-9af8-42ae-9eb0-e55ceab1567c
2026-05-26 15:20:58.078 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:20:58,078: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[926f2452-13b3-4bc4-b168-bdd23aa32b90] succeeded in 7.498536687111482s: None
2026-05-26 15:21:01.387 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=52 | mode=full
2026-05-26 15:21:01.390 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=ceb620d9-ac0e-4254-b317-2cf0ad39b080 | mode=full | segments=22 | review_audio=True
2026-05-26 15:21:04.481 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=ceb620d9-ac0e-4254-b317-2cf0ad39b080 | mode=full
2026-05-26 15:21:06.896 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 52 READY | mode=full | segments=22
2026-05-26 15:21:06.912 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=56 | mode=full | title=Các phép toán trên tập hợp. | chars=1326 | estimated_tokens=665 | estimated_audio_seconds=145
2026-05-26 15:21:09.106 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=56 | mode=full | rag=true | tts=true
2026-05-26 15:21:09.108 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=3 | review_chars=577
2026-05-26 15:21:09.110 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=55 | mode=full | main_scripts=3 | review_chars=577
2026-05-26 15:21:09.112 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=55 | mode=full | total_scripts=3
2026-05-26 15:21:09.112 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=55 | mode=full | segment=1/3 | chars=140
2026-05-26 15:21:09.145 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=56 | mode=full | title=Các phép toán trên tập hợp. | raw_chars=1326
2026-05-26 15:21:09.148 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Các phép toán trên tập hợp. | chars=1326 | estimated_tokens=665 | estimated_audio_seconds=145
2026-05-26 15:21:09.148 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Các phép toán trên tập hợp.
2026-05-26 15:21:09.149 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1326
2026-05-26 15:21:12.684 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 2 vectors for chapter_id=71a64335-0d8b-427a-a8bb-bc776d9d5e3c
2026-05-26 15:21:17.994 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=55 | mode=full | segment=1/3 | duration_ms=8928
2026-05-26 15:21:17.995 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=55 | mode=full | segment=2/3 | chars=313
2026-05-26 15:21:29.613 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=55 | mode=full | segment=2/3 | duration_ms=19656
2026-05-26 15:21:29.613 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=55 | mode=full | segment=3/3 | chars=151
2026-05-26 15:21:33.128 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=5 | review_chars=572
2026-05-26 15:21:33.128 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=56 | mode=full | main_scripts=5 | review_chars=572
2026-05-26 15:21:33.130 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=56 | mode=full | total_scripts=5
2026-05-26 15:21:33.132 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=56 | mode=full | segment=1/5 | chars=623
2026-05-26 15:21:34.386 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=55 | mode=full | segment=3/3 | duration_ms=9240
2026-05-26 15:21:34.387 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=55 | mode=full | created_segments=3/3
2026-05-26 15:21:34.387 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=55 | mode=full | chars=577
[2026-05-26 15:21:49,650: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:21:50,533: INFO/MainProcess] Task triam.notifications.scan_due[dfb926fb-2ee8-4c84-b2c8-1364e2577bed] received
2026-05-26 15:21:53.761 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=56 | mode=full | segment=1/5 | duration_ms=37152
2026-05-26 15:21:53.762 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=56 | mode=full | segment=2/5 | chars=739
2026-05-26 15:21:55.147 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=55 | mode=full
2026-05-26 15:21:55.147 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=83190ca5-9af8-42ae-9eb0-e55ceab1567c | mode=full | segments=3 | review_audio=True
2026-05-26 15:21:58.055 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:21:58,057: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[dfb926fb-2ee8-4c84-b2c8-1364e2577bed] succeeded in 7.518683852977119s: None
2026-05-26 15:21:58.213 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=83190ca5-9af8-42ae-9eb0-e55ceab1567c | mode=full
2026-05-26 15:22:00.625 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 55 READY | mode=full | segments=3
2026-05-26 15:22:00.627 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=57 | mode=full | title=Khái niệm ánh xạ | chars=360 | estimated_tokens=192 | estimated_audio_seconds=41
2026-05-26 15:22:02.818 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=57 | mode=full | rag=true | tts=true
2026-05-26 15:22:02.823 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=57 | mode=full | title=Khái niệm ánh xạ | raw_chars=360
2026-05-26 15:22:02.823 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Khái niệm ánh xạ | chars=360 | estimated_tokens=192 | estimated_audio_seconds=41
2026-05-26 15:22:02.824 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Khái niệm ánh xạ
2026-05-26 15:22:02.829 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=360
2026-05-26 15:22:06.142 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=8b8686b5-971d-4513-8471-f0fec3b10d12
2026-05-26 15:22:18.175 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=4 | review_chars=465
2026-05-26 15:22:18.178 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=57 | mode=full | main_scripts=4 | review_chars=465
2026-05-26 15:22:18.179 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=57 | mode=full | total_scripts=4
2026-05-26 15:22:18.180 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=57 | mode=full | segment=1/4 | chars=397
2026-05-26 15:22:24.483 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=56 | mode=full | segment=2/5 | duration_ms=45888
2026-05-26 15:22:24.486 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=56 | mode=full | segment=3/5 | chars=739
2026-05-26 15:22:29.091 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=57 | mode=full | segment=1/4 | duration_ms=24192
2026-05-26 15:22:29.092 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=57 | mode=full | segment=2/4 | chars=174
2026-05-26 15:22:35.190 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=57 | mode=full | segment=2/4 | duration_ms=9504
2026-05-26 15:22:35.192 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=57 | mode=full | segment=3/4 | chars=267
2026-05-26 15:22:43.608 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=56 | mode=full | segment=3/5 | duration_ms=44976
2026-05-26 15:22:43.609 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=56 | mode=full | segment=4/5 | chars=677
2026-05-26 15:22:44.314 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=57 | mode=full | segment=3/4 | duration_ms=17880
2026-05-26 15:22:44.315 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=57 | mode=full | segment=4/4 | chars=306
[2026-05-26 15:22:49,650: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:22:50,313: INFO/MainProcess] Task triam.notifications.scan_due[76f1221b-d9fe-4eec-a14a-2192642d199b] received
2026-05-26 15:22:55.993 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=57 | mode=full | segment=4/4 | duration_ms=18672
2026-05-26 15:22:55.995 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=57 | mode=full | created_segments=4/4
2026-05-26 15:22:55.995 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=57 | mode=full | chars=465
2026-05-26 15:22:57.841 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:22:57,841: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[76f1221b-d9fe-4eec-a14a-2192642d199b] succeeded in 7.522965713054873s: None
2026-05-26 15:23:01.132 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=56 | mode=full | segment=4/5 | duration_ms=40416
2026-05-26 15:23:01.141 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=56 | mode=full | segment=5/5 | chars=703
2026-05-26 15:23:14.974 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=57 | mode=full
2026-05-26 15:23:14.976 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=8b8686b5-971d-4513-8471-f0fec3b10d12 | mode=full | segments=4 | review_audio=True
2026-05-26 15:23:18.051 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=8b8686b5-971d-4513-8471-f0fec3b10d12 | mode=full
2026-05-26 15:23:20.471 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 57 READY | mode=full | segments=4
2026-05-26 15:23:20.477 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=58 | mode=full | title=Các ánh xạ đặc biệt | chars=574 | estimated_tokens=320 | estimated_audio_seconds=70
2026-05-26 15:23:22.670 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=58 | mode=full | rag=true | tts=true
2026-05-26 15:23:22.677 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=58 | mode=full | title=Các ánh xạ đặc biệt | raw_chars=574
2026-05-26 15:23:22.681 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Các ánh xạ đặc biệt | chars=574 | estimated_tokens=320 | estimated_audio_seconds=70
2026-05-26 15:23:22.682 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Các ánh xạ đặc biệt
2026-05-26 15:23:22.683 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=574
2026-05-26 15:23:25.909 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=56 | mode=full | segment=5/5 | duration_ms=46896
2026-05-26 15:23:25.910 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=56 | mode=full | created_segments=5/5
2026-05-26 15:23:25.912 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=56 | mode=full | chars=572
2026-05-26 15:23:26.839 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=8e5e5838-2e6e-45ed-9e6e-b463fb09cba5
2026-05-26 15:23:40.339 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=5 | review_chars=627
2026-05-26 15:23:40.340 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=58 | mode=full | main_scripts=5 | review_chars=627
2026-05-26 15:23:40.340 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=58 | mode=full | total_scripts=5
2026-05-26 15:23:40.340 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=58 | mode=full | segment=1/5 | chars=229
2026-05-26 15:23:45.408 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=56 | mode=full
2026-05-26 15:23:45.409 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=71a64335-0d8b-427a-a8bb-bc776d9d5e3c | mode=full | segments=5 | review_audio=True
2026-05-26 15:23:48.563 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=71a64335-0d8b-427a-a8bb-bc776d9d5e3c | mode=full
[2026-05-26 15:23:49,650: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:23:50,532: INFO/MainProcess] Task triam.notifications.scan_due[cac8a2d8-e48d-4b15-bd5e-62cdfba44128] received
2026-05-26 15:23:50.990 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 56 READY | mode=full | segments=5
2026-05-26 15:23:50.995 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=59 | mode=full | title=Giới thiệu các tập hợp số | chars=169 | estimated_tokens=111 | estimated_audio_seconds=19
2026-05-26 15:23:53.203 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=59 | mode=full | rag=true | tts=true
2026-05-26 15:23:53.212 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=59 | mode=full | title=Giới thiệu các tập hợp số | raw_chars=169
2026-05-26 15:23:53.212 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Giới thiệu các tập hợp số | chars=169 | estimated_tokens=111 | estimated_audio_seconds=19
2026-05-26 15:23:53.213 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Giới thiệu các tập hợp số
2026-05-26 15:23:53.214 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=169
2026-05-26 15:23:56.134 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=58 | mode=full | segment=1/5 | duration_ms=16344
2026-05-26 15:23:56.134 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=58 | mode=full | segment=2/5 | chars=239
2026-05-26 15:23:57.227 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=4509daaf-b229-4618-9e3f-33ea1182f8cd
2026-05-26 15:23:58.175 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:23:58,176: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[cac8a2d8-e48d-4b15-bd5e-62cdfba44128] succeeded in 7.641065024072304s: None
2026-05-26 15:24:03.927 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=58 | mode=full | segment=2/5 | duration_ms=14376
2026-05-26 15:24:03.928 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=58 | mode=full | segment=3/5 | chars=202
2026-05-26 15:24:10.338 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=5 | review_chars=338
2026-05-26 15:24:10.338 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=59 | mode=full | main_scripts=5 | review_chars=338
2026-05-26 15:24:10.339 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=59 | mode=full | total_scripts=5
2026-05-26 15:24:10.339 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=59 | mode=full | segment=1/5 | chars=95
2026-05-26 15:24:15.133 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=58 | mode=full | segment=3/5 | duration_ms=12192
2026-05-26 15:24:15.134 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=58 | mode=full | segment=4/5 | chars=298
2026-05-26 15:24:15.790 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=59 | mode=full | segment=1/5 | duration_ms=8616
2026-05-26 15:24:15.793 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=59 | mode=full | segment=2/5 | chars=156
2026-05-26 15:24:22.686 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=59 | mode=full | segment=2/5 | duration_ms=13968
2026-05-26 15:24:22.687 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=59 | mode=full | segment=3/5 | chars=99
2026-05-26 15:24:23.767 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=58 | mode=full | segment=4/5 | duration_ms=19056
2026-05-26 15:24:23.770 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=58 | mode=full | segment=5/5 | chars=350
2026-05-26 15:24:26.563 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=59 | mode=full | segment=3/5 | duration_ms=7800
2026-05-26 15:24:26.564 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=59 | mode=full | segment=4/5 | chars=27
2026-05-26 15:24:30.129 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=59 | mode=full | segment=4/5 | duration_ms=2688
2026-05-26 15:24:30.130 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=59 | mode=full | segment=5/5 | chars=43
2026-05-26 15:24:32.626 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=59 | mode=full | segment=5/5 | duration_ms=3480
2026-05-26 15:24:32.628 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=59 | mode=full | created_segments=5/5
2026-05-26 15:24:32.630 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=59 | mode=full | chars=338
2026-05-26 15:24:42.505 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=58 | mode=full | segment=5/5 | duration_ms=24168
2026-05-26 15:24:42.505 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=58 | mode=full | created_segments=5/5
2026-05-26 15:24:42.509 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=58 | mode=full | chars=627
2026-05-26 15:24:47.304 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=59 | mode=full
2026-05-26 15:24:47.308 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=4509daaf-b229-4618-9e3f-33ea1182f8cd | mode=full | segments=5 | review_audio=True
[2026-05-26 15:24:49,650: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-26 15:24:50.415 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=4509daaf-b229-4618-9e3f-33ea1182f8cd | mode=full
[2026-05-26 15:24:50,532: INFO/MainProcess] Task triam.notifications.scan_due[0ae5c9af-788d-4e07-9cc4-23ce4c514737] received
2026-05-26 15:24:52.828 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 59 READY | mode=full | segments=5
2026-05-26 15:24:52.834 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=60 | mode=full | title=Phép toán số học trên tập số  nguyên | chars=304 | estimated_tokens=180 | estimated_audio_seconds=25
2026-05-26 15:24:55.047 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=60 | mode=full | rag=true | tts=true
2026-05-26 15:24:55.052 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=60 | mode=full | title=Phép toán số học trên tập số  nguyên | raw_chars=304
2026-05-26 15:24:55.052 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Phép toán số học trên tập số  nguyên | chars=304 | estimated_tokens=180 | estimated_audio_seconds=25
2026-05-26 15:24:55.053 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Phép toán số học trên tập số  nguyên
2026-05-26 15:24:55.054 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=304
2026-05-26 15:24:58.044 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:24:58,046: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[0ae5c9af-788d-4e07-9cc4-23ce4c514737] succeeded in 7.511370170977898s: None
2026-05-26 15:24:58.512 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=58 | mode=full
2026-05-26 15:24:58.513 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=8e5e5838-2e6e-45ed-9e6e-b463fb09cba5 | mode=full | segments=5 | review_audio=True
2026-05-26 15:25:01.583 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=8e5e5838-2e6e-45ed-9e6e-b463fb09cba5 | mode=full
2026-05-26 15:25:03.996 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 58 READY | mode=full | segments=5
2026-05-26 15:25:04.009 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=61 | mode=full | title=Một số tính chất của tập số nguyên | chars=163 | estimated_tokens=80 | estimated_audio_seconds=20
2026-05-26 15:25:06.218 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=61 | mode=full | rag=true | tts=true
2026-05-26 15:25:06.225 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=61 | mode=full | title=Một số tính chất của tập số nguyên | raw_chars=163
2026-05-26 15:25:06.227 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Một số tính chất của tập số nguyên | chars=163 | estimated_tokens=80 | estimated_audio_seconds=20
2026-05-26 15:25:06.228 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Một số tính chất của tập số nguyên
2026-05-26 15:25:09.562 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=5b493ae6-1de8-4054-a80a-a17ea4bbb80c
2026-05-26 15:25:10.241 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=ebc609de-7c6a-4de2-b227-f6fefd33f8c0
2026-05-26 15:25:18.099 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=4 | review_chars=454
2026-05-26 15:25:18.100 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=60 | mode=full | main_scripts=4 | review_chars=454
2026-05-26 15:25:18.106 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=60 | mode=full | total_scripts=4
2026-05-26 15:25:18.106 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=60 | mode=full | segment=1/4 | chars=242
2026-05-26 15:25:18.150 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=163
2026-05-26 15:25:23.244 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=60 | mode=full | segment=1/4 | duration_ms=14520
2026-05-26 15:25:23.246 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=60 | mode=full | segment=2/4 | chars=254
2026-05-26 15:25:25.169 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=2 | review_chars=478
2026-05-26 15:25:25.170 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=61 | mode=full | main_scripts=2 | review_chars=478
2026-05-26 15:25:25.170 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=61 | mode=full | total_scripts=2
2026-05-26 15:25:25.172 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=61 | mode=full | segment=1/2 | chars=167
2026-05-26 15:25:31.755 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=60 | mode=full | segment=2/4 | duration_ms=17064
2026-05-26 15:25:31.756 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=60 | mode=full | segment=3/4 | chars=265
2026-05-26 15:25:35.439 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=61 | mode=full | segment=1/2 | duration_ms=10752
2026-05-26 15:25:35.439 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=61 | mode=full | segment=2/2 | chars=280
2026-05-26 15:25:38.642 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=60 | mode=full | segment=3/4 | duration_ms=14400
2026-05-26 15:25:38.643 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=60 | mode=full | segment=4/4 | chars=327
2026-05-26 15:25:45.476 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=61 | mode=full | segment=2/2 | duration_ms=18072
2026-05-26 15:25:45.478 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=61 | mode=full | created_segments=2/2
2026-05-26 15:25:45.478 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=61 | mode=full | chars=478
[2026-05-26 15:25:49,650: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:25:50,313: INFO/MainProcess] Task triam.notifications.scan_due[476d7e9e-99cb-4fb1-a724-ad688d184a87] received
2026-05-26 15:25:50.972 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=60 | mode=full | segment=4/4 | duration_ms=18936
2026-05-26 15:25:50.973 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=60 | mode=full | created_segments=4/4
2026-05-26 15:25:50.974 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=60 | mode=full | chars=454
2026-05-26 15:25:57.475 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=61 | mode=full
2026-05-26 15:25:57.476 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=ebc609de-7c6a-4de2-b227-f6fefd33f8c0 | mode=full | segments=2 | review_audio=True
2026-05-26 15:25:57.829 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:25:57,831: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[476d7e9e-99cb-4fb1-a724-ad688d184a87] succeeded in 7.513981465017423s: None
2026-05-26 15:26:00.569 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=ebc609de-7c6a-4de2-b227-f6fefd33f8c0 | mode=full
2026-05-26 15:26:02.985 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 61 READY | mode=full | segments=2
2026-05-26 15:26:02.985 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=62 | mode=full | title=Phép chia trên tập số nguyên | chars=320 | estimated_tokens=175 | estimated_audio_seconds=43
2026-05-26 15:26:05.184 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=62 | mode=full | rag=true | tts=true
2026-05-26 15:26:05.201 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=62 | mode=full | title=Phép chia trên tập số nguyên | raw_chars=320
2026-05-26 15:26:05.204 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Phép chia trên tập số nguyên | chars=320 | estimated_tokens=175 | estimated_audio_seconds=43
2026-05-26 15:26:05.204 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Phép chia trên tập số nguyên
2026-05-26 15:26:05.205 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=320
2026-05-26 15:26:08.486 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=fc98afae-ee41-4d12-8191-3f25a27170d8
2026-05-26 15:26:10.890 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=60 | mode=full
2026-05-26 15:26:10.891 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=5b493ae6-1de8-4054-a80a-a17ea4bbb80c | mode=full | segments=4 | review_audio=True
2026-05-26 15:26:13.967 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=5b493ae6-1de8-4054-a80a-a17ea4bbb80c | mode=full
2026-05-26 15:26:16.380 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 60 READY | mode=full | segments=4
2026-05-26 15:26:16.381 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=63 | mode=full | title=Uớc số chung lớn nhất, bội số chung nhỏ nhất | chars=952 | estimated_tokens=538 | estimated_audio_seconds=97
2026-05-26 15:26:18.567 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=63 | mode=full | rag=true | tts=true
2026-05-26 15:26:18.577 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=63 | mode=full | title=Uớc số chung lớn nhất, bội số chung nhỏ nhất | raw_chars=952
2026-05-26 15:26:18.581 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Uớc số chung lớn nhất, bội số chung nhỏ nhất | chars=952 | estimated_tokens=538 | estimated_audio_seconds=97
2026-05-26 15:26:18.584 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Uớc số chung lớn nhất, bội số chung nhỏ nhất
2026-05-26 15:26:20.788 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=3 | review_chars=472
2026-05-26 15:26:20.788 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=62 | mode=full | main_scripts=3 | review_chars=472
2026-05-26 15:26:20.789 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=62 | mode=full | total_scripts=3
2026-05-26 15:26:20.789 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=62 | mode=full | segment=1/3 | chars=300
2026-05-26 15:26:20.817 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=952
2026-05-26 15:26:21.924 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=d99bddec-e2f6-4fa3-9f69-2ff850eb66f4
2026-05-26 15:26:31.940 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=62 | mode=full | segment=1/3 | duration_ms=19440
2026-05-26 15:26:31.942 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=62 | mode=full | segment=2/3 | chars=242
2026-05-26 15:26:36.455 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=5 | review_chars=558
2026-05-26 15:26:36.461 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=63 | mode=full | main_scripts=5 | review_chars=558
2026-05-26 15:26:36.463 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=63 | mode=full | total_scripts=5
2026-05-26 15:26:36.464 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=63 | mode=full | segment=1/5 | chars=389
2026-05-26 15:26:38.990 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=62 | mode=full | segment=2/3 | duration_ms=17784
2026-05-26 15:26:38.993 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=62 | mode=full | segment=3/3 | chars=182
2026-05-26 15:26:45.127 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=62 | mode=full | segment=3/3 | duration_ms=12168
2026-05-26 15:26:45.129 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=62 | mode=full | created_segments=3/3
2026-05-26 15:26:45.132 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=62 | mode=full | chars=472
[2026-05-26 15:26:49,650: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-26 15:26:50.232 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=63 | mode=full | segment=1/5 | duration_ms=26280
2026-05-26 15:26:50.234 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=63 | mode=full | segment=2/5 | chars=201
[2026-05-26 15:26:50,532: INFO/MainProcess] Task triam.notifications.scan_due[535d7e43-54b8-4623-955e-5dfdda446d15] received
2026-05-26 15:26:56.659 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=63 | mode=full | segment=2/5 | duration_ms=12648
2026-05-26 15:26:56.659 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=63 | mode=full | segment=3/5 | chars=361
2026-05-26 15:26:58.044 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:26:58,044: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[535d7e43-54b8-4623-955e-5dfdda446d15] succeeded in 7.510660958942026s: None
2026-05-26 15:26:58.133 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=62 | mode=full
2026-05-26 15:26:58.136 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=fc98afae-ee41-4d12-8191-3f25a27170d8 | mode=full | segments=3 | review_audio=True
2026-05-26 15:27:01.207 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=fc98afae-ee41-4d12-8191-3f25a27170d8 | mode=full
2026-05-26 15:27:03.615 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 62 READY | mode=full | segments=3
2026-05-26 15:27:03.629 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=64 | mode=full | title=Số nguyên tố | chars=665 | estimated_tokens=360 | estimated_audio_seconds=74
2026-05-26 15:27:05.842 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=64 | mode=full | rag=true | tts=true
2026-05-26 15:27:05.862 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=64 | mode=full | title=Số nguyên tố | raw_chars=665
2026-05-26 15:27:05.864 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Số nguyên tố | chars=665 | estimated_tokens=360 | estimated_audio_seconds=74
2026-05-26 15:27:05.865 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Số nguyên tố
2026-05-26 15:27:05.865 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=665
2026-05-26 15:27:09.252 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=63 | mode=full | segment=3/5 | duration_ms=23976
2026-05-26 15:27:09.253 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=63 | mode=full | segment=4/5 | chars=489
2026-05-26 15:27:10.402 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=359b0a2d-ed0e-4bb8-a52a-9c2f4eb29f6c
2026-05-26 15:27:18.560 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=63 | mode=full | segment=4/5 | duration_ms=27552
2026-05-26 15:27:18.564 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=63 | mode=full | segment=5/5 | chars=711
2026-05-26 15:27:29.094 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=7 | review_chars=653
2026-05-26 15:27:29.098 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=64 | mode=full | main_scripts=7 | review_chars=653
2026-05-26 15:27:29.098 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=64 | mode=full | total_scripts=7
2026-05-26 15:27:29.098 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=64 | mode=full | segment=1/7 | chars=215
2026-05-26 15:27:35.526 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=64 | mode=full | segment=1/7 | duration_ms=12888
2026-05-26 15:27:35.527 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=64 | mode=full | segment=2/7 | chars=275
2026-05-26 15:27:47.262 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=64 | mode=full | segment=2/7 | duration_ms=18816
2026-05-26 15:27:47.263 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=64 | mode=full | segment=3/7 | chars=231
[2026-05-26 15:27:49,651: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:27:50,433: INFO/MainProcess] Task triam.notifications.scan_due[afaac49c-d1bd-4723-981e-cbe92f463a7c] received
2026-05-26 15:27:52.652 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=63 | mode=full | segment=5/5 | duration_ms=47976
2026-05-26 15:27:52.653 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=63 | mode=full | created_segments=5/5
2026-05-26 15:27:52.653 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=63 | mode=full | chars=558
2026-05-26 15:27:57.945 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:27:57,946: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[afaac49c-d1bd-4723-981e-cbe92f463a7c] succeeded in 7.510075811063871s: None
2026-05-26 15:27:58.850 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=64 | mode=full | segment=3/7 | duration_ms=15504
2026-05-26 15:27:58.851 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=64 | mode=full | segment=4/7 | chars=225
2026-05-26 15:28:07.520 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=64 | mode=full | segment=4/7 | duration_ms=12960
2026-05-26 15:28:07.520 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=64 | mode=full | segment=5/7 | chars=161
2026-05-26 15:28:09.788 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=63 | mode=full
2026-05-26 15:28:09.789 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=d99bddec-e2f6-4fa3-9f69-2ff850eb66f4 | mode=full | segments=5 | review_audio=True
2026-05-26 15:28:12.857 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=d99bddec-e2f6-4fa3-9f69-2ff850eb66f4 | mode=full
2026-05-26 15:28:15.273 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 63 READY | mode=full | segments=5
2026-05-26 15:28:15.279 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=65 | mode=full | title=Nguyên lý nhân | chars=3462 | estimated_tokens=1734 | estimated_audio_seconds=377
2026-05-26 15:28:17.470 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=65 | mode=full | rag=true | tts=true
2026-05-26 15:28:17.479 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=65 | mode=full | title=Nguyên lý nhân | raw_chars=3462
2026-05-26 15:28:17.493 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Nguyên lý nhân | chars=3462 | estimated_tokens=1734 | estimated_audio_seconds=377
2026-05-26 15:28:17.494 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Nguyên lý nhân
2026-05-26 15:28:17.494 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=3462
2026-05-26 15:28:20.350 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=64 | mode=full | segment=5/7 | duration_ms=11736
2026-05-26 15:28:20.351 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=64 | mode=full | segment=6/7 | chars=300
2026-05-26 15:28:22.312 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 4 vectors for chapter_id=330a154b-16c4-4335-b301-b66334df650e
2026-05-26 15:28:28.774 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=64 | mode=full | segment=6/7 | duration_ms=18480
2026-05-26 15:28:28.774 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=64 | mode=full | segment=7/7 | chars=251
2026-05-26 15:28:40.523 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=64 | mode=full | segment=7/7 | duration_ms=16656
2026-05-26 15:28:40.526 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=64 | mode=full | created_segments=7/7
2026-05-26 15:28:40.528 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=64 | mode=full | chars=653
2026-05-26 15:28:43.904 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=17 | review_chars=684
2026-05-26 15:28:43.905 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=65 | mode=full | main_scripts=17 | review_chars=684
2026-05-26 15:28:43.908 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=65 | mode=full | total_scripts=17
2026-05-26 15:28:43.909 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=65 | mode=full | segment=1/17 | chars=314
[2026-05-26 15:28:49,651: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:28:50,527: INFO/MainProcess] Task triam.notifications.scan_due[f2a032f8-5dae-4f62-943f-3abe52298996] received
2026-05-26 15:28:56.962 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=65 | mode=full | segment=1/17 | duration_ms=21048
2026-05-26 15:28:56.965 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=65 | mode=full | segment=2/17 | chars=231
2026-05-26 15:28:58.037 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:28:58,038: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f2a032f8-5dae-4f62-943f-3abe52298996] succeeded in 7.509825302986428s: None
2026-05-26 15:29:02.846 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=64 | mode=full
2026-05-26 15:29:02.851 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=359b0a2d-ed0e-4bb8-a52a-9c2f4eb29f6c | mode=full | segments=7 | review_audio=True
2026-05-26 15:29:05.939 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=359b0a2d-ed0e-4bb8-a52a-9c2f4eb29f6c | mode=full
2026-05-26 15:29:08.352 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 64 READY | mode=full | segments=7
2026-05-26 15:29:08.355 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=66 | mode=full | title=Nguyên lý cộng | chars=1662 | estimated_tokens=807 | estimated_audio_seconds=181
2026-05-26 15:29:10.551 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=66 | mode=full | rag=true | tts=true
2026-05-26 15:29:10.558 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=66 | mode=full | title=Nguyên lý cộng | raw_chars=1662
2026-05-26 15:29:10.563 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Nguyên lý cộng | chars=1662 | estimated_tokens=807 | estimated_audio_seconds=181
2026-05-26 15:29:10.564 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Nguyên lý cộng
2026-05-26 15:29:10.565 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1662
2026-05-26 15:29:13.522 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=65 | mode=full | segment=2/17 | duration_ms=13848
2026-05-26 15:29:13.522 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=65 | mode=full | segment=3/17 | chars=228
2026-05-26 15:29:14.879 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 2 vectors for chapter_id=d8f7cfaa-d91e-469e-b2d6-2b2f713eca08
2026-05-26 15:29:24.754 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=65 | mode=full | segment=3/17 | duration_ms=13488
2026-05-26 15:29:24.755 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=65 | mode=full | segment=4/17 | chars=404
2026-05-26 15:29:30.183 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=6 | review_chars=606
2026-05-26 15:29:30.185 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=66 | mode=full | main_scripts=6 | review_chars=606
2026-05-26 15:29:30.187 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=66 | mode=full | total_scripts=6
2026-05-26 15:29:30.187 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=66 | mode=full | segment=1/6 | chars=404
2026-05-26 15:29:42.106 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=65 | mode=full | segment=4/17 | duration_ms=26232
2026-05-26 15:29:42.107 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=65 | mode=full | segment=5/17 | chars=223
2026-05-26 15:29:48.758 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=66 | mode=full | segment=1/6 | duration_ms=24144
2026-05-26 15:29:48.759 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=66 | mode=full | segment=2/6 | chars=310
[2026-05-26 15:29:49,651: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:29:50,526: INFO/MainProcess] Task triam.notifications.scan_due[d726f30c-dfd8-4f37-b73f-e79a08a230aa] received
2026-05-26 15:29:53.195 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=65 | mode=full | segment=5/17 | duration_ms=11928
2026-05-26 15:29:53.195 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=65 | mode=full | segment=6/17 | chars=405
2026-05-26 15:29:56.762 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=66 | mode=full | segment=2/6 | duration_ms=18432
2026-05-26 15:29:56.763 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=66 | mode=full | segment=3/6 | chars=428
2026-05-26 15:29:58.042 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:29:58,044: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d726f30c-dfd8-4f37-b73f-e79a08a230aa] succeeded in 7.514707003952935s: None
2026-05-26 15:30:02.824 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=65 | mode=full | segment=6/17 | duration_ms=23256
2026-05-26 15:30:02.826 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=65 | mode=full | segment=7/17 | chars=247
2026-05-26 15:30:11.293 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=66 | mode=full | segment=3/6 | duration_ms=27312
2026-05-26 15:30:11.293 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=66 | mode=full | segment=4/6 | chars=435
2026-05-26 15:30:12.521 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=65 | mode=full | segment=7/17 | duration_ms=17400
2026-05-26 15:30:12.522 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=65 | mode=full | segment=8/17 | chars=207
2026-05-26 15:30:24.813 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=65 | mode=full | segment=8/17 | duration_ms=13704
2026-05-26 15:30:24.816 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=65 | mode=full | segment=9/17 | chars=310
2026-05-26 15:30:31.014 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=66 | mode=full | segment=4/6 | duration_ms=27240
2026-05-26 15:30:31.015 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=66 | mode=full | segment=5/6 | chars=260
2026-05-26 15:30:39.016 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=65 | mode=full | segment=9/17 | duration_ms=22224
2026-05-26 15:30:39.016 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=65 | mode=full | segment=10/17 | chars=327
2026-05-26 15:30:40.205 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=66 | mode=full | segment=5/6 | duration_ms=15504
2026-05-26 15:30:40.206 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=66 | mode=full | segment=6/6 | chars=552
[2026-05-26 15:30:49,652: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:30:52,007: INFO/MainProcess] Task triam.notifications.scan_due[a4900c94-2480-4403-8cee-cea705a5bd25] received
2026-05-26 15:30:53.566 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=65 | mode=full | segment=10/17 | duration_ms=22848
2026-05-26 15:30:53.567 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=65 | mode=full | segment=11/17 | chars=268
2026-05-26 15:30:58.680 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=66 | mode=full | segment=6/6 | duration_ms=33768
2026-05-26 15:30:58.681 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=66 | mode=full | created_segments=6/6
2026-05-26 15:30:58.681 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=66 | mode=full | chars=606
2026-05-26 15:30:59.675 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:30:59,676: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a4900c94-2480-4403-8cee-cea705a5bd25] succeeded in 7.666603090940043s: None
2026-05-26 15:31:03.712 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=65 | mode=full | segment=11/17 | duration_ms=19056
2026-05-26 15:31:03.713 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=65 | mode=full | segment=12/17 | chars=221
2026-05-26 15:31:11.666 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=65 | mode=full | segment=12/17 | duration_ms=15528
2026-05-26 15:31:11.667 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=65 | mode=full | segment=13/17 | chars=448
2026-05-26 15:31:16.411 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=66 | mode=full
2026-05-26 15:31:16.414 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=d8f7cfaa-d91e-469e-b2d6-2b2f713eca08 | mode=full | segments=6 | review_audio=True
2026-05-26 15:31:20.937 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=d8f7cfaa-d91e-469e-b2d6-2b2f713eca08 | mode=full
2026-05-26 15:31:23.398 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 66 READY | mode=full | segments=6
2026-05-26 15:31:23.401 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=67 | mode=full | title=Nguyên lý bù trừ | chars=1987 | estimated_tokens=1030 | estimated_audio_seconds=235
2026-05-26 15:31:25.633 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=67 | mode=full | rag=true | tts=true
2026-05-26 15:31:25.638 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=67 | mode=full | title=Nguyên lý bù trừ | raw_chars=1987
2026-05-26 15:31:25.641 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Nguyên lý bù trừ | chars=1987 | estimated_tokens=1030 | estimated_audio_seconds=235
2026-05-26 15:31:25.644 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Nguyên lý bù trừ
2026-05-26 15:31:25.644 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1987
2026-05-26 15:31:29.386 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 2 vectors for chapter_id=7cd3d700-04df-4a2d-a025-c846e1aa2843
2026-05-26 15:31:30.611 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=65 | mode=full | segment=13/17 | duration_ms=27264
2026-05-26 15:31:30.612 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=65 | mode=full | segment=14/17 | chars=241
2026-05-26 15:31:39.688 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=65 | mode=full | segment=14/17 | duration_ms=15912
2026-05-26 15:31:39.688 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=65 | mode=full | segment=15/17 | chars=303
[2026-05-26 15:31:49,655: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:31:50,532: INFO/MainProcess] Task triam.notifications.scan_due[62a5367a-7e85-4d1b-88c9-eb59bcfcca58] received
2026-05-26 15:31:51.543 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=5 | review_chars=634
2026-05-26 15:31:51.547 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=67 | mode=full | main_scripts=5 | review_chars=634
2026-05-26 15:31:51.547 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=67 | mode=full | total_scripts=5
2026-05-26 15:31:51.548 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=67 | mode=full | segment=1/5 | chars=565
2026-05-26 15:31:55.006 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=65 | mode=full | segment=15/17 | duration_ms=20088
2026-05-26 15:31:55.008 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=65 | mode=full | segment=16/17 | chars=229
2026-05-26 15:31:58.045 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:31:58,046: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[62a5367a-7e85-4d1b-88c9-eb59bcfcca58] succeeded in 7.509973917971365s: None
2026-05-26 15:32:03.862 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=65 | mode=full | segment=16/17 | duration_ms=13896
2026-05-26 15:32:03.863 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=65 | mode=full | segment=17/17 | chars=357
2026-05-26 15:32:09.214 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=67 | mode=full | segment=1/5 | duration_ms=34680
2026-05-26 15:32:09.216 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=67 | mode=full | segment=2/5 | chars=624
2026-05-26 15:32:16.209 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=65 | mode=full | segment=17/17 | duration_ms=20808
2026-05-26 15:32:16.213 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=65 | mode=full | created_segments=17/17
2026-05-26 15:32:16.213 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=65 | mode=full | chars=684
2026-05-26 15:32:39.163 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=65 | mode=full
2026-05-26 15:32:39.164 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=330a154b-16c4-4335-b301-b66334df650e | mode=full | segments=17 | review_audio=True
2026-05-26 15:32:42.288 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=330a154b-16c4-4335-b301-b66334df650e | mode=full
2026-05-26 15:32:44.731 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 65 READY | mode=full | segments=17
2026-05-26 15:32:44.737 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=68 | mode=full | title=Nguyên lý  DIRICHLET | chars=4120 | estimated_tokens=2126 | estimated_audio_seconds=425
2026-05-26 15:32:46.961 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=68 | mode=full | rag=true | tts=true
2026-05-26 15:32:46.964 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=68 | mode=full | title=Nguyên lý  DIRICHLET | raw_chars=4120
2026-05-26 15:32:46.968 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Nguyên lý  DIRICHLET | chars=4120 | estimated_tokens=2126 | estimated_audio_seconds=425
2026-05-26 15:32:46.969 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Nguyên lý  DIRICHLET
2026-05-26 15:32:46.970 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=4120
[2026-05-26 15:32:49,655: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:32:50,310: INFO/MainProcess] Task triam.notifications.scan_due[c9b3f08b-297c-4e62-99e1-925c3a9af7e4] received
2026-05-26 15:32:50.703 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=67 | mode=full | segment=2/5 | duration_ms=44328
2026-05-26 15:32:50.703 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=67 | mode=full | segment=3/5 | chars=762
2026-05-26 15:32:52.884 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 5 vectors for chapter_id=2353124c-e965-4ec5-bb38-bf28dda1f0ab
2026-05-26 15:32:57.829 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:32:57,830: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c9b3f08b-297c-4e62-99e1-925c3a9af7e4] succeeded in 7.518358665984124s: None
2026-05-26 15:33:14.546 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=67 | mode=full | segment=3/5 | duration_ms=51912
2026-05-26 15:33:14.548 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=67 | mode=full | segment=4/5 | chars=452
2026-05-26 15:33:15.977 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=19 | review_chars=783
2026-05-26 15:33:15.977 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=68 | mode=full | main_scripts=19 | review_chars=783
2026-05-26 15:33:15.977 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=68 | mode=full | total_scripts=19
2026-05-26 15:33:15.978 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=1/19 | chars=235
2026-05-26 15:33:26.331 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=1/19 | duration_ms=14424
2026-05-26 15:33:26.333 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=2/19 | chars=209
2026-05-26 15:33:32.192 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=2/19 | duration_ms=12552
2026-05-26 15:33:32.193 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=3/19 | chars=232
2026-05-26 15:33:39.022 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=3/19 | duration_ms=13200
2026-05-26 15:33:39.023 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=4/19 | chars=352
2026-05-26 15:33:40.434 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=67 | mode=full | segment=4/5 | duration_ms=29328
2026-05-26 15:33:40.436 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=67 | mode=full | segment=5/5 | chars=932
[2026-05-26 15:33:49,655: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:33:50,526: INFO/MainProcess] Task triam.notifications.scan_due[7c32d941-c63c-4a45-8483-655d8e3788f3] received
2026-05-26 15:33:52.255 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=4/19 | duration_ms=20160
2026-05-26 15:33:52.257 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=5/19 | chars=417
2026-05-26 15:33:58.038 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:33:58,039: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[7c32d941-c63c-4a45-8483-655d8e3788f3] succeeded in 7.507835865020752s: None
2026-05-26 15:34:02.179 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=5/19 | duration_ms=22800
2026-05-26 15:34:02.181 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=6/19 | chars=132
2026-05-26 15:34:06.653 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=67 | mode=full | segment=5/5 | duration_ms=67416
2026-05-26 15:34:06.657 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=67 | mode=full | created_segments=5/5
2026-05-26 15:34:06.659 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=67 | mode=full | chars=634
2026-05-26 15:34:07.076 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=6/19 | duration_ms=7872
2026-05-26 15:34:07.079 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=7/19 | chars=219
2026-05-26 15:34:14.805 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=7/19 | duration_ms=13680
2026-05-26 15:34:14.807 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=8/19 | chars=187
2026-05-26 15:34:21.413 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=8/19 | duration_ms=11112
2026-05-26 15:34:21.417 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=9/19 | chars=308
2026-05-26 15:34:29.300 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=67 | mode=full
2026-05-26 15:34:29.304 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=7cd3d700-04df-4a2d-a025-c846e1aa2843 | mode=full | segments=5 | review_audio=True
2026-05-26 15:34:32.418 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=7cd3d700-04df-4a2d-a025-c846e1aa2843 | mode=full
2026-05-26 15:34:34.864 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 67 READY | mode=full | segments=5
2026-05-26 15:34:34.867 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=69 | mode=full | title=Chỉnh hợp | chars=1253 | estimated_tokens=680 | estimated_audio_seconds=139
2026-05-26 15:34:37.088 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=69 | mode=full | rag=true | tts=true
2026-05-26 15:34:37.094 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=69 | mode=full | title=Chỉnh hợp | raw_chars=1253
2026-05-26 15:34:37.099 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Chỉnh hợp | chars=1253 | estimated_tokens=680 | estimated_audio_seconds=139
2026-05-26 15:34:37.104 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Chỉnh hợp
2026-05-26 15:34:37.105 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1253
2026-05-26 15:34:39.985 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=9/19 | duration_ms=18312
2026-05-26 15:34:39.986 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=10/19 | chars=307
2026-05-26 15:34:41.675 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 2 vectors for chapter_id=f1c52eb9-5e7f-4629-b319-aac55a831eb9
[2026-05-26 15:34:49,656: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:34:50,526: INFO/MainProcess] Task triam.notifications.scan_due[d202f35a-b6f6-4a9c-b78a-31fcfa93fd6e] received
2026-05-26 15:34:51.736 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=10/19 | duration_ms=19920
2026-05-26 15:34:51.738 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=11/19 | chars=114
2026-05-26 15:34:58.032 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:34:58,034: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[d202f35a-b6f6-4a9c-b78a-31fcfa93fd6e] succeeded in 7.506186229060404s: None
2026-05-26 15:34:58.300 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=6 | review_chars=556
2026-05-26 15:34:58.301 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=69 | mode=full | main_scripts=6 | review_chars=556
2026-05-26 15:34:58.304 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=69 | mode=full | total_scripts=6
2026-05-26 15:34:58.306 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=69 | mode=full | segment=1/6 | chars=287
2026-05-26 15:34:59.709 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=11/19 | duration_ms=8256
2026-05-26 15:34:59.710 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=12/19 | chars=286
2026-05-26 15:35:10.667 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=12/19 | duration_ms=16367
2026-05-26 15:35:10.668 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=13/19 | chars=375
2026-05-26 15:35:12.076 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=69 | mode=full | segment=1/6 | duration_ms=18576
2026-05-26 15:35:12.080 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=69 | mode=full | segment=2/6 | chars=288
2026-05-26 15:35:17.729 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=69 | mode=full | segment=2/6 | duration_ms=6720
2026-05-26 15:35:17.730 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=69 | mode=full | segment=3/6 | chars=392
2026-05-26 15:35:23.065 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=13/19 | duration_ms=20568
2026-05-26 15:35:23.065 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=14/19 | chars=227
2026-05-26 15:35:23.501 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=69 | mode=full | segment=3/6 | duration_ms=120
2026-05-26 15:35:23.503 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=69 | mode=full | segment=4/6 | chars=456
2026-05-26 15:35:33.208 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=14/19 | duration_ms=13464
2026-05-26 15:35:33.210 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=15/19 | chars=293
2026-05-26 15:35:38.416 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=69 | mode=full | segment=4/6 | duration_ms=26352
2026-05-26 15:35:38.417 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=69 | mode=full | segment=5/6 | chars=290
2026-05-26 15:35:43.194 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=15/19 | duration_ms=16248
2026-05-26 15:35:43.199 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=16/19 | chars=383
[2026-05-26 15:35:49,661: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:35:50,699: INFO/MainProcess] Task triam.notifications.scan_due[55829238-dcfc-4bff-b6da-0f5700ffebd9] received
2026-05-26 15:35:51.672 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=69 | mode=full | segment=5/6 | duration_ms=21720
2026-05-26 15:35:51.676 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=69 | mode=full | segment=6/6 | chars=524
2026-05-26 15:35:56.313 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=16/19 | duration_ms=24792
2026-05-26 15:35:56.314 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=17/19 | chars=413
2026-05-26 15:35:58.401 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:35:58,406: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[55829238-dcfc-4bff-b6da-0f5700ffebd9] succeeded in 7.494318429031409s: None
2026-05-26 15:36:07.096 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=69 | mode=full | segment=6/6 | duration_ms=33384
2026-05-26 15:36:07.097 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=69 | mode=full | created_segments=6/6
2026-05-26 15:36:07.097 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=69 | mode=full | chars=556
2026-05-26 15:36:08.089 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=17/19 | duration_ms=26712
2026-05-26 15:36:08.090 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=18/19 | chars=319
2026-05-26 15:36:16.800 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=18/19 | duration_ms=21816
2026-05-26 15:36:16.802 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=68 | mode=full | segment=19/19 | chars=321
2026-05-26 15:36:22.264 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=69 | mode=full
2026-05-26 15:36:22.267 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=f1c52eb9-5e7f-4629-b319-aac55a831eb9 | mode=full | segments=6 | review_audio=True
2026-05-26 15:36:25.393 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=f1c52eb9-5e7f-4629-b319-aac55a831eb9 | mode=full
2026-05-26 15:36:27.844 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 69 READY | mode=full | segments=6
2026-05-26 15:36:27.845 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=70 | mode=full | title=Hoán vị | chars=1523 | estimated_tokens=807 | estimated_audio_seconds=168
2026-05-26 15:36:30.073 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=70 | mode=full | rag=true | tts=true
2026-05-26 15:36:30.082 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=70 | mode=full | title=Hoán vị | raw_chars=1523
2026-05-26 15:36:30.086 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Hoán vị | chars=1523 | estimated_tokens=807 | estimated_audio_seconds=168
2026-05-26 15:36:30.087 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Hoán vị
2026-05-26 15:36:30.088 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1523
2026-05-26 15:36:33.511 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=68 | mode=full | segment=19/19 | duration_ms=22056
2026-05-26 15:36:33.511 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=68 | mode=full | created_segments=19/19
2026-05-26 15:36:33.515 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=68 | mode=full | chars=783
2026-05-26 15:36:34.865 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 2 vectors for chapter_id=61c21ca0-4646-44d2-8921-f59e234f526d
2026-05-26 15:36:44.220 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=7 | review_chars=745
2026-05-26 15:36:44.221 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=70 | mode=full | main_scripts=7 | review_chars=745
2026-05-26 15:36:44.222 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=70 | mode=full | total_scripts=7
2026-05-26 15:36:44.224 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=70 | mode=full | segment=1/7 | chars=277
[2026-05-26 15:36:49,662: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:36:50,536: INFO/MainProcess] Task triam.notifications.scan_due[49b747da-4425-44f9-b0a5-cdec4cc3e3be] received
2026-05-26 15:36:51.626 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=68 | mode=full
2026-05-26 15:36:51.631 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=2353124c-e965-4ec5-bb38-bf28dda1f0ab | mode=full | segments=19 | review_audio=True
2026-05-26 15:36:54.786 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=2353124c-e965-4ec5-bb38-bf28dda1f0ab | mode=full
2026-05-26 15:36:57.250 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 68 READY | mode=full | segments=19
2026-05-26 15:36:57.254 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=71 | mode=full | title=Tổ hợp | chars=988 | estimated_tokens=504 | estimated_audio_seconds=107
2026-05-26 15:36:58.251 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:36:58,251: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[49b747da-4425-44f9-b0a5-cdec4cc3e3be] succeeded in 7.498012305935845s: None
2026-05-26 15:36:59.500 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=71 | mode=full | rag=true | tts=true
2026-05-26 15:36:59.503 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=71 | mode=full | title=Tổ hợp | raw_chars=988
2026-05-26 15:36:59.505 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Tổ hợp | chars=988 | estimated_tokens=504 | estimated_audio_seconds=107
2026-05-26 15:36:59.505 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Tổ hợp
2026-05-26 15:36:59.505 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=988
2026-05-26 15:37:02.411 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=70 | mode=full | segment=1/7 | duration_ms=19488
2026-05-26 15:37:02.412 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=70 | mode=full | segment=2/7 | chars=243
2026-05-26 15:37:03.768 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=c1d78c9c-eabf-40cf-a2bf-2604fd2f34ec
2026-05-26 15:37:12.760 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=4 | review_chars=570
2026-05-26 15:37:12.761 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=71 | mode=full | main_scripts=4 | review_chars=570
2026-05-26 15:37:12.762 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=71 | mode=full | total_scripts=4
2026-05-26 15:37:12.763 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=71 | mode=full | segment=1/4 | chars=278
2026-05-26 15:37:19.578 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=70 | mode=full | segment=2/7 | duration_ms=15288
2026-05-26 15:37:19.580 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=70 | mode=full | segment=3/7 | chars=245
2026-05-26 15:37:21.958 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=71 | mode=full | segment=1/4 | duration_ms=17376
2026-05-26 15:37:21.959 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=71 | mode=full | segment=2/4 | chars=179
2026-05-26 15:37:26.907 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=71 | mode=full | segment=2/4 | duration_ms=11856
2026-05-26 15:37:26.911 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=71 | mode=full | segment=3/4 | chars=521
2026-05-26 15:37:29.503 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=70 | mode=full | segment=3/7 | duration_ms=14664
2026-05-26 15:37:29.505 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=70 | mode=full | segment=4/7 | chars=245
2026-05-26 15:37:41.999 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=70 | mode=full | segment=4/7 | duration_ms=15840
2026-05-26 15:37:42.003 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=70 | mode=full | segment=5/7 | chars=272
2026-05-26 15:37:47.118 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=71 | mode=full | segment=3/4 | duration_ms=30984
2026-05-26 15:37:47.118 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=71 | mode=full | segment=4/4 | chars=483
[2026-05-26 15:37:49,673: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:37:50,327: INFO/MainProcess] Task triam.notifications.scan_due[89b6ec89-ef39-43ee-9f02-e21d2765f8fb] received
2026-05-26 15:37:53.759 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=70 | mode=full | segment=5/7 | duration_ms=15744
2026-05-26 15:37:53.761 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=70 | mode=full | segment=6/7 | chars=259
2026-05-26 15:37:57.880 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:37:57,882: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[89b6ec89-ef39-43ee-9f02-e21d2765f8fb] succeeded in 7.550521809025668s: None
2026-05-26 15:38:05.291 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=71 | mode=full | segment=4/4 | duration_ms=29184
2026-05-26 15:38:05.291 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=71 | mode=full | created_segments=4/4
2026-05-26 15:38:05.292 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=71 | mode=full | chars=570
2026-05-26 15:38:07.498 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=70 | mode=full | segment=6/7 | duration_ms=17784
2026-05-26 15:38:07.500 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=70 | mode=full | segment=7/7 | chars=271
2026-05-26 15:38:15.681 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=70 | mode=full | segment=7/7 | duration_ms=15864
2026-05-26 15:38:15.681 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=70 | mode=full | created_segments=7/7
2026-05-26 15:38:15.681 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=70 | mode=full | chars=745
2026-05-26 15:38:19.739 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=70 | mode=full
2026-05-26 15:38:19.739 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=61c21ca0-4646-44d2-8921-f59e234f526d | mode=full | segments=7 | review_audio=True
2026-05-26 15:38:22.866 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=61c21ca0-4646-44d2-8921-f59e234f526d | mode=full
2026-05-26 15:38:25.321 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 70 READY | mode=full | segments=7
2026-05-26 15:38:25.324 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=72 | mode=full | title=Chỉnh hợp lặp | chars=1842 | estimated_tokens=936 | estimated_audio_seconds=198
2026-05-26 15:38:27.553 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=72 | mode=full | rag=true | tts=true
2026-05-26 15:38:27.556 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=72 | mode=full | title=Chỉnh hợp lặp | raw_chars=1842
2026-05-26 15:38:27.558 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Chỉnh hợp lặp | chars=1842 | estimated_tokens=936 | estimated_audio_seconds=198
2026-05-26 15:38:27.558 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Chỉnh hợp lặp
2026-05-26 15:38:27.559 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1842
2026-05-26 15:38:30.763 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=71 | mode=full
2026-05-26 15:38:30.764 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=c1d78c9c-eabf-40cf-a2bf-2604fd2f34ec | mode=full | segments=4 | review_audio=True
2026-05-26 15:38:33.895 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=c1d78c9c-eabf-40cf-a2bf-2604fd2f34ec | mode=full
2026-05-26 15:38:36.349 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 71 READY | mode=full | segments=4
2026-05-26 15:38:36.361 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=73 | mode=full | title=Tổ hợp lặp | chars=3285 | estimated_tokens=1686 | estimated_audio_seconds=352
2026-05-26 15:38:38.591 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=73 | mode=full | rag=true | tts=true
2026-05-26 15:38:38.597 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=73 | mode=full | title=Tổ hợp lặp | raw_chars=3285
2026-05-26 15:38:38.605 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Tổ hợp lặp | chars=3285 | estimated_tokens=1686 | estimated_audio_seconds=352
2026-05-26 15:38:38.606 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Tổ hợp lặp
2026-05-26 15:38:42.557 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 4 vectors for chapter_id=12b2741b-6057-4e1e-9322-020f6206e734
2026-05-26 15:38:43.252 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 2 vectors for chapter_id=0653354d-fef5-4507-8e69-4f9a58ea8e4c
[2026-05-26 15:38:49,674: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:38:50,546: INFO/MainProcess] Task triam.notifications.scan_due[539cae3c-80ba-4de1-ac74-c658062e4c71] received
2026-05-26 15:38:58.251 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:38:58,252: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[539cae3c-80ba-4de1-ac74-c658062e4c71] succeeded in 7.491967382025905s: None
2026-05-26 15:39:02.622 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=11 | review_chars=685
2026-05-26 15:39:02.624 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=72 | mode=full | main_scripts=11 | review_chars=685
2026-05-26 15:39:02.624 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=72 | mode=full | total_scripts=11
2026-05-26 15:39:02.626 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=72 | mode=full | segment=1/11 | chars=225
2026-05-26 15:39:02.660 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=3285
2026-05-26 15:39:10.832 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=72 | mode=full | segment=1/11 | duration_ms=14904
2026-05-26 15:39:10.833 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=72 | mode=full | segment=2/11 | chars=120
2026-05-26 15:39:18.140 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=72 | mode=full | segment=2/11 | duration_ms=8664
2026-05-26 15:39:18.142 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=72 | mode=full | segment=3/11 | chars=292
2026-05-26 15:39:18.827 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=7 | review_chars=491
2026-05-26 15:39:18.829 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=73 | mode=full | main_scripts=7 | review_chars=491
2026-05-26 15:39:18.829 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=73 | mode=full | total_scripts=7
2026-05-26 15:39:18.831 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=73 | mode=full | segment=1/7 | chars=228
2026-05-26 15:39:28.298 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=73 | mode=full | segment=1/7 | duration_ms=15000
2026-05-26 15:39:28.299 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=73 | mode=full | segment=2/7 | chars=168
2026-05-26 15:39:29.013 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=72 | mode=full | segment=3/11 | duration_ms=18648
2026-05-26 15:39:29.014 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=72 | mode=full | segment=4/11 | chars=250
2026-05-26 15:39:34.386 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=73 | mode=full | segment=2/7 | duration_ms=12264
2026-05-26 15:39:34.387 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=73 | mode=full | segment=3/7 | chars=332
2026-05-26 15:39:39.900 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=72 | mode=full | segment=4/11 | duration_ms=18240
2026-05-26 15:39:39.901 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=72 | mode=full | segment=5/11 | chars=476
2026-05-26 15:39:43.172 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=73 | mode=full | segment=3/7 | duration_ms=22464
2026-05-26 15:39:43.173 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=73 | mode=full | segment=4/7 | chars=217
[2026-05-26 15:39:49,674: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:39:50,546: INFO/MainProcess] Task triam.notifications.scan_due[92eb2f23-2ce0-47ff-8bba-5f9ce1f01827] received
2026-05-26 15:39:52.803 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=72 | mode=full | segment=5/11 | duration_ms=26472
2026-05-26 15:39:52.805 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=72 | mode=full | segment=6/11 | chars=326
2026-05-26 15:39:54.261 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=73 | mode=full | segment=4/7 | duration_ms=14976
2026-05-26 15:39:54.266 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=73 | mode=full | segment=5/7 | chars=253
2026-05-26 15:39:58.271 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:39:58,272: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[92eb2f23-2ce0-47ff-8bba-5f9ce1f01827] succeeded in 7.50808663002681s: None
2026-05-26 15:40:01.439 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=72 | mode=full | segment=6/11 | duration_ms=21816
2026-05-26 15:40:01.439 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=72 | mode=full | segment=7/11 | chars=214
2026-05-26 15:40:02.527 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=73 | mode=full | segment=5/7 | duration_ms=15888
2026-05-26 15:40:02.531 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=73 | mode=full | segment=6/7 | chars=288
2026-05-26 15:40:09.058 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=72 | mode=full | segment=7/11 | duration_ms=13440
2026-05-26 15:40:09.059 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=72 | mode=full | segment=8/11 | chars=125
2026-05-26 15:40:14.044 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=72 | mode=full | segment=8/11 | duration_ms=8183
2026-05-26 15:40:14.045 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=72 | mode=full | segment=9/11 | chars=346
2026-05-26 15:40:16.558 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=73 | mode=full | segment=6/7 | duration_ms=19248
2026-05-26 15:40:16.560 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=73 | mode=full | segment=7/7 | chars=302
2026-05-26 15:40:26.708 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=73 | mode=full | segment=7/7 | duration_ms=18912
2026-05-26 15:40:26.709 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=73 | mode=full | created_segments=7/7
2026-05-26 15:40:26.709 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=73 | mode=full | chars=491
2026-05-26 15:40:31.602 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=72 | mode=full | segment=9/11 | duration_ms=24672
2026-05-26 15:40:31.605 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=72 | mode=full | segment=10/11 | chars=259
2026-05-26 15:40:38.515 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=73 | mode=full
2026-05-26 15:40:38.515 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=12b2741b-6057-4e1e-9322-020f6206e734 | mode=full | segments=7 | review_audio=True
2026-05-26 15:40:41.638 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=12b2741b-6057-4e1e-9322-020f6206e734 | mode=full
2026-05-26 15:40:44.090 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 73 READY | mode=full | segments=7
2026-05-26 15:40:44.094 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=74 | mode=full | title=Phép chia hết | chars=563 | estimated_tokens=324 | estimated_audio_seconds=74
2026-05-26 15:40:46.331 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=74 | mode=full | rag=true | tts=true
2026-05-26 15:40:46.333 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=74 | mode=full | title=Phép chia hết | raw_chars=563
2026-05-26 15:40:46.335 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Phép chia hết | chars=563 | estimated_tokens=324 | estimated_audio_seconds=74
2026-05-26 15:40:46.335 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Phép chia hết
2026-05-26 15:40:46.336 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=563
[2026-05-26 15:40:49,674: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:40:50,555: INFO/MainProcess] Task triam.notifications.scan_due[8d51c372-c4b9-448f-b877-bcd418e89e8a] received
2026-05-26 15:40:53.031 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=72 | mode=full | segment=10/11 | duration_ms=19176
2026-05-26 15:40:53.032 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=72 | mode=full | segment=11/11 | chars=300
2026-05-26 15:40:54.237 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=517a9eda-afad-41e8-bf6c-0118bba5883e
2026-05-26 15:40:58.273 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:40:58,274: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8d51c372-c4b9-448f-b877-bcd418e89e8a] succeeded in 7.505305403959937s: None
2026-05-26 15:40:58.523 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=72 | mode=full | segment=11/11 | duration_ms=16440
2026-05-26 15:40:58.524 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=72 | mode=full | created_segments=11/11
2026-05-26 15:40:58.524 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=72 | mode=full | chars=685
2026-05-26 15:41:14.676 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=72 | mode=full
2026-05-26 15:41:14.679 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=0653354d-fef5-4507-8e69-4f9a58ea8e4c | mode=full | segments=11 | review_audio=True
2026-05-26 15:41:17.969 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=0653354d-fef5-4507-8e69-4f9a58ea8e4c | mode=full
2026-05-26 15:41:20.436 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 72 READY | mode=full | segments=11
2026-05-26 15:41:20.443 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=75 | mode=full | title=Phép chia có dư | chars=166 | estimated_tokens=87 | estimated_audio_seconds=21
2026-05-26 15:41:22.681 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=75 | mode=full | rag=true | tts=true
2026-05-26 15:41:22.682 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=5 | review_chars=597
2026-05-26 15:41:22.684 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=74 | mode=full | main_scripts=5 | review_chars=597
2026-05-26 15:41:22.685 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=74 | mode=full | total_scripts=5
2026-05-26 15:41:22.686 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=74 | mode=full | segment=1/5 | chars=248
2026-05-26 15:41:22.711 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=75 | mode=full | title=Phép chia có dư | raw_chars=166
2026-05-26 15:41:22.714 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Phép chia có dư | chars=166 | estimated_tokens=87 | estimated_audio_seconds=21
2026-05-26 15:41:22.715 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Phép chia có dư
2026-05-26 15:41:22.715 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=166
2026-05-26 15:41:26.078 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=6934e445-58f0-4b27-8c45-25d9fbf62006
2026-05-26 15:41:34.750 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=4 | review_chars=428
2026-05-26 15:41:34.752 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=75 | mode=full | main_scripts=4 | review_chars=428
2026-05-26 15:41:34.753 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=75 | mode=full | total_scripts=4
2026-05-26 15:41:34.755 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=75 | mode=full | segment=1/4 | chars=127
2026-05-26 15:41:36.900 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=74 | mode=full | segment=1/5 | duration_ms=16920
2026-05-26 15:41:36.904 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=74 | mode=full | segment=2/5 | chars=312
2026-05-26 15:41:44.119 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=75 | mode=full | segment=1/4 | duration_ms=8568
2026-05-26 15:41:44.123 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=75 | mode=full | segment=2/4 | chars=211
2026-05-26 15:41:47.755 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=74 | mode=full | segment=2/5 | duration_ms=20880
2026-05-26 15:41:47.756 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=74 | mode=full | segment=3/5 | chars=137
[2026-05-26 15:41:49,675: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:41:50,544: INFO/MainProcess] Task triam.notifications.scan_due[07161ff0-fb80-4732-a5c2-37cf85a4d517] received
2026-05-26 15:41:57.186 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=74 | mode=full | segment=3/5 | duration_ms=11952
2026-05-26 15:41:57.190 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=74 | mode=full | segment=4/5 | chars=263
2026-05-26 15:41:57.944 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=75 | mode=full | segment=2/4 | duration_ms=13176
2026-05-26 15:41:57.944 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=75 | mode=full | segment=3/4 | chars=158
2026-05-26 15:41:59.938 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:41:59,938: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[07161ff0-fb80-4732-a5c2-37cf85a4d517] succeeded in 9.180336049059406s: None
2026-05-26 15:42:03.071 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=75 | mode=full | segment=3/4 | duration_ms=11736
2026-05-26 15:42:03.072 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=75 | mode=full | segment=4/4 | chars=72
2026-05-26 15:42:06.177 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=75 | mode=full | segment=4/4 | duration_ms=4656
2026-05-26 15:42:06.178 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=75 | mode=full | created_segments=4/4
2026-05-26 15:42:06.180 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=75 | mode=full | chars=428
2026-05-26 15:42:09.275 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=74 | mode=full | segment=4/5 | duration_ms=18000
2026-05-26 15:42:09.276 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=74 | mode=full | segment=5/5 | chars=354
2026-05-26 15:42:19.198 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=75 | mode=full
2026-05-26 15:42:19.198 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=6934e445-58f0-4b27-8c45-25d9fbf62006 | mode=full | segments=4 | review_audio=True
2026-05-26 15:42:22.316 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=6934e445-58f0-4b27-8c45-25d9fbf62006 | mode=full
2026-05-26 15:42:24.759 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 75 READY | mode=full | segments=4
2026-05-26 15:42:24.765 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=76 | mode=full | title=Ước chung lớn nhất (UCLN) | chars=2279 | estimated_tokens=1246 | estimated_audio_seconds=248
2026-05-26 15:42:26.986 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=76 | mode=full | rag=true | tts=true
2026-05-26 15:42:26.988 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=76 | mode=full | title=Ước chung lớn nhất (UCLN) | raw_chars=2279
2026-05-26 15:42:26.990 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Ước chung lớn nhất (UCLN) | chars=2279 | estimated_tokens=1246 | estimated_audio_seconds=248
2026-05-26 15:42:26.994 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Ước chung lớn nhất (UCLN)
2026-05-26 15:42:26.996 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=2279
2026-05-26 15:42:30.250 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=74 | mode=full | segment=5/5 | duration_ms=26088
2026-05-26 15:42:30.250 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=74 | mode=full | created_segments=5/5
2026-05-26 15:42:30.251 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=74 | mode=full | chars=597
2026-05-26 15:42:31.922 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 3 vectors for chapter_id=1ce197a5-c168-44e3-a380-7baf248a7cac
2026-05-26 15:42:47.595 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=74 | mode=full
2026-05-26 15:42:47.595 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=517a9eda-afad-41e8-bf6c-0118bba5883e | mode=full | segments=5 | review_audio=True
[2026-05-26 15:42:49,676: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:42:50,331: INFO/MainProcess] Task triam.notifications.scan_due[b976f9ef-eeba-45e5-b387-8eaaeb87c6fb] received
2026-05-26 15:42:50.706 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=517a9eda-afad-41e8-bf6c-0118bba5883e | mode=full
2026-05-26 15:42:53.148 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 74 READY | mode=full | segments=5
2026-05-26 15:42:53.149 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=77 | mode=full | title=Bội chung nhỏ nhất (BCNN) | chars=1192 | estimated_tokens=653 | estimated_audio_seconds=132
2026-05-26 15:42:55.380 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=77 | mode=full | rag=true | tts=true
2026-05-26 15:42:55.388 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=77 | mode=full | title=Bội chung nhỏ nhất (BCNN) | raw_chars=1192
2026-05-26 15:42:55.389 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Bội chung nhỏ nhất (BCNN) | chars=1192 | estimated_tokens=653 | estimated_audio_seconds=132
2026-05-26 15:42:55.390 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Bội chung nhỏ nhất (BCNN)
2026-05-26 15:42:58.248 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:42:58,249: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b976f9ef-eeba-45e5-b387-8eaaeb87c6fb] succeeded in 7.915277326013893s: None
2026-05-26 15:42:58.969 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=d257b3e2-f02b-4ce5-a30d-6a9a09ca646b
2026-05-26 15:43:02.319 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=22 | review_chars=590
2026-05-26 15:43:02.321 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=76 | mode=full | main_scripts=22 | review_chars=590
2026-05-26 15:43:02.324 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=76 | mode=full | total_scripts=22
2026-05-26 15:43:02.326 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=1/22 | chars=146
2026-05-26 15:43:02.366 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1192
2026-05-26 15:43:09.170 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=1/22 | duration_ms=9912
2026-05-26 15:43:09.172 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=2/22 | chars=233
2026-05-26 15:43:22.648 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=2/22 | duration_ms=16032
2026-05-26 15:43:22.651 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=3/22 | chars=274
2026-05-26 15:43:25.174 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=14 | review_chars=679
2026-05-26 15:43:25.175 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=77 | mode=full | main_scripts=14 | review_chars=679
2026-05-26 15:43:25.176 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=77 | mode=full | total_scripts=14
2026-05-26 15:43:25.177 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=77 | mode=full | segment=1/14 | chars=126
2026-05-26 15:43:30.125 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=3/22 | duration_ms=18096
2026-05-26 15:43:30.126 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=4/22 | chars=246
2026-05-26 15:43:30.570 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=77 | mode=full | segment=1/14 | duration_ms=8496
2026-05-26 15:43:30.575 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=77 | mode=full | segment=2/14 | chars=248
2026-05-26 15:43:39.934 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=77 | mode=full | segment=2/14 | duration_ms=19728
2026-05-26 15:43:39.936 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=77 | mode=full | segment=3/14 | chars=229
2026-05-26 15:43:44.830 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=4/22 | duration_ms=19488
2026-05-26 15:43:44.832 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=5/22 | chars=116
2026-05-26 15:43:46.670 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=77 | mode=full | segment=3/14 | duration_ms=15864
2026-05-26 15:43:46.674 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=77 | mode=full | segment=4/14 | chars=215
2026-05-26 15:43:47.206 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=5/22 | duration_ms=6048
2026-05-26 15:43:47.207 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=6/22 | chars=349
[2026-05-26 15:43:49,676: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:43:50,546: INFO/MainProcess] Task triam.notifications.scan_due[2d20b8ef-371a-4fb8-a3f2-eb6d66fee439] received
2026-05-26 15:43:52.161 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=77 | mode=full | segment=4/14 | duration_ms=15576
2026-05-26 15:43:52.164 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=77 | mode=full | segment=5/14 | chars=223
2026-05-26 15:43:56.913 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=77 | mode=full | segment=5/14 | duration_ms=14496
2026-05-26 15:43:56.916 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=77 | mode=full | segment=6/14 | chars=291
2026-05-26 15:43:58.527 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:43:58,528: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2d20b8ef-371a-4fb8-a3f2-eb6d66fee439] succeeded in 7.765817423001863s: None
2026-05-26 15:43:59.550 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=6/22 | duration_ms=28488
2026-05-26 15:43:59.551 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=7/22 | chars=251
2026-05-26 15:44:06.273 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=77 | mode=full | segment=6/14 | duration_ms=17088
2026-05-26 15:44:06.277 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=77 | mode=full | segment=7/14 | chars=209
2026-05-26 15:44:07.725 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=7/22 | duration_ms=17448
2026-05-26 15:44:07.726 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=8/22 | chars=383
2026-05-26 15:44:11.705 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=77 | mode=full | segment=7/14 | duration_ms=14592
2026-05-26 15:44:11.706 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=77 | mode=full | segment=8/14 | chars=138
2026-05-26 15:44:15.943 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=77 | mode=full | segment=8/14 | duration_ms=8520
2026-05-26 15:44:15.945 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=77 | mode=full | segment=9/14 | chars=247
2026-05-26 15:44:19.108 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=8/22 | duration_ms=26928
2026-05-26 15:44:19.108 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=9/22 | chars=280
2026-05-26 15:44:25.793 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=77 | mode=full | segment=9/14 | duration_ms=14808
2026-05-26 15:44:25.794 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=77 | mode=full | segment=10/14 | chars=297
2026-05-26 15:44:27.178 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=9/22 | duration_ms=20952
2026-05-26 15:44:27.179 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=10/22 | chars=163
2026-05-26 15:44:31.389 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=10/22 | duration_ms=13872
2026-05-26 15:44:31.390 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=11/22 | chars=218
2026-05-26 15:44:37.265 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=77 | mode=full | segment=10/14 | duration_ms=18000
2026-05-26 15:44:37.267 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=77 | mode=full | segment=11/14 | chars=375
2026-05-26 15:44:39.989 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=11/22 | duration_ms=17592
2026-05-26 15:44:39.991 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=12/22 | chars=200
2026-05-26 15:44:44.401 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=77 | mode=full | segment=11/14 | duration_ms=25128
2026-05-26 15:44:44.401 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=77 | mode=full | segment=12/14 | chars=199
2026-05-26 15:44:45.618 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=12/22 | duration_ms=14808
2026-05-26 15:44:45.620 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=13/22 | chars=123
2026-05-26 15:44:48.651 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=77 | mode=full | segment=12/14 | duration_ms=13248
2026-05-26 15:44:48.651 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=77 | mode=full | segment=13/14 | chars=230
2026-05-26 15:44:49.125 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=13/22 | duration_ms=9456
2026-05-26 15:44:49.126 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=14/22 | chars=106
[2026-05-26 15:44:49,676: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:44:50,549: INFO/MainProcess] Task triam.notifications.scan_due[cb51414b-8615-45db-9861-cf7a04c1a96a] received
2026-05-26 15:44:52.993 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=14/22 | duration_ms=8064
2026-05-26 15:44:52.995 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=15/22 | chars=127
2026-05-26 15:44:55.088 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=77 | mode=full | segment=13/14 | duration_ms=17112
2026-05-26 15:44:55.090 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=77 | mode=full | segment=14/14 | chars=186
2026-05-26 15:44:55.686 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=15/22 | duration_ms=9504
2026-05-26 15:44:55.689 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=16/22 | chars=105
2026-05-26 15:44:58.533 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:44:58,534: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[cb51414b-8615-45db-9861-cf7a04c1a96a] succeeded in 7.76857406005729s: None
2026-05-26 15:44:59.328 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=16/22 | duration_ms=8592
2026-05-26 15:44:59.329 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=17/22 | chars=128
2026-05-26 15:45:00.426 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=77 | mode=full | segment=14/14 | duration_ms=12000
2026-05-26 15:45:00.427 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=77 | mode=full | created_segments=14/14
2026-05-26 15:45:00.427 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=77 | mode=full | chars=679
2026-05-26 15:45:04.393 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=17/22 | duration_ms=10200
2026-05-26 15:45:04.395 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=18/22 | chars=188
2026-05-26 15:45:09.864 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=18/22 | duration_ms=13944
2026-05-26 15:45:09.865 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=19/22 | chars=172
2026-05-26 15:45:13.363 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=19/22 | duration_ms=10008
2026-05-26 15:45:13.365 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=20/22 | chars=296
2026-05-26 15:45:18.794 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=77 | mode=full
2026-05-26 15:45:18.796 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=d257b3e2-f02b-4ce5-a30d-6a9a09ca646b | mode=full | segments=14 | review_audio=True
2026-05-26 15:45:21.939 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=d257b3e2-f02b-4ce5-a30d-6a9a09ca646b | mode=full
2026-05-26 15:45:24.398 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 77 READY | mode=full | segments=14
2026-05-26 15:45:24.401 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=78 | mode=full | title=Số nguyên tố | chars=256 | estimated_tokens=126 | estimated_audio_seconds=29
2026-05-26 15:45:26.628 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=78 | mode=full | rag=true | tts=true
2026-05-26 15:45:26.634 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=78 | mode=full | title=Số nguyên tố | raw_chars=256
2026-05-26 15:45:26.637 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Số nguyên tố | chars=256 | estimated_tokens=126 | estimated_audio_seconds=29
2026-05-26 15:45:26.639 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Số nguyên tố
2026-05-26 15:45:26.640 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=256
2026-05-26 15:45:29.618 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=20/22 | duration_ms=20136
2026-05-26 15:45:29.619 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=21/22 | chars=304
2026-05-26 15:45:30.928 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=e7e61fea-de92-44af-9696-48f5c9c15870
2026-05-26 15:45:34.456 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=2 | review_chars=402
2026-05-26 15:45:34.458 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=78 | mode=full | main_scripts=2 | review_chars=402
2026-05-26 15:45:34.460 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=78 | mode=full | total_scripts=2
2026-05-26 15:45:34.461 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=78 | mode=full | segment=1/2 | chars=211
2026-05-26 15:45:38.713 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=21/22 | duration_ms=20976
2026-05-26 15:45:38.714 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=76 | mode=full | segment=22/22 | chars=416
2026-05-26 15:45:39.616 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=78 | mode=full | segment=1/2 | duration_ms=12648
2026-05-26 15:45:39.616 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=78 | mode=full | segment=2/2 | chars=79
2026-05-26 15:45:45.477 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=78 | mode=full | segment=2/2 | duration_ms=7320
2026-05-26 15:45:45.478 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=78 | mode=full | created_segments=2/2
2026-05-26 15:45:45.478 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=78 | mode=full | chars=402
[2026-05-26 15:45:49,678: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:45:50,546: INFO/MainProcess] Task triam.notifications.scan_due[f0f366a7-d6e7-4b08-bb8f-a753c2ef0666] received
2026-05-26 15:45:58.528 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:45:58,528: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f0f366a7-d6e7-4b08-bb8f-a753c2ef0666] succeeded in 7.768437204998918s: None
2026-05-26 15:46:00.797 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=78 | mode=full
2026-05-26 15:46:00.798 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=e7e61fea-de92-44af-9696-48f5c9c15870 | mode=full | segments=2 | review_audio=True
2026-05-26 15:46:03.917 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=e7e61fea-de92-44af-9696-48f5c9c15870 | mode=full
2026-05-26 15:46:06.373 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 78 READY | mode=full | segments=2
2026-05-26 15:46:06.380 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=79 | mode=full | title=Hợp số | chars=648 | estimated_tokens=352 | estimated_audio_seconds=75
2026-05-26 15:46:08.605 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=79 | mode=full | rag=true | tts=true
2026-05-26 15:46:08.613 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=79 | mode=full | title=Hợp số | raw_chars=648
2026-05-26 15:46:08.628 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Hợp số | chars=648 | estimated_tokens=352 | estimated_audio_seconds=75
2026-05-26 15:46:08.628 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Hợp số
2026-05-26 15:46:08.628 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=648
2026-05-26 15:46:12.269 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=76 | mode=full | segment=22/22 | duration_ms=28104
2026-05-26 15:46:12.271 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=76 | mode=full | created_segments=22/22
2026-05-26 15:46:12.272 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=76 | mode=full | chars=590
2026-05-26 15:46:13.691 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=ed14022c-86f1-4223-a457-2959a8504ad3
2026-05-26 15:46:21.846 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=5 | review_chars=537
2026-05-26 15:46:21.848 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=79 | mode=full | main_scripts=5 | review_chars=537
2026-05-26 15:46:21.849 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=79 | mode=full | total_scripts=5
2026-05-26 15:46:21.851 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=79 | mode=full | segment=1/5 | chars=228
2026-05-26 15:46:28.537 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=79 | mode=full | segment=1/5 | duration_ms=13536
2026-05-26 15:46:28.543 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=79 | mode=full | segment=2/5 | chars=167
2026-05-26 15:46:33.415 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=76 | mode=full
2026-05-26 15:46:33.418 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=1ce197a5-c168-44e3-a380-7baf248a7cac | mode=full | segments=22 | review_audio=True
2026-05-26 15:46:36.581 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=1ce197a5-c168-44e3-a380-7baf248a7cac | mode=full
2026-05-26 15:46:39.030 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 76 READY | mode=full | segments=22
2026-05-26 15:46:39.036 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=80 | mode=full | title=Bảng số nguyên tố - Sàng Erathosthene | chars=884 | estimated_tokens=431 | estimated_audio_seconds=98
2026-05-26 15:46:41.266 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=80 | mode=full | rag=true | tts=true
2026-05-26 15:46:41.275 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=80 | mode=full | title=Bảng số nguyên tố - Sàng Erathosthene | raw_chars=884
2026-05-26 15:46:41.279 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Bảng số nguyên tố - Sàng Erathosthene | chars=884 | estimated_tokens=431 | estimated_audio_seconds=98
2026-05-26 15:46:41.281 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Bảng số nguyên tố - Sàng Erathosthene
2026-05-26 15:46:41.283 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=884
2026-05-26 15:46:44.607 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=79 | mode=full | segment=2/5 | duration_ms=12936
2026-05-26 15:46:44.608 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=79 | mode=full | segment=3/5 | chars=290
2026-05-26 15:46:45.867 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=7f3d448c-3269-4fd4-99c3-8a36aed21080
[2026-05-26 15:46:49,678: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:46:50,548: INFO/MainProcess] Task triam.notifications.scan_due[3052e752-b3e7-4e6c-9875-404d808af19b] received
2026-05-26 15:46:53.972 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=79 | mode=full | segment=3/5 | duration_ms=19296
2026-05-26 15:46:53.975 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=79 | mode=full | segment=4/5 | chars=280
2026-05-26 15:46:55.727 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=4 | review_chars=667
2026-05-26 15:46:55.728 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=80 | mode=full | main_scripts=4 | review_chars=667
2026-05-26 15:46:55.729 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=80 | mode=full | total_scripts=4
2026-05-26 15:46:55.729 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=80 | mode=full | segment=1/4 | chars=293
2026-05-26 15:46:58.525 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:46:58,527: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3052e752-b3e7-4e6c-9875-404d808af19b] succeeded in 7.765030006994493s: None
2026-05-26 15:47:03.586 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=80 | mode=full | segment=1/4 | duration_ms=17328
2026-05-26 15:47:03.587 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=80 | mode=full | segment=2/4 | chars=176
2026-05-26 15:47:05.582 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=79 | mode=full | segment=4/5 | duration_ms=18312
2026-05-26 15:47:05.584 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=79 | mode=full | segment=5/5 | chars=242
2026-05-26 15:47:10.535 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=80 | mode=full | segment=2/4 | duration_ms=10992
2026-05-26 15:47:10.536 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=80 | mode=full | segment=3/4 | chars=444
2026-05-26 15:47:12.903 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=79 | mode=full | segment=5/5 | duration_ms=14832
2026-05-26 15:47:12.906 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=79 | mode=full | created_segments=5/5
2026-05-26 15:47:12.910 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=79 | mode=full | chars=537
2026-05-26 15:47:28.258 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=80 | mode=full | segment=3/4 | duration_ms=27576
2026-05-26 15:47:28.259 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=80 | mode=full | segment=4/4 | chars=626
2026-05-26 15:47:35.916 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=79 | mode=full
2026-05-26 15:47:35.917 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=ed14022c-86f1-4223-a457-2959a8504ad3 | mode=full | segments=5 | review_audio=True
2026-05-26 15:47:39.045 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=ed14022c-86f1-4223-a457-2959a8504ad3 | mode=full
2026-05-26 15:47:41.498 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 79 READY | mode=full | segments=5
2026-05-26 15:47:41.501 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=81 | mode=full | title=Định lý cơ bản của số học | chars=1611 | estimated_tokens=858 | estimated_audio_seconds=181
2026-05-26 15:47:43.726 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=81 | mode=full | rag=true | tts=true
2026-05-26 15:47:43.732 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=81 | mode=full | title=Định lý cơ bản của số học | raw_chars=1611
2026-05-26 15:47:43.735 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Định lý cơ bản của số học | chars=1611 | estimated_tokens=858 | estimated_audio_seconds=181
2026-05-26 15:47:43.736 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Định lý cơ bản của số học
2026-05-26 15:47:43.739 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1611
2026-05-26 15:47:47.507 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=80 | mode=full | segment=4/4 | duration_ms=38568
2026-05-26 15:47:47.509 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=80 | mode=full | created_segments=4/4
2026-05-26 15:47:47.510 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=80 | mode=full | chars=667
2026-05-26 15:47:48.946 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 2 vectors for chapter_id=1a261f6b-cfb4-492c-947a-5d17474e1d8b
[2026-05-26 15:47:49,680: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:47:50,337: INFO/MainProcess] Task triam.notifications.scan_due[e1036015-9abc-4d3c-b2e9-7a439b97f9ea] received
2026-05-26 15:47:58.124 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:47:58,125: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[e1036015-9abc-4d3c-b2e9-7a439b97f9ea] succeeded in 7.786538472981192s: None
2026-05-26 15:48:11.073 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=11 | review_chars=758
2026-05-26 15:48:11.076 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=81 | mode=full | main_scripts=11 | review_chars=758
2026-05-26 15:48:11.077 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=81 | mode=full | total_scripts=11
2026-05-26 15:48:11.078 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=81 | mode=full | segment=1/11 | chars=400
2026-05-26 15:48:15.634 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=80 | mode=full
2026-05-26 15:48:15.635 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=7f3d448c-3269-4fd4-99c3-8a36aed21080 | mode=full | segments=4 | review_audio=True
2026-05-26 15:48:18.754 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=7f3d448c-3269-4fd4-99c3-8a36aed21080 | mode=full
2026-05-26 15:48:21.216 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 80 READY | mode=full | segments=4
2026-05-26 15:48:21.221 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=82 | mode=full | title=Phương trình nguyên | chars=202 | estimated_tokens=114 | estimated_audio_seconds=24
2026-05-26 15:48:23.451 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=82 | mode=full | rag=true | tts=true
2026-05-26 15:48:23.465 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=82 | mode=full | title=Phương trình nguyên | raw_chars=202
2026-05-26 15:48:23.471 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Phương trình nguyên | chars=202 | estimated_tokens=114 | estimated_audio_seconds=24
2026-05-26 15:48:23.473 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Phương trình nguyên
2026-05-26 15:48:23.476 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=202
2026-05-26 15:48:26.885 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=81 | mode=full | segment=1/11 | duration_ms=26496
2026-05-26 15:48:26.886 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=81 | mode=full | segment=2/11 | chars=343
2026-05-26 15:48:27.956 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=57b28f7e-3824-49ca-8436-2056f9151109
2026-05-26 15:48:32.773 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=2 | review_chars=496
2026-05-26 15:48:32.780 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=82 | mode=full | main_scripts=2 | review_chars=496
2026-05-26 15:48:32.781 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=82 | mode=full | total_scripts=2
2026-05-26 15:48:32.781 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=82 | mode=full | segment=1/2 | chars=161
2026-05-26 15:48:36.224 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=82 | mode=full | segment=1/2 | duration_ms=8688
2026-05-26 15:48:36.226 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=82 | mode=full | segment=2/2 | chars=343
2026-05-26 15:48:36.894 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=81 | mode=full | segment=2/11 | duration_ms=20472
2026-05-26 15:48:36.895 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=81 | mode=full | segment=3/11 | chars=331
2026-05-26 15:48:48.330 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=82 | mode=full | segment=2/2 | duration_ms=23040
2026-05-26 15:48:48.334 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=82 | mode=full | created_segments=2/2
2026-05-26 15:48:48.336 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=82 | mode=full | chars=496
2026-05-26 15:48:49.089 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=81 | mode=full | segment=3/11 | duration_ms=20664
2026-05-26 15:48:49.092 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=81 | mode=full | segment=4/11 | chars=417
[2026-05-26 15:48:49,680: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:48:50,550: INFO/MainProcess] Task triam.notifications.scan_due[58039c34-6ad6-46da-8715-44770d473f8e] received
2026-05-26 15:48:58.312 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:48:58,314: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[58039c34-6ad6-46da-8715-44770d473f8e] succeeded in 7.762066919938661s: None
2026-05-26 15:49:02.083 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=81 | mode=full | segment=4/11 | duration_ms=28992
2026-05-26 15:49:02.088 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=81 | mode=full | segment=5/11 | chars=481
2026-05-26 15:49:03.135 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=82 | mode=full
2026-05-26 15:49:03.140 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=57b28f7e-3824-49ca-8436-2056f9151109 | mode=full | segments=2 | review_audio=True
2026-05-26 15:49:06.265 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=57b28f7e-3824-49ca-8436-2056f9151109 | mode=full
2026-05-26 15:49:08.720 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 82 READY | mode=full | segments=2
2026-05-26 15:49:08.720 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=83 | mode=full | title=Phương trình nguyên bậc nhất 2 ẩn | chars=1711 | estimated_tokens=913 | estimated_audio_seconds=202
2026-05-26 15:49:10.945 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=83 | mode=full | rag=true | tts=true
2026-05-26 15:49:10.957 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=83 | mode=full | title=Phương trình nguyên bậc nhất 2 ẩn | raw_chars=1711
2026-05-26 15:49:10.962 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Phương trình nguyên bậc nhất 2 ẩn | chars=1711 | estimated_tokens=913 | estimated_audio_seconds=202
2026-05-26 15:49:10.964 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Phương trình nguyên bậc nhất 2 ẩn
2026-05-26 15:49:10.965 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1711
2026-05-26 15:49:14.726 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 2 vectors for chapter_id=8620fc05-8d36-4f57-8b9e-e6d5d6c774d2
2026-05-26 15:49:27.576 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=81 | mode=full | segment=5/11 | duration_ms=31752
2026-05-26 15:49:27.578 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=81 | mode=full | segment=6/11 | chars=305
2026-05-26 15:49:36.148 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=81 | mode=full | segment=6/11 | duration_ms=18984
2026-05-26 15:49:36.149 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=81 | mode=full | segment=7/11 | chars=273
2026-05-26 15:49:46.267 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=81 | mode=full | segment=7/11 | duration_ms=20112
2026-05-26 15:49:46.270 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=81 | mode=full | segment=8/11 | chars=216
[2026-05-26 15:49:49,681: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:49:50,334: INFO/MainProcess] Task triam.notifications.scan_due[4f08b3eb-f716-426a-8504-753d1718c3eb] received
2026-05-26 15:49:52.611 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=81 | mode=full | segment=8/11 | duration_ms=16968
2026-05-26 15:49:52.612 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=81 | mode=full | segment=9/11 | chars=212
2026-05-26 15:49:58.036 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:49:58,037: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[4f08b3eb-f716-426a-8504-753d1718c3eb] succeeded in 7.699966269079596s: None
2026-05-26 15:50:00.470 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=81 | mode=full | segment=9/11 | duration_ms=16416
2026-05-26 15:50:00.471 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=81 | mode=full | segment=10/11 | chars=431
2026-05-26 15:50:03.212 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=11 | review_chars=624
2026-05-26 15:50:03.223 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=83 | mode=full | main_scripts=11 | review_chars=624
2026-05-26 15:50:03.223 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=83 | mode=full | total_scripts=11
2026-05-26 15:50:03.224 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=83 | mode=full | segment=1/11 | chars=257
2026-05-26 15:50:11.484 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=81 | mode=full | segment=10/11 | duration_ms=26856
2026-05-26 15:50:11.484 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=81 | mode=full | segment=11/11 | chars=282
2026-05-26 15:50:13.077 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=83 | mode=full | segment=1/11 | duration_ms=16344
2026-05-26 15:50:13.080 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=83 | mode=full | segment=2/11 | chars=246
2026-05-26 15:50:19.722 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=81 | mode=full | segment=11/11 | duration_ms=17328
2026-05-26 15:50:19.724 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=81 | mode=full | created_segments=11/11
2026-05-26 15:50:19.726 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=81 | mode=full | chars=758
2026-05-26 15:50:27.317 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=83 | mode=full | segment=2/11 | duration_ms=14616
2026-05-26 15:50:27.318 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=83 | mode=full | segment=3/11 | chars=393
2026-05-26 15:50:35.601 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=81 | mode=full
2026-05-26 15:50:35.602 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=1a261f6b-cfb4-492c-947a-5d17474e1d8b | mode=full | segments=11 | review_audio=True
2026-05-26 15:50:38.721 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=1a261f6b-cfb4-492c-947a-5d17474e1d8b | mode=full
2026-05-26 15:50:41.196 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 81 READY | mode=full | segments=11
2026-05-26 15:50:41.202 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=84 | mode=full | title=Phương trình nguyên bậc nhất nhiều ẩn | chars=1556 | estimated_tokens=776 | estimated_audio_seconds=170
2026-05-26 15:50:43.433 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=84 | mode=full | rag=true | tts=true
2026-05-26 15:50:43.439 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=84 | mode=full | title=Phương trình nguyên bậc nhất nhiều ẩn | raw_chars=1556
2026-05-26 15:50:43.443 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Phương trình nguyên bậc nhất nhiều ẩn | chars=1556 | estimated_tokens=776 | estimated_audio_seconds=170
2026-05-26 15:50:43.445 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Phương trình nguyên bậc nhất nhiều ẩn
2026-05-26 15:50:43.445 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1556
2026-05-26 15:50:46.950 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=83 | mode=full | segment=3/11 | duration_ms=25464
2026-05-26 15:50:46.953 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=83 | mode=full | segment=4/11 | chars=321
2026-05-26 15:50:48.494 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 2 vectors for chapter_id=272a2689-19f1-482e-a959-6c321b98da3b
[2026-05-26 15:50:49,681: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:50:50,558: INFO/MainProcess] Task triam.notifications.scan_due[c8d1be66-8309-4c85-8b66-e0ab21526b58] received
2026-05-26 15:50:58.396 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:50:58,397: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[c8d1be66-8309-4c85-8b66-e0ab21526b58] succeeded in 7.6257220399565995s: None
2026-05-26 15:50:59.059 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=83 | mode=full | segment=4/11 | duration_ms=21912
2026-05-26 15:50:59.061 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=83 | mode=full | segment=5/11 | chars=363
2026-05-26 15:51:09.858 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=83 | mode=full | segment=5/11 | duration_ms=23952
2026-05-26 15:51:09.859 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=83 | mode=full | segment=6/11 | chars=170
2026-05-26 15:51:09.947 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=7 | review_chars=667
2026-05-26 15:51:09.949 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=84 | mode=full | main_scripts=7 | review_chars=667
2026-05-26 15:51:09.950 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=84 | mode=full | total_scripts=7
2026-05-26 15:51:09.951 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=84 | mode=full | segment=1/7 | chars=209
2026-05-26 15:51:13.473 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=83 | mode=full | segment=6/11 | duration_ms=9528
2026-05-26 15:51:13.474 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=83 | mode=full | segment=7/11 | chars=375
2026-05-26 15:51:16.229 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=84 | mode=full | segment=1/7 | duration_ms=15408
2026-05-26 15:51:16.232 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=84 | mode=full | segment=2/7 | chars=266
2026-05-26 15:51:21.578 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=83 | mode=full | segment=7/11 | duration_ms=21912
2026-05-26 15:51:21.580 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=83 | mode=full | segment=8/11 | chars=256
2026-05-26 15:51:24.641 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=84 | mode=full | segment=2/7 | duration_ms=14160
2026-05-26 15:51:24.642 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=84 | mode=full | segment=3/7 | chars=276
2026-05-26 15:51:28.980 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=83 | mode=full | segment=8/11 | duration_ms=13440
2026-05-26 15:51:28.982 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=83 | mode=full | segment=9/11 | chars=386
2026-05-26 15:51:35.794 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=84 | mode=full | segment=3/7 | duration_ms=16128
2026-05-26 15:51:35.795 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=84 | mode=full | segment=4/7 | chars=462
2026-05-26 15:51:41.546 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=83 | mode=full | segment=9/11 | duration_ms=23592
2026-05-26 15:51:41.547 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=83 | mode=full | segment=10/11 | chars=291
[2026-05-26 15:51:49,681: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-26 15:51:49.774 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=84 | mode=full | segment=4/7 | duration_ms=28680
2026-05-26 15:51:49.778 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=84 | mode=full | segment=5/7 | chars=357
2026-05-26 15:51:50.492 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=83 | mode=full | segment=10/11 | duration_ms=19800
2026-05-26 15:51:50.495 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=83 | mode=full | segment=11/11 | chars=304
[2026-05-26 15:51:50,551: INFO/MainProcess] Task triam.notifications.scan_due[34e6f349-5e93-4c4f-900a-0438ede182f0] received
2026-05-26 15:51:58.148 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:51:58,148: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[34e6f349-5e93-4c4f-900a-0438ede182f0] succeeded in 7.5964877819642425s: None
2026-05-26 15:51:58.832 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=83 | mode=full | segment=11/11 | duration_ms=18240
2026-05-26 15:51:58.832 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=83 | mode=full | created_segments=11/11
2026-05-26 15:51:58.841 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=83 | mode=full | chars=624
2026-05-26 15:51:59.995 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=84 | mode=full | segment=5/7 | duration_ms=23568
2026-05-26 15:51:59.996 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=84 | mode=full | segment=6/7 | chars=352
2026-05-26 15:52:11.519 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=84 | mode=full | segment=6/7 | duration_ms=21408
2026-05-26 15:52:11.523 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=84 | mode=full | segment=7/7 | chars=451
2026-05-26 15:52:14.595 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=83 | mode=full
2026-05-26 15:52:14.596 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=8620fc05-8d36-4f57-8b9e-e6d5d6c774d2 | mode=full | segments=11 | review_audio=True
2026-05-26 15:52:17.721 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=8620fc05-8d36-4f57-8b9e-e6d5d6c774d2 | mode=full
2026-05-26 15:52:20.175 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 83 READY | mode=full | segments=11
2026-05-26 15:52:20.177 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=85 | mode=full | title=Quan hệ đồng dư | chars=1506 | estimated_tokens=800 | estimated_audio_seconds=180
2026-05-26 15:52:22.426 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=85 | mode=full | rag=true | tts=true
2026-05-26 15:52:22.435 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=85 | mode=full | title=Quan hệ đồng dư | raw_chars=1506
2026-05-26 15:52:22.439 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Quan hệ đồng dư | chars=1506 | estimated_tokens=800 | estimated_audio_seconds=180
2026-05-26 15:52:22.440 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Quan hệ đồng dư
2026-05-26 15:52:22.441 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1506
2026-05-26 15:52:25.909 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=84 | mode=full | segment=7/7 | duration_ms=29112
2026-05-26 15:52:25.910 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=84 | mode=full | created_segments=7/7
2026-05-26 15:52:25.910 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=84 | mode=full | chars=667
2026-05-26 15:52:27.085 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 2 vectors for chapter_id=579c522b-245b-4983-aff5-a4c550a6abbd
2026-05-26 15:52:42.348 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=11 | review_chars=462
2026-05-26 15:52:42.349 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=85 | mode=full | main_scripts=11 | review_chars=462
2026-05-26 15:52:42.350 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=85 | mode=full | total_scripts=11
2026-05-26 15:52:42.351 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=85 | mode=full | segment=1/11 | chars=217
2026-05-26 15:52:43.530 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=84 | mode=full
2026-05-26 15:52:43.530 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=272a2689-19f1-482e-a959-6c321b98da3b | mode=full | segments=7 | review_audio=True
2026-05-26 15:52:46.655 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=272a2689-19f1-482e-a959-6c321b98da3b | mode=full
2026-05-26 15:52:49.107 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 84 READY | mode=full | segments=7
2026-05-26 15:52:49.109 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=86 | mode=full | title=Phương trình đồng dư một ẩn | chars=2163 | estimated_tokens=1003 | estimated_audio_seconds=228
[2026-05-26 15:52:49,681: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:52:50,335: INFO/MainProcess] Task triam.notifications.scan_due[ef65e742-49cc-4d63-8dad-58e7906910dd] received
2026-05-26 15:52:51.358 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=86 | mode=full | rag=true | tts=true
2026-05-26 15:52:51.382 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=86 | mode=full | title=Phương trình đồng dư một ẩn | raw_chars=2163
2026-05-26 15:52:51.390 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Phương trình đồng dư một ẩn | chars=2163 | estimated_tokens=1003 | estimated_audio_seconds=228
2026-05-26 15:52:51.398 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Phương trình đồng dư một ẩn
2026-05-26 15:52:51.400 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=2163
2026-05-26 15:52:54.795 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=85 | mode=full | segment=1/11 | duration_ms=16248
2026-05-26 15:52:54.796 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=85 | mode=full | segment=2/11 | chars=278
2026-05-26 15:52:55.960 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 3 vectors for chapter_id=d5316cc3-7cac-49ca-9188-694a6505960e
2026-05-26 15:52:58.215 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:52:58,216: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[ef65e742-49cc-4d63-8dad-58e7906910dd] succeeded in 7.667422887985595s: None
2026-05-26 15:53:04.591 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=85 | mode=full | segment=2/11 | duration_ms=17568
2026-05-26 15:53:04.592 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=85 | mode=full | segment=3/11 | chars=312
2026-05-26 15:53:09.262 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=10 | review_chars=696
2026-05-26 15:53:09.266 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=86 | mode=full | main_scripts=10 | review_chars=696
2026-05-26 15:53:09.267 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=86 | mode=full | total_scripts=10
2026-05-26 15:53:09.268 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=86 | mode=full | segment=1/10 | chars=196
2026-05-26 15:53:13.104 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=85 | mode=full | segment=3/11 | duration_ms=20424
2026-05-26 15:53:13.105 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=85 | mode=full | segment=4/11 | chars=314
2026-05-26 15:53:15.108 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=86 | mode=full | segment=1/10 | duration_ms=14208
2026-05-26 15:53:15.110 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=86 | mode=full | segment=2/10 | chars=346
2026-05-26 15:53:24.015 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=85 | mode=full | segment=4/11 | duration_ms=24168
2026-05-26 15:53:24.016 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=85 | mode=full | segment=5/11 | chars=92
2026-05-26 15:53:26.135 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=85 | mode=full | segment=5/11 | duration_ms=6240
2026-05-26 15:53:26.136 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=85 | mode=full | segment=6/11 | chars=230
2026-05-26 15:53:27.956 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=86 | mode=full | segment=2/10 | duration_ms=24864
2026-05-26 15:53:27.956 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=86 | mode=full | segment=3/10 | chars=235
2026-05-26 15:53:33.112 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=85 | mode=full | segment=6/11 | duration_ms=15432
2026-05-26 15:53:33.115 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=85 | mode=full | segment=7/11 | chars=327
2026-05-26 15:53:34.800 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=86 | mode=full | segment=3/10 | duration_ms=12456
2026-05-26 15:53:34.801 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=86 | mode=full | segment=4/10 | chars=321
2026-05-26 15:53:41.218 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=86 | mode=full | segment=4/10 | duration_ms=19008
2026-05-26 15:53:41.219 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=86 | mode=full | segment=5/10 | chars=287
2026-05-26 15:53:42.486 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=85 | mode=full | segment=7/11 | duration_ms=23088
2026-05-26 15:53:42.487 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=85 | mode=full | segment=8/11 | chars=420
[2026-05-26 15:53:49,681: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:53:50,754: INFO/MainProcess] Task triam.notifications.scan_due[8bdaca31-2fd6-421a-a400-d249d036ad25] received
2026-05-26 15:53:54.167 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=85 | mode=full | segment=8/11 | duration_ms=30432
2026-05-26 15:53:54.168 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=85 | mode=full | segment=9/11 | chars=493
2026-05-26 15:53:55.275 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=86 | mode=full | segment=5/10 | duration_ms=19104
2026-05-26 15:53:55.277 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=86 | mode=full | segment=6/10 | chars=218
2026-05-26 15:53:58.382 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:53:58,383: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8bdaca31-2fd6-421a-a400-d249d036ad25] succeeded in 7.625187555095181s: None
2026-05-26 15:54:00.522 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=86 | mode=full | segment=6/10 | duration_ms=13872
2026-05-26 15:54:00.526 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=86 | mode=full | segment=7/10 | chars=417
2026-05-26 15:54:09.597 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=85 | mode=full | segment=9/11 | duration_ms=34032
2026-05-26 15:54:09.598 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=85 | mode=full | segment=10/11 | chars=303
2026-05-26 15:54:12.068 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=86 | mode=full | segment=7/10 | duration_ms=21696
2026-05-26 15:54:12.071 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=86 | mode=full | segment=8/10 | chars=376
2026-05-26 15:54:18.962 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=85 | mode=full | segment=10/11 | duration_ms=22824
2026-05-26 15:54:18.962 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=85 | mode=full | segment=11/11 | chars=256
2026-05-26 15:54:20.275 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=86 | mode=full | segment=8/10 | duration_ms=21120
2026-05-26 15:54:20.276 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=86 | mode=full | segment=9/10 | chars=391
2026-05-26 15:54:26.723 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=85 | mode=full | segment=11/11 | duration_ms=17520
2026-05-26 15:54:26.726 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=85 | mode=full | created_segments=11/11
2026-05-26 15:54:26.727 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=85 | mode=full | chars=462
2026-05-26 15:54:33.379 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=86 | mode=full | segment=9/10 | duration_ms=22104
2026-05-26 15:54:33.380 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=86 | mode=full | segment=10/10 | chars=344
2026-05-26 15:54:40.867 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=85 | mode=full
2026-05-26 15:54:40.868 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=579c522b-245b-4983-aff5-a4c550a6abbd | mode=full | segments=11 | review_audio=True
2026-05-26 15:54:44.210 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=579c522b-245b-4983-aff5-a4c550a6abbd | mode=full
2026-05-26 15:54:46.684 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 85 READY | mode=full | segments=11
2026-05-26 15:54:46.690 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=87 | mode=full | title=Phương trình đồng dư bậc nhất một ẩn | chars=927 | estimated_tokens=495 | estimated_audio_seconds=106
2026-05-26 15:54:48.953 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=87 | mode=full | rag=true | tts=true
2026-05-26 15:54:48.957 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=87 | mode=full | title=Phương trình đồng dư bậc nhất một ẩn | raw_chars=927
2026-05-26 15:54:48.963 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Phương trình đồng dư bậc nhất một ẩn | chars=927 | estimated_tokens=495 | estimated_audio_seconds=106
2026-05-26 15:54:48.965 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Phương trình đồng dư bậc nhất một ẩn
2026-05-26 15:54:48.965 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=927
[2026-05-26 15:54:49,682: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:54:50,525: INFO/MainProcess] Task triam.notifications.scan_due[3ca16ce8-9752-472a-9cca-989244ab63a7] received
2026-05-26 15:54:52.061 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=86 | mode=full | segment=10/10 | duration_ms=20448
2026-05-26 15:54:52.062 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=86 | mode=full | created_segments=10/10
2026-05-26 15:54:52.063 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=86 | mode=full | chars=696
2026-05-26 15:54:53.403 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=2cc1ebfe-e6a2-42eb-9792-4bcfec29045c
2026-05-26 15:54:58.279 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:54:58,281: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[3ca16ce8-9752-472a-9cca-989244ab63a7] succeeded in 7.754605997004546s: None
2026-05-26 15:55:02.118 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=6 | review_chars=670
2026-05-26 15:55:02.119 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=87 | mode=full | main_scripts=6 | review_chars=670
2026-05-26 15:55:02.119 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=87 | mode=full | total_scripts=6
2026-05-26 15:55:02.120 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=87 | mode=full | segment=1/6 | chars=309
2026-05-26 15:55:06.839 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=86 | mode=full
2026-05-26 15:55:06.839 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=d5316cc3-7cac-49ca-9188-694a6505960e | mode=full | segments=10 | review_audio=True
2026-05-26 15:55:09.986 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=d5316cc3-7cac-49ca-9188-694a6505960e | mode=full
2026-05-26 15:55:12.460 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 86 READY | mode=full | segments=10
2026-05-26 15:55:12.469 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=88 | mode=full | title=Hệ phương trình đồng dư bậc nhất một ẩn | chars=2554 | estimated_tokens=1320 | estimated_audio_seconds=274
2026-05-26 15:55:14.701 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=88 | mode=full | rag=true | tts=true
2026-05-26 15:55:14.713 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=88 | mode=full | title=Hệ phương trình đồng dư bậc nhất một ẩn | raw_chars=2554
2026-05-26 15:55:14.720 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Hệ phương trình đồng dư bậc nhất một ẩn | chars=2554 | estimated_tokens=1320 | estimated_audio_seconds=274
2026-05-26 15:55:14.722 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Hệ phương trình đồng dư bậc nhất một ẩn
2026-05-26 15:55:14.722 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=2554
2026-05-26 15:55:17.807 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=87 | mode=full | segment=1/6 | duration_ms=19704
2026-05-26 15:55:17.810 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=87 | mode=full | segment=2/6 | chars=273
2026-05-26 15:55:20.032 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 3 vectors for chapter_id=a2ed6b40-4388-4b50-9bfb-11b7ff83ffe6
2026-05-26 15:55:28.361 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=87 | mode=full | segment=2/6 | duration_ms=17232
2026-05-26 15:55:28.365 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=87 | mode=full | segment=3/6 | chars=297
2026-05-26 15:55:37.879 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=87 | mode=full | segment=3/6 | duration_ms=21192
2026-05-26 15:55:37.883 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=87 | mode=full | segment=4/6 | chars=214
2026-05-26 15:55:44.610 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=87 | mode=full | segment=4/6 | duration_ms=13152
2026-05-26 15:55:44.611 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=87 | mode=full | segment=5/6 | chars=329
[2026-05-26 15:55:49,682: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:55:50,552: INFO/MainProcess] Task triam.notifications.scan_due[f95ecaf5-3477-479a-95b1-eee00093f8c6] received
2026-05-26 15:55:55.477 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=87 | mode=full | segment=5/6 | duration_ms=20544
2026-05-26 15:55:55.479 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=87 | mode=full | segment=6/6 | chars=348
2026-05-26 15:55:55.513 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=17 | review_chars=669
2026-05-26 15:55:55.515 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=88 | mode=full | main_scripts=17 | review_chars=669
2026-05-26 15:55:55.515 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=88 | mode=full | total_scripts=17
2026-05-26 15:55:55.516 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=88 | mode=full | segment=1/17 | chars=175
2026-05-26 15:55:58.181 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:55:58,184: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f95ecaf5-3477-479a-95b1-eee00093f8c6] succeeded in 7.62989284505602s: None
2026-05-26 15:56:01.442 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=88 | mode=full | segment=1/17 | duration_ms=12840
2026-05-26 15:56:01.445 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=88 | mode=full | segment=2/17 | chars=260
2026-05-26 15:56:03.706 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=87 | mode=full | segment=6/6 | duration_ms=20376
2026-05-26 15:56:03.707 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=87 | mode=full | created_segments=6/6
2026-05-26 15:56:03.708 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=87 | mode=full | chars=670
2026-05-26 15:56:06.710 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=88 | mode=full | segment=2/17 | duration_ms=14640
2026-05-26 15:56:06.712 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=88 | mode=full | segment=3/17 | chars=347
2026-05-26 15:56:17.716 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=88 | mode=full | segment=3/17 | duration_ms=23184
2026-05-26 15:56:17.720 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=88 | mode=full | segment=4/17 | chars=272
2026-05-26 15:56:24.504 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=87 | mode=full
2026-05-26 15:56:24.505 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=2cc1ebfe-e6a2-42eb-9792-4bcfec29045c | mode=full | segments=6 | review_audio=True
2026-05-26 15:56:27.618 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=2cc1ebfe-e6a2-42eb-9792-4bcfec29045c | mode=full
2026-05-26 15:56:30.069 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 87 READY | mode=full | segments=6
2026-05-26 15:56:30.072 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=89 | mode=full | title=Hệ phương trình đồng dư bậc cao một ẩn | chars=1996 | estimated_tokens=1106 | estimated_audio_seconds=226
2026-05-26 15:56:32.317 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=89 | mode=full | rag=true | tts=true
2026-05-26 15:56:32.326 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=89 | mode=full | title=Hệ phương trình đồng dư bậc cao một ẩn | raw_chars=1996
2026-05-26 15:56:32.330 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Hệ phương trình đồng dư bậc cao một ẩn | chars=1996 | estimated_tokens=1106 | estimated_audio_seconds=226
2026-05-26 15:56:32.332 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Hệ phương trình đồng dư bậc cao một ẩn
2026-05-26 15:56:32.333 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1996
2026-05-26 15:56:35.546 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=88 | mode=full | segment=4/17 | duration_ms=17808
2026-05-26 15:56:35.547 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=88 | mode=full | segment=5/17 | chars=243
2026-05-26 15:56:44.769 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=88 | mode=full | segment=5/17 | duration_ms=19680
2026-05-26 15:56:44.770 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=88 | mode=full | segment=6/17 | chars=395
[2026-05-26 15:56:49,682: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:56:50,554: INFO/MainProcess] Task triam.notifications.scan_due[b7ccc138-0f50-4ceb-b93b-48cad3054404] received
2026-05-26 15:56:51.373 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 2 vectors for chapter_id=07895cde-4277-46c9-bde0-4b856f539a82
2026-05-26 15:56:56.639 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=88 | mode=full | segment=6/17 | duration_ms=29712
2026-05-26 15:56:56.641 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=88 | mode=full | segment=7/17 | chars=171
2026-05-26 15:56:58.175 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:56:58,176: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b7ccc138-0f50-4ceb-b93b-48cad3054404] succeeded in 7.62088483502157s: None
2026-05-26 15:57:00.277 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=88 | mode=full | segment=7/17 | duration_ms=10488
2026-05-26 15:57:00.278 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=88 | mode=full | segment=8/17 | chars=330
2026-05-26 15:57:08.476 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=88 | mode=full | segment=8/17 | duration_ms=24288
2026-05-26 15:57:08.479 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=88 | mode=full | segment=9/17 | chars=369
2026-05-26 15:57:14.837 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=15 | review_chars=682
2026-05-26 15:57:14.839 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=89 | mode=full | main_scripts=15 | review_chars=682
2026-05-26 15:57:14.840 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=89 | mode=full | total_scripts=15
2026-05-26 15:57:14.841 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=89 | mode=full | segment=1/15 | chars=204
2026-05-26 15:57:19.788 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=88 | mode=full | segment=9/17 | duration_ms=23160
2026-05-26 15:57:19.789 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=88 | mode=full | segment=10/17 | chars=346
2026-05-26 15:57:20.563 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=89 | mode=full | segment=1/15 | duration_ms=14328
2026-05-26 15:57:20.564 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=89 | mode=full | segment=2/15 | chars=101
2026-05-26 15:57:24.905 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=89 | mode=full | segment=2/15 | duration_ms=8712
2026-05-26 15:57:24.906 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=89 | mode=full | segment=3/15 | chars=291
2026-05-26 15:57:30.708 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=89 | mode=full | segment=3/15 | duration_ms=18912
2026-05-26 15:57:30.710 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=89 | mode=full | segment=4/15 | chars=425
2026-05-26 15:57:31.729 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=88 | mode=full | segment=10/17 | duration_ms=21120
2026-05-26 15:57:31.730 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=88 | mode=full | segment=11/17 | chars=201
2026-05-26 15:57:38.131 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=88 | mode=full | segment=11/17 | duration_ms=11616
2026-05-26 15:57:38.131 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=88 | mode=full | segment=12/17 | chars=379
2026-05-26 15:57:42.612 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=89 | mode=full | segment=4/15 | duration_ms=28800
2026-05-26 15:57:42.612 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=89 | mode=full | segment=5/15 | chars=233
2026-05-26 15:57:46.768 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=88 | mode=full | segment=12/17 | duration_ms=20640
2026-05-26 15:57:46.770 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=88 | mode=full | segment=13/17 | chars=405
2026-05-26 15:57:49.280 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=89 | mode=full | segment=5/15 | duration_ms=13416
2026-05-26 15:57:49.283 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=89 | mode=full | segment=6/15 | chars=297
[2026-05-26 15:57:49,691: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 15:57:50,349: INFO/MainProcess] Task triam.notifications.scan_due[b5b323b9-8268-4a3d-ba2c-1938cef92e6e] received
2026-05-26 15:57:52.667 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=88 | mode=full | segment=13/17 | duration_ms=23496
2026-05-26 15:57:52.667 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=88 | mode=full | segment=14/17 | chars=369
2026-05-26 15:57:57.995 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:57:57,997: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[b5b323b9-8268-4a3d-ba2c-1938cef92e6e] succeeded in 7.645882130018435s: None
2026-05-26 15:58:02.702 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=89 | mode=full | segment=6/15 | duration_ms=19584
2026-05-26 15:58:02.703 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=89 | mode=full | segment=7/15 | chars=223
2026-05-26 15:58:04.084 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=88 | mode=full | segment=14/17 | duration_ms=22752
2026-05-26 15:58:04.085 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=88 | mode=full | segment=15/17 | chars=594
2026-05-26 15:58:09.532 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=89 | mode=full | segment=7/15 | duration_ms=12552
2026-05-26 15:58:09.535 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=89 | mode=full | segment=8/15 | chars=178
2026-05-26 15:58:15.238 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=89 | mode=full | segment=8/15 | duration_ms=10680
2026-05-26 15:58:15.240 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=89 | mode=full | segment=9/15 | chars=215
2026-05-26 15:58:19.333 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=88 | mode=full | segment=15/17 | duration_ms=36552
2026-05-26 15:58:19.336 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=88 | mode=full | segment=16/17 | chars=422
2026-05-26 15:58:20.608 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=89 | mode=full | segment=9/15 | duration_ms=14136
2026-05-26 15:58:20.619 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=89 | mode=full | segment=10/15 | chars=133
2026-05-26 15:58:25.185 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=89 | mode=full | segment=10/15 | duration_ms=8808
2026-05-26 15:58:25.186 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=89 | mode=full | segment=11/15 | chars=383
2026-05-26 15:58:28.333 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=88 | mode=full | segment=16/17 | duration_ms=25224
2026-05-26 15:58:28.333 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=88 | mode=full | segment=17/17 | chars=515
2026-05-26 15:58:34.870 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=89 | mode=full | segment=11/15 | duration_ms=25128
2026-05-26 15:58:34.872 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=89 | mode=full | segment=12/15 | chars=263
2026-05-26 15:58:40.334 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=88 | mode=full | segment=17/17 | duration_ms=31800
2026-05-26 15:58:40.337 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=88 | mode=full | created_segments=17/17
2026-05-26 15:58:40.338 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=88 | mode=full | chars=669
2026-05-26 15:58:44.563 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=89 | mode=full | segment=12/15 | duration_ms=16536
2026-05-26 15:58:44.565 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=89 | mode=full | segment=13/15 | chars=272
[2026-05-26 15:58:49,691: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-26 15:58:50.056 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=89 | mode=full | segment=13/15 | duration_ms=17616
2026-05-26 15:58:50.057 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=89 | mode=full | segment=14/15 | chars=268
[2026-05-26 15:58:50,560: INFO/MainProcess] Task triam.notifications.scan_due[a2b6e7b8-d0c0-4171-86d2-751304f93958] received
2026-05-26 15:58:52.734 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=88 | mode=full
2026-05-26 15:58:52.739 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=a2ed6b40-4388-4b50-9bfb-11b7ff83ffe6 | mode=full | segments=17 | review_audio=True
2026-05-26 15:58:55.884 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=a2ed6b40-4388-4b50-9bfb-11b7ff83ffe6 | mode=full
2026-05-26 15:58:58.167 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:58:58,168: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a2b6e7b8-d0c0-4171-86d2-751304f93958] succeeded in 7.606035176082514s: None
2026-05-26 15:58:58.343 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 88 READY | mode=full | segments=17
2026-05-26 15:58:58.348 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=90 | mode=full | title=Ứng dụng của lý thuyết đồng dư | chars=169 | estimated_tokens=88 | estimated_audio_seconds=18
2026-05-26 15:59:00.581 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=90 | mode=full | rag=true | tts=true
2026-05-26 15:59:00.588 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=90 | mode=full | title=Ứng dụng của lý thuyết đồng dư | raw_chars=169
2026-05-26 15:59:00.592 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Ứng dụng của lý thuyết đồng dư | chars=169 | estimated_tokens=88 | estimated_audio_seconds=18
2026-05-26 15:59:00.593 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Ứng dụng của lý thuyết đồng dư
2026-05-26 15:59:00.594 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=169
2026-05-26 15:59:04.047 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=89 | mode=full | segment=14/15 | duration_ms=16800
2026-05-26 15:59:04.047 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=89 | mode=full | segment=15/15 | chars=389
2026-05-26 15:59:05.544 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=0bcb13f7-b971-4000-8645-d2f0850b6e3e
2026-05-26 15:59:08.263 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=1 | review_chars=244
2026-05-26 15:59:08.266 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=90 | mode=full | main_scripts=1 | review_chars=244
2026-05-26 15:59:08.266 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=90 | mode=full | total_scripts=1
2026-05-26 15:59:08.269 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=90 | mode=full | segment=1/1 | chars=188
2026-05-26 15:59:13.099 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=89 | mode=full | segment=15/15 | duration_ms=23016
2026-05-26 15:59:13.103 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=89 | mode=full | created_segments=15/15
2026-05-26 15:59:13.107 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=89 | mode=full | chars=682
2026-05-26 15:59:13.777 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=90 | mode=full | segment=1/1 | duration_ms=11280
2026-05-26 15:59:13.780 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=90 | mode=full | created_segments=1/1
2026-05-26 15:59:13.781 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=90 | mode=full | chars=244
2026-05-26 15:59:18.741 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=90 | mode=full
2026-05-26 15:59:18.745 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=0bcb13f7-b971-4000-8645-d2f0850b6e3e | mode=full | segments=1 | review_audio=True
2026-05-26 15:59:21.867 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=0bcb13f7-b971-4000-8645-d2f0850b6e3e | mode=full
2026-05-26 15:59:24.320 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 90 READY | mode=full | segments=1
2026-05-26 15:59:24.324 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=91 | mode=full | title=Các hàm băm | chars=1105 | estimated_tokens=536 | estimated_audio_seconds=119
2026-05-26 15:59:26.552 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=91 | mode=full | rag=true | tts=true
2026-05-26 15:59:26.555 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=91 | mode=full | title=Các hàm băm | raw_chars=1105
2026-05-26 15:59:26.557 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Các hàm băm | chars=1105 | estimated_tokens=536 | estimated_audio_seconds=119
2026-05-26 15:59:26.559 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Các hàm băm
2026-05-26 15:59:26.560 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=1105
2026-05-26 15:59:30.212 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=89 | mode=full
2026-05-26 15:59:30.213 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=07895cde-4277-46c9-bde0-4b856f539a82 | mode=full | segments=15 | review_audio=True
2026-05-26 15:59:33.348 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=07895cde-4277-46c9-bde0-4b856f539a82 | mode=full
2026-05-26 15:59:35.796 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 89 READY | mode=full | segments=15
2026-05-26 15:59:35.802 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=92 | mode=full | title=Các số giả ngẫu nhiên | chars=876 | estimated_tokens=449 | estimated_audio_seconds=100
2026-05-26 15:59:38.034 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=92 | mode=full | rag=true | tts=true
2026-05-26 15:59:38.933 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=926fe7b9-3a1d-41e1-8fe2-6a9ca0655439
2026-05-26 15:59:38.944 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=92 | mode=full | title=Các số giả ngẫu nhiên | raw_chars=876
2026-05-26 15:59:38.949 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Các số giả ngẫu nhiên | chars=876 | estimated_tokens=449 | estimated_audio_seconds=100
2026-05-26 15:59:38.952 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Các số giả ngẫu nhiên
2026-05-26 15:59:42.297 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 1 vectors for chapter_id=de05adc0-dfa2-4bdc-a7b5-dd14b9e40539
2026-05-26 15:59:42.302 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=5 | review_chars=530
2026-05-26 15:59:42.302 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=91 | mode=full | main_scripts=5 | review_chars=530
2026-05-26 15:59:42.302 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=91 | mode=full | total_scripts=5
2026-05-26 15:59:42.303 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=91 | mode=full | segment=1/5 | chars=240
2026-05-26 15:59:42.334 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=876
[2026-05-26 15:59:49,691: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
2026-05-26 15:59:50.100 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=91 | mode=full | segment=1/5 | duration_ms=12864
2026-05-26 15:59:50.103 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=91 | mode=full | segment=2/5 | chars=279
[2026-05-26 15:59:50,346: INFO/MainProcess] Task triam.notifications.scan_due[8d4b9e0b-8442-4bdf-8950-71ad2d7db30a] received
2026-05-26 15:59:54.091 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=4 | review_chars=612
2026-05-26 15:59:54.092 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=92 | mode=full | main_scripts=4 | review_chars=612
2026-05-26 15:59:54.093 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=92 | mode=full | total_scripts=4
2026-05-26 15:59:54.094 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=92 | mode=full | segment=1/4 | chars=302
2026-05-26 15:59:57.929 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 15:59:57,930: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8d4b9e0b-8442-4bdf-8950-71ad2d7db30a] succeeded in 7.582707591005601s: None
2026-05-26 15:59:59.288 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=91 | mode=full | segment=2/5 | duration_ms=20616
2026-05-26 15:59:59.289 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=91 | mode=full | segment=3/5 | chars=311
2026-05-26 16:00:00.998 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=92 | mode=full | segment=1/4 | duration_ms=17232
2026-05-26 16:00:00.999 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=92 | mode=full | segment=2/4 | chars=393
2026-05-26 16:00:11.522 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=92 | mode=full | segment=2/4 | duration_ms=25368
2026-05-26 16:00:11.525 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=92 | mode=full | segment=3/4 | chars=354
2026-05-26 16:00:12.410 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=91 | mode=full | segment=3/5 | duration_ms=19392
2026-05-26 16:00:12.411 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=91 | mode=full | segment=4/5 | chars=353
2026-05-26 16:00:23.895 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=91 | mode=full | segment=4/5 | duration_ms=20976
2026-05-26 16:00:23.899 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=91 | mode=full | segment=5/5 | chars=357
2026-05-26 16:00:27.699 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=92 | mode=full | segment=3/4 | duration_ms=21480
2026-05-26 16:00:27.700 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=92 | mode=full | segment=4/4 | chars=248
2026-05-26 16:00:33.761 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=91 | mode=full | segment=5/5 | duration_ms=20832
2026-05-26 16:00:33.762 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=91 | mode=full | created_segments=5/5
2026-05-26 16:00:33.762 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=91 | mode=full | chars=530
2026-05-26 16:00:35.290 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=92 | mode=full | segment=4/4 | duration_ms=20808
2026-05-26 16:00:35.291 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=92 | mode=full | created_segments=4/4
2026-05-26 16:00:35.291 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=92 | mode=full | chars=612
2026-05-26 16:00:48.002 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=91 | mode=full
2026-05-26 16:00:48.004 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=926fe7b9-3a1d-41e1-8fe2-6a9ca0655439 | mode=full | segments=5 | review_audio=True
[2026-05-26 16:00:49,691: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 16:00:50,561: INFO/MainProcess] Task triam.notifications.scan_due[f3a86a23-e43a-480c-a405-06822cc3d0e6] received
2026-05-26 16:00:51.290 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=926fe7b9-3a1d-41e1-8fe2-6a9ca0655439 | mode=full
2026-05-26 16:00:53.832 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 91 READY | mode=full | segments=5
2026-05-26 16:00:53.838 | INFO     | app.services.workers.chapter_worker:process_chapter:79 - Chapter processing start | chapter=93 | mode=full | title=Mật mã | chars=2142 | estimated_tokens=1074 | estimated_audio_seconds=226
2026-05-26 16:00:56.080 | INFO     | app.services.workers.chapter_worker:process_chapter:106 - Chapter pipelines dispatch | chapter=93 | mode=full | rag=true | tts=true
2026-05-26 16:00:56.085 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:151 - TTS pipeline start | chapter=93 | mode=full | title=Mật mã | raw_chars=2142
2026-05-26 16:00:56.089 | INFO     | app.services.llm_service:normalize_text_for_speech:176 - Normalize preflight | mode=full | title=Mật mã | chars=2142 | estimated_tokens=1074 | estimated_audio_seconds=226
2026-05-26 16:00:56.093 | INFO     | app.services.llm_service:normalize_text_for_speech:187 - Normalize strategy | mode=full | strategy=single_call | title=Mật mã
2026-05-26 16:00:56.095 | INFO     | app.services.llm_service:_call_normalize_llm:136 - LLM normalize start | mode=full | context=single | chars=2142
2026-05-26 16:00:58.272 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 16:00:58,272: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[f3a86a23-e43a-480c-a405-06822cc3d0e6] succeeded in 7.710225832997821s: None
2026-05-26 16:00:59.601 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=92 | mode=full
2026-05-26 16:00:59.605 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=de05adc0-dfa2-4bdc-a7b5-dd14b9e40539 | mode=full | segments=4 | review_audio=True
2026-05-26 16:01:02.744 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=de05adc0-dfa2-4bdc-a7b5-dd14b9e40539 | mode=full
2026-05-26 16:01:05.204 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 92 READY | mode=full | segments=4
[2026-05-26 16:01:07,441: INFO/ForkPoolWorker-1] Retrying request to /chat/completions in 0.415326 seconds
2026-05-26 16:01:09.108 | INFO     | app.services.embed_service:embed_and_save_chapter:78 - RAG: Saved 3 vectors for chapter_id=96242909-5757-4c78-b411-1821d1324b91
2026-05-26 16:01:21.736 | INFO     | app.services.llm_service:_call_normalize_llm:157 - LLM normalize done | mode=full | context=single | scripts=6 | review_chars=628
2026-05-26 16:01:21.736 | INFO     | app.services.workers.tts_worker:run_tts_pipeline:158 - TTS pipeline normalized | chapter=93 | mode=full | main_scripts=6 | review_chars=628
2026-05-26 16:01:21.736 | INFO     | app.services.workers.tts_worker:_generate_main_segments:46 - TTS main segments start | chapter=93 | mode=full | total_scripts=6
2026-05-26 16:01:21.737 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=93 | mode=full | segment=1/6 | chars=351
2026-05-26 16:01:27.642 | INFO     | logging:callHandlers:1762 - 10.16.5.171:19412 - "GET /robots.txt HTTP/1.1" 404
2026-05-26 16:01:28.774 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=93 | mode=full | segment=1/6 | duration_ms=18744
2026-05-26 16:01:28.777 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=93 | mode=full | segment=2/6 | chars=337
2026-05-26 16:01:28.868 | INFO     | logging:callHandlers:1762 - 10.16.25.130:63820 - "GET /robots.txt HTTP/1.1" 404
2026-05-26 16:01:33.669 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=93 | mode=full | segment=2/6 | duration_ms=240
2026-05-26 16:01:33.672 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=93 | mode=full | segment=3/6 | chars=456
2026-05-26 16:01:49.307 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=93 | mode=full | segment=3/6 | duration_ms=40560
2026-05-26 16:01:49.308 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=93 | mode=full | segment=4/6 | chars=206
[2026-05-26 16:01:49,692: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 16:01:50,562: INFO/MainProcess] Task triam.notifications.scan_due[babf1397-1a57-401e-80c5-6e96d82bcf3c] received
2026-05-26 16:01:55.240 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=93 | mode=full | segment=4/6 | duration_ms=13608
2026-05-26 16:01:55.243 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=93 | mode=full | segment=5/6 | chars=333
2026-05-26 16:01:58.143 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 16:01:58,144: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[babf1397-1a57-401e-80c5-6e96d82bcf3c] succeeded in 7.580855980981141s: None
2026-05-26 16:02:06.111 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=93 | mode=full | segment=5/6 | duration_ms=22872
2026-05-26 16:02:06.114 | INFO     | app.services.workers.tts_worker:_generate_main_segments:51 - TTS segment start | chapter=93 | mode=full | segment=6/6 | chars=405
2026-05-26 16:02:26.629 | INFO     | app.services.workers.tts_worker:_generate_main_segments:68 - TTS segment done | chapter=93 | mode=full | segment=6/6 | duration_ms=25440
2026-05-26 16:02:26.631 | INFO     | app.services.workers.tts_worker:_generate_main_segments:80 - TTS main segments done | chapter=93 | mode=full | created_segments=6/6
2026-05-26 16:02:26.632 | INFO     | app.services.workers.tts_worker:_generate_review_audio:99 - TTS review start | chapter=93 | mode=full | chars=628
2026-05-26 16:02:46.178 | INFO     | app.services.workers.tts_worker:_generate_review_audio:103 - TTS review done | chapter=93 | mode=full
2026-05-26 16:02:46.179 | INFO     | app.services.workers.tts_worker:_store_tts_result:120 - TTS DB store start | chapter_id=96242909-5757-4c78-b411-1821d1324b91 | mode=full | segments=6 | review_audio=True
[2026-05-26 16:02:49,692: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 16:02:50,352: INFO/MainProcess] Task triam.notifications.scan_due[a0d52b62-b76f-4192-b027-55a4dad638e9] received
2026-05-26 16:02:50.479 | INFO     | app.services.workers.tts_worker:_store_tts_result:131 - TTS DB store done | chapter_id=96242909-5757-4c78-b411-1821d1324b91 | mode=full
2026-05-26 16:02:52.849 | INFO     | app.services.workers.chapter_worker:process_chapter:114 - ✅ Chapter 93 READY | mode=full | segments=6
2026-05-26 16:02:57.182 | INFO     | app.services.workers.book_pipeline:_create_book_ready_notification_safely:142 - Content-ready book-ready event | book_id=4ef0ad48-0e8f-457d-b278-3d3fe3da0905 | mode=full | created=True
2026-05-26 16:02:57.985 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 16:02:57,991: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a0d52b62-b76f-4192-b027-55a4dad638e9] succeeded in 7.637873111991212s: None
2026-05-26 16:02:58.894 | INFO     | app.services.workers.book_pipeline:run_background_processing:413 - 🎉 Book 4ef0ad48-0e8f-457d-b278-3d3fe3da0905 READY — tất cả chapters đã xử lý xong.
[2026-05-26 16:02:58,914: INFO/ForkPoolWorker-1] Task triam.books.process[0ae58bba-c2fe-4d4b-829b-fe77c8aeadb6] succeeded in 5572.755958726979s: None
[2026-05-26 16:02:59,801: INFO/MainProcess] Task triam.books.process[0ae58bba-c2fe-4d4b-829b-fe77c8aeadb6] received
2026-05-26 16:02:59.804 | INFO     | app.tasks.book_tasks:process_book_task:23 - Celery process_book_task started | book_id=4ef0ad48-0e8f-457d-b278-3d3fe3da0905 | mode=full | job_id=541e7dc7-79d0-43c7-99c4-59c1bb1b354e
2026-05-26 16:03:00.446 | INFO     | app.tasks.book_tasks:process_book_task:28 - Skip process_book_task because job is already READY | book_id=4ef0ad48-0e8f-457d-b278-3d3fe3da0905 | job_id=541e7dc7-79d0-43c7-99c4-59c1bb1b354e
[2026-05-26 16:03:00,447: INFO/ForkPoolWorker-1] Task triam.books.process[0ae58bba-c2fe-4d4b-829b-fe77c8aeadb6] succeeded in 0.6431001080200076s: None
[2026-05-26 16:03:49,694: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 16:03:50,564: INFO/MainProcess] Task triam.notifications.scan_due[bb0b1d58-6242-4568-8e8f-cab19679d41d] received
2026-05-26 16:03:58.218 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 16:03:58,220: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[bb0b1d58-6242-4568-8e8f-cab19679d41d] succeeded in 7.651678564958274s: None
[2026-05-26 16:04:49,699: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 16:04:50,355: INFO/MainProcess] Task triam.notifications.scan_due[8b6a9e2b-86c9-4f8d-b6ef-ed5a3d2e6b61] received
2026-05-26 16:04:57.958 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 16:04:57,958: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[8b6a9e2b-86c9-4f8d-b6ef-ed5a3d2e6b61] succeeded in 7.599831904051825s: None
2026-05-26 16:05:05.396 | INFO     | logging:callHandlers:1762 - 10.16.25.130:49054 - "GET /?logs=container HTTP/1.1" 200
2026-05-26 16:05:08.402 | INFO     | logging:callHandlers:1762 - 10.16.5.171:11063 - "GET /?logs=container HTTP/1.1" 200
[2026-05-26 16:05:49,699: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 16:05:50,570: INFO/MainProcess] Task triam.notifications.scan_due[a45c6c5b-2393-469b-baef-8a59a57965c6] received
2026-05-26 16:05:58.400 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 16:05:58,401: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[a45c6c5b-2393-469b-baef-8a59a57965c6] succeeded in 7.614320536958985s: None
[2026-05-26 16:06:49,702: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 16:06:50,575: INFO/MainProcess] Task triam.notifications.scan_due[eac1e028-1b78-4b81-871a-b2da78b0e16a] received
2026-05-26 16:06:58.435 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 16:06:58,438: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[eac1e028-1b78-4b81-871a-b2da78b0e16a] succeeded in 7.646997472038493s: None
[2026-05-26 16:07:49,704: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 16:07:51,158: INFO/MainProcess] Task triam.notifications.scan_due[03b7cde6-8024-4d44-aad9-9a08512c4cd4] received
2026-05-26 16:07:58.792 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 16:07:58,794: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[03b7cde6-8024-4d44-aad9-9a08512c4cd4] succeeded in 7.628770966082811s: None
[2026-05-26 16:08:49,705: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
[2026-05-26 16:08:50,575: INFO/MainProcess] Task triam.notifications.scan_due[2872ea19-81a6-4d3b-811c-993878131b3b] received
2026-05-26 16:08:58.556 | INFO     | app.tasks.notification_tasks:scan_due_notifications_task:40 - Notification scan done | created=0 | recovered=0 | should_deliver=False
[2026-05-26 16:08:58,557: INFO/ForkPoolWorker-1] Task triam.notifications.scan_due[2872ea19-81a6-4d3b-811c-993878131b3b] succeeded in 7.767214972991496s: None
