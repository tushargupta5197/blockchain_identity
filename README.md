# Decentalized Identity Management System

## How to use

### User

To open the command line interface of user ``python3 cli.py``
+ To initialize the user : use `(initialize | init) user` and enter the queried data to initialize an account:
   ```
   # DIMS> init user
     Enter your name: Alice Garcia
     Please give your wallet file path (will be created if not existing): ./wallet.yaml
     Enter your ssn: 121001
     
     Wallet Loaded 
     Hello Alice Garcia
   # Alice>
   ```
+ To show the current contents of the wallet, use `(display | show | view) wallet`.
  ```
  # Alice> display wallet
  ```
+ Since we do not have any certificates yet, the wallet is empty. Let's get some certificates now.

+ To setup the issuer from whom you want the certificate, use `set issuer`:
  ```
  # Alice> set issuer
  Enter the issuer from which you want a certificate: ABC University
  ```
  This will show the issuer details such as url, certificate schema, etc. if successful and create certificate for <b>ABC University</b>.
+ Now, you can view various details of the certificate issued by the company such as name or public key as:
```
# Alice> get certificate name
# Alice> get cert pkey
```
+ To obtain the certificate issued by the issuer, use `get (certificate | cert)`
  ```
  # Alice> get cert
  ```
  Now we have to wait while our issuer gathers up the details, makes the certificate, calculates the merkle root and signs it and sends it to be uploaded to the ethereum blockchain. 
  After this is done, use:
  ```
  # Alice> show wallet
  ```
  to view your newly obtained certificate!
+ Now we will use our newly obtained transcript from ABC University to apply for a job in <b>XYZ Company</b>. Execute:
  ```
  # Alice> set issuer
  Enter the issuer from which you want a certificate: XYZ Company
  ...
  # Alice> get cert
  ```
  You will be asked for various data needed by the company, some of which (marked as V) will be verified from the transcript. DIMS will automatically make a proof ensuring that only the fields required by the company are exposed and other fields are still private.
  
+ Again, we can use both of our certificates to get a loan certificate from the <b>SBI Bank</b>. Execute the following:
  ```
  # Alice> set issuer
  Enter the issuer from which you want a certificate: SBI Bank
  ...
  # Alice> get cert
  ```
+ Now that we have many certificates, we can view our wallet again to see all of them. 
  ```
  # Alice> show wallet
  ```
+ You can also view individual certificates by using `(display | show | view) (cert | certificate)` and enter the certificate to display that:
  ```
  # Alice> show cert
  ...
  Which one do you want to view? : loan
  ```

### Server

To open the command line interface of user 1``python3 issuer_cli.py``

+ To setup a Issuer : use `setup issuer` and enter the data - 
```
# DIMS> setup issuer
Enter Name: SBI Bank
Enter your port number: 8082
Enter your certificate name: loan
Enter database_name: sbi
Enter your requirements, and type 'done' when done:
Salary>10000
Requirement added: Salary>10000

Execute: python3 generated_SBI_Bank.py in future to run your Flassk server
# SBI Bank> setup server
STARTING SERVER...
```

