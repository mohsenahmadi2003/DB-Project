INSERT INTO BANK_ACCOUNT (user_id, account_number, primary_password, amount, rate, date_opened, account_status,
                          description)
VALUES (3, '77773333666633338888', '9876', 2500.00, 0.01, '2022-04-05', 0, 'Investment 2 account'),

       (1, '85464584568495151231', '1234', 10000.00, 0.05, '2023-01-01', 0, 'Primary account'),
       (2, '98765432101234567892', '5678', 8000.00, 0.03, '2022-12-15', 0, 'Savings account'),
       (2, '55556666777788885555', '4321', 12000.00, 0.02, '2023-02-20', 0, 'Personal account'),
       (2, '99998888777766661111', '6789', 3000.00, 0.04, '2023-03-10', 0, 'Closed account');

select *
from bank_account;