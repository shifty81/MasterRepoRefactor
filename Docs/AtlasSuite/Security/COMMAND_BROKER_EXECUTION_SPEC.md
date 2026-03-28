# Command Broker Execution Specification

## Purpose
Turn the command broker into a real execution enforcement layer for approved local tools.

## Security Model
Every process launch must be:
- tool-registered
- argument-validated
- working-root-validated
- timeout-bounded
- audit-linked
- optionally dry-run capable

## Required Execution Controls
- exact executable path or trusted resolution
- allowed argument patterns
- allowed working directory roots
- max runtime timeout
- stdout and stderr capture
- max output size
- exit code capture
- optional environment allowlist
- optional hidden-window process creation on Windows

## Result Model
```cpp
struct CommandExecutionResult
{
    bool launched;
    bool completed;
    bool timedOut;
    int exitCode;
    std::string stdoutText;
    std::string stderrText;
    std::string auditCorrelationId;
};
```

## Deny Conditions
- unregistered tool
- executable path mismatch
- disallowed args
- working dir outside allowed roots
- disallowed environment variable injection
- timeout exceeded

## Recommended First Allowed Tools
- cmake configure
- cmake build
- ctest
- blender batch import
- archive unzip worker

## Required Tests
- unregistered tool denied
- bad args denied
- outside-repo working dir denied
- timeout kills child process
- dry-run generates audit event without launching
