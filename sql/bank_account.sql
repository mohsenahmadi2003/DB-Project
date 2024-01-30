INSERT INTO BANK_ACCOUNT (user_id, account_number, primary_password, amount, rate, date_opened, account_status, description)
VALUES
(4, '12345678901234567891', '1234', 5000.00, 0.05, '2023-01-01', 1, 'Primary account'),
(4, '98765432101234567892', '5678', 8000.00, 0.03, '2022-12-15', 1, 'Savings account'),
(4, '55556666777788885555', '4321', 12000.00, 0.02, '2023-02-20', 1, 'Personal account'),
(4, '99998888777766661111', '6789', 3000.00, 0.04, '2023-03-10', 1, 'Closed account'),
(4, '44445555666633338888', '9876', 9500.00, 0.01, '2023-04-05', 1, 'Investment account');

select *
from bank_account;