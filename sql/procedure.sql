DELIMITER //
-- Procedure for UpdatePassword
CREATE PROCEDURE UpdatePassword(IN userId INT, IN prevPassword VARCHAR(64), IN newPassword VARCHAR(64))
BEGIN
    DECLARE existingPassword VARCHAR(64);

    -- بررسی صحت رمز عبور قبلی
    SELECT password INTO existingPassword FROM USERS WHERE id = userId;

    IF existingPassword IS NOT NULL THEN
        IF existingPassword = prevPassword THEN
            -- آپدیت رمز عبور جدید
            UPDATE USERS SET password = newPassword WHERE id = userId;
            SELECT "رمز عبور با موفقیت به روز رسانی شد." AS Message, 1 AS Result;

        ELSE
            SELECT "رمز عبور فعلی اشتباه است." AS Message, 0 AS Result;
        END IF;
    ELSE
        SELECT "کاربری با این شناسه وجود ندارد." AS Message, 0 AS Result;
    END IF;
END//

DELIMITER ;


DELIMITER //

CREATE PROCEDURE LoginUser(IN p_username VARCHAR(32), IN p_password VARCHAR(64))
BEGIN
    DECLARE v_user_count INT;
    DECLARE v_email VARCHAR(32);
    DECLARE v_username VARCHAR(32);
    DECLARE v_first_name VARCHAR(32);
    DECLARE v_last_name VARCHAR(32);
    DECLARE v_id INT;

    SELECT COUNT(*), id, email, username, first_name, last_name
    INTO v_user_count, v_id, v_email, v_username, v_first_name, v_last_name
    FROM USERS
    WHERE username = p_username
      AND password = p_password;

    IF v_user_count > 0 THEN
        SELECT 1            AS result,
               v_id         as id,
               v_email      AS email,
               v_username   AS username,
               v_first_name AS first_name,
               v_last_name  AS last_name;
    ELSE
        SELECT 0 AS result;
    END IF;
END //

DELIMITER ;


DELIMITER //
-- GetUserBankAccounts PROCEDURE
CREATE PROCEDURE GetUserBankAccounts(IN user_id_input INT)
BEGIN
    DECLARE user_exists INT;

    -- بررسی وجود کاربر با شناسه داده شده
    SELECT COUNT(*) INTO user_exists FROM USERS WHERE id = user_id_input;

    -- اگر کاربر وجود نداشته باشد، خطا برگردانید
    IF user_exists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid user ID.';
    ELSE
        -- اگر کاربر وجود داشته باشد، اطلاعات حساب‌های کاربر را برگردانید
        SELECT id,
               user_id,
               account_number,
               primary_password,
               amount,
               date_opened,
               date_closed,
               account_status,
               description
        FROM BANK_ACCOUNT
        WHERE user_id = user_id_input;
    END IF;
END //

DELIMITER ;


DELIMITER //
-- PROCEDURE BlockBankAccount
CREATE PROCEDURE BlockBankAccount(
    IN account_number_input VARCHAR(20),
    IN description_input VARCHAR(255)
)
BEGIN
    DECLARE account_exists INT;

    -- شروع ترانزاکشن
    START TRANSACTION;

    -- بررسی وجود حساب بانکی با شماره حساب ورودی
    SELECT COUNT(*) INTO account_exists FROM BANK_ACCOUNT WHERE account_number = account_number_input;

    IF account_exists > 0 AND description_input IS NOT NULL THEN
        -- وضعیت حساب را به مسدود شده تغییر می‌دهیم
        UPDATE BANK_ACCOUNT
        SET account_status = TRUE,
            description    = description_input,
            date_closed    = NOW()
        WHERE account_number = account_number_input;
        SELECT 'موفقیت امیز' AS Message, 1 AS Result;
        -- تایید ترانزاکشن در صورت موفقیت
        COMMIT;
    ELSE
        -- لغو ترانزاکشن در صورت عدم وجود حساب
        ROLLBACK;
        SELECT 'حساب با شماره وارد شده یافت نشد' AS Message, 0 AS Result;
    END IF;

END //

DELIMITER ;

