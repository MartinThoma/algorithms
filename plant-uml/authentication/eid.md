title German eID Authentication (via AusweisApp2 and eID Server)

User->Frontend: Click "Login with eID"
Frontend->Backend: Request eID auth session
Backend->eID Server: Create session\nRequest TcToken
eID Server->Backend: Return TcToken URL
Backend->Frontend: Return TcToken URL or QR Code
Frontend->AusweisApp2: Start session via TcToken URL
note right of AusweisApp2: Prompt user to insert ID card\nand enter PIN
User->AusweisApp2: Enter PIN
AusweisApp2->eID Server: Perform authentication\nRequest user attributes
eID Server->AusweisApp2: Return signed user data
AusweisApp2->Frontend: Redirect with token (optional)
Frontend->Backend: Exchange token for user info
note right of Backend: Verify signature\nExtract identity attributes
Backend->Frontend: Authentication successful
Frontend->User: Redirect to app (logged in)
