-- migrate:up
CREATE TABLE "users_permissions" (
    "user_id" INTEGER NOT NULL,
    "permission_id" TEXT NOT NULL,
    PRIMARY KEY ("user_id", "permission_id"),
    FOREIGN KEY ("user_id") REFERENCES "user" ("id"),
    FOREIGN KEY ("permission_id") REFERENCES "permission" ("id")
);

CREATE INDEX "idx_users_permissions_user_id_permission_id" ON "users_permissions" ("user_id", "permission_id" DESC);
CREATE INDEX "idx_users_permissions_permission_id" ON "users_permissions" ("permission_id" DESC);

-- migrate:down

DROP TABLE "users_permissions";
