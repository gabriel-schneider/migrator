-- migrate:up

CREATE TABLE "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "public_id" TEXT NOT NULL UNIQUE,
    "email" TEXT NOT NULL UNIQUE,
    "name" TEXT NOT NULL,
    "created_at" TEXT
);
CREATE INDEX "idx_user_public_id" ON "user" ("public_id" DESC);
CREATE INDEX "idx_user_id" ON "user" ("id" DESC);

-- migrate:down

DROP INDEX "idx_user_public_id";
DROP INDEX "idx_user_id";
DROP TABLE "user";