DELIMITER //
-- PROCEDURE GetAccountOwnerName
CREATE PROCEDURE GetAccountOwnerName(
    IN account_number_input VARCHAR(20)
)
BEGIN
    DECLARE user_exists INT;
    DECLARE first_name_output VARCHAR(255);
    DECLARE last_name_output VARCHAR(255);
    DECLARE username_output VARCHAR(255);

    -- بررسی وجود کاربر با شماره حساب ورودی
    SELECT COUNT(*) INTO user_exists FROM BANK_ACCOUNT WHERE account_number = account_number_input;

    IF user_exists > 0 THEN
        SELECT u.first_name, u.last_name, u.username
        INTO first_name_output, last_name_output, username_output
        FROM BANK_ACCOUNT AS b
                 INNER JOIN USERS AS u ON b.user_id = u.id
        WHERE b.account_number = account_number_input;

        SELECT 1 AS Message, first_name_output, last_name_output, username_output;
    ELSE
        SELECT 0 AS Messsage;
    END IF;
END //

DELIMITER ;


DELIMITER //
CREATE PROCEDURE GetRecentTransactionsByUser(
    IN account_number_input VARCHAR(20),
    IN transaction_count INT
)
BEGIN
    DECLARE _user_id INT;

    -- یافتن شناسه‌ی کاربر بر اساس شماره حساب ورودی
    SELECT user_id INTO _user_id FROM BANK_ACCOUNT WHERE account_number = account_number_input;

    IF _user_id IS NOT NULL THEN
        -- بازیابی تراکنش‌های اخیر کاربر
        SELECT 1       AS Message,
               id,
               source_account_number,
               destination_account_number,
               amount,
               transaction_date,
               status,
               description,
               CASE
                   WHEN source_account_number = account_number_input THEN 'Withdraw'
                   ELSE 'Deposit'
                   END AS transaction_type
        FROM TRANSACTION AS t
        WHERE t.source_account_number = account_number_input
           OR t.destination_account_number = account_number_input
        ORDER BY t.transaction_date DESC
        LIMIT transaction_count;
    ELSE
        SELECT 0 AS Message;
    END IF;
END //
DELIMITER ;


DELIMITER //

CREATE PROCEDURE CalculateAccountBalance(
    IN account_number VARCHAR(20),
    IN start_date TIMESTAMP,
    IN end_date TIMESTAMP
)
BEGIN
    DECLARE balance NUMERIC(20, 2);
    -- Check if start_date is less than end_date and both are of type TIMESTAMP
    IF start_date <= end_date THEN

        -- Calculate balance changes during the specified period and display transactions
        SELECT 1       AS Status,
               source_account_number,
               destination_account_number,
               amount,
               transaction_date,
               status,
               description,
               CASE
                   WHEN source_account_number = account_number AND source_account_balance IS NOT NULL
                       THEN source_account_balance
                   WHEN destination_account_number = account_number AND
                        transaction.destination_account_balance IS NOT NULL THEN destination_account_balance
                   END AS new_balance,
               CASE
                   WHEN source_account_number = account_number THEN 'Withdraw'
                   ELSE 'Deposit'
                   END AS transaction_type
        FROM `TRANSACTION`
        WHERE (source_account_number = account_number OR destination_account_number = account_number)
          AND transaction_date BETWEEN start_date AND end_date
        ORDER BY transaction_date ASC;
    ELSE
        SELECT 0 AS Status, 'تاریخ ها اشتباه وارد شده اند' AS Message;
    END IF;

END //

DELIMITER ;


DELIMITER //
-- PROCEDURE for Process_Transaction
CREATE PROCEDURE `Process_Transaction`(
    IN source_account_number_input VARCHAR(20),
    IN destination_account_number_input VARCHAR(20),
    IN amount_input NUMERIC(10, 2),
    IN description_input VARCHAR(255))
BEGIN
    DECLARE _transaction_id INT;
    DECLARE _transaction_date TIMESTAMP;
    DECLARE rollback_required BOOLEAN DEFAULT FALSE;

    -- Declare continue handler for any exception
    DECLARE CONTINUE
        HANDLER FOR SQLEXCEPTION
        BEGIN
            SET rollback_required = TRUE;
        END;

    -- Start the transaction

    START TRANSACTION;

    SET _transaction_date = NOW();
