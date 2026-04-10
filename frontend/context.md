# Anti-Fraud System — Context

## Overview
This system is designed to **prevent financial fraud in real time** by evaluating the risk of user actions within a banking or money-movement environment.  
Rather than only detecting fraud after it occurs, the system focuses on **prevention through dynamic risk assessment and automated decision-making**.

---

## Core Principle
Every user action is treated as a **risk evaluation event**.

Risk is not static. It is continuously recalculated based on:
- user behavior
- transaction context
- device and network signals
- recent security-related events

The system adapts its response dynamically to minimize fraud while maintaining user experience.

---

## Event Flow

### 1. Trigger Event
An event initiates the evaluation process. Examples include:
- user login
- money transfer
- adding a new beneficiary
- credential changes (password, email, 2FA)

---

### 2. Signal Collection
The system gathers and computes relevant signals, such as:
- transaction amount vs user baseline
- action frequency (velocity)
- device trust level
- geolocation consistency
- recent security events (OTP usage, password reset)

---

### 3. Risk Evaluation
All signals are aggregated into a **risk score**.

The score reflects:
- behavioral anomalies
- contextual inconsistencies
- known fraud patterns or network associations

---

### 4. Decision Engine
Based on the risk score, the system determines the appropriate action:

- **Low risk** → approve action  
- **Medium risk** → require step-up authentication (OTP, MFA)  
- **High risk** → block or reject action  

---

### 5. Automated Response
The system executes the decision in real time:
- allow transaction
- request additional verification
- block operation
- freeze session or account
- generate alerts for monitoring systems

---

### 6. Continuous Monitoring
During the user session:
- risk is recalculated dynamically
- anomalies trigger re-evaluation
- additional controls may be applied if risk increases

---

### 7. Post-Event Analysis
After execution:
- transactions are analyzed for patterns (e.g., fraud networks, mule accounts)
- models and rules are updated to improve future detection

---

## Key Objective
To **intercept and stop fraudulent activity before funds are moved**, while minimizing friction for legitimate users.

---

## Design Philosophy
- Real-time decisioning is critical
- Combine multiple weak signals into strong indicators
- Prefer adaptive responses over static rules
- Balance security with user experience