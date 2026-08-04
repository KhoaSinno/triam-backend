## Table `books`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `user_id` | `uuid` |  |
| `title` | `text` |  |
| `author` | `text` |  Nullable |
| `file_url` | `text` |  Nullable |
| `document_type` | `text` |  Nullable |
| `total_sections` | `int4` |  Nullable |
| `total_units` | `int4` |  Nullable |
| `status` | `text` |  Nullable |
| `error_message` | `text` |  Nullable |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |
| `is_shared` | `bool` |  |
| `parent_shared_id` | `uuid` |  Nullable |
| `ai_summary` | `json` |  Nullable |
| `ai_summary_status` | `text` |  |
| `ai_summary_error` | `text` |  Nullable |

## Table `notification_settings`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `user_id` | `uuid` | Primary |
| `timezone` | `text` |  |
| `reminders_enabled` | `bool` |  |
| `spaced_review_enabled` | `bool` |  |
| `reminder_time` | `text` |  |
| `quiet_hours_start` | `text` |  |
| `quiet_hours_end` | `text` |  |
| `daily_cap` | `int4` |  |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Table `notification_outbox`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `user_id` | `uuid` |  |
| `type` | `notificationtype` |  |
| `channel` | `notificationchannel` |  |
| `status` | `notificationstatus` |  |
| `payload` | `jsonb` |  |
| `due_at` | `timestamptz` |  |
| `next_retry_at` | `timestamptz` |  Nullable |
| `locked_at` | `timestamptz` |  Nullable |
| `locked_by` | `text` |  Nullable |
| `sent_at` | `timestamptz` |  Nullable |
| `attempts` | `int4` |  |
| `error_message` | `text` |  Nullable |
| `idempotency_key` | `text` |  Unique |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Table `user_device_tokens`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `user_id` | `uuid` |  |
| `device_token` | `text` |  |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Table `study_contexts`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `user_id` | `uuid` |  |
| `title` | `text` |  |
| `is_auto_generated` | `bool` |  |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Table `study_context_document_links`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `context_id` | `uuid` | Primary |
| `book_id` | `uuid` | Primary |

## Table `reading_plans`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `book_id` | `uuid` |  |
| `mode` | `planmode` |  |
| `pace` | `int4` |  |
| `status` | `text` |  |
| `reminder_time` | `text` |  |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |
| `started_at` | `timestamptz` |  Nullable |
| `paused_at` | `timestamptz` |  Nullable |
| `completed_at` | `timestamptz` |  Nullable |

## Table `processing_jobs`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `user_id` | `uuid` |  |
| `book_id` | `uuid` |  Nullable |
| `job_type` | `processingjobtype` |  |
| `status` | `processingjobstatus` |  |
| `mode` | `planmode` |  Nullable |
| `progress_percent` | `int4` |  |
| `current_step` | `text` |  Nullable |
| `total_units` | `int4` |  |
| `done_units` | `int4` |  |
| `failed_units` | `int4` |  |
| `estimated_input_tokens` | `int4` |  Nullable |
| `estimated_audio_seconds` | `int4` |  Nullable |
| `error_message` | `text` |  Nullable |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |
| `started_at` | `timestamptz` |  Nullable |
| `finished_at` | `timestamptz` |  Nullable |

