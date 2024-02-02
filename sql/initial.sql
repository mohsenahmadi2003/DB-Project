-- drop database bank;
-- create database bank;
-- use bank;

CREATE TABLE `USERS` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(32) UNIQUE,
    password VARCHAR(64),
    first_name VARCHAR(32),
    last_name VARCHAR(32),
    national_code VARCHAR(10),
    date_of_birth DATE,
    address VARCHAR(255),
    phone_number VARCHAR(20) UNIQUE,
    email VARCHAR(32) UNIQUE,
    last_login TIMESTAMP,
    date_joined TIMESTAMP,
    is_superuser BOOLEAN
);



CREATE TABLE `BANK_ACCOUNT` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    account_number VARCHAR(20) UNIQUE,
    primary_password VARCHAR(4),
    amount NUMERIC(20,2),
    rate NUMERIC(10,2),
    date_opened TIMESTAMP,
    date_closed TIMESTAMP,
    account_status BOOLEAN,
    description VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES USERS(id)
);


CREATE TABLE `LOAN` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    account_number VARCHAR(20),
    loan_amount NUMERIC(20,2),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    loan_status BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES USERS(id),
    FOREIGN KEY (account_number) REFERENCES BANK_ACCOUNT(account_number)
);


CREATE TABLE `LOAN_PAYMENT` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    loan_id INT,
    paid_amount NUMERIC(10, 2),
    paid_date TIMESTAMP,
    status BOOLEAN,
    count_of_payment TINYINT,
    FOREIGN KEY (loan_id) REFERENCES LOAN(id)
);


CREATE TABLE `TRANSACTION` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_account_number VARCHAR(20),
    destination_account_number VARCHAR(20),
    amount NUMERIC(10, 2),
    current_balance NUMERIC(20, 2),
    transaction_date TIMESTAMP,
    status VARCHAR(10),
    description VARCHAR(255),
    FOREIGN KEY (source_account_number) REFERENCES BANK_ACCOUNT(account_number),
    FOREIGN KEY (destination_account_number) REFERENCES BANK_ACCOUNT(account_number)
);

CREATE TABLE `SECONDARY_PASSWORDS` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bank_account_number VARCHAR(20),
    transaction_id INT,
    secondary_password VARCHAR(8),
    expire_time TIMESTAMP,
    UNIQUE (bank_account_number, transaction_id),
    FOREIGN KEY (bank_account_number) REFERENCES BANK_ACCOUNT(account_number),
    FOREIGN KEY (transaction_id) REFERENCES TRANSACTION(id)
);



-- ALTER TABLE `BANK_ACCOUNT` ADD FOREIGN KEY (`user_id`) REFERENCES `USERS` (`id`);

-- ALTER TABLE `LOAN` ADD FOREIGN KEY (`account_number`) REFERENCES `BANK_ACCOUNT` (`account_number`);

-- ALTER TABLE `LOAN` ADD FOREIGN KEY (`user_id`) REFERENCES `USERS` (`id`);

-- ALTER TABLE `LOAN_PAYMENT` ADD FOREIGN KEY (`loan_id`) REFERENCES `LOAN` (`id`);

-- ALTER TABLE `TRANSACTION` ADD FOREIGN KEY (`source_account_number`) REFERENCES `BANK_ACCOUNT` (`account_number`);

-- ALTER TABLE `TRANSACTION` ADD FOREIGN KEY (`destination_account_number`) REFERENCES `BANK_ACCOUNT` (`account_number`);

