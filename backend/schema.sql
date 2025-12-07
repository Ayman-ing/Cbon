CREATE TABLE "users" (
  "id" uuid PRIMARY KEY,
  "full_name" text,
  "email" text UNIQUE,
  "password_hash" text,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "projects" (
  "id" uuid PRIMARY KEY,
  "owner_id" uuid,
  "title" text,
  "description" text,
  "status" text,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "project_members" (
  "user_id" uuid,
  "project_id" uuid,
  "role" text,
  "joined_at" timestamp,
  "primary" key(user_id,project_id)
);

CREATE TABLE "tasks" (
  "id" uuid PRIMARY KEY,
  "project_id" uuid,
  "assigned_to" uuid,
  "title" text,
  "description" text,
  "status" text,
  "priority" int,
  "due_date" date,
  "position" int,
  "created_at" timestamp,
  "updated_at" timestamp
);

ALTER TABLE "projects" ADD FOREIGN KEY ("owner_id") REFERENCES "users" ("id");

ALTER TABLE "project_members" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "project_members" ADD FOREIGN KEY ("project_id") REFERENCES "projects" ("id");

ALTER TABLE "tasks" ADD FOREIGN KEY ("project_id") REFERENCES "projects" ("id");

ALTER TABLE "tasks" ADD FOREIGN KEY ("assigned_to") REFERENCES "users" ("id");
