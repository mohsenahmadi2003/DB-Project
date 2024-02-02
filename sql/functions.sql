DELIMITER $$

CREATE FUNCTION GetAccountOwnerNameFunction(account_number VARCHAR(20)) RETURNS VARCHAR(64)
    READS SQL DATA
BEGIN
    DECLARE owner_name VARCHAR(64);

    -- تنظیم مقدار اولیه برابر با NULL
    SET owner_name = NULL;

    -- جستجو برای یافتن نام صاحب حساب
    SELECT CONCAT(u.first_name, ' ', u.last_name)
    INTO owner_name
    FROM BANK_ACCOUNT ba
             INNER JOIN USERS u ON ba.user_id = u.id
    WHERE ba.account_number = account_number
      AND account_status = 0;

    -- بررسی اینکه آیا اطلاعاتی یافت شده یا نه
    IF owner_name IS NULL THEN
        SET owner_name = 'Not found';
    END IF;

    RETURN owner_name;
END$$

DELIMITER ;


DELIMITER $$

CREATE FUNCTION CheckSecondaryPassword(_transaction_id INT, _secondary_password VARCHAR(8)) RETURNS INT
    READS SQL DATA
    RETURN (SELECT IFNULL(
                           (SELECT 1
                            FROM secondary_passwords
                            WHERE transaction_id = _transaction_id
                              AND secondary_password = _secondary_password
                              AND NOW() < expire_time
                            LIMIT 1),
                           0
                       ));


DELIMITER ;

DELIMITER $$

CREATE FUNCTION ValidateTransactionAmount(amount NUMERIC(10, 2)) RETURNS BOOLEAN
    NO SQL
BEGIN
    IF amount IS NULL OR amount < 0 THEN
        RETURN FALSE;
    ELSE
        RETURN TRUE;
    END IF;
END;

DELIMITER ;

CREATE FUNCTION GetEmailWithAccountNumber(_account_number VARCHAR(20)) RETURNS VARCHAR(32)
    READS SQL DATA
BEGIN

    DECLARE _email VARCHAR(32);
    DECLARE _user_id INT;

    SELECT user_id
    INTO _user_id
    FROM bank_account
    WHERE account_number = _account_number;

    SELECT email
    INTO _email
    FROM users
    WHERE id = _user_id;

    RETURN _email;
END;

CREATE FUNCTION GetAmountAccount(_account_number VARCHAR(20)) RETURNS DECIMAL(20, 2)
    READS SQL DATA
BEGIN

    DECLARE balance DECIMAL(20, 2);

    SELECT amount
    INTO balance
    FROM bank_account
    WHERE account_number = _account_number;

    RETURN balance;
END;


DELIMITER //

CREATE FUNCTION GetActiveLoanId(
    account_number_input VARCHAR(20)
)
    RETURNS INT
    READS SQL DATA

BEGIN
    DECLARE loan_id INT;

    -- Check if an active loan exists for the given account number
    SELECT id
    INTO loan_id
    FROM LOAN
    WHERE account_number = account_number_input
      AND loan_status = 1;

    -- Return loan_id if an active loan exists, otherwise return 0
    IF loan_id IS NOT NULL THEN
        RETURN loan_id;
    ELSE
        RETURN 0;
    END IF;
END //

DELIMITER ;


DELIMITER //

CREATE FUNCTION GetSmallestUnpaidInstallment(
    loan_id_input INT
)
    RETURNS INT
    READS SQL DATA

BEGIN
    DECLARE smallest_id INT DEFAULT 0;

    -- Find the smallest unpaid installment amount for the given loan_id
    SELECT MIN(id)
    INTO smallest_id
    FROM LOAN_PAYMENT
    WHERE loan_id = loan_id_input
      AND status = 0;

    -- Return the smallest unpaid installment amount
    RETURN smallest_id;
END//

DELIMITER ;


DELIMITER //

CREATE FUNCTION GetMinBalanceByAccountNumber(
    account_number_input VARCHAR(20))
    RETURNS NUMERIC(20, 2)
    READS SQL DATA
BEGIN
    DECLARE min_balance_source NUMERIC(20, 2);
    DECLARE min_balance_destination NUMERIC(20, 2);
    DECLARE start_date TIMESTAMP;
    DECLARE end_date TIMESTAMP;

    SET start_date = NOW() - INTERVAL 2 MONTH;
    SET end_date = NOW();
    -- Find minimum balance based on source_account_number
    SELECT MIN(source_account_balance)
    INTO min_balance_source
    FROM transaction
    WHERE source_account_number = account_number_input AND transaction_date BETWEEN start_date AND end_date;

    -- Find minimum balance based on destination_account_number
    SELECT MIN(destination_account_balance)
    INTO min_balance_destination
    FROM transaction
    WHERE destination_account_number = account_number_input AND transaction_date BETWEEN start_date AND end_date;

    -- Return the minimum balance
    RETURN LEAST(COALESCE(min_balance_source, min_balance_destination), COALESCE(min_balance_destination, min_balance_source));
END //

DELIMITER ;

