# wasla_test

i had create a simple table for products which contain products name and price and other info 

i create 2 api endpoint 
url : https://o9pmj2gw45.execute-api.us-east-1.amazonaws.com/production/list
one work with get method to get all product list in table 

the second one is product 
url : https://o9pmj2gw45.execute-api.us-east-1.amazonaws.com/production/product
which work with 
get 
to get this specific product by id 
POST 
to add new record or product 

PUT 

require id / key and value 
for updating existing record 

id to catch the record 
key for which title need to update Ex "price "
value the new value 

DELETE
need id to delete record 

in responsive found the postman request with the authentication 
just run it on postman 

in case of need new token 

from postman 
Authorization section 
select 
OAuth 2.0 
request : headers
in below found get new access token 
will generate window with login or sign up option 
add email and passowrd , add verfication code from sent email 
the new token will be generated and cached in postmen 




To deploy 

create table with dynamodb with name "WASLA_Table" Partition key "id"  "String"

create lambda function and add lambda function 

create Amazon Cognito new user pool 

create Api from ApiGateway  add resources list and product 
list have get method 
product have get / post / delete / put method 
add authentication that had been created in cognito section 

deploy all 
