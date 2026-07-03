Output ../mega-agents-cli-workflow.gif

Require uvx

Set Shell "bash"
Set FontSize 14
Set Width 1100
Set Height 520
Set Theme "Catppuccin Mocha"
Set WindowBar Colorful
Set TypingSpeed 40ms
Set PlaybackSpeed 1.8

Type "# agents-cli — real verified workflow"
Enter
Sleep 600ms
Type "uvx google-agents-cli --version"
Enter
Sleep 2s
Type "cd /tmp && uvx google-agents-cli create demo-agent --prototype --yes"
Enter
Sleep 10s
Type "cd /tmp/demo-agent && uvx google-agents-cli info"
Enter
Sleep 3s
Type "uvx google-agents-cli eval metric list | head -8"
Enter
Sleep 3s
