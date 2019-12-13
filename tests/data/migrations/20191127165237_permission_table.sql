-- migrate:up

CREATE TABLE "permission" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL,
    "description" TEXT
);

CREATE INDEX "idx_permission_id" ON "permission" ("id" DESC);

-- migrate:down

DROP INDEX "idx_permission_id";
DROP TABLE "permission";
