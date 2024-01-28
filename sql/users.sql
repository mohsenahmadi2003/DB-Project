select * from users;
-- delete from bank.users;
INSERT INTO USERS (username, password, first_name, last_name, national_code, date_of_birth, address, phone_number, email, last_login, date_joined, is_superuser) 
VALUES ('admin', '123', 'Admin', 'User', '1234567890', '1990-01-01', 'Admin Address', '1234567890', 'admin@example.com', NOW(), NOW(), TRUE);
