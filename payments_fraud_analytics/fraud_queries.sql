--Create Merchant TABLE
CREATE TABLE "merchants" (
	"merchant_id"	INTEGER,
	"merchant_name"	TEXT,
	"category"	TEXT,
	"region"	TEXT,
	PRIMARY KEY("merchant_id")
)

--Create users TABLE
CREATE TABLE "users" (
	"user_id"	INTEGER,
	"signup_date"	TEXT,
	PRIMARY KEY("user_id")
)

--create ledger TABLE
CCREATE TABLE "ledger" (
	"transaction_id"	TEXT,
	"user_id"	INTEGER,
	"merchant_id"	INTEGER,
	"transaction_time"	TEXT,
	"amount_inr"	INTEGER,
	"payment_method"	TEXT,
	"status"	TEXT,
	"risk_score"	INTEGER,
	PRIMARY KEY("transaction_id"),
	FOREIGN KEY("user_id") REFERENCES "users"("user_id"),
	FOREIGN KEY("merchant_id_id") REFERENCES "merchants"("merchant_id")
)

--Verify the Data
SELECT 'users' AS table_name, COUNT(*) AS row_count
FROM users
UNION ALL
SELECT 'merchants', COUNT(*)
FROM merchants
UNION ALL
SELECT 'ledger', COUNT(*)
FROM ledger

--Query 1: DISTINCT Categories of Merchants
SELECT DISTINCT category
FROM merchants
ORDER BY category

--Query 2: Top 10 Highest Transactions
SELECT transaction_id,
       user_id,
       amount_inr,
       transaction_time
FROM ledger
WHERE status = 'captured'
ORDER BY amount_inr DESC
LIMIT 10

--Query 3: Merchant-wise Transaction Volume
SELECT merchant_id,
       COUNT(*) AS transaction_count,
       SUM(amount_inr) AS total_amount
FROM ledger
GROUP BY merchant_id
ORDER BY total_amount DESC

--Query 4: Merchants Having More Than 15 Transactions
SELECT merchant_id,
       COUNT(*) AS txn_count
FROM ledger
GROUP BY merchant_id
HAVING COUNT(*) > 15
ORDER BY txn_count DESC

--Query 5: Merchant Performance
SELECT m.merchant_name,
       m.category,
       COUNT(l.transaction_id) AS txn_count,
       SUM(l.amount_inr) AS total_amount
FROM merchants m
INNER JOIN ledger l
     ON m.merchant_id = l.merchant_id
GROUP BY m.merchant_id,
         m.merchant_name,
         m.category
ORDER BY total_amount DESC

--Query 6: Users with or without Transactions
SELECT u.user_id,
       u.signup_date,
       COUNT(l.transaction_id) AS transaction_count
FROM users u
LEFT JOIN ledger l
     ON u.user_id = l.user_id
GROUP BY u.user_id, u.signup_date
ORDER BY transaction_count DESC

--Quantify chargeback impact: count of chargeback transactions, unique users affected, total chargeback amount.
SELECT
    COUNT(*) AS chargeback_transactions,
    COUNT(DISTINCT user_id) AS unique_users_affected,
    SUM(amount_inr) AS total_chargeback_amount
FROM ledger
WHERE status = 'chargeback'


--Identify burner accounts: users whose signup_date is less than 30 days before their transaction's transaction_time, restricted to status = 'chargeback'
SELECT
    l.transaction_id,
    l.user_id,
    u.signup_date,
    l.transaction_time,
    ROUND(
       julianday(l.transaction_time) -
       julianday(u.signup_date),
       2
    ) AS age_days,
    l.amount_inr
FROM ledger l
INNER JOIN users u
     ON l.user_id = u.user_id
WHERE l.status = 'chargeback'
  AND julianday(l.transaction_time) >= julianday(u.signup_date)
  AND (
      julianday(l.transaction_time)
      - julianday(u.signup_date)
  ) < 30
ORDER BY age_days

--Detect velocity attacks: users with 3 or more transactions within any 10-minute window. 
SELECT
    user_id,
    datetime(
        (strftime('%s', transaction_time) / 600) * 600,
        'unixepoch'
    ) AS ten_min_bucket,
    COUNT(*) AS transaction_count,
    MIN(transaction_time) AS earliest_transaction,
    MAX(transaction_time) AS latest_transaction
FROM ledger
GROUP BY
    user_id,
    ten_min_bucket
HAVING COUNT(*) >= 3
ORDER BY user_id,
         earliest_transaction