-- Insert transaction record
    INSERT INTO TRANSACTION (source_account_number, destination_account_number, amount, transaction_date, status,
                             description)
    VALUES (source_account_number_input, destination_account_number_input, amount_input, _transaction_date,
            'Pending',
            description_input);

    -- Get the transaction id
    SET @_transaction_id = LAST_INSERT_ID();

    /*    SELECT id
        INTO _transaction_id
        FROM TRANSACTION
        WHERE source_account_number = source_account_number_input
          AND destination_account_number = destination_account_number_input
          AND amount = amount_input
          AND transaction_date = _transaction_date
          AND status = 'Pending'
          AND description = description_input
        LIMIT 1;*/

-- Check if rollback is required
    IF rollback_required THEN
        -- Transaction failed
        ROLLBACK;
        SELECT '0' AS Message;
    ELSE
        -- Commit the transaction
        COMMIT;
-- Transaction processed successfully
        SELECT '1' AS Message, _transaction_id as transaction_id;

    END IF;
END//

DELIMITER ;


DELIMITER //

CREATE PROCEDURE TransferFunds(
    IN source_account_number VARCHAR(20),
    IN destination_account_number VARCHAR(20),
    IN transfer_amount NUMERIC(10, 2),
    IN t_id INT
)
BEGIN
    DECLARE source_balance NUMERIC(20, 2);
    DECLARE destination_balance NUMERIC(20, 2);

    -- Start transaction
    START TRANSACTION;

    -- Check if the source account has sufficient balance
    SELECT amount INTO source_balance FROM BANK_ACCOUNT WHERE account_number = source_account_number;
    IF source_balance < transfer_amount THEN
        ROLLBACK;
        SELECT 0 AS Mesagge;

    ELSE
        -- Deduct amount from source account
        UPDATE BANK_ACCOUNT
        SET amount = amount - transfer_amount
        WHERE account_number = source_account_number;

        -- Add amount to destination account
        UPDATE BANK_ACCOUNT
        SET amount = amount + transfer_amount
        WHERE account_number = destination_account_number;

        SELECT amount INTO destination_balance FROM BANK_ACCOUNT WHERE account_number = destination_account_number;

        SET source_balance = source_balance - transfer_amount;
        SET destination_balance = destination_balance + transfer_amount;


        UPDATE TRANSACTION
        SET status                      = 'Completed',
            source_account_balance      = source_balance,
            destination_account_balance = destination_balance
        WHERE id = t_id;

        -- Commit transaction
        COMMIT;

        SELECT 1 AS Mesagge;
    END IF;

END //
DELIMITER ;


DELIMITER //

-- PROCEDURE for SecondaryPassword
CREATE PROCEDURE `SecondaryPassword`(
    IN t_id INT,
    IN source_account_number_input VARCHAR(20)
)
BEGIN
    DECLARE _secondary_password VARCHAR(8);
    DECLARE rollback_required BOOLEAN DEFAULT FALSE;
    DECLARE _transaction_id INT;
    DECLARE exist_transaction INT;
    DECLARE exist_secondary_password INT;

    -- Declare continue handler for any exception
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            SET rollback_required = TRUE;
        END;

    -- Start the transaction

    START TRANSACTION;

    SELECT CASE
               WHEN EXISTS (SELECT id FROM TRANSACTION WHERE id = t_id) THEN 1
               ELSE 0
               END AS exist_transaction
    INTO exist_transaction;

    SELECT CASE
               WHEN EXISTS (SELECT transaction_id FROM SECONDARY_PASSWORDS WHERE transaction_id = t_id) THEN 1
               ELSE 0
               END AS exist_secondary_password
    INTO exist_secondary_password;

    SET _secondary_password = LPAD(FLOOR(RAND() * POW(10, 8)), 8, '0');

    IF exist_transaction = 1 THEN
        IF exist_secondary_password = 1 THEN
            UPDATE SECONDARY_PASSWORDS
            SET secondary_password = _secondary_password,
                expire_time        = NOW() + INTERVAL 60 SECOND
            WHERE transaction_id = t_id;
        ELSE
            INSERT INTO SECONDARY_PASSWORDS (bank_account_number, transaction_id, secondary_password, expire_time)
            VALUES (source_account_number_input, t_id, _secondary_password, NOW() + INTERVAL 60 SECOND);

        END IF;

        SET _transaction_id = t_id;

    ELSE
        ROLLBACK;
        SELECT '0' AS Message;
    END IF;

    -- Check if rollback is required
    IF rollback_required THEN
        -- Transaction failed
        ROLLBACK;
        SELECT '0' AS Message;
    ELSE
        -- Commit the transaction
        COMMIT;

        SELECT '1' AS Message, _secondary_password as password;

    END IF;

