# Quizzical

## Introduction

Quizzical is a terminal-based quiz game, using [The Open Trivia
Database](https://opentdb.com/) as the back end.

![Quizzical](https://raw.githubusercontent.com/davep/quizzical/main/images/quizzical.png)

## Installing

### pipx

The package can be installed using [`pipx`](https://pypa.github.io/pipx/):

```sh
$ pipx install quizzical
```

### Homebrew

The package is available via Homebrew. Use the following commands to install:

```sh
$ brew tap davep/homebrew
$ brew install quizzical
```

## Running

Once installed run the `quizzical` command.

## Playing the game

Hopefully the interface is pretty straightforward: run up the application,
use the `New` button to create a new quiz with your choice of parameters,
use the `Run` button to play a game. When you run a new game you'll be shown
the parameters:

![Starting a new quiz](https://raw.githubusercontent.com/davep/quizzical/main/images/start-quiz.png)

and once you start you'll be shown a series of questions; press keys
<kbd>1</kbd>, <kbd>2</kbd>, <kbd>3</kbd> or <kbd>4</kbd> to answer each one.

![An example question](https://raw.githubusercontent.com/davep/quizzical/main/images/question.png)

Once the quiz is over you can view your results and see which answers were
right and which were wrong:

![Viewing some results](https://raw.githubusercontent.com/davep/quizzical/main/images/results.png)

## Getting help

If you need help, or have any ideas, please feel free to [raise an
issue](https://github.com/davep/quizzical/issues) or [start a
discussion](https://github.com/davep/quizzical/discussions).

## TODO

Things I'm considering adding or addressing:

- [ ] Add session token support (less frequent question repeats).
- [ ] More quiz information in the main quiz list.
- [ ] Record scores for each game played, provide a history view.
- [ ] Allow answering a question with the mouse.

[//]: # (README.md ends here)
