## 🐛 Bug Ticket

### Title
Authentication - Logout Button Non-Responsive - Safari Browser

### Description
The logout button fails to respond to user interaction when accessed through Safari browser. Users are unable to terminate their session through the standard logout mechanism, potentially leaving their accounts accessible on shared devices.

### Steps to Reproduce
1. Open Safari browser and navigate to the application
2. Log in with valid user credentials
3. Navigate to any authenticated page within the application
4. Locate the logout button (typically in header/navigation area)
5. Click on the logout button
6. Observe that no action occurs

### Expected Behavior
Upon clicking the logout button, the user should be immediately logged out of their session, have their authentication tokens cleared, and be redirected to the login page or home page.

### Actual Behavior
The logout button appears clickable but does not respond to mouse clicks. No visual feedback occurs, no network requests are initiated, and the user remains logged in. The button does not show any loading states or error messages.

### Environment
- **Browser:** Safari (version to be confirmed)
- **Operating System:** macOS (assumed based on Safari usage)
- **Device Type:** Desktop
- **Application Version:** Current production
- **User Role/Type:** All authenticated users

### Severity/Priority
**Level:** High
**Justification:** This issue prevents users from securely ending their sessions, which poses a security risk especially on shared or public computers. It affects a major browser platform and has no apparent workaround.

### Additional Information
- **Reproducibility:** Always (on Safari)
- **Workaround:** Users must manually clear browser cookies/cache or close all browser windows
- **First Observed:** Recently reported
- **Screenshots/Logs:** Browser console logs should be captured to check for JavaScript errors