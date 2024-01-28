DELIMITER //
-- Function for Login 
CREATE FUNCTION LoginUser(p_username VARCHAR(32), p_password VARCHAR(64))
RETURNS BOOLEAN
READS SQL DATA
BEGIN
  DECLARE v_user_count INT; 

  SELECT COUNT(*)
  INTO v_user_count
  FROM users
  WHERE username = p_username AND password = p_password;

  IF v_user_count > 0 THEN
    RETURN TRUE;
  ELSE
    RETURN FALSE;
  END IF;
END //

DELIMITER ;