## Table `book_sections`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `book_id` | `uuid` |  |
| `parent_id` | `uuid` |  Nullable |
| `section_index` | `int4` |  |
| `title` | `text` |  |
| `level` | `int4` |  |
| `path` | `text` |  |
| `text_content` | `text` |  Nullable |
| `text_char_count` | `int4` |  |
| `page_start` | `int4` |  Nullable |
| `page_end` | `int4` |  Nullable |
| `source_href` | `text` |  Nullable |
| `source_anchor` | `text` |  Nullable |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Table `learning_units`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `user_id` | `uuid` |  |
| `book_id` | `uuid` |  |
| `mode` | `planmode` |  |
| `unit_index` | `int4` |  |
| `title` | `text` |  |
| `unit_type` | `text` |  |
| `status` | `processingjobstatus` |  |
| `source_text_char_count` | `int4` |  |
| `estimated_tokens` | `int4` |  |
| `estimated_audio_seconds` | `int4` |  |
| `main_segment_count` | `int4` |  |
| `review_audio_url` | `text` |  Nullable |
| `review_text` | `text` |  Nullable |
| `planner_reason` | `text` |  Nullable |
| `error_message` | `text` |  Nullable |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |
| `started_at` | `timestamptz` |  Nullable |
| `finished_at` | `timestamptz` |  Nullable |

## Table `user_notifications`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `user_id` | `uuid` |  |
| `outbox_id` | `uuid` |  Nullable Unique |
| `type` | `notificationtype` |  |
| `title` | `text` |  |
| `body` | `text` |  |
| `action_type` | `text` |  Nullable |
| `action_payload` | `jsonb` |  Nullable |
| `read_at` | `timestamptz` |  Nullable |
| `created_at` | `timestamptz` |  |

## Table `chat_threads`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `context_id` | `uuid` |  |
| `title` | `text` |  |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Table `reading_plan_schedule_slots`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `user_id` | `uuid` |  |
| `plan_id` | `uuid` |  |
| `book_id` | `uuid` |  |
| `weekday` | `int4` |  |
| `reminder_time` | `text` |  |
| `timezone` | `text` |  |
| `is_active` | `bool` |  |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Table `learning_unit_sources`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `learning_unit_id` | `uuid` | Primary |
| `section_id` | `uuid` | Primary |
| `source_order` | `int4` |  |

## Table `learning_unit_segments`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `int4` | Primary |
| `learning_unit_id` | `uuid` |  |
| `segment_index` | `int4` |  |
| `audio_url` | `text` |  Nullable |
| `text_content` | `text` |  Nullable |
| `duration_ms` | `int4` |  Nullable |
| `created_at` | `timestamptz` |  |

## Table `chat_messages`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `thread_id` | `uuid` |  |
| `is_user` | `bool` |  |
| `text` | `text` |  |
| `source` | `text` |  |
| `timestamp` | `timestamptz` |  |

## Table `direct_book_context`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `user_id` | `uuid` | Primary |
| `book_id` | `uuid` | Primary |
| `context_id` | `uuid` |  |
| `primary_thread_id` | `uuid` |  |

## Table `learning_unit_progress`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `user_id` | `uuid` |  |
| `book_id` | `uuid` |  |
| `learning_unit_id` | `uuid` |  |
| `mode` | `planmode` |  |
| `current_segment_id` | `int4` |  Nullable |
| `last_segment_index` | `int4` |  |
| `position_ms` | `int4` |  |
| `listened_ms` | `int4` |  |
| `total_duration_ms` | `int4` |  |
| `progress_percent` | `int4` |  |
| `max_progress_percent` | `int4` |  |
| `status` | `learningprogressstatus` |  |
| `started_at` | `timestamptz` |  Nullable |
| `last_activity_at` | `timestamptz` |  Nullable |
| `completed_at` | `timestamptz` |  Nullable |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Table `spaced_review_items`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `user_id` | `uuid` |  |
| `book_id` | `uuid` |  |
| `learning_unit_id` | `uuid` |  Nullable |
| `mode` | `planmode` |  |
| `interval_days` | `int4` |  |
| `sequence_index` | `int4` |  |
| `due_at` | `timestamptz` |  |
| `status` | `reviewitemstatus` |  |
| `review_text_snapshot` | `text` |  Nullable |
| `anchor_completed_at` | `timestamptz` |  Nullable |
| `source_unit_progress_id` | `uuid` |  Nullable |
| `notified_at` | `timestamptz` |  Nullable |
| `last_reviewed_at` | `timestamptz` |  Nullable |
| `completed_at` | `timestamptz` |  Nullable |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Table `alembic_version`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `version_num` | `varchar` | Primary |

