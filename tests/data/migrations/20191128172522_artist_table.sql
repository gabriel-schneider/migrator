-- migrate:up

CREATE TABLE "artist" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "public_id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "visible" INTEGER,
    "media_id" INTEGER,
    "created_at" TEXT,
    FOREIGN KEY ("media_id") REFERENCES "media" ("id")
);

CREATE INDEX "idx_artist_id" ON "artist" ("id");
CREATE INDEX "idx_artist_public_id" ON "artist" ("public_id");

-- migrate:down

DROP INDEX "idx_artist_id";
DROP INDEX "idx_artist_public_id";
DROP TABLE "artist";