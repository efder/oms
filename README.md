# Offline Messaging API

## Setup
If you want to reproduce the results that I get please create a sample virtual environment and install the requirements. (Used Python3.7)
```
    virtualenv dev && source dev/bin/activate && pip install -r requirements
```

## **Main Requirements**

### **1. Authentication**
  
  Token based authentication is employed using django-knox package and 'accounts' app is responsible for registration, login and logout. The related endpoints are,
  ```
  /api/auth/register
  /api/auth/login
  /api/auth/logout
  ```
  Basic workflow of registration is like,

  i. User attempts to sign up to the system with his/her username, password and optionally email. (System ensures singularity of usernames)

  ii. If the attempt is successful, the system returns first token to the user. (Default timeout duration for token is 10 hours by default, but it can be adjusted using TOKEN_TTL parameter of knox settings.) 
  
  iii. User then can access to the resources that he/she authorized to.

  Basic workflow of login is like,

  i. User attempts to sign in to the system with his/her username and password.
  
  ii. If the credentials are correct newly created token are returned and user is authenticated, in other scenarios user is informed about what went wrong (e.g. password field is missing, incorrect credentials)

  Basic workflow of logout is like,
  
  i. User sends to a POST request with an empty body to logout endpoint (his/her token need to be in header's Authorization field) and his/her token expires.

  **Note: Returned token need to be kept in request header's Authorization field in the format <Token [usertoken]>.**

### **2. Messaging**

The app responsible for messaging is 'messageservice' and related endpoints are,
```
/api/message
/api/message/sent
/api/message/received
```
**Note: For all workflows, user needs to be authenticated**

Basic workflow for sending message is,

i. Sender creates a message data contatining receiver (need to be username) and content information and posts message data to the /api/message end. Sample,
```
{"receiver": "receiver_username", "content": "Hello, receiver!"}
```

ii. If the receiver username exists and sender is **not blocked** by the receiver the message is sent to the receiver.

Basic workflow for listing past messages is basically sending get request to /api/message endpoint. This lists both sent and received messages. Users also can use /api/message/sent and api/message/received end points to list their sent and received messages.

### **3. Blocking**
Users can use /api/block endpoint to block the other users. They need to prepare data like, 
```
{"blocked": "user_to_be_blocked"}
```
and send post request to /api/block with that data. If the user exists and not blocked before systems blocks that user.

### **4. Logging and Errors**
Details of internal server errors (code 500) are not sent to the user and logged in debug level detail on server side. User just get the message,
```
  {"detail": "Something went wrong"}
```
Besides simple logs of requests and debug level system errors, 

i. Login

ii. Invalid Login

iii. Successful Message

iv. Blocked Message

v. Block User

logs are kept.

### **5. Testing**
There are 26 different unit test cases for different scenarios. They can be reached at tests.py file under their related apps. All the tests can be run as,
```
python manage.py test
```

## Optional Requirements

### **1.Categorization and Pagination**
Users can filter the results of their sent and received messages by username and date using url parameters. For instance sending GET request to,
```
/api/message/sent?receiver=rcvr&date=2020-03-30&page=1
```
yields the result of "first page of the messages sent to the rcvr in 30 March 2020".

Basic page number pagination strategy employed here. Also exception handling mechanisms are employed for url parameters.