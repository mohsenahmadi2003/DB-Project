select * from users;
-- delete from bank.users;
INSERT INTO USERS (username, password, first_name, last_name, national_code, date_of_birth, address, phone_number, email, last_login, date_joined, is_superuser) 
VALUES ('admin', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'Admin', 'User', '1234567890', '1990-01-01', 'Admin Address', '1234567890', 'admin@example.com', NOW(), NOW(), TRUE);
