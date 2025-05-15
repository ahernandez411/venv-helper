# Virtual Environment Helper

This tool helps with the creation of python virtual environments (venv). Once the venv is created it also has the ability to setup system and user certificate trusts in the venv.

## Setup Alias for Tool

This tool works best when it is aliased in your `.bashrc` file. This can be accomplished by:
1. Clone the [venv-helper](https://github.com/ahernandez411/venv-helper) repository
1. Copy the full path to it
1. Open `.bashrc` with a command like `code ~/.bashrc`
1. Add the following code above the source line
```
venv-helper() {
  python3 "/home/<user>/path/to/venv-helper//src/venv-helper.py" "$@"
}
```
1. Save the file
1. Run `source ~/.bashrc` to make the alias available

## Using the Tool

The tool can perform to actions:
1. Initialize the Virtual Environment (venv)
1. Setup certificate trusts

>Note:<br />For help run `venv-helper -h` to see help documentation.

### Intialize venv

1. Run `venv-helper --action init-venv` to tell the tool to create a script to setup a venv in the repository. 
1. Run `bash venv-scripts/init-venv.sh` to initialize the venv

### Setup Certificate Trusts

1. Run `venv-helper --action cert-setup` to tell the tool to create a script that will allow system and user certs to be trusted.
1. Run `bash venv-scripts/cert-setup.sh` to trust certs
