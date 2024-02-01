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
    WHERE ba.account_number = account_number AND account_status = 1;

    -- بررسی اینکه آیا اطلاعاتی یافت شده یا نه
    IF owner_name IS NULL THEN
        SET owner_name = 'Not found';
    END IF;

    RETURN owner_name;
END$$

DELIMITER ;


DELIMITER $$

CREATE FUNCTION CheckSecondaryPassword(_transaction_id INT, secondary_password VARCHAR(8)) RETURNS INT
    READS SQL DATA
BEGIN

    DECLARE password VARCHAR(8) DEFAULT NULL;
#     DECLARE ex_time TIMESTAMP;

    SELECT secondary_password
    INTO password
    FROM secondary_passwords
    WHERE transaction_id = _transaction_id
      AND expire_time >= NOW();

    IF password = secondary_password THEN
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;

END$$

DELIMITER ;



CREATE FUNCTION ValidateTransactionAmount(amount NUMERIC(10, 2)) RETURNS BOOLEAN
    NO SQL
BEGIN
    IF amount IS NULL OR amount < 0 THEN
        RETURN FALSE;
    ELSE
        RETURN TRUE;
    END IF;
END;
