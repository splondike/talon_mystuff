mode: user.typescript
mode: command
and code.language: typescript
-
state lambda:
    insert("() => {}")
    key(left:7)

state fragment:
    insert("<></>")
    key(left:3)

state console:
    insert("console.log();")
    key(left:2)

state interface: "interface "
