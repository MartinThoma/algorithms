title Passkey Authentication

User->Frontend: Initiate login
Frontend->Authenticator: Request credential (create or get)
note right of Authenticator: User verifies with biometric/PIN
Authenticator->Frontend: Return signed assertion
Frontend->Backend: Send assertion for verification
note right of Backend: Verify signature and user identity
Backend->Frontend: Authentication successful
Frontend->User: Grant access to app
