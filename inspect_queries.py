import sqlite3
import pandas as pd

conn = sqlite3.connect('data.sqlite')

print('Step 1 result')
print(pd.read_sql("""
SELECT e.firstName, e.lastName, e.jobTitle
FROM employees e JOIN offices o ON e.officeCode=o.officeCode
WHERE o.city='Boston'
""", conn))

print('\nStep 9 counts')
print(pd.read_sql("""
SELECT o.officeCode, o.city, COUNT(c.customerNumber) AS n_customers
FROM offices o
LEFT JOIN employees e ON o.officeCode=e.officeCode
LEFT JOIN customers c ON e.employeeNumber=c.salesRepEmployeeNumber
GROUP BY o.officeCode,o.city
ORDER BY n_customers DESC, o.officeCode
""", conn))

print('\nStep 9 distinct counts')
print(pd.read_sql("""
SELECT o.officeCode, o.city, COUNT(DISTINCT c.customerNumber) AS n_customers
FROM offices o
LEFT JOIN employees e ON o.officeCode=e.officeCode
LEFT JOIN customers c ON e.employeeNumber=c.salesRepEmployeeNumber
GROUP BY o.officeCode,o.city
ORDER BY n_customers DESC, o.officeCode
""", conn))

print('\nStep 10 candidates')
print(pd.read_sql("""
SELECT e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
FROM employees e
JOIN offices o ON e.officeCode=o.officeCode
JOIN customers c ON e.employeeNumber=c.salesRepEmployeeNumber
JOIN orders ord ON c.customerNumber=ord.customerNumber
JOIN orderdetails od ON ord.orderNumber=od.orderNumber
WHERE od.productCode IN (
    SELECT od2.productCode
    FROM orderdetails od2
    JOIN orders ord2 ON od2.orderNumber=ord2.orderNumber
    JOIN customers c2 ON ord2.customerNumber=c2.customerNumber
    GROUP BY od2.productCode
    HAVING COUNT(DISTINCT c2.customerNumber) < 20
)
GROUP BY e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
ORDER BY e.firstName, e.lastName
LIMIT 20
""", conn))

print('\nProducts with <20 customers')
print(pd.read_sql("""
SELECT od.productCode, COUNT(DISTINCT c.customerNumber) AS numcustomers
FROM orderdetails od
JOIN orders o ON od.orderNumber=o.orderNumber
JOIN customers c ON o.customerNumber=c.customerNumber
GROUP BY od.productCode
HAVING COUNT(DISTINCT c.customerNumber) < 20
ORDER BY numcustomers, od.productCode
LIMIT 20
""", conn))

conn.close()
