ProfileTool
========================

**Author:** Jayden Navarro

**Email:** jdndeveloper@gmail.com

**LinkedIn:** [Jayden Navarro](https://www.linkedin.com/in/jaydennavarro)

**Twitter:** [@JaydenNavarro](https://twitter.com/JaydenNavarro)

**Google+:** [Jayden Navarro](https://plus.google.com/u/0/+JaydenNavarro/posts)

**GitHub:** [JDNdeveloper](http://www.github.com/JDNdeveloper)

## Description:

Python tool to easily manipulate bash profiles.

## Overview:

The general usage is that you create sections in your profile (using start and end token comments, described below), and then define regex conditions to be run against these sections to form lists of information when the profile is parsed. This information can then be modified, and passed back to the ProfileTool which will write it back to the profile.

The original use case for this was to define my current workspace name (i.e. project) and package (i.e. active folder), so that when I logged into my server I was immediately in the active directory I wanted to be in. This could easily be accomplished by a single line in a bash profile, but I wanted to be able to easily switch active packages and between different projects, so I decided to write a handful of scripts (e.g. new project, delete project, set default project, set default package, list projects) to read and/or modify the profile accordingly. This required laborous custom parsing for each tool, so I decided to abstract it to a common tool that would let me manipulate python data structures and then handle the conversion to and from the file for me, and thus ProfileTool was born. A `src/example_profile` is provided showing a bare-bones version of the profile I typically use.

## API:

### Bash Profile Format:

In order to use this tool, you must include `pt` (**p**rofile**t**ool) tokens in your file. These tokens take the following form:

```bash
# pt_start group_name
...
...
# pt_end group_name
```

The lines between the start and end tokens are called a capture group. They will be parsed using the regex you define in capture_groups.py. Currently the capture groups `default_project` and `projects` are defined, but you can easily add more. Refer to the examples section for more details.

### ProfileTool:

#### __init__( self, profile_path ):
Constructor takes in path to bash profile. If none provided, defaults to `~/.bashrc`.

#### readGroups( self ):
Parses all capture groups and converts them to python lists using the regex defined in capture_groups.py.

A dictionary is returned that maps group names to a list of their captured items. The captured items are stored as a tuple of the matched regex expressions from the regex list for that capture group.

#### writeGroups( self, groups ):
Writes the groups back to the bash profile using the group format defined in capture_groups.py.

## Examples:

### Creating a capture group

**NOTE: I highly suggest you backup your profile before using `writeGroups()` on self made capture groups, as a slight mistake may lead to all contents within your capture group being deleted.**

In this example I'll be adding a capture group for aliases. This will allow you to parse your profile for aliases, manipulate them however you like, then write them back to your profile.

#### Define the `rgx_` and `fmt_`:

In order to parse the alias, we'll want to define two regular expressions, one to match the alias name, and one to match the command we're aliasing. We'll call this capture group `alias`.

In order to properly re-output the group, you will need to provide the format.

Open `capture_groups.py` and add:

```python
...
# CAPTURE_GROUP: alias
rgx_alias = [ r'alias (.*)=.*', r'alias .*=(.*)' ]
fmt_alias = 'alias %s=%s\n'
...
```

The first regex will capture the lefthand side, and the second will capture the right hand side.

The format will take the two captured items and substitute them back into the format string where `%s` currently is.

#### Edit bash profile to include token:

To show ProfileTool where to look, you'll need to wrap your alias section with `pt` tokens.

Open `~/.bashrc` or `~/.bash_profile` and add:

```bash
...
# pt_start alias
...
alias em="emacs"
...
# pt_end alias
...
```

### Using the ProfileTool to read and write aliases

In this section I will provide a bash profile, and show how the ProfileTool can be used to change an alias. This example assumes you've implemented the alias capture group as shown in the previous example.

```bash
# .bashrc

# pt_start alias
alias em="emacs"
alias ls="ls -l"
alias vi="vim"
# pt_end alias
```

The following Python script will change the vi alias from "vim" to "emacs".

```python
import profile_tool as pt

# create an instance, pass in path to bash profile,
# or leave blank to use ~/.bashrc
ptool = pt.profile_tool()
groups = ptool.readGroups()

# grab the alias group
alias_group = groups[ 'alias' ]

# alias_group is a list of tuples, as follows:
# [ ('em', '"emacs"'), ('ls', '"ls -l"'), ('vi', '"vim"') ]

# it will make life easier to convert this to a dictionary
alias_dict = dict( alias_group )

# modify the vi alias
alias_dict[ 'vi' ] = '"emacs"'

# write it back to the groups as a list of tuples
groups[ 'alias' ] = alias_dict.items()

# write it back to ~/.bashrc
ptool.writeGroups( groups )
```

Now your `~/.bashrc` should look as follows:

```bash
# .bashrc

# pt_start alias
alias em="emacs"
alias ls="ls -l"
alias vi="emacs"
# pt_end alias
```

### Project Examples

I have included example Python scripts in `src/examples` that can be used to add a project, delete a project, set a default project, or a set default package. In order to run these scripts, they will need to be in the same directory as profile_tool.py (which currently they are not).

To avoid depending on profile_tool.py being in your current directory, you can [add the directory holding profile_tool.py to your PYTHONPATH](http://stackoverflow.com/a/3402176/903996).

## Testing

* `src/profile_tool_test.py` unit tests `src/profile_tool.py`. It depends on `example_profile` and `profile_tool.py`.
* `src/examples/proj_test.py` unit tests all `src/examples/*` project scripts. It depends on `example_profile` being in a directory one level higher, and depends on all project scripts in `src/examples/*`.