END//

DELIMITER ;

DELIMITER //
-- PROCEDURE for Cancel_Process_Transaction
CREATE PROCEDURE `Cancel_Process_Transaction`(
    IN t_id INT,
    IN input_source_account_number VARCHAR(20),
    IN input_destination_account_number VARCHAR(20))
BEGIN
    DECLARE exist_transaction INT;
    DECLARE source_balance NUMERIC(10, 2);
    DECLARE destination_balance NUMERIC(10, 2);
    DECLARE rollback_required BOOLEAN DEFAULT FALSE;

    -- Declare continue handler for any exception
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            SET rollback_required = TRUE;
        END;

    -- Start the transaction

    START TRANSACTION;

    -- Check if the transaction exists
    SELECT CASE
               WHEN EXISTS (SELECT id FROM `transaction` WHERE id = t_id) THEN 1
               ELSE 0
               END
    INTO exist_transaction;

    IF exist_transaction = 1 THEN
        -- Update transaction status
        SELECT amount
        INTO source_balance
        from bank_account
        where account_number = input_source_account_number;

        SELECT amount
        INTO destination_balance
        from bank_account
        where account_number = input_destination_account_number;

        UPDATE `transaction`
        SET status                      = 'Failed',
            source_account_balance      = source_balance,
            destination_account_balance = destination_balance
        WHERE id = t_id;
    ELSE
        -- Rollback if transaction doesn't exist
        ROLLBACK;
        SELECT '0' AS Message;
    END IF;

    -- Check if rollback is required
    IF rollback_required THEN
        -- Transaction failed
        ROLLBACK;
        SELECT '0' AS Message;
    ELSE
        -- Commit the transaction
        COMMIT;
        -- Transaction processed successfully
        SELECT '1' AS Message;
    END IF;
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE InsertLoanAndPayments(
    IN input_user_id INT,
    IN input_account_number VARCHAR(20),
    IN input_loan_amount NUMERIC(20, 2)
)
BEGIN
    DECLARE bank_interest_rate DECIMAL(5, 2);
    DECLARE total_loan_amount NUMERIC(20, 2);
    DECLARE balance NUMERIC(20, 2);
    DECLARE monthly_payment_amount NUMERIC(10, 2);
    DECLARE start_date TIMESTAMP;
    DECLARE end_date TIMESTAMP;
    DECLARE i INT DEFAULT 1;

    -- Declare rollback_required variable
    DECLARE rollback_required BOOLEAN DEFAULT FALSE;


    -- Declare continue handler for any exception
    DECLARE CONTINUE
        HANDLER FOR SQLEXCEPTION
        BEGIN
            SET rollback_required = TRUE;
        END;

    -- Start the transaction
    START TRANSACTION;

    -- Calculate bank interest rate (20%)
    SET bank_interest_rate = 0.2;

    -- Calculate total loan amount
    SET total_loan_amount = input_loan_amount + (input_loan_amount * bank_interest_rate);

    -- Calculate monthly payment amount
    SET monthly_payment_amount = total_loan_amount / 12;

    -- Get start and end date for loan
    SET start_date = NOW();
    SET end_date = DATE_ADD(start_date, INTERVAL 1 YEAR);

    -- Insert loan record
    INSERT INTO LOAN (user_id, account_number, loan_amount, start_date, end_date, loan_status)
    VALUES (input_user_id, input_account_number, input_loan_amount, start_date, end_date, 1);

    -- Get the id of the inserted loan
    SET @loan_id = LAST_INSERT_ID();

    -- Insert loan payments for 12 months
    WHILE i <= 12
        DO
            INSERT INTO LOAN_PAYMENT (loan_id, paid_amount, paid_date, status)
            VALUES (@loan_id, monthly_payment_amount, DATE_ADD(start_date, INTERVAL i MONTH), 0);
            SET i = i + 1;
        END WHILE;

    UPDATE BANK_ACCOUNT
    SET amount = amount + input_loan_amount
    WHERE account_number = input_account_number;

    SELECT amount
    INTO balance
    FROM BANK_ACCOUNT
    WHERE account_number = input_account_number;

    -- Insert transaction record for the loan deposit
    INSERT INTO TRANSACTION (source_account_number, destination_account_number, amount, transaction_date, status,
                             description, source_account_balance, destination_account_balance)
    VALUES ('Bank', input_account_number, input_loan_amount, NOW(),
            'Completed', 'Loan deposit', 0, balance);

    -- Check if rollback is required
    IF rollback_required THEN
        -- Transaction failed
        ROLLBACK;
        SELECT '0' AS Message;
    ELSE
        -- Commit the transaction
        COMMIT;
        -- Transaction processed successfully
        SELECT '1' AS Message;
    END IF;

