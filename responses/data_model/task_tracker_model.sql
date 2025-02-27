CREATE TYPE cadence_enum AS ENUM ('DAILY', 'WEEKLY', 'MONTHLY');

CREATE TYPE occurrence_status_enum as ENUM ('NOT_STARTED', 'IN_PROGRESS', 'COMPLETED');

CREATE TABLE "Worker" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "name" varchar(255) NOT NULL,
  "active" boolean DEFAULT true,
  "created_at" timestamp DEFAULT (now())
);

COMMENT ON COLUMN "Worker"."name" IS 'Worker full name';
COMMENT ON COLUMN "Worker"."active" IS 'Whether the worker is active';

CREATE TABLE "Task" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar(255) NOT NULL,
  "cadence" cadence_enum NOT NULL,
  "occurrences" INTEGER NOT NULL,
  "initialized_at" timestamp,
  "created_at" timestamp DEFAULT (now())
);

COMMENT ON COLUMN "Task"."name" IS 'Task name';
COMMENT ON COLUMN "Task"."cadence" IS 'A task can reoccur at a cadence of daily, weekly, monthly';
COMMENT ON COLUMN "Task"."occurrences" IS 'A task will repeat at a cadence and complete after x occurrences';
COMMENT ON COLUMN "Task"."initialized_at" IS 'The task will begin on a certain date and time';

CREATE TABLE "Occurrence" (
  "id" SERIAL PRIMARY KEY,
  "task_id" INTEGER references "Task"("id"),
  "occurrence_timestamp" timestamp NOT NULL,
  "occurrence_status" occurrence_status_enum NOT NULL,
  "created_at" timestamp DEFAULT (now())
);

COMMENT ON COLUMN "Occurrence"."occurrence_timestamp" IS 'This will be populated by a script to indicate when an occurrence needs to happen';

CREATE TABLE "OccurrenceAssignment" (
    "id" SERIAL PRIMARY KEY,
	"task_worker_id" uuid references "Worker" ("id"),
    "occurrence_id" INTEGER references "Occurrence" ("id"),
	"created_at" timestamp DEFAULT (now())
);

COMMENT ON COLUMN "OccurrenceAssignment"."task_worker_id" IS 'Multiple people can work on an Occurrence';