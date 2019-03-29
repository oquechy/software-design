# Architecture of CLI

![Architecture](cli-architecture.png)

## Controller

* Controller prompts user to start or continue typing, reads the input line by line and passes lines to the Expansion module. 
* Then the whole expanded command is passed by Controller to an Interpreter to be split into several Processes.
* Controller runs resulting processes in the given order and passes them inputs and a shell environment.

![Architecture](cli-resources.png)

### Expansion module
Iterates through the line, expands environment variables depending on quotes and returns a line split into words as a result.

### Interpreter
Iterates through tokens, classifies them and wraps into Processes.

### Process
Base class has an abstract method ```run(input, scope)```, which allows Controller to manipulate piped inputs.