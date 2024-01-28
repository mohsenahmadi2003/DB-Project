DELIMITER //

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
