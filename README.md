<h1 align="center">Productivity Manager</h1>
<p align="center">An application to remind &amp; help you to stay productive at all times.</p>

## How Will This Help Me? 
Productivity Manager has two simple, yet essentially profound features and these are:
productivity reminders and blocking websites at certain time periods or intervals.
For instance, blocking any kind of social media at work hours will help you focus at work
instead of getting side tracked, let procrastination be a thing of the past. 

This all is managed by a command-line interface with very simple syntax.

## Software Components
- [Command-line Interface](./src/interface.py) (CLI) <br>
Responsible for creating, editing and deleting entries user-controlled, writes data.

- [Backend Entry Manager](./src/manager.py) <br>
Responsible for notifying the user and DNS-blocking websites, receives CLI data.

(Data transmission from CLI to manager is done via raw text file.)
