-- migrate:up

INSERT INTO "permission" VALUES ("user.create", "Criar usuários", "");
INSERT INTO "permission" VALUES ("user.read", "Ler usuários", "");
INSERT INTO "permission" VALUES ("user.update", "Modificar usuários", "");
INSERT INTO "permission" VALUES ("user.delete", "Excluir usuários", "");

-- migrate:down

DELETE FROM "permission" WHERE id IN ("user.create", "user.read", "user.update", "user.delete");