Output ../step-05-run-agent.gif

Require uvx

Set Shell "bash"
Set FontSize 14
Set Width 1100
Set Height 520
Set Theme "Catppuccin Mocha"
Set WindowBar Colorful
Set TypingSpeed 28ms
Set PlaybackSpeed 1.5

Type "cd /tmp/caveman-agent-demo"
Enter
Sleep 400ms
Type "uvx google-agents-cli run 'What is the weather in San Francisco?'"
Enter
Sleep 14s
