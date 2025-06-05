[Task 4] - Effective PR Review using Role Prompting


TASK:
You've submitted code for review and received feedback that seems superficial. 
You need to use AI to get a deeper analysis of your code from different perspectives.
Your task is to craft a prompt using the following instructions:

* Choose one of the provided processUserData function implementations as the target for your AI-driven review:
    1) processUserData.java
    2) processUserData.js
    3) processUserData.py
    4) processUserData.cs
    5) processUserData.go

* Define Expert Roles and Analysis Focus - Your prompt must instruct the AI to adopt the following three expert personas sequentially, providing an analysis from each viewpoint. 
  The focus areas for each role could be as an Experienced Developer,  a Security Engineer,  a Performance Specialist.
* Create the Prompt - The prompt must clearly instruct the AI to:
    1) Take the provided code snippet as input.
    2) Analyze it from each of the three specified expert perspectives (Developer, Security Engineer, Performance Specialist).
    3) For each perspective, provide specific, actionable recommendations and observations to improve the code.


PROMPT:

You will analyze a Python code file by adopting three distinct expert personas sequentially. 
For each role, provide a thorough analysis with specific, actionable recommendations.

**YOUR TASK:** Analyze the provided Python code from three expert perspectives. 
For each role, think deeply about the code through that specific lens and provide concrete, actionable feedback.

---

## ROLE 1: EXPERIENCED DEVELOPER
**Persona:** You are a senior Python developer with 15+ years of experience in building production systems. You've seen countless codebases and know what makes code maintainable, readable, and robust.

**Focus Areas:**
- Code organization and architecture patterns
- Readability and maintainability
- Error handling and edge cases
- Design patterns and best practices
- Code smells and anti-patterns
- Documentation and naming conventions
- Testing considerations

**Analysis Requirements:**
- Identify specific areas where the code structure could be improved
- Point out any violations of Python conventions (PEP 8, idiomatic Python)
- Suggest refactoring opportunities with concrete examples
- Highlight missing error handling with specific scenarios
- Recommend design pattern improvements where applicable

---

## ROLE 2: SECURITY ENGINEER
**Persona:** You are a cybersecurity expert specializing in application security with deep knowledge of OWASP Top 10 and secure coding practices. You think like an attacker to protect systems.

**Focus Areas:**
- Input validation and sanitization
- Authentication and authorization flaws
- Data exposure and information leakage
- Injection vulnerabilities (SQL, command, etc.)
- Cryptographic weaknesses
- Dependency vulnerabilities
- Secure data handling and storage
- API security considerations

**Analysis Requirements:**
- Identify specific security vulnerabilities with exploitation scenarios
- Point out unsafe practices with concrete attack vectors
- Suggest security hardening measures with implementation details
- Highlight any sensitive data handling issues
- Recommend security libraries or frameworks where appropriate

---

## ROLE 3: PERFORMANCE SPECIALIST
**Persona:** You are a performance engineer who optimizes Python applications for speed and efficiency. You understand algorithmic complexity, memory management, and system-level optimizations.

**Focus Areas:**
- Time complexity and algorithmic efficiency
- Memory usage and potential leaks
- I/O operations and blocking calls
- Database query optimization
- Caching opportunities
- Concurrent/parallel processing potential
- Resource management
- Scalability bottlenecks

**Analysis Requirements:**
- Identify specific performance bottlenecks with benchmarking suggestions
- Calculate Big O complexity for critical functions
- Point out inefficient data structures or algorithms
- Suggest optimization techniques with expected improvements
- Highlight blocking operations that could be made asynchronous
- Recommend profiling points and optimization strategies

---

## OUTPUT FORMAT:
For each role, structure your analysis as follows:

### [ROLE NAME] ANALYSIS

**Critical Issues:** (Issues that must be addressed immediately)
- Issue 1: [Specific problem] → [Concrete solution with code example if applicable]
- Issue 2: [Specific problem] → [Concrete solution with code example if applicable]

**Recommendations:** (Improvements that would significantly enhance the code)
- Recommendation 1: [What to improve] → [How to implement with specific steps]
- Recommendation 2: [What to improve] → [How to implement with specific steps]

**Best Practices to Apply:**
- Practice 1: [Specific practice] → [How it applies to this code]
- Practice 2: [Specific practice] → [How it applies to this code]

**Code Examples:** (Where applicable, provide refactored code snippets)

---

Remember: 
- Be specific, not generic. Reference actual line numbers, function names, and variables
- Provide actionable recommendations that can be immediately implemented
- Include code examples for complex suggestions
- Consider the context and apparent purpose of the code
- Prioritize feedback by severity and impact

Now, analyze the provided Python code from each of these three expert perspectives.
