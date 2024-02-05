# Bank Project

Welcome to the Bank project!

This project is part of a database course, featuring the following functionalities:

- Creating bank accounts
- Conducting transactions between accounts
- Requesting loans
- Retrieving transaction logs based on date and count
- Making loan installment payments
- Viewing the bank's proposed loans
- And much more.

## Entity-Relationship Diagram (ERD)

You can view the Entity-Relationship Diagram (ERD) for the database schema and table relationships in the following PDF file:

[Download ERD PDF](https://github.com/mohsenahmadi2003/DB-Project/blob/main/ER.pdf)

## Project Preview

![Bank Project Preview](https://github.com/mohsenahmadi2003/DB-Project/blob/main/bank.gif)

## Getting Started

To begin using the project, follow the steps below:

### Prerequisites

- Ensure Python 3 is installed on your system
- Install Git on your system
- Access to a MySQL database server

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mohsenahmadi2003/DB-Project.git
   ```
2. Navigate to the project directory:

   ```bash
   cd DB-Project
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Open the `config.ini` file located in `db/config.ini` and add the following content:

   ```ini
   [database]
   host = localhost
   user = your_username
   password = your_password
   database = your_database_name
   ```

   Replace `your_username`, `your_password`, and `your_database_name` with your actual database credentials.
2. Configure the email settings by adding the following to the `utils/mail.ini` file:

   ```ini
   [email]
   smtpServer = smtp.gmail.com
   port = 587
   senderEmail = your_email@example.com
   password = your_email_password
   ```

   Replace `smtp.example.com`, `587`, `your_email@example.com`, and `your_email_password` with your actual Gmail email configuration details.

### Running SQL Scripts

To set up the database schema and populate it with initial data, follow these steps:

1. Ensure MySQL is installed on your system.
2. Open your MySQL client (e.g., MySQL Workbench, phpMyAdmin).
3. Create a new database using the following SQL command:

   ```sql
   CREATE DATABASE your_database_name;
   ```

   Replace `your_database_name` with the desired name for your database.
4. Use the newly created database:

   ```sql
   USE your_database_name;
   ```
5. Open and execute the `sql/schema.sql` file in your MySQL client. This file contains the SQL commands to create the database schema.
6. Open and execute the `sql/procedure.sql` and `sql/functions.sql` file in your MySQL client. This file contains the SQL commands to set up procedures and functions.

After completing these steps, your database should be set up and ready to use with the application.

### Running the Application

1. Start the application:

   ```bash
   python main.py
   ```

## Contributing

Contributions are welcome! If you'd like to contribute to the project, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch with a descriptive name for your feature or bug fix.
3. Make your changes and commit them to your branch.
4. Push your changes to your fork of the repository.
5. Submit a pull request to the main repository.

Please make sure your code follows the project's coding standards and includes appropriate tests.

## License

This project is licensed under the [MIT License](LICENSE).
