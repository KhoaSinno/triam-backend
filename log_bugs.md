sau khi tôi gọi log thì nó bị lỗi như này:

Lenovo@KhoaSinoo MINGW64 /w/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend (dev)
$ python tests/test_threads_for_book.py
============================================================
  KIỂM THỬ: GET /threads/for-book/{book_id} endpoint
============================================================

============================================================
  TEST 1: Lần đầu gọi → tạo auto context + thread
============================================================
   📤 Gọi GET /threads/for-book/c4948bc6-e328-48f5-9fba-0b6c0ee8044d
   ❌ Status 500: {"detail":"Lỗi hệ thống nội bộ."}

============================================================
  TEST 2: Gọi lần 2 → idempotent (return cùng thread)
============================================================
   📤 Gọi lần 1...
   ✅ Lần 1: thread_id = None
   📤 Gọi lần 2...
   ✅ Lần 2: thread_id = None
   ✅ context_id match: None
   ✅ thread_id match: None

   ✅ TEST 2 PASS: Idempotent behavior confirmed

============================================================
  TEST 3: Concurrent requests → race-safe (no duplicate)
============================================================
   🔥 Sending 5 concurrent requests...
   ✅ All 5 requests succeeded
   Thread IDs: {None}
   Context IDs: {None}
   📋 Checking DB for duplicate threads...

   ✅ TEST 3 PASS: Concurrent requests are race-safe

============================================================
  TEST 4: DirectBookContext structure validation
============================================================
   📤 Creating auto context for book fac9ca94-63ce-4ded-b61e-af804e53ca18...

Lỗi không mong đợi: 'context_id'
Traceback (most recent call last):
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\tests\test_threads_for_book.py", line 407, in <module>
    asyncio.run(main())
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\runners.py", line 195, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\base_events.py", line 691, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\tests\test_threads_for_book.py", line 384, in main
    results["TEST 4 (DirectBookContext structure)"] = await test_direct_book_context_structure()
                                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\tests\test_threads_for_book.py", line 214, in test_direct_book_context_structure
    context_id = data["context_id"]
                 ~~~~^^^^^^^^^^^^^^
KeyError: 'context_id'
(triam-backend) 




