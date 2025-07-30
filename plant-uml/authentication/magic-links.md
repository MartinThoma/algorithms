title Magic Link Authentication

User->Frontend: Enter email
Frontend->Backend: Request magic link\nfor email
Backend->Backend:Generate token\nStore token in DB; associate\ntoken with the user
Backend->Email Provider: Send magic link (token)\nto email
Email Provider->User: Deliver magic link
User->Frontend: Click magic link
Frontend->Backend: Verify token
note right of Backend: Check token validity and expiration
Backend->Frontend: Authentication successful
Frontend->User: Redirect to app (logged in)