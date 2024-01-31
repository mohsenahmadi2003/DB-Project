DELIMITER $$

CREATE FUNCTION GetAccountOwnerNameFunction(account_number VARCHAR(20)) RETURNS VARCHAR(64) READS SQL DATA
BEGIN
    DECLARE owner_name VARCHAR(64);

    SELECT CONCAT(u.first_name, ' ', u.last_name)
    INTO owner_name
    FROM BANK_ACCOUNT ba
    INNER JOIN USERS u ON ba.user_id = u.id
    WHERE ba.account_number = account_number;

    RETURN owner_name;
END$$

DELIMITER ;