/////// Log khi server start: ////





 └ <sqlalchemy.orm.unitofwork.UOWTransaction object at 0x00000239EFC11730>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\unitofwork.py", line 466, in execute
    rec.execute(self)
    │   │       └ <sqlalchemy.orm.unitofwork.UOWTransaction object at 0x00000239EFC11730>
    │   └ <function SaveUpdateAll.execute at 0x000002399B17CCC0>
    └ SaveUpdateAll(Mapper[StudyContextDocumentLink(study_context_document_links)])
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\unitofwork.py", line 642, in execute
    util.preloaded.orm_persistence.save_obj(
    │    │         │               └ <function save_obj at 0x000002399B17FA60>
    │    │         └ <module 'sqlalchemy.orm.persistence' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqla...
    │    └ <module 'sqlalchemy.util.preloaded' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqlal...
    └ <module 'sqlalchemy.util' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqlalchemy\\uti...
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\persistence.py", line 93, in save_obj
    _emit_insert_statements(
    └ <function _emit_insert_statements at 0x000002399B1CDEE0>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\persistence.py", line 1048, in _emit_insert_statements
    result = connection.execute(
             │          └ <function Connection.execute at 0x0000023999E9A980>
             └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB90D40>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1419, in execute
    return meth(
           └ <bound method ClauseElement._execute_on_connection of <sqlalchemy.sql.dml.Insert object at 0x00000239EFC11D30>>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 527, in _execute_on_connection
    return connection._execute_clauseelement(
           │          └ <function Connection._execute_clauseelement at 0x0000023999E9ACA0>
           └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB90D40>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1641, in _execute_clauseelement
    ret = self._execute_context(
          │    └ <function Connection._execute_context at 0x0000023999E9AE80>
          └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB90D40>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in _execute_context
    return self._exec_single_context(
           │    └ <function Connection._exec_single_context at 0x0000023999E9AF20>
           └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB90D40>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in _exec_single_context
    self._handle_dbapi_exception(
    │    └ <function Connection._handle_dbapi_exception at 0x0000023999E9B1A0>
    └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB90D40>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2363, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
          │                    │              │                 └ ForeignKeyViolation('insert or update on table "study_context_document_links" violates foreign key constraint "study_context_...
          │                    │              └ (<class 'psycopg2.errors.ForeignKeyViolation'>, ForeignKeyViolation('insert or update on table "study_context_document_links"...
          │                    └ <method 'with_traceback' of 'BaseException' objects>
          └ IntegrityError('(psycopg2.errors.ForeignKeyViolation) insert or update on table "study_context_document_links" violates forei...
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
    │    │       └ <function DefaultDialect.do_execute at 0x000002399AF29C60>
    │    └ <sqlalchemy.dialects.postgresql.psycopg2.PGDialect_psycopg2 object at 0x000002399CAE8A10>
    └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB90D40>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    │      │       │          └ {'context_id': UUID('8d5d4382-e0b8-4bcf-ae89-940f6e603c62'), 'book_id': UUID('66abae2c-7252-4a75-8224-e4758d5b8798')}
    │      │       └ 'INSERT INTO study_context_document_links (context_id, book_id) VALUES (%(context_id)s::UUID, %(book_id)s::UUID)'
    │      └ <method 'execute' of 'psycopg2.extensions.cursor' objects>
    └ <cursor object at 0x00000239EFECC040; closed: -1>

sqlalchemy.exc.IntegrityError: (psycopg2.errors.ForeignKeyViolation) insert or update on table "study_context_document_links" violates foreign key constraint "study_context_document_links_book_id_fkey"
DETAIL:  Key (book_id)=(66abae2c-7252-4a75-8224-e4758d5b8798) is not present in table "books".

[SQL: INSERT INTO study_context_document_links (context_id, book_id) VALUES (%(context_id)s::UUID, %(book_id)s::UUID)]
[parameters: {'context_id': UUID('8d5d4382-e0b8-4bcf-ae89-940f6e603c62'), 'book_id': UUID('66abae2c-7252-4a75-8224-e4758d5b8798')}]
(Background on this error at: https://sqlalche.me/e/20/gkpj)


During handling of the above exception, another exception occurred:


Traceback (most recent call last):

  File "<string>", line 1, in <module>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\spawn.py", line 122, in spawn_main
    exitcode = _main(fd, parent_sentinel)
               │     │   └ 376
               │     └ 3
               └ <function _main at 0x00000239962FBF60>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\spawn.py", line 135, in _main
    return self._bootstrap(parent_sentinel)
           │    │          └ 376
           │    └ <function BaseProcess._bootstrap at 0x00000239961FFF60>
           └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
    │    └ <function BaseProcess.run at 0x00000239961FF4C0>
    └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    │    │        │    │        │    └ {'config': <uvicorn.config.Config object at 0x00000239962BD0D0>, 'target': <bound method Server.run of <uvicorn.server.Server...
    │    │        │    │        └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
    │    │        │    └ ()
    │    │        └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
    │    └ <function subprocess_started at 0x00000239986CBBA0>
    └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    │              └ [<socket.socket fd=812, family=2, type=1, proto=6, laddr=('0.0.0.0', 8000)>]
    └ <bound method Server.run of <uvicorn.server.Server object at 0x000002399886C440>>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\server.py", line 67, in run
    return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
           │           │    │             │                      │    │      └ <function Config.get_loop_factory at 0x0000023998680400>
           │           │    │             │                      │    └ <uvicorn.config.Config object at 0x00000239962BD0D0>
           │           │    │             │                      └ <uvicorn.server.Server object at 0x000002399886C440>
           │           │    │             └ [<socket.socket fd=812, family=2, type=1, proto=6, laddr=('0.0.0.0', 8000)>]
           │           │    └ <function Server.serve at 0x00000239986CAF20>
           │           └ <uvicorn.server.Server object at 0x000002399886C440>
           └ <function run at 0x0000023997F1C360>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\runners.py", line 195, in run
    return runner.run(main)
           │      │   └ <coroutine object Server.serve at 0x000002399883B3E0>
           │      └ <function Runner.run at 0x0000023997FB7EC0>
           └ <asyncio.runners.Runner object at 0x00000239987174A0>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           │    │     │                  └ <Task pending name='Task-1' coro=<Server.serve() running at W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-pac...
           │    │     └ <function BaseEventLoop.run_until_complete at 0x0000023997FB5B20>
           │    └ <_WindowsSelectorEventLoop running=True closed=False debug=False>
           └ <asyncio.runners.Runner object at 0x00000239987174A0>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\base_events.py", line 678, in run_until_complete
    self.run_forever()
    │    └ <function BaseEventLoop.run_forever at 0x0000023997FB5A80>
    └ <_WindowsSelectorEventLoop running=True closed=False debug=False>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\base_events.py", line 645, in run_forever
    self._run_once()
    │    └ <function BaseEventLoop._run_once at 0x0000023997FB7880>
    └ <_WindowsSelectorEventLoop running=True closed=False debug=False>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\base_events.py", line 1999, in _run_once
    handle._run()
    │      └ <function Handle._run at 0x0000023997EEDBC0>
    └ <Handle Task.task_wakeup(<Future finished result=False>)>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12026-05-15 14:08:59.272 | ERROR    | app.main:global_exception_handler:38 - Unhandled Exception:
Traceback (most recent call last):

  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
    │    │       └ <function DefaultDialect.do_execute at 0x000002399AF29C60>
    │    └ <sqlalchemy.dialects.postgresql.psycopg2.PGDialect_psycopg2 object at 0x000002399CAE8A10>
    └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB43230>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    │      │       │          └ {'context_id': UUID('2609cb9c-a8d5-45d1-b793-5950701e1845'), 'book_id': UUID('66abae2c-7252-4a75-8224-e4758d5b8798')}
    │      │       └ 'INSERT INTO study_context_document_links (context_id, book_id) VALUES (%(context_id)s::UUID, %(book_id)s::UUID)'
    │      └ <method 'execute' of 'psycopg2.extensions.cursor' objects>
    └ <cursor object at 0x00000239EFECD540; closed: -1>

psycopg2.errors.ForeignKeyViolation: insert or update on table "study_context_document_links" violates foreign key constraint "study_context_document_links_book_id_fkey"
DETAIL:  Key (book_id)=(66abae2c-7252-4a75-8224-e4758d5b8798) is not present in table "books".



The above exception was the direct cause of the following exception:


Traceback (most recent call last):

  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\app\repositories\study_context_thread_repo.py", line 57, in get_or_create_thread_for_book_repo
    session.flush()  # To get new_thread.id populated
    │       └ <function Session.flush at 0x000002399B1F44A0>
    └ <sqlmodel.orm.session.Session object at 0x00000239EFEC0C80>

  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 4331, in flush
    self._flush(objects)
    │    │      └ None
    │    └ <function Session._flush at 0x000002399B1F4680>
    └ <sqlmodel.orm.session.Session object at 0x00000239EFEC0C80>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 4466, in _flush
    with util.safe_reraise():
         │    └ <class 'sqlalchemy.util.langhelpers.safe_reraise'>
         └ <module 'sqlalchemy.util' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqlalchemy\\uti...
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 121, in __exit__
    raise exc_value.with_traceback(exc_tb)
          │         │              └ <traceback object at 0x00000239EFED1A80>
          │         └ <method 'with_traceback' of 'BaseException' objects>
          └ IntegrityError('(psycopg2.errors.ForeignKeyViolation) insert or update on table "study_context_document_links" violates forei...
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 4427, in _flush
    flush_context.execute()
    │             └ <function UOWTransaction.execute at 0x000002399B17C180>
    └ <sqlalchemy.orm.unitofwork.UOWTransaction object at 0x00000239EFB43AD0>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\unitofwork.py", line 466, in execute
    rec.execute(self)
    │   │       └ <sqlalchemy.orm.unitofwork.UOWTransaction object at 0x00000239EFB43AD0>
    │   └ <function SaveUpdateAll.execute at 0x000002399B17CCC0>
    └ SaveUpdateAll(Mapper[StudyContextDocumentLink(study_context_document_links)])
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\unitofwork.py", line 642, in execute
    util.preloaded.orm_persistence.save_obj(
    │    │         │               └ <function save_obj at 0x000002399B17FA60>
    │    │         └ <module 'sqlalchemy.orm.persistence' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqla...
    │    └ <module 'sqlalchemy.util.preloaded' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqlal...
    └ <module 'sqlalchemy.util' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqlalchemy\\uti...
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\persistence.py", line 93, in save_obj
    _emit_insert_statements(
    └ <function _emit_insert_statements at 0x000002399B1CDEE0>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\persistence.py", line 1048, in _emit_insert_statements
    result = connection.execute(
             │          └ <function Connection.execute at 0x0000023999E9A980>
             └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB43230>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1419, in execute
    return meth(
           └ <bound method ClauseElement._execute_on_connection of <sqlalchemy.sql.dml.Insert object at 0x00000239EFC11D30>>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 527, in _execute_on_connection
    return connection._execute_clauseelement(
           │          └ <function Connection._execute_clauseelement at 0x0000023999E9ACA0>
           └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB43230>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1641, in _execute_clauseelement
    ret = self._execute_context(
          │    └ <function Connection._execute_context at 0x0000023999E9AE80>
          └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB43230>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in _execute_context
    return self._exec_single_context(
           │    └ <function Connection._exec_single_context at 0x0000023999E9AF20>
           └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB43230>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in _exec_single_context
    self._handle_dbapi_exception(
    │    └ <function Connection._handle_dbapi_exception at 0x0000023999E9B1A0>
    └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB43230>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2363, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
          │                    │              │                 └ ForeignKeyViolation('insert or update on table "study_context_document_links" violates foreign key constraint "study_context_...
          │                    │              └ (<class 'psycopg2.errors.ForeignKeyViolation'>, ForeignKeyViolation('insert or update on table "study_context_document_links"...
          │                    └ <method 'with_traceback' of 'BaseException' objects>
          └ IntegrityError('(psycopg2.errors.ForeignKeyViolation) insert or update on table "study_context_document_links" violates forei...
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
    │    │       └ <function DefaultDialect.do_execute at 0x000002399AF29C60>
    │    └ <sqlalchemy.dialects.postgresql.psycopg2.PGDialect_psycopg2 object at 0x000002399CAE8A10>
    └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB43230>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    │      │       │          └ {'context_id': UUID('2609cb9c-a8d5-45d1-b793-5950701e1845'), 'book_id': UUID('66abae2c-7252-4a75-8224-e4758d5b8798')}
    │      │       └ 'INSERT INTO study_context_document_links (context_id, book_id) VALUES (%(context_id)s::UUID, %(book_id)s::UUID)'
    │      └ <method 'execute' of 'psycopg2.extensions.cursor' objects>
    └ <cursor object at 0x00000239EFECD540; closed: -1>

sqlalchemy.exc.IntegrityError: (psycopg2.errors.ForeignKeyViolation) insert or update on table "study_context_document_links" violates foreign key constraint "study_context_document_links_book_id_fkey"
DETAIL:  Key (book_id)=(66abae2c-7252-4a75-8224-e4758d5b8798) is not present in table "books".

[SQL: INSERT INTO study_context_document_links (context_id, book_id) VALUES (%(context_id)s::UUID, %(book_id)s::UUID)]
[parameters: {'context_id': UUID('2609cb9c-a8d5-45d1-b793-5950701e1845'), 'book_id': UUID('66abae2c-7252-4a75-8224-e4758d5b8798')}]
(Background on this error at: https://sqlalche.me/e/20/gkpj)


During handling of the above exception, another exception occurred:


Traceback (most recent call last):

  File "<string>", line 1, in <module>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\spawn.py", line 122, in spawn_main
    exitcode = _main(fd, parent_sentinel)
               │     │   └ 376
               │     └ 3
               └ <function _main at 0x00000239962FBF60>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\spawn.py", line 135, in _main
    return self._bootstrap(parent_sentinel)
           │    │          └ 376
           │    └ <function BaseProcess._bootstrap at 0x00000239961FFF60>
           └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
    │    └ <function BaseProcess.run at 0x00000239961FF4C0>
    └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    │    │        │    │        │    └ {'config': <uvicorn.config.Config object at 0x00000239962BD0D0>, 'target': <bound method Server.run of <uvicorn.server.Server...
    │    │        │    │        └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
    │    │        │    └ ()
    │    │        └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
    │    └ <function subprocess_started at 0x00000239986CBBA0>
    └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    │              └ [<socket.socket fd=812, family=2, type=1, proto=6, laddr=('0.0.0.0', 8000)>]
    └ <bound method Server.run of <uvicorn.server.Server object at 0x000002399886C440>>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\server.py", line 67, in run
    return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
           │           │    │             │                      │    │      └ <function Config.get_loop_factory at 0x0000023998680400>
           │           │    │             │                      │    └ <uvicorn.config.Config object at 0x00000239962BD0D0>
           │           │    │             │                      └ <uvicorn.server.Server object at 0x000002399886C440>
           │           │    │             └ [<socket.socket fd=812, family=2, type=1, proto=6, laddr=('0.0.0.0', 8000)>]
           │           │    └ <function Server.serve at 0x00000239986CAF20>
           │           └ <uvicorn.server.Server object at 0x000002399886C440>
           └ <function run at 0x0000023997F1C360>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\runners.py", line 195, in run
    return runner.run(main)
           │      │   └ <coroutine object Server.serve at 0x000002399883B3E0>
           │      └ <function Runner.run at 0x0000023997FB7EC0>
           └ <asyncio.runners.Runner object at 0x00000239987174A0>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           │    │     │                  └ <Task pending name='Task-1' coro=<Server.serve() running at W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-pac...
           │    │     └ <function BaseEventLoop.run_until_complete at 0x0000023997FB5B20>
           │    └ <_WindowsSelectorEventLoop running=True closed=False debug=False>
           └ <asyncio.runners.Runner object at 0x00000239987174A0>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\base_events.py", line 678, in run_until_complete
    self.run_forever()
    │    └ <function BaseEventLoop.run_forever at 0x0000023997FB5A80>
    └ <_WindowsSelectorEventLoop running=True closed=False debug=False>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\base_events.py", line 645, in run_forever
    self._run_once()
    │    └ <function BaseEventLoop._run_once at 0x0000023997FB7880>
    └ <_WindowsSelectorEventLoop running=True closed=False debug=False>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\base_events.py", line 1999, in _run_once
    handle._run()
    │      └ <function Handle._run at 0x0000023997EEDBC0>
    └ <Handle Task.task_wakeup(<Future finished res2026-05-15 14:08:59.286 | INFO     | logging:callHandlers:1762 - 127.0.0.1:64366 - "GET /api/v1/threads/for-book/66abae2c-7252-4a75-8224-e4758d5b8798 HTTP/1.1" 500
2026-05-15 14:08:59.286 | ERROR    | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):

  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
    │    │       └ <function DefaultDialect.do_execute at 0x000002399AF29C60>
    │    └ <sqlalchemy.dialects.postgresql.psycopg2.PGDialect_psycopg2 object at 0x000002399CAE8A10>
    └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB43230>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    │      │       │          └ {'context_id': UUID('2609cb9c-a8d5-45d1-b793-5950701e1845'), 'book_id': UUID('66abae2c-7252-4a75-8224-e4758d5b8798')}
    │      │       └ 'INSERT INTO study_context_document_links (context_id, book_id) VALUES (%(context_id)s::UUID, %(book_id)s::UUID)'
    │      └ <method 'execute' of 'psycopg2.extensions.cursor' objects>
    └ <cursor object at 0x00000239EFECD540; closed: -1>

psycopg2.errors.ForeignKeyViolation: insert or update on table "study_context_document_links" violates foreign key constraint "study_context_document_links_book_id_fkey"
DETAIL:  Key (book_id)=(66abae2c-7252-4a75-8224-e4758d5b8798) is not present in table "books".



The above exception was the direct cause of the following exception:


Traceback (most recent call last):

  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\app\repositories\study_context_thread_repo.py", line 57, in get_or_create_thread_for_book_repo
    session.flush()  # To get new_thread.id populated
    │       └ <function Session.flush at 0x000002399B1F44A0>
    └ <sqlmodel.orm.session.Session object at 0x00000239EFEC0C80>

  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 4331, in flush
    self._flush(objects)
    │    │      └ None
    │    └ <function Session._flush at 0x000002399B1F4680>
    └ <sqlmodel.orm.session.Session object at 0x00000239EFEC0C80>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 4466, in _flush
    with util.safe_reraise():
         │    └ <class 'sqlalchemy.util.langhelpers.safe_reraise'>
         └ <module 'sqlalchemy.util' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqlalchemy\\uti...
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 121, in __exit__
    raise exc_value.with_traceback(exc_tb)
          │         │              └ <traceback object at 0x00000239EFED1A80>
          │         └ <method 'with_traceback' of 'BaseException' objects>
          └ IntegrityError('(psycopg2.errors.ForeignKeyViolation) insert or update on table "study_context_document_links" violates forei...
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 4427, in _flush
    flush_context.execute()
    │             └ <function UOWTransaction.execute at 0x000002399B17C180>
    └ <sqlalchemy.orm.unitofwork.UOWTransaction object at 0x00000239EFB43AD0>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\unitofwork.py", line 466, in execute
    rec.execute(self)
    │   │       └ <sqlalchemy.orm.unitofwork.UOWTransaction object at 0x00000239EFB43AD0>
    │   └ <function SaveUpdateAll.execute at 0x000002399B17CCC0>
    └ SaveUpdateAll(Mapper[StudyContextDocumentLink(study_context_document_links)])
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\unitofwork.py", line 642, in execute
    util.preloaded.orm_persistence.save_obj(
    │    │         │               └ <function save_obj at 0x000002399B17FA60>
    │    │         └ <module 'sqlalchemy.orm.persistence' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqla...
    │    └ <module 'sqlalchemy.util.preloaded' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqlal...
    └ <module 'sqlalchemy.util' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqlalchemy\\uti...
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\persistence.py", line 93, in save_obj
    _emit_insert_statements(
    └ <function _emit_insert_statements at 0x000002399B1CDEE0>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\persistence.py", line 1048, in _emit_insert_statements
    result = connection.execute(
             │          └ <function Connection.execute at 0x0000023999E9A980>
             └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB43230>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1419, in execute
    return meth(
           └ <bound method ClauseElement._execute_on_connection of <sqlalchemy.sql.dml.Insert object at 0x00000239EFC11D30>>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 527, in _execute_on_connection
    return connection._execute_clauseelement(
           │          └ <function Connection._execute_clauseelement at 0x0000023999E9ACA0>
           └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB43230>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1641, in _execute_clauseelement
    ret = self._execute_context(
          │    └ <function Connection._execute_context at 0x0000023999E9AE80>
          └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB43230>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in _execute_context
    return self._exec_single_context(
           │    └ <function Connection._exec_single_context at 0x0000023999E9AF20>
           └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB43230>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in _exec_single_context
    self._handle_dbapi_exception(
    │    └ <function Connection._handle_dbapi_exception at 0x0000023999E9B1A0>
    └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB43230>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2363, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
          │                    │              │                 └ ForeignKeyViolation('insert or update on table "study_context_document_links" violates foreign key constraint "study_context_...
          │                    │              └ (<class 'psycopg2.errors.ForeignKeyViolation'>, ForeignKeyViolation('insert or update on table "study_context_document_links"...
          │                    └ <method 'with_traceback' of 'BaseException' objects>
          └ IntegrityError('(psycopg2.errors.ForeignKeyViolation) insert or update on table "study_context_document_links" violates forei...
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
    │    │       └ <function DefaultDialect.do_execute at 0x000002399AF29C60>
    │    └ <sqlalchemy.dialects.postgresql.psycopg2.PGDialect_psycopg2 object at 0x000002399CAE8A10>
    └ <sqlalchemy.engine.base.Connection object at 0x00000239EFB43230>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    │      │       │          └ {'context_id': UUID('2609cb9c-a8d5-45d1-b793-5950701e1845'), 'book_id': UUID('66abae2c-7252-4a75-8224-e4758d5b8798')}
    │      │       └ 'INSERT INTO study_context_document_links (context_id, book_id) VALUES (%(context_id)s::UUID, %(book_id)s::UUID)'
    │      └ <method 'execute' of 'psycopg2.extensions.cursor' objects>
    └ <cursor object at 0x00000239EFECD540; closed: -1>

sqlalchemy.exc.IntegrityError: (psycopg2.errors.ForeignKeyViolation) insert or update on table "study_context_document_links" violates foreign key constraint "study_context_document_links_book_id_fkey"
DETAIL:  Key (book_id)=(66abae2c-7252-4a75-8224-e4758d5b8798) is not present in table "books".

[SQL: INSERT INTO study_context_document_links (context_id, book_id) VALUES (%(context_id)s::UUID, %(book_id)s::UUID)]
[parameters: {'context_id': UUID('2609cb9c-a8d5-45d1-b793-5950701e1845'), 'book_id': UUID('66abae2c-7252-4a75-8224-e4758d5b8798')}]
(Background on this error at: https://sqlalche.me/e/20/gkpj)


During handling of the above exception, another exception occurred:


Traceback (most recent call last):

  File "<string>", line 1, in <module>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\spawn.py", line 122, in spawn_main
    exitcode = _main(fd, parent_sentinel)
               │     │   └ 376
               │     └ 3
               └ <function _main at 0x00000239962FBF60>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\spawn.py", line 135, in _main
    return self._bootstrap(parent_sentinel)
           │    │          └ 376
           │    └ <function BaseProcess._bootstrap at 0x00000239961FFF60>
           └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
    │    └ <function BaseProcess.run at 0x00000239961FF4C0>
    └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    │    │        │    │        │    └ {'config': <uvicorn.config.Config object at 0x00000239962BD0D0>, 'target': <bound method Server.run of <uvicorn.server.Server...
    │    │        │    │        └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
    │    │        │    └ ()
    │    │        └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
    │    └ <function subprocess_started at 0x00000239986CBBA0>
    └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    │              └ [<socket.socket fd=812, family=2, type=1, proto=6, laddr=('0.0.0.0', 8000)>]
    └ <bound method Server.run of <uvicorn.server.Server object at 0x000002399886C440>>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\server.py", line 67, in run
    return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
           │           │    │             │                      │    │      └ <function Config.get_loop_factory at 0x0000023998680400>
           │           │    │             │                      │    └ <uvicorn.config.Config object at 0x00000239962BD0D0>
           │           │    │             │                      └ <uvicorn.server.Server object at 0x000002399886C440>
           │           │    │             └ [<socket.socket fd=812, family=2, type=1, proto=6, laddr=('0.0.0.0', 8000)>]
           │           │    └ <function Server.serve at 0x00000239986CAF20>
           │           └ <uvicorn.server.Server object at 0x000002399886C440>
           └ <function run at 0x0000023997F1C360>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\runners.py", line 195, in run
    return runner.run(main)
           │      │   └ <coroutine object Server.serve at 0x000002399883B3E0>
           │      └ <function Runner.run at 0x0000023997FB7EC0>
           └ <asyncio.runners.Runner object at 0x00000239987174A0>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           │    │     │                  └ <Task pending name='Task-1' coro=<Server.serve() running at W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-pac...
           │    │     └ <function BaseEventLoop.run_until_complete at 0x0000023997FB5B20>
           │    └ <_WindowsSelectorEventLoop running=True closed=False debug=False>
           └ <asyncio.runners.Runner object at 0x00000239987174A0>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\base_events.py", line 678, in run_until_complete
    self.run_forever()
    │    └ <function BaseEventLoop.run_forever at 0x0000023997FB5A80>
    └ <_WindowsSelectorEventLoop running=True closed=False debug=False>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\base_events.py", line 645, in run_forever
    self._run_once()
    │    └ <function BaseEventLoop._run_once at 0x0000023997FB7880>
    └ <_WindowsSelectorEventLoop running=True closed=False debug=False>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\base_events.py", line 1999, in _run_once
    handle._run()
    │      └ <function Handle._run at 0x0000023997EEDBC0>
    └ <Handle Task.task_wakeup(<Future finished result=False>)>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12026-05-15 14:08:59.301 | INFO     | logging:callHandlers:1762 - 127.0.0.1:64567 - "GET /api/v1/threads/None/messages HTTP/1.1" 422
2026-05-15 14:08:59.482 | ERROR    | app.main:global_exception_handler:38 - Unhandled Exception:
Traceback (most recent call last):

  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
    │    │       └ <function DefaultDialect.do_execute at 0x000002399AF29C60>
    │    └ <sqlalchemy.dialects.postgresql.psycopg2.PGDialect_psycopg2 object at 0x000002399CAE8A10>
    └ <sqlalchemy.engine.base.Connection object at 0x00000239EFEC3500>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    │      │       │          └ {'context_id': UUID('031cc388-4617-45a2-b73f-f20ce9bea37a'), 'book_id': UUID('fac9ca94-63ce-4ded-b61e-af804e53ca18')}
    │      │       └ 'INSERT INTO study_context_document_links (context_id, book_id) VALUES (%(context_id)s::UUID, %(book_id)s::UUID)'
    │      └ <method 'execute' of 'psycopg2.extensions.cursor' objects>
    └ <cursor object at 0x00000239EFECE7A0; closed: -1>

psycopg2.errors.ForeignKeyViolation: insert or update on table "study_context_document_links" violates foreign key constraint "study_context_document_links_book_id_fkey"
DETAIL:  Key (book_id)=(fac9ca94-63ce-4ded-b61e-af804e53ca18) is not present in table "books".



The above exception was the direct cause of the following exception:


Traceback (most recent call last):

  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\app\repositories\study_context_thread_repo.py", line 57, in get_or_create_thread_for_book_repo
    session.flush()  # To get new_thread.id populated
    │       └ <function Session.flush at 0x000002399B1F44A0>
    └ <sqlmodel.orm.session.Session object at 0x00000239EFEC3350>

  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 4331, in flush
    self._flush(objects)
    │    │      └ None
    │    └ <function Session._flush at 0x000002399B1F4680>
    └ <sqlmodel.orm.session.Session object at 0x00000239EFEC3350>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 4466, in _flush
    with util.safe_reraise():
         │    └ <class 'sqlalchemy.util.langhelpers.safe_reraise'>
         └ <module 'sqlalchemy.util' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqlalchemy\\uti...
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 121, in __exit__
    raise exc_value.with_traceback(exc_tb)
          │         │              └ <traceback object at 0x00000239EFEDECC0>
          │         └ <method 'with_traceback' of 'BaseException' objects>
          └ IntegrityError('(psycopg2.errors.ForeignKeyViolation) insert or update on table "study_context_document_links" violates forei...
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 4427, in _flush
    flush_context.execute()
    │             └ <function UOWTransaction.execute at 0x000002399B17C180>
    └ <sqlalchemy.orm.unitofwork.UOWTransaction object at 0x00000239EFC114F0>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\unitofwork.py", line 466, in execute
    rec.execute(self)
    │   │       └ <sqlalchemy.orm.unitofwork.UOWTransaction object at 0x00000239EFC114F0>
    │   └ <function SaveUpdateAll.execute at 0x000002399B17CCC0>
    └ SaveUpdateAll(Mapper[StudyContextDocumentLink(study_context_document_links)])
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\unitofwork.py", line 642, in execute
    util.preloaded.orm_persistence.save_obj(
    │    │         │               └ <function save_obj at 0x000002399B17FA60>
    │    │         └ <module 'sqlalchemy.orm.persistence' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqla...
    │    └ <module 'sqlalchemy.util.preloaded' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqlal...
    └ <module 'sqlalchemy.util' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqlalchemy\\uti...
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\persistence.py", line 93, in save_obj
    _emit_insert_statements(
    └ <function _emit_insert_statements at 0x000002399B1CDEE0>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\persistence.py", line 1048, in _emit_insert_statements
    result = connection.execute(
             │          └ <function Connection.execute at 0x0000023999E9A980>
             └ <sqlalchemy.engine.base.Connection object at 0x00000239EFEC3500>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1419, in execute
    return meth(
           └ <bound method ClauseElement._execute_on_connection of <sqlalchemy.sql.dml.Insert object at 0x00000239EFC11D30>>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 527, in _execute_on_connection
    return connection._execute_clauseelement(
           │          └ <function Connection._execute_clauseelement at 0x0000023999E9ACA0>
           └ <sqlalchemy.engine.base.Connection object at 0x00000239EFEC3500>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1641, in _execute_clauseelement
    ret = self._execute_context(
          │    └ <function Connection._execute_context at 0x0000023999E9AE80>
          └ <sqlalchemy.engine.base.Connection object at 0x00000239EFEC3500>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in _execute_context
    return self._exec_single_context(
           │    └ <function Connection._exec_single_context at 0x0000023999E9AF20>
           └ <sqlalchemy.engine.base.Connection object at 0x00000239EFEC3500>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in _exec_single_context
    self._handle_dbapi_exception(
    │    └ <function Connection._handle_dbapi_exception at 0x0000023999E9B1A0>
    └ <sqlalchemy.engine.base.Connection object at 0x00000239EFEC3500>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2363, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
          │                    │              │                 └ ForeignKeyViolation('insert or update on table "study_context_document_links" violates foreign key constraint "study_context_...
          │                    │              └ (<class 'psycopg2.errors.ForeignKeyViolation'>, ForeignKeyViolation('insert or update on table "study_context_document_links"...
          │                    └ <method 'with_traceback' of 'BaseException' objects>
          └ IntegrityError('(psycopg2.errors.ForeignKeyViolation) insert or update on table "study_context_document_links" violates forei...
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
    │    │       └ <function DefaultDialect.do_execute at 0x000002399AF29C60>
    │    └ <sqlalchemy.dialects.postgresql.psycopg2.PGDialect_psycopg2 object at 0x000002399CAE8A10>
    └ <sqlalchemy.engine.base.Connection object at 0x00000239EFEC3500>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    │      │       │          └ {'context_id': UUID('031cc388-4617-45a2-b73f-f20ce9bea37a'), 'book_id': UUID('fac9ca94-63ce-4ded-b61e-af804e53ca18')}
    │      │       └ 'INSERT INTO study_context_document_links (context_id, book_id) VALUES (%(context_id)s::UUID, %(book_id)s::UUID)'
    │      └ <method 'execute' of 'psycopg2.extensions.cursor' objects>
    └ <cursor object at 0x00000239EFECE7A0; closed: -1>

sqlalchemy.exc.IntegrityError: (psycopg2.errors.ForeignKeyViolation) insert or update on table "study_context_document_links" violates foreign key constraint "study_context_document_links_book_id_fkey"
DETAIL:  Key (book_id)=(fac9ca94-63ce-4ded-b61e-af804e53ca18) is not present in table "books".

[SQL: INSERT INTO study_context_document_links (context_id, book_id) VALUES (%(context_id)s::UUID, %(book_id)s::UUID)]
[parameters: {'context_id': UUID('031cc388-4617-45a2-b73f-f20ce9bea37a'), 'book_id': UUID('fac9ca94-63ce-4ded-b61e-af804e53ca18')}]
(Background on this error at: https://sqlalche.me/e/20/gkpj)


During handling of the above exception, another exception occurred:


Traceback (most recent call last):

  File "<string>", line 1, in <module>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\spawn.py", line 122, in spawn_main
    exitcode = _main(fd, parent_sentinel)
               │     │   └ 376
               │     └ 3
               └ <function _main at 0x00000239962FBF60>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\spawn.py", line 135, in _main
    return self._bootstrap(parent_sentinel)
           │    │          └ 376
           │    └ <function BaseProcess._bootstrap at 0x00000239961FFF60>
           └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
    │    └ <function BaseProcess.run at 0x00000239961FF4C0>
    └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    │    │        │    │        │    └ {'config': <uvicorn.config.Config object at 0x00000239962BD0D0>, 'target': <bound method Server.run of <uvicorn.server.Server...
    │    │        │    │        └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
    │    │        │    └ ()
    │    │        └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
    │    └ <function subprocess_started at 0x00000239986CBBA0>
    └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    │              └ [<socket.socket fd=812, family=2, type=1, proto=6, laddr=('0.0.0.0', 8000)>]
    └ <bound method Server.run of <uvicorn.server.Server object at 0x000002399886C440>>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\server.py", line 67, in run
    return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
           │           │    │             │                      │    │      └ <function Config.get_loop_factory at 0x0000023998680400>
           │           │    │             │                      │    └ <uvicorn.config.Config object at 0x00000239962BD0D0>
           │           │    │             │                      └ <uvicorn.server.Server object at 0x000002399886C440>
           │           │    │             └ [<socket.socket fd=812, family=2, type=1, proto=6, laddr=('0.0.0.0', 8000)>]
           │           │    └ <function Server.serve at 0x00000239986CAF20>
           │           └ <uvicorn.server.Server object at 0x000002399886C440>
           └ <function run at 0x0000023997F1C360>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\runners.py", line 195, in run
    return runner.run(main)
           │      │   └ <coroutine object Server.serve at 0x000002399883B3E0>
           │      └ <function Runner.run at 0x0000023997FB7EC0>
           └ <asyncio.runners.Runner object at 0x00000239987174A0>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           │    │     │                  └ <Task pending name='Task-1' coro=<Server.serve() running at W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-pac...
           │    │     └ <function BaseEventLoop.run_until_complete at 0x0000023997FB5B20>
           │    └ <_WindowsSelectorEventLoop running=True closed=False debug=False>
           └ <asyncio.runners.Runner object at 0x00000239987174A0>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\base_events.py", line 678, in run_until_complete
    self.run_forever()
    │    └ <function BaseEventLoop.run_forever at 0x0000023997FB5A80>
    └ <_WindowsSelectorEventLoop running=True closed=False debug=False>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\base_events.py", line 645, in run_forever
    self._run_once()
    │    └ <function BaseEventLoop._run_once at 0x0000023997FB7880>
    └ <_WindowsSelectorEventLoop running=True closed=False debug=False>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\base_events.py", line 1999, in _run_once
    handle._run()
    │      └ <function Handle._run at 0x0000023997EEDBC0>
    └ <Handle Task.task_wakeup(<Future finished res2026-05-15 14:08:59.497 | INFO     | logging:callHandlers:1762 - 127.0.0.1:64568 - "GET /api/v1/threads/for-book/fac9ca94-63ce-4ded-b61e-af804e53ca18 HTTP/1.1" 500
2026-05-15 14:08:59.497 | ERROR    | logging:callHandlers:1762 - Exception in ASGI application

Traceback (most recent call last):

  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
    │    │       └ <function DefaultDialect.do_execute at 0x000002399AF29C60>
    │    └ <sqlalchemy.dialects.postgresql.psycopg2.PGDialect_psycopg2 object at 0x000002399CAE8A10>
    └ <sqlalchemy.engine.base.Connection object at 0x00000239EFEC3500>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    │      │       │          └ {'context_id': UUID('031cc388-4617-45a2-b73f-f20ce9bea37a'), 'book_id': UUID('fac9ca94-63ce-4ded-b61e-af804e53ca18')}
    │      │       └ 'INSERT INTO study_context_document_links (context_id, book_id) VALUES (%(context_id)s::UUID, %(book_id)s::UUID)'
    │      └ <method 'execute' of 'psycopg2.extensions.cursor' objects>
    └ <cursor object at 0x00000239EFECE7A0; closed: -1>

psycopg2.errors.ForeignKeyViolation: insert or update on table "study_context_document_links" violates foreign key constraint "study_context_document_links_book_id_fkey"
DETAIL:  Key (book_id)=(fac9ca94-63ce-4ded-b61e-af804e53ca18) is not present in table "books".



The above exception was the direct cause of the following exception:


Traceback (most recent call last):

  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\app\repositories\study_context_thread_repo.py", line 57, in get_or_create_thread_for_book_repo
    session.flush()  # To get new_thread.id populated
    │       └ <function Session.flush at 0x000002399B1F44A0>
    └ <sqlmodel.orm.session.Session object at 0x00000239EFEC3350>

  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 4331, in flush
    self._flush(objects)
    │    │      └ None
    │    └ <function Session._flush at 0x000002399B1F4680>
    └ <sqlmodel.orm.session.Session object at 0x00000239EFEC3350>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 4466, in _flush
    with util.safe_reraise():
         │    └ <class 'sqlalchemy.util.langhelpers.safe_reraise'>
         └ <module 'sqlalchemy.util' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqlalchemy\\uti...
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 121, in __exit__
    raise exc_value.with_traceback(exc_tb)
          │         │              └ <traceback object at 0x00000239EFEDECC0>
          │         └ <method 'with_traceback' of 'BaseException' objects>
          └ IntegrityError('(psycopg2.errors.ForeignKeyViolation) insert or update on table "study_context_document_links" violates forei...
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\session.py", line 4427, in _flush
    flush_context.execute()
    │             └ <function UOWTransaction.execute at 0x000002399B17C180>
    └ <sqlalchemy.orm.unitofwork.UOWTransaction object at 0x00000239EFC114F0>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\unitofwork.py", line 466, in execute
    rec.execute(self)
    │   │       └ <sqlalchemy.orm.unitofwork.UOWTransaction object at 0x00000239EFC114F0>
    │   └ <function SaveUpdateAll.execute at 0x000002399B17CCC0>
    └ SaveUpdateAll(Mapper[StudyContextDocumentLink(study_context_document_links)])
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\unitofwork.py", line 642, in execute
    util.preloaded.orm_persistence.save_obj(
    │    │         │               └ <function save_obj at 0x000002399B17FA60>
    │    │         └ <module 'sqlalchemy.orm.persistence' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqla...
    │    └ <module 'sqlalchemy.util.preloaded' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqlal...
    └ <module 'sqlalchemy.util' from 'W:\\WorkSpace_IT\\_CAPSTON_PROJECT\\triam-backend\\.venv\\Lib\\site-packages\\sqlalchemy\\uti...
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\persistence.py", line 93, in save_obj
    _emit_insert_statements(
    └ <function _emit_insert_statements at 0x000002399B1CDEE0>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\orm\persistence.py", line 1048, in _emit_insert_statements
    result = connection.execute(
             │          └ <function Connection.execute at 0x0000023999E9A980>
             └ <sqlalchemy.engine.base.Connection object at 0x00000239EFEC3500>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1419, in execute
    return meth(
           └ <bound method ClauseElement._execute_on_connection of <sqlalchemy.sql.dml.Insert object at 0x00000239EFC11D30>>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 527, in _execute_on_connection
    return connection._execute_clauseelement(
           │          └ <function Connection._execute_clauseelement at 0x0000023999E9ACA0>
           └ <sqlalchemy.engine.base.Connection object at 0x00000239EFEC3500>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1641, in _execute_clauseelement
    ret = self._execute_context(
          │    └ <function Connection._execute_context at 0x0000023999E9AE80>
          └ <sqlalchemy.engine.base.Connection object at 0x00000239EFEC3500>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in _execute_context
    return self._exec_single_context(
           │    └ <function Connection._exec_single_context at 0x0000023999E9AF20>
           └ <sqlalchemy.engine.base.Connection object at 0x00000239EFEC3500>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in _exec_single_context
    self._handle_dbapi_exception(
    │    └ <function Connection._handle_dbapi_exception at 0x0000023999E9B1A0>
    └ <sqlalchemy.engine.base.Connection object at 0x00000239EFEC3500>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2363, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
          │                    │              │                 └ ForeignKeyViolation('insert or update on table "study_context_document_links" violates foreign key constraint "study_context_...
          │                    │              └ (<class 'psycopg2.errors.ForeignKeyViolation'>, ForeignKeyViolation('insert or update on table "study_context_document_links"...
          │                    └ <method 'with_traceback' of 'BaseException' objects>
          └ IntegrityError('(psycopg2.errors.ForeignKeyViolation) insert or update on table "study_context_document_links" violates forei...
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
    │    │       └ <function DefaultDialect.do_execute at 0x000002399AF29C60>
    │    └ <sqlalchemy.dialects.postgresql.psycopg2.PGDialect_psycopg2 object at 0x000002399CAE8A10>
    └ <sqlalchemy.engine.base.Connection object at 0x00000239EFEC3500>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    │      │       │          └ {'context_id': UUID('031cc388-4617-45a2-b73f-f20ce9bea37a'), 'book_id': UUID('fac9ca94-63ce-4ded-b61e-af804e53ca18')}
    │      │       └ 'INSERT INTO study_context_document_links (context_id, book_id) VALUES (%(context_id)s::UUID, %(book_id)s::UUID)'
    │      └ <method 'execute' of 'psycopg2.extensions.cursor' objects>
    └ <cursor object at 0x00000239EFECE7A0; closed: -1>

sqlalchemy.exc.IntegrityError: (psycopg2.errors.ForeignKeyViolation) insert or update on table "study_context_document_links" violates foreign key constraint "study_context_document_links_book_id_fkey"
DETAIL:  Key (book_id)=(fac9ca94-63ce-4ded-b61e-af804e53ca18) is not present in table "books".

[SQL: INSERT INTO study_context_document_links (context_id, book_id) VALUES (%(context_id)s::UUID, %(book_id)s::UUID)]
[parameters: {'context_id': UUID('031cc388-4617-45a2-b73f-f20ce9bea37a'), 'book_id': UUID('fac9ca94-63ce-4ded-b61e-af804e53ca18')}]
(Background on this error at: https://sqlalche.me/e/20/gkpj)


During handling of the above exception, another exception occurred:


Traceback (most recent call last):

  File "<string>", line 1, in <module>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\spawn.py", line 122, in spawn_main
    exitcode = _main(fd, parent_sentinel)
               │     │   └ 376
               │     └ 3
               └ <function _main at 0x00000239962FBF60>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\spawn.py", line 135, in _main
    return self._bootstrap(parent_sentinel)
           │    │          └ 376
           │    └ <function BaseProcess._bootstrap at 0x00000239961FFF60>
           └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
    │    └ <function BaseProcess.run at 0x00000239961FF4C0>
    └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    │    │        │    │        │    └ {'config': <uvicorn.config.Config object at 0x00000239962BD0D0>, 'target': <bound method Server.run of <uvicorn.server.Server...
    │    │        │    │        └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
    │    │        │    └ ()
    │    │        └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
    │    └ <function subprocess_started at 0x00000239986CBBA0>
    └ <SpawnProcess name='SpawnProcess-1' parent=17576 started>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    │              └ [<socket.socket fd=812, family=2, type=1, proto=6, laddr=('0.0.0.0', 8000)>]
    └ <bound method Server.run of <uvicorn.server.Server object at 0x000002399886C440>>
  File "W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-packages\uvicorn\server.py", line 67, in run
    return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
           │           │    │             │                      │    │      └ <function Config.get_loop_factory at 0x0000023998680400>
           │           │    │             │                      │    └ <uvicorn.config.Config object at 0x00000239962BD0D0>
           │           │    │             │                      └ <uvicorn.server.Server object at 0x000002399886C440>
           │           │    │             └ [<socket.socket fd=812, family=2, type=1, proto=6, laddr=('0.0.0.0', 8000)>]
           │           │    └ <function Server.serve at 0x00000239986CAF20>
           │           └ <uvicorn.server.Server object at 0x000002399886C440>
           └ <function run at 0x0000023997F1C360>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\runners.py", line 195, in run
    return runner.run(main)
           │      │   └ <coroutine object Server.serve at 0x000002399883B3E0>
           │      └ <function Runner.run at 0x0000023997FB7EC0>
           └ <asyncio.runners.Runner object at 0x00000239987174A0>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           │    │     │                  └ <Task pending name='Task-1' coro=<Server.serve() running at W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\.venv\Lib\site-pac...
           │    │     └ <function BaseEventLoop.run_until_complete at 0x0000023997FB5B20>
           │    └ <_WindowsSelectorEventLoop running=True closed=False debug=False>
           └ <asyncio.runners.Runner object at 0x00000239987174A0>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\base_events.py", line 678, in run_until_complete
    self.run_forever()
    │    └ <function BaseEventLoop.run_forever at 0x0000023997FB5A80>
    └ <_WindowsSelectorEventLoop running=True closed=False debug=False>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\base_events.py", line 645, in run_forever
    self._run_once()
    │    └ <function BaseEventLoop._run_once at 0x0000023997FB7880>
    └ <_WindowsSelectorEventLoop running=True closed=False debug=False>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\Lib\asyncio\base_events.py", line 1999, in _run_once
    handle._run()
    │      └ <function Handle._run at 0x0000023997EEDBC0>
    └ <Handle Task.task_wakeup(<Future finished result=False>)>
  File "C:\Users\Lenovo\AppData\Roaming\uv\python\cpython-3.1WARNING:  WatchFiles detected changes in 'tests\test_threads_for_book.py'. Reloading...
 2026-05-15 14:09:27.530 | INFO     | logging:callHandlers:1762 - Shutting down
2026-05-15 14:09:27.640 | INFO     | logging:callHandlers:1762 - Waiting for application shutdown.
2026-05-15 14:09:27.640 | INFO     | app.main:lifespan:21 - Đang dọn dẹp tài nguyên...
2026-05-15 14:09:27.641 | INFO     | logging:callHandlers:1762 - Application shutdown complete.