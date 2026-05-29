Lenovo@KhoaSinoo MINGW64 /w/WorkSpace_IT/\_CAPSTON_PROJECT/triam-backend (dev)
$ ./start.sh
Starting realtime voice agent...
Skipping Celery document worker because ENABLE_CELERY_WORKER=false
Skipping Celery notification worker because ENABLE_NOTIFICATION_WORKER=false
Skipping Celery Beat because ENABLE_CELERY_BEAT=false
Starting FastAPI on port 8000...
2026-05-29 08:28:06.616 | INFO | logging:callHandlers:1762 - starting worker
{"message": "starting worker", "level": "INFO", "name": "livekit.agents", "version": "1.5.8", "rtc-version": "1.1.7", "timestamp": "2026-05-29T01:28:06.616168+00:00"}
2026-05-29 08:28:06.617 | INFO | logging:callHandlers:1762 - plugin registered
{"message": "plugin registered", "level": "INFO", "name": "livekit.agents", "plugin": "livekit.plugins.openai", "version": "1.5.8", "timestamp": "2026-05-29T01:28:06.617406+00:00"}
2026-05-29 08:28:06.618 | INFO | logging:callHandlers:1762 - HTTP server listening on :8081
{"message": "HTTP server listening on :8081", "level": "INFO", "name": "livekit.agents", "timestamp": "2026-05-29T01:28:06.618414+00:00"}
2026-05-29 08:28:06.620 | INFO | logging:callHandlers:1762 - initializing job runner
{"message": "initializing job runner", "level": "INFO", "name": "livekit.agents", "tid": 10944, "timestamp": "2026-05-29T01:28:06.620414+00:00"}
2026-05-29 08:28:06.620 | INFO | logging:callHandlers:1762 - job runner initialized
{"message": "job runner initialized", "level": "INFO", "name": "livekit.agents", "tid": 10944, "elapsed_time": 0.0, "timestamp": "2026-05-29T01:28:06.620414+00:00"}
2026-05-29 08:28:07.842 | INFO | logging:callHandlers:1762 - registered worker
{"message": "registered worker", "level": "INFO", "name": "livekit.agents", "agent_name": "triam-voice-agent", "id": "AW_eBGWHZuQDjwd", "url": "wss://tri-am-bmdl413w.livekit.cloud", "region": "India South", "protocol": 17, "timestamp": "2026-05-29T01:28:07.842446+00:00"}
2026-05-29 08:28:35.888 | INFO | logging:callHandlers:1762 - Started server process [7588]
2026-05-29 08:28:35.889 | INFO | logging:callHandlers:1762 - Waiting for application startup.
2026-05-29 08:28:35.889 | INFO | app.main:lifespan:16 - Khởi động hệ thống... (TRIAM)
2026-05-29 08:28:35.890 | INFO | logging:callHandlers:1762 - Application startup complete.
2026-05-29 08:28:35.890 | INFO | logging:callHandlers:1762 - Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
2026-05-29 08:28:56.115 | INFO | logging:callHandlers:1762 - 127.0.0.1:50849 - "GET / HTTP/1.1" 200
2026-05-29 08:28:56.157 | INFO | logging:callHandlers:1762 - 127.0.0.1:50850 - "GET /favicon.ico HTTP/1.1" 404
2026-05-29 08:29:00.673 | INFO | logging:callHandlers:1762 - 127.0.0.1:50849 - "GET /docs HTTP/1.1" 200
2026-05-29 08:29:01.299 | INFO | logging:callHandlers:1762 - 127.0.0.1:50849 - "GET /openapi.json HTTP/1.1" 200
2026-05-29 08:29:37.438 | INFO | logging:callHandlers:1762 - 127.0.0.1:50866 - "GET /api/v1/books HTTP/1.1" 401
2026-05-29 08:36:47.964 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
psycopg2.errors.UndefinedColumn: column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 736, in app
await route.handle(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 290, in handle
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 101, in app
response = await f(request)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, \**values)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio\to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 986, in run
result = context.run(func, *args)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\api\v1\routers\audiobooks.py", line 29, in read_all_books
return list_books(session, current_user.sub)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\services\audiobook_service.py", line 23, in list_books
return audiobook_repo.get_audiobooks_by_user(session, user_id)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\repositories\audiobook_repo.py", line 18, in get_audiobooks_by_user
return list(session.exec(select(Book).where(Book.user_id == user_id)).all())
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlmodel\orm\session.py", line 75, in exec
results = super().execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2351, in execute
return self.\_execute_internal(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2249, in \_execute_internal
result: Result[Any] = compile_state_cls.orm_execute_statement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\context.py", line 306, in orm_execute_statement
result = conn.execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1419, in execute
return meth(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 527, in \_execute_on_connection
return connection.\_execute_clauseelement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1641, in \_execute_clauseelement
ret = self.\_execute_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in \_execute_context
return self.\_exec_single_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in \_exec_single_context
self.\_handle_dbapi_exception(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2363, in \_handle_dbapi_exception
raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedColumn) column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

[SQL: SELECT books.id, books.user_id, books.title, books.author, books.file_url, books.document_type, books.total_chapters, books.total_sections, books.total_units, books.status, books.error_message, books.created_at, books.updated_at
FROM books
WHERE books.user_id = %(user_id_1)s::UUID]
[parameters: {'user_id_1': UUID('895813bc-dc5e-40c0-8753-b9c3ef9b476a')}]
(Background on this error at: https://sqlalche.me/e/20/f405)
2026-05-29 08:36:48.193 | INFO | logging:callHandlers:1762 - 127.0.0.1:50278 - "GET /api/v1/books HTTP/1.1" 500
2026-05-29 08:36:48.193 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
psycopg2.errors.UndefinedColumn: column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\protocols\http\h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\errors.py", line 186, in **call**
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 736, in app
await route.handle(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 290, in handle
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 101, in app
response = await f(request)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, \**values)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio\to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 986, in run
result = context.run(func, *args)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\api\v1\routers\audiobooks.py", line 29, in read_all_books
return list_books(session, current_user.sub)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\services\audiobook_service.py", line 23, in list_books
return audiobook_repo.get_audiobooks_by_user(session, user_id)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\repositories\audiobook_repo.py", line 18, in get_audiobooks_by_user
return list(session.exec(select(Book).where(Book.user_id == user_id)).all())
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlmodel\orm\session.py", line 75, in exec
results = super().execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2351, in execute
return self.\_execute_internal(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2249, in \_execute_internal
result: Result[Any] = compile_state_cls.orm_execute_statement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\context.py", line 306, in orm_execute_statement
result = conn.execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1419, in execute
return meth(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 527, in \_execute_on_connection
return connection.\_execute_clauseelement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1641, in \_execute_clauseelement
ret = self.\_execute_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in \_execute_context
return self.\_exec_single_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in \_exec_single_context
self.\_handle_dbapi_exception(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2363, in \_handle_dbapi_exception
raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedColumn) column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

[SQL: SELECT books.id, books.user_id, books.title, books.author, books.file_url, books.document_type, books.total_chapters, books.total_sections, books.total_units, books.status, books.error_message, books.created_at, books.updated_at
FROM books
WHERE books.user_id = %(user_id_1)s::UUID]
[parameters: {'user_id_1': UUID('895813bc-dc5e-40c0-8753-b9c3ef9b476a')}]
(Background on this error at: https://sqlalche.me/e/20/f405)
2026-05-29 08:39:49.188 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
psycopg2.errors.UndefinedColumn: column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 736, in app
await route.handle(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 290, in handle
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 101, in app
response = await f(request)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, \**values)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio\to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 986, in run
result = context.run(func, *args)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\api\v1\routers\audiobooks.py", line 34, in read_book
return get_book(session, book_id, current_user.sub)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\services\audiobook_service.py", line 27, in get_book
book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\repositories\audiobook_repo.py", line 26, in get_book_by_id_and_user
return session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlmodel\orm\session.py", line 75, in exec
results = super().execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2351, in execute
return self.\_execute_internal(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2249, in \_execute_internal
result: Result[Any] = compile_state_cls.orm_execute_statement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\context.py", line 306, in orm_execute_statement
result = conn.execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1419, in execute
return meth(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 527, in \_execute_on_connection
return connection.\_execute_clauseelement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1641, in \_execute_clauseelement
ret = self.\_execute_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in \_execute_context
return self.\_exec_single_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in \_exec_single_context
self.\_handle_dbapi_exception(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2363, in \_handle_dbapi_exception
raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedColumn) column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

[SQL: SELECT books.id, books.user_id, books.title, books.author, books.file_url, books.document_type, books.total_chapters, books.total_sections, books.total_units, books.status, books.error_message, books.created_at, books.updated_at
FROM books
WHERE books.id = %(id_1)s::UUID AND books.user_id = %(user_id_1)s::UUID]
[parameters: {'id_1': UUID('5ef640e3-40f5-4fa6-8343-b6fd6a03c305'), 'user_id_1': UUID('895813bc-dc5e-40c0-8753-b9c3ef9b476a')}]
(Background on this error at: https://sqlalche.me/e/20/f405)
2026-05-29 08:39:49.191 | INFO | logging:callHandlers:1762 - 127.0.0.1:60920 - "GET /api/v1/books/5ef640e3-40f5-4fa6-8343-b6fd6a03c305 HTTP/1.1" 500
2026-05-29 08:39:49.191 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
psycopg2.errors.UndefinedColumn: column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\protocols\http\h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\errors.py", line 186, in **call**
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 736, in app
await route.handle(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 290, in handle
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 101, in app
response = await f(request)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, \**values)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio\to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 986, in run
result = context.run(func, *args)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\api\v1\routers\audiobooks.py", line 34, in read_book
return get_book(session, book_id, current_user.sub)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\services\audiobook_service.py", line 27, in get_book
book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\repositories\audiobook_repo.py", line 26, in get_book_by_id_and_user
return session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlmodel\orm\session.py", line 75, in exec
results = super().execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2351, in execute
return self.\_execute_internal(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2249, in \_execute_internal
result: Result[Any] = compile_state_cls.orm_execute_statement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\context.py", line 306, in orm_execute_statement
result = conn.execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1419, in execute
return meth(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 527, in \_execute_on_connection
return connection.\_execute_clauseelement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1641, in \_execute_clauseelement
ret = self.\_execute_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in \_execute_context
return self.\_exec_single_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in \_exec_single_context
self.\_handle_dbapi_exception(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2363, in \_handle_dbapi_exception
raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedColumn) column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

[SQL: SELECT books.id, books.user_id, books.title, books.author, books.file_url, books.document_type, books.total_chapters, books.total_sections, books.total_units, books.status, books.error_message, books.created_at, books.updated_at
FROM books
WHERE books.id = %(id_1)s::UUID AND books.user_id = %(user_id_1)s::UUID]
[parameters: {'id_1': UUID('5ef640e3-40f5-4fa6-8343-b6fd6a03c305'), 'user_id_1': UUID('895813bc-dc5e-40c0-8753-b9c3ef9b476a')}]
(Background on this error at: https://sqlalche.me/e/20/f405)
2026-05-29 08:40:12.810 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
psycopg2.errors.UndefinedColumn: column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 736, in app
await route.handle(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 290, in handle
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 101, in app
response = await f(request)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, \**values)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio\to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 986, in run
result = context.run(func, *args)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\api\v1\routers\audiobooks.py", line 49, in get_book_learning_units_endpoint
return get_book_learning_units(session, book_id, current_user.sub, mode)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\services\audiobook_service.py", line 134, in get_book_learning_units
book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\repositories\audiobook_repo.py", line 26, in get_book_by_id_and_user
return session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlmodel\orm\session.py", line 75, in exec
results = super().execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2351, in execute
return self.\_execute_internal(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2249, in \_execute_internal
result: Result[Any] = compile_state_cls.orm_execute_statement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\context.py", line 306, in orm_execute_statement
result = conn.execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1419, in execute
return meth(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 527, in \_execute_on_connection
return connection.\_execute_clauseelement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1641, in \_execute_clauseelement
ret = self.\_execute_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in \_execute_context
return self.\_exec_single_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in \_exec_single_context
self.\_handle_dbapi_exception(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2363, in \_handle_dbapi_exception
raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedColumn) column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

[SQL: SELECT books.id, books.user_id, books.title, books.author, books.file_url, books.document_type, books.total_chapters, books.total_sections, books.total_units, books.status, books.error_message, books.created_at, books.updated_at
FROM books
WHERE books.id = %(id_1)s::UUID AND books.user_id = %(user_id_1)s::UUID]
[parameters: {'id_1': UUID('5ef640e3-40f5-4fa6-8343-b6fd6a03c305'), 'user_id_1': UUID('895813bc-dc5e-40c0-8753-b9c3ef9b476a')}]
(Background on this error at: https://sqlalche.me/e/20/f405)
2026-05-29 08:40:12.813 | INFO | logging:callHandlers:1762 - 127.0.0.1:60924 - "GET /api/v1/books/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/learning-units?mode=full HTTP/1.1" 500
2026-05-29 08:40:12.813 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
psycopg2.errors.UndefinedColumn: column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\protocols\http\h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\errors.py", line 186, in **call**
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 736, in app
await route.handle(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 290, in handle
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 101, in app
response = await f(request)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, \**values)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio\to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 986, in run
result = context.run(func, *args)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\api\v1\routers\audiobooks.py", line 49, in get_book_learning_units_endpoint
return get_book_learning_units(session, book_id, current_user.sub, mode)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\services\audiobook_service.py", line 134, in get_book_learning_units
book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\repositories\audiobook_repo.py", line 26, in get_book_by_id_and_user
return session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlmodel\orm\session.py", line 75, in exec
results = super().execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2351, in execute
return self.\_execute_internal(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2249, in \_execute_internal
result: Result[Any] = compile_state_cls.orm_execute_statement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\context.py", line 306, in orm_execute_statement
result = conn.execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1419, in execute
return meth(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 527, in \_execute_on_connection
return connection.\_execute_clauseelement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1641, in \_execute_clauseelement
ret = self.\_execute_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in \_execute_context
return self.\_exec_single_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in \_exec_single_context
self.\_handle_dbapi_exception(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2363, in \_handle_dbapi_exception
raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedColumn) column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

[SQL: SELECT books.id, books.user_id, books.title, books.author, books.file_url, books.document_type, books.total_chapters, books.total_sections, books.total_units, books.status, books.error_message, books.created_at, books.updated_at
FROM books
WHERE books.id = %(id_1)s::UUID AND books.user_id = %(user_id_1)s::UUID]
[parameters: {'id_1': UUID('5ef640e3-40f5-4fa6-8343-b6fd6a03c305'), 'user_id_1': UUID('895813bc-dc5e-40c0-8753-b9c3ef9b476a')}]
(Background on this error at: https://sqlalche.me/e/20/f405)
2026-05-29 08:40:26.485 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
psycopg2.errors.UndefinedColumn: column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 736, in app
await route.handle(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 290, in handle
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 101, in app
response = await f(request)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, \**values)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio\to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 986, in run
result = context.run(func, *args)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\api\v1\routers\audiobooks.py", line 44, in get_book_outline_endpoint
return get_book_outline(session, book_id, current_user.sub)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\services\audiobook_service.py", line 102, in get_book_outline
book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\repositories\audiobook_repo.py", line 26, in get_book_by_id_and_user
return session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlmodel\orm\session.py", line 75, in exec
results = super().execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2351, in execute
return self.\_execute_internal(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2249, in \_execute_internal
result: Result[Any] = compile_state_cls.orm_execute_statement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\context.py", line 306, in orm_execute_statement
result = conn.execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1419, in execute
return meth(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 527, in \_execute_on_connection
return connection.\_execute_clauseelement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1641, in \_execute_clauseelement
ret = self.\_execute_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in \_execute_context
return self.\_exec_single_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in \_exec_single_context
self.\_handle_dbapi_exception(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2363, in \_handle_dbapi_exception
raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedColumn) column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

[SQL: SELECT books.id, books.user_id, books.title, books.author, books.file_url, books.document_type, books.total_chapters, books.total_sections, books.total_units, books.status, books.error_message, books.created_at, books.updated_at
FROM books
WHERE books.id = %(id_1)s::UUID AND books.user_id = %(user_id_1)s::UUID]
[parameters: {'id_1': UUID('5ef640e3-40f5-4fa6-8343-b6fd6a03c305'), 'user_id_1': UUID('895813bc-dc5e-40c0-8753-b9c3ef9b476a')}]
(Background on this error at: https://sqlalche.me/e/20/f405)
2026-05-29 08:40:26.487 | INFO | logging:callHandlers:1762 - 127.0.0.1:60926 - "GET /api/v1/books/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/outline HTTP/1.1" 500
2026-05-29 08:40:26.488 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
psycopg2.errors.UndefinedColumn: column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\protocols\http\h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\errors.py", line 186, in **call**
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 736, in app
await route.handle(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 290, in handle
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 101, in app
response = await f(request)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, \**values)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio\to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 986, in run
result = context.run(func, *args)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\api\v1\routers\audiobooks.py", line 44, in get_book_outline_endpoint
return get_book_outline(session, book_id, current_user.sub)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\services\audiobook_service.py", line 102, in get_book_outline
book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\repositories\audiobook_repo.py", line 26, in get_book_by_id_and_user
return session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlmodel\orm\session.py", line 75, in exec
results = super().execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2351, in execute
return self.\_execute_internal(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2249, in \_execute_internal
result: Result[Any] = compile_state_cls.orm_execute_statement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\context.py", line 306, in orm_execute_statement
result = conn.execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1419, in execute
return meth(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 527, in \_execute_on_connection
return connection.\_execute_clauseelement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1641, in \_execute_clauseelement
ret = self.\_execute_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in \_execute_context
return self.\_exec_single_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in \_exec_single_context
self.\_handle_dbapi_exception(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2363, in \_handle_dbapi_exception
raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedColumn) column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

[SQL: SELECT books.id, books.user_id, books.title, books.author, books.file_url, books.document_type, books.total_chapters, books.total_sections, books.total_units, books.status, books.error_message, books.created_at, books.updated_at
FROM books
WHERE books.id = %(id_1)s::UUID AND books.user_id = %(user_id_1)s::UUID]
[parameters: {'id_1': UUID('5ef640e3-40f5-4fa6-8343-b6fd6a03c305'), 'user_id_1': UUID('895813bc-dc5e-40c0-8753-b9c3ef9b476a')}]
(Background on this error at: https://sqlalche.me/e/20/f405)
2026-05-29 08:40:46.338 | ERROR | app.main:global_exception_handler:42 - Unhandled Exception:
Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
psycopg2.errors.UndefinedColumn: column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 736, in app
await route.handle(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 290, in handle
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 101, in app
response = await f(request)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, \**values)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio\to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 986, in run
result = context.run(func, *args)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\api\v1\routers\audiobooks.py", line 39, in get_book_details_endpoint
return get_book_details(session, book_id, current_user.sub, mode=mode)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\services\audiobook_service.py", line 82, in get_book_details
book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\repositories\audiobook_repo.py", line 26, in get_book_by_id_and_user
return session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlmodel\orm\session.py", line 75, in exec
results = super().execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2351, in execute
return self.\_execute_internal(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2249, in \_execute_internal
result: Result[Any] = compile_state_cls.orm_execute_statement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\context.py", line 306, in orm_execute_statement
result = conn.execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1419, in execute
return meth(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 527, in \_execute_on_connection
return connection.\_execute_clauseelement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1641, in \_execute_clauseelement
ret = self.\_execute_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in \_execute_context
return self.\_exec_single_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in \_exec_single_context
self.\_handle_dbapi_exception(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2363, in \_handle_dbapi_exception
raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedColumn) column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

[SQL: SELECT books.id, books.user_id, books.title, books.author, books.file_url, books.document_type, books.total_chapters, books.total_sections, books.total_units, books.status, books.error_message, books.created_at, books.updated_at
FROM books
WHERE books.id = %(id_1)s::UUID AND books.user_id = %(user_id_1)s::UUID]
[parameters: {'id_1': UUID('5ef640e3-40f5-4fa6-8343-b6fd6a03c305'), 'user_id_1': UUID('895813bc-dc5e-40c0-8753-b9c3ef9b476a')}]
(Background on this error at: https://sqlalche.me/e/20/f405)
2026-05-29 08:40:46.341 | INFO | logging:callHandlers:1762 - 127.0.0.1:60928 - "GET /api/v1/books/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/details?mode=full HTTP/1.1" 500
2026-05-29 08:40:46.341 | ERROR | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
psycopg2.errors.UndefinedColumn: column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\protocols\http\h11_impl.py", line 410, in run_asgi
result = await app( # type: ignore[func-returns-value]
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 60, in **call**
return await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\applications.py", line 1135, in **call**
await super().**call**(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\applications.py", line 107, in **call**
await self.middleware_stack(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\errors.py", line 186, in **call**
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in **call**
await self.app(scope, receive, \_send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in **call**
await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in **call**
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 716, in **call**
await self.middleware_stack(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 736, in app
await route.handle(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\routing.py", line 290, in handle
await self.app(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 115, in app
await wrap_app_handling_exceptions(app, request)(scope, receive, send)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 53, in wrapped_app
raise exc
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette_exception_handler.py", line 42, in wrapped_app
await app(scope, receive, sender)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 101, in app
response = await f(request)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 355, in app
raw_response = await run_endpoint_function(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\fastapi\routing.py", line 245, in run_endpoint_function
return await run_in_threadpool(dependant.call, \**values)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\starlette\concurrency.py", line 32, in run_in_threadpool
return await anyio.to_thread.run_sync(func)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio\to_thread.py", line 63, in run_sync
return await get_async_backend().run_sync_in_worker_thread(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 2502, in run_sync_in_worker_thread
return await future
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\anyio_backends_asyncio.py", line 986, in run
result = context.run(func, *args)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\api\v1\routers\audiobooks.py", line 39, in get_book_details_endpoint
return get_book_details(session, book_id, current_user.sub, mode=mode)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\services\audiobook_service.py", line 82, in get_book_details
book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\app\repositories\audiobook_repo.py", line 26, in get_book_by_id_and_user
return session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlmodel\orm\session.py", line 75, in exec
results = super().execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2351, in execute
return self.\_execute_internal(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2249, in \_execute_internal
result: Result[Any] = compile_state_cls.orm_execute_statement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\context.py", line 306, in orm_execute_statement
result = conn.execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1419, in execute
return meth(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 527, in \_execute_on_connection
return connection.\_execute_clauseelement(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1641, in \_execute_clauseelement
ret = self.\_execute_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in \_execute_context
return self.\_exec_single_context(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in \_exec_single_context
self.\_handle_dbapi_exception(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2363, in \_handle_dbapi_exception
raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "W:\WorkSpace_IT_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
cursor.execute(statement, parameters)
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedColumn) column books.total_sections does not exist
LINE 1: ...e_url, books.document_type, books.total_chapters, books.tota...
^

[SQL: SELECT books.id, books.user_id, books.title, books.author, books.file_url, books.document_type, books.total_chapters, books.total_sections, books.total_units, books.status, books.error_message, books.created_at, books.updated_at
FROM books
WHERE books.id = %(id_1)s::UUID AND books.user_id = %(user_id_1)s::UUID]
[parameters: {'id_1': UUID('5ef640e3-40f5-4fa6-8343-b6fd6a03c305'), 'user_id_1': UUID('895813bc-dc5e-40c0-8753-b9c3ef9b476a')}]
(Background on this error at: https://sqlalche.me/e/20/f405)
