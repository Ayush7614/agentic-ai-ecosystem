Output ../step-06-login-status.gif

Require uvx

Set Shell "bash"
Set FontSize 15
Set Width 1100
Set Height 520
Set Theme "Catppuccin Mocha"
Set WindowBar Colorful
Set TypingSpeed 35ms
Set PlaybackSpeed 1.2

Type "uvx google-agents-cli login --status"
Enter
Sleep 3s
Type "uvx google-agents-cli login --help | head -12"
Enter
Sleep 3s
