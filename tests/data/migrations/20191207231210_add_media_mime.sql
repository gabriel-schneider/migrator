-- migrate:up
ALTER TABLE "media" ADD "mime_type" TEXT;

-- migrate:down
ALTER TABLE "media" DROP COLUMN "mime_type";
