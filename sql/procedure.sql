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
            SELECT "رمز عبور با موفقیت به روز رسانی شد." AS Message;
        ELSE
            SELECT "رمز عبور قبلی اشتباه است." AS Message;
        END IF;
    ELSE
        SELECT "کاربری با این شناسه وجود ندارد." AS Message;
    END IF;
END//

DELIMITER ;


DELIMITER //
-- PROCEDURE for Process_Transaction
CREATE PROCEDURE `Process_Transaction`(
    IN source_account_number_input VARCHAR(20),
    IN destination_account_number_input VARCHAR(20),
    IN amount_input NUMERIC(10, 2),
    IN description_input VARCHAR(255)
)
BEGIN
    DECLARE _transaction_id INT;
    DECLARE _secondary_password VARCHAR(8);
    DECLARE _transaction_date TIMESTAMP;
    DECLARE rollback_required BOOLEAN DEFAULT FALSE;

    -- Declare continue handler for any exception
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            SET rollback_required = TRUE;
        END;

    -- Start the transaction
    START TRANSACTION;

    SET _transaction_date = NOW();
    -- Insert transaction record
    INSERT INTO TRANSACTION (source_account_number, destination_account_number, amount, transaction_date, status,
                             description)
    VALUES (source_account_number_input, destination_account_number_input, amount_input, _transaction_date, 'Pending',
            description_input);

    -- Get the transaction id
    SELECT id
    INTO _transaction_id
    FROM TRANSACTION
    WHERE source_account_number = source_account_number_input
      AND destination_account_number = destination_account_number_input
      AND amount = amount_input
      AND transaction_date = _transaction_date
      AND status = 'Pending'
      AND description = description_input
    LIMIT 1;


    -- Insert secondary password record
    SET _secondary_password = LPAD(FLOOR(RAND() * POW(10, 8)), 8, '0');

    INSERT INTO SECONDARY_PASSWORDS (bank_account_number, transaction_id, secondary_password, expire_time)
    VALUES (source_account_number_input, _transaction_id, _secondary_password, TIMESTAMPADD(MINUTE, 2, NOW()));

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
