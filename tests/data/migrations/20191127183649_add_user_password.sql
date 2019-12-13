-- migrate:up
ALTER TABLE "user" ADD "password" TEXT;

-- migrate:down

ALTER TABLE "user" DROP "password";