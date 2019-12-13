-- migrate:up

CREATE TABLE "media" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "public_id" TEXT NOT NULL,
    "filename" TEXT NOT NULL,
    "width" INTEGER,
    "height" INTEGER,
    "size" INTEGER
);

CREATE INDEX "idx_media_id" ON "media" ("id" DESC);
CREATE INDEX "idx_media_public_id" ON "media" ("public_id" DESC);

-- migrate:down

DROP INDEX "idx_media_id";
DROP INDEX "idx_media_public_id";
DROP INDEX "media";
