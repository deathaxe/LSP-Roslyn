# LSP-Roslyn

C# support for Sublime Text's LSP plugin.

Uses [Roslyn Language Server](https://www.nuget.org/packages/roslyn-language-server)
to provide completions, validation, formatting and other features for C# files.

## Installation

1. Install [LSP](https://packagecontrol.io/packages/LSP) and [LSP-Roslyn](https://packagecontrol.io/Packages/LSP-Roslyn) from Package Control.
2. Restart Sublime Text.

> [!NOTE]
>
> The plugin does not distribute but install language server from official sources.
> via `dotnet tool install roslyn-language-server --global --prerelease`.

### Requirements

- .NET 10 runtime
- Roslyn Language Server v5.9.0+

## Configuration

Open configuration file 
by running `Preferences: LSP-Roslyn Settings` from Command Palette 
or via Main Menu (`Preferences > Package Settings > LSP > Servers > LSP-Roslyn`).