END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE GetAccountLoans(
    IN account_number_input VARCHAR(20)
)
BEGIN
    SELECT *
    FROM LOAN
    WHERE account_number = account_number_input;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE GetLoanInstallments(
    IN loan_id_input INT
)
BEGIN
    SELECT *
    FROM LOAN_PAYMENT
    WHERE loan_id = loan_id_input;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE GetLoanPaymentStatus(
    IN loan_id_input INT
)
BEGIN
    -- Declare variables
    DECLARE total_paid_amount NUMERIC(20, 2) DEFAULT 0.0;
    DECLARE remaining_amount NUMERIC(20, 2) DEFAULT 0.0;

    -- Get total paid amount and remaining amount for the loan
    SELECT SUM(CASE WHEN status = 1 THEN paid_amount ELSE 0 END),
           SUM(CASE WHEN status = 0 THEN paid_amount ELSE 0 END)
    INTO total_paid_amount, remaining_amount
    FROM LOAN_PAYMENT
    WHERE loan_id = loan_id_input;

    -- Return total paid amount and remaining amount
    SELECT total_paid_amount, remaining_amount;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE PayLoanInstallment(
    IN account_number_input VARCHAR(20),
    IN amount_to_pay NUMERIC(10, 2),
    IN loan_id_input INT,
    IN installment_id_input INT,
    IN t_id INT
)
BEGIN
    -- Declare rollback_required variable
    DECLARE rollback_required BOOLEAN DEFAULT FALSE;
    DECLARE new_amount NUMERIC(10, 2);

    -- Declare continue handler for any exception
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            SET rollback_required = TRUE;
        END;

    SELECT amount AS amt
    FROM bank_account
    WHERE account_number = account_number_input;

    -- Start transaction
    START TRANSACTION;
    IF @amt < amount_to_pay THEN
        ROLLBACK;
        SELECT '0' AS Message;

    ELSE

        -- Update balance in BANK_ACCOUNT table
        UPDATE BANK_ACCOUNT
        SET amount = amount - amount_to_pay
        WHERE account_number = account_number_input;

        SELECT amount
        INTO new_amount
        FROM BANK_ACCOUNT
        WHERE account_number = account_number_input;

        -- Insert transaction record
        UPDATE TRANSACTION
        SET transaction_date       = NOW(),
            status                 = 'Completed',
            description            = CONCAT('Loan ', loan_id_input, ' Payment for loan installment ID: ',
                                            installment_id_input),
            source_account_balance = new_amount

        WHERE id = t_id;

        -- Update loan payment status
        UPDATE LOAN_PAYMENT
        SET status = 1
        WHERE id = installment_id_input;

    end if;


    -- Check if rollback is required
    IF rollback_required THEN
        -- Transaction failed
        ROLLBACK;
        SELECT '0' AS Message;
    ELSE
        -- Commit the transaction
        COMMIT;
        -- Transaction processed successfully
        SELECT '1' AS Message;
    END IF;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE GenerateLoanProposals(
    IN input_loan_amount NUMERIC(20, 2)
)
BEGIN
    DECLARE bank_interest_rate DECIMAL(5, 2);
    DECLARE total_loan_amount NUMERIC(20, 2);
    DECLARE monthly_payment_amount NUMERIC(10, 2);
    DECLARE start_date TIMESTAMP;
    DECLARE end_date TIMESTAMP;

    DECLARE output_data TEXT DEFAULT '';

    -- Calculate bank interest rate (20%)
    SET bank_interest_rate = 0.2;

    WHILE input_loan_amount > 100
        DO
            -- Calculate total loan amount
            SET total_loan_amount = input_loan_amount + (input_loan_amount * bank_interest_rate);

            -- Calculate monthly payment amount
            SET monthly_payment_amount = total_loan_amount / 12;

            -- Get start and end date for loan
            SET start_date = NOW();
            SET end_date = DATE_ADD(start_date, INTERVAL 1 YEAR);

            SET output_data =
                    CONCAT(output_data, input_loan_amount, ' ', total_loan_amount, ' ', monthly_payment_amount, ' ',
                           DATE(start_date), ' ', DATE(end_date), '\n');

            SET input_loan_amount = input_loan_amount - 100;
        END WHILE;

    SELECT output_data AS generated_data;

