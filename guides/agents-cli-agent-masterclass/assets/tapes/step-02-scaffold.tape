Output ../step-02-scaffold-create.gif

Require uvx

Set Shell "bash"
Set FontSize 15
Set Width 1100
Set Height 520
Set Theme "Catppuccin Mocha"
Set WindowBar Colorful
Set TypingSpeed 30ms
Set PlaybackSpeed 1.3

Type "cd /tmp && rm -rf caveman-agent-demo"
Enter
Sleep 500ms
Type "uvx google-agents-cli create caveman-agent-demo --prototype --yes"
Enter
Sleep 12s
Type "ls caveman-agent-demo/"
Enter
Sleep 2s
