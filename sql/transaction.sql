INSERT INTO `TRANSACTION` (source_account_number, destination_account_number, amount, transaction_date, status, description) VALUES
('12345678901234567891', '98765432101234567892', 1500.00, '2023-01-05', 'Completed', 'Transfer from primary account to savings account'),
('98765432101234567892', '55556666777788885555', 3000.00, '2022-12-20', 'Completed', 'Transfer from savings account to personal account'),
('55556666777788885555', '99998888777766661111', 2000.00, '2023-02-25', 'Completed', 'Transfer from personal account to closed account'),
('99998888777766661111', '44445555666633338888', 500.00, '2023-03-15', 'Completed', 'Transfer from closed account to investment account'),
('44445555666633338888', '12345678901234567891', 700.00, '2023-04-10', 'Completed', 'Transfer from investment account to primary account');

select *
from transaction