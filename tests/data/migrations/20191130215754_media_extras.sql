-- migrate:up

ALTER TABLE "media" ADD "name" TEXT;
ALTER TABLE "media" ADD "description" TEXT;


-- migrate:down

ALTER TABLE "media" DROP COLUMN "name";
ALTER TABLE "media" DROP COLUMN "description";
