Output ../step-03-install-info.gif

Require uvx

Set Shell "bash"
Set FontSize 15
Set Width 1100
Set Height 520
Set Theme "Catppuccin Mocha"
Set WindowBar Colorful
Set TypingSpeed 30ms
Set PlaybackSpeed 1.4

Type "cd /tmp/caveman-agent-demo"
Enter
Sleep 500ms
Type "uvx google-agents-cli install"
Enter
Sleep 10s
Type "uvx google-agents-cli info"
Enter
Sleep 4s