## Table `admin_users`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `user_id` | `uuid` | Primary |
| `role` | `text` |  |
| `is_active` | `bool` |  |
| `note` | `text` |  Nullable |
| `created_by` | `uuid` |  Nullable |
| `revoked_by` | `uuid` |  Nullable |
| `created_at` | `timestamptz` |  |
| `revoked_at` | `timestamptz` |  Nullable |

## Table `admin_audit_logs`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `admin_user_id` | `uuid` |  |
| `action` | `text` |  |
| `target_type` | `text` |  Nullable |
| `target_id` | `uuid` |  Nullable |
| `metadata` | `jsonb` |  Nullable |
| `created_at` | `timestamptz` |  |

## Table `book_section_knowledge`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `int4` | Primary |
| `book_id` | `uuid` |  |
| `section_id` | `uuid` |  |
| `chunk_index` | `int4` |  |
| `content` | `text` |  |
| `content_hash` | `text` |  |
| `embedding_model` | `text` |  |
| `embedding_version` | `text` |  |
| `char_count` | `int4` |  |
| `token_count` | `int4` |  Nullable |
| `embedding` | `vector` |  Nullable |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |
| `search_text` | `text` |  |

## Table `book_learning_states`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `user_id` | `uuid` |  |
| `book_id` | `uuid` |  |
| `mode` | `planmode` |  |
| `status` | `text` |  |
| `book_progress_percent` | `int4` |  |
| `completed_units` | `int4` |  |
| `playable_units` | `int4` |  |
| `last_learning_unit_id` | `uuid` |  Nullable |
| `last_segment_id` | `int4` |  Nullable |
| `last_segment_index` | `int4` |  Nullable |
| `position_ms` | `int4` |  |
| `started_at` | `timestamptz` |  Nullable |
| `last_activity_at` | `timestamptz` |  Nullable |
| `completed_at` | `timestamptz` |  Nullable |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Table `reading_plan_sessions`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `user_id` | `uuid` |  |
| `plan_id` | `uuid` |  |
| `book_id` | `uuid` |  |
| `mode` | `planmode` |  |
| `session_index` | `int4` |  |
| `scheduled_at` | `timestamptz` |  |
| `local_date` | `text` |  |
| `reminder_time` | `text` |  |
| `timezone` | `text` |  |
| `status` | `text` |  |
| `completed_units` | `int4` |  |
| `total_units` | `int4` |  |
| `started_at` | `timestamptz` |  Nullable |
| `completed_at` | `timestamptz` |  Nullable |
| `skipped_at` | `timestamptz` |  Nullable |
| `missed_at` | `timestamptz` |  Nullable |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |
| `missed_notified_at` | `timestamptz` |  Nullable |

## Table `reading_plan_session_units`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `session_id` | `uuid` |  |
| `plan_id` | `uuid` |  |
| `book_id` | `uuid` |  |
| `learning_unit_id` | `uuid` |  |
| `unit_order` | `int4` |  |
| `status` | `text` |  |
| `completed_at` | `timestamptz` |  Nullable |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |

## Custom Types / Enums

### `planmode`

`FULL` | `PARETO`

### `processingjobtype`

`UPLOAD` | `GENERATE_PLAN` | `SWITCH_MODE` | `NOTIFICATION` | `REVIEW`

### `processingjobstatus`

`QUEUED` | `PROCESSING` | `PARTIAL_READY` | `READY` | `ERROR` | `CANCELLED`

### `learningprogressstatus`

`NOT_STARTED` | `IN_PROGRESS` | `COMPLETED`

### `reviewitemstatus`

`PENDING` | `DUE` | `COMPLETED` | `SKIPPED` | `CANCELLED`

### `notificationtype`