END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE ChangeLoanStatus(
    IN loan_id_input INT
)
BEGIN
    -- Declare rollback_required variable
    DECLARE rollback_required BOOLEAN DEFAULT FALSE;

    -- Declare continue handler for any exception
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            SET rollback_required = TRUE;
        END;

    -- Start transaction
    START TRANSACTION;

    -- Update loan payment status
    UPDATE LOAN
    SET loan_status = 0
    WHERE id = loan_id_input;

    -- Check if rollback is required
    IF rollback_required THEN
        -- Transaction failed
        ROLLBACK;
        SELECT '0' AS Message;
    ELSE
        -- Commit the transaction
        COMMIT;
        -- Transaction processed successfully
        SELECT '1' AS Message;
    END IF;
END //

DELIMITER ;



-- Admin Procedure

DELIMITER $$

CREATE PROCEDURE `AddUser`(IN p_username VARCHAR(32),
                               IN p_password VARCHAR(64),
                               IN p_first_name VARCHAR(32),
                               IN p_last_name VARCHAR(32),
                               IN p_national_code VARCHAR(10),
                               IN p_date_of_birth DATE,
                               IN p_address VARCHAR(255),
                               IN p_phone_number VARCHAR(20),
                               IN p_email VARCHAR(32),
                               IN p_is_superuser BOOLEAN)
BEGIN
    DECLARE exit handler for sqlexception
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    DECLARE exit handler for sqlwarning
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Check if username already exists
    IF EXISTS (SELECT 1 FROM USERS WHERE username = p_username) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'نام کاربری تکراری است';
    END IF;

    -- Check if phone_number already exists
    IF EXISTS (SELECT 1 FROM USERS WHERE phone_number = p_phone_number) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'شماره تلفن تکراری است';
    END IF;

    -- Check if email already exists
    IF EXISTS (SELECT 1 FROM USERS WHERE email = p_email) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'ایمیل تکراری است';
    END IF;

    -- Insert user into USERS table
    INSERT INTO USERS (username, password, first_name, last_name, national_code, date_of_birth, address, phone_number, email, date_joined, is_superuser)
    VALUES (p_username, p_password, p_first_name, p_last_name, p_national_code, p_date_of_birth, p_address, p_phone_number, p_email, NOW(), p_is_superuser);

    COMMIT;

    SELECT 1 AS Message;
END$$

DELIMITER ;


DELIMITER $$

CREATE PROCEDURE `AddBankAccount`(
    IN p_user_id INT,
    IN p_account_number VARCHAR(20),
    IN p_primary_password VARCHAR(4),
    IN p_amount NUMERIC(20,2),
    IN p_date_opened TIMESTAMP,
    IN p_date_closed TIMESTAMP,
    IN p_account_status BOOLEAN,
    IN p_description VARCHAR(255)
)
BEGIN
    DECLARE exit handler for sqlexception
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    DECLARE exit handler for sqlwarning
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Check if account_number already exists
    IF EXISTS (SELECT 1 FROM BANK_ACCOUNT WHERE account_number = p_account_number) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'شماره حساب تکراری است';
    END IF;

    -- Insert bank account into BANK_ACCOUNT table
    INSERT INTO BANK_ACCOUNT (
        user_id,
        account_number,
        primary_password,
        amount,
        date_opened,
        date_closed,
        account_status,
        description
    ) VALUES (
        p_user_id,
        p_account_number,
        p_primary_password,
        p_amount,
        p_date_opened,
        p_date_closed,
        p_account_status,
        p_description
    );

    -- Insert transaction record for the loan deposit
    INSERT INTO TRANSACTION (source_account_number, destination_account_number, amount, transaction_date, status,
                             description, source_account_balance, destination_account_balance)
    VALUES ('Bank', p_account_number, p_amount, NOW(),
            'Completed', 'Bank deposit', 0, p_amount);
    COMMIT;

    SELECT 1 AS Message;
END$$

DELIMITER ;
