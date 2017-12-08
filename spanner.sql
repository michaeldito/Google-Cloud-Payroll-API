CREATE TABLE Company (
    CompanyId INT64 NOT NULL,
    CompanyName STRING(MAX) NOT NULL,
) PRIMARY KEY (CompanyId);


CREATE TABLE Employees (
    EmployeeId INT64 NOT NULL,
    CompanyId INT64 NOT NULL,
    EmployeeSsn INT64 NOT NULL,
    HourlyPayRate FLOAT64 NOT NULL,
    Name STRING(25) NOT NULL,
) PRIMARY KEY (EmployeeId);


CREATE TABLE Paystubs (
    CompanyId INT64 NOT NULL,
    EmployeeId INT64,
    PayPeriod STRING(MAX) NOT NULL,
    Pay FLOAT64 NOT NULL,
) PRIMARY KEY (CompanyId, EmployeeId, PayPeriod);


CREATE TABLE Timesheets (
    TimesheetId INT64 NOT NULL,
    CompanyId INT64 NOT NULL,
    Date DATE NOT NULL,
    EmployeeId INT64 NOT NULL,
    HoursWorked FLOAT64 NOT NULL,
    PayPeriod STRING(MAX) NOT NULL,
    Type STRING(MAX) NOT NULL,
) PRIMARY KEY (TimesheetId);