`PLAN_REMINDER` | `CONTENT_READY` | `SPACED_REVIEW_DUE`

### `notificationchannel`

`IN_APP` | `PUSH` | `ALL`

### `notificationstatus`

`PENDING` | `PROCESSING` | `SENT` | `FAILED` | `CANCELLED` | `SKIPPED`

## RLS Policies

### `books`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can read own books` | SELECT | authenticated | PERMISSIVE | `(user_id = ( SELECT auth.uid() AS uid))` | — |
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `study_contexts`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can read own study contexts` | SELECT | authenticated | PERMISSIVE | `(user_id = ( SELECT auth.uid() AS uid))` | — |
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `study_context_document_links`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can read own study context document links` | SELECT | authenticated | PERMISSIVE | `(EXISTS ( SELECT 1    FROM study_contexts sc   WHERE ((sc.id = study_context_document_links.context_id) AND (sc.user_id = ( SELECT auth.uid() AS uid)))))` | — |
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `direct_book_context`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can read own direct book contexts` | SELECT | authenticated | PERMISSIVE | `(user_id = ( SELECT auth.uid() AS uid))` | — |
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `alembic_version`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `book_learning_states`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `book_sections`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can read own book sections` | SELECT | authenticated | PERMISSIVE | `(EXISTS ( SELECT 1    FROM books b   WHERE ((b.id = book_sections.book_id) AND (b.user_id = ( SELECT auth.uid() AS uid)))))` | — |
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `learning_units`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can read own learning units` | SELECT | authenticated | PERMISSIVE | `(user_id = ( SELECT auth.uid() AS uid))` | — |
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `learning_unit_segments`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can read own learning unit segments` | SELECT | authenticated | PERMISSIVE | `(EXISTS ( SELECT 1    FROM learning_units lu   WHERE ((lu.id = learning_unit_segments.learning_unit_id) AND (lu.user_id = ( SELECT auth.uid() AS uid)))))` | — |
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `reading_plans`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can read own reading plans` | SELECT | authenticated | PERMISSIVE | `(EXISTS ( SELECT 1    FROM books b   WHERE ((b.id = reading_plans.book_id) AND (b.user_id = ( SELECT auth.uid() AS uid)))))` | — |
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `reading_plan_schedule_slots`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can read own reading plan slots` | SELECT | authenticated | PERMISSIVE | `(user_id = ( SELECT auth.uid() AS uid))` | — |
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `learning_unit_progress`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can read own learning progress` | SELECT | authenticated | PERMISSIVE | `(user_id = ( SELECT auth.uid() AS uid))` | — |
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `user_notifications`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can read own notifications` | SELECT | authenticated | PERMISSIVE | `(user_id = ( SELECT auth.uid() AS uid))` | — |
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `notification_settings`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can read own notification settings` | SELECT | authenticated | PERMISSIVE | `(user_id = ( SELECT auth.uid() AS uid))` | — |
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `chat_threads`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can read own context threads` | SELECT | authenticated | PERMISSIVE | `(EXISTS ( SELECT 1    FROM study_contexts sc   WHERE ((sc.id = chat_threads.context_id) AND (sc.user_id = ( SELECT auth.uid() AS uid)))))` | — |
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `chat_messages`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Users can read own context messages` | SELECT | authenticated | PERMISSIVE | `(EXISTS ( SELECT 1    FROM (chat_threads ct      JOIN study_contexts sc ON ((sc.id = ct.context_id)))   WHERE ((ct.id = chat_messages.thread_id) AND (sc.user_id = ( SELECT auth.uid() AS uid)))))` | — |
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `user_device_tokens`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `learning_unit_sources`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `spaced_review_items`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `processing_jobs`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `notification_outbox`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `reading_plan_sessions`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `reading_plan_session_units`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `admin_users`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `admin_audit_logs`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

### `book_section_knowledge`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Allow service_role full access` | ALL | service_role | PERMISSIVE | `true` | `true` |

