
import argparse
import os

class VenvHelper:
    def __init__(self):
        print("")
        print("--------------------------------------------------")
        print("Initialize Virtual Environment Helper")
        print("--------------------------------------------------")

        parser = argparse.ArgumentParser(
            prog="Virtual Environment Helper",
            description="The tool will either help initialize your virtual environment or set it up with your user and os level certificates within a WSL distribution",
        )        
        self._setup_arguments(parser)
        args = parser.parse_args()

        self.output_dir = "venv-scripts"
        self.action = args.action
        print(f"- Running in Mode: '{self.action}'")


    def run(self):    
       print("")
       print("--------------------------------------------------")
       print("Run Virtual Environment Helper")
       print("--------------------------------------------------")

       if self.action == "init-venv":
           print(f"- Create init script in {self.output_dir}")
           self._create_init_script()
       
       elif self.action == "cert-setup":
           print(f"- Create cert setup script in {self.output_dir}")
           self._create_cert_setup_script()
       

    def _create_cert_setup_script(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

        cacert_pem_paths = self._find_cacert_pem_files()

        if not cacert_pem_paths:
            print("- Could not find certifi in lib. Please run init-venv.sh before running cert-setup")
            return  
        else:
            print(f"- Found {len(cacert_pem_paths)} where cacert.pem is located")      

        tab = "\t"
        lines = [
            "#!/bin/bash"
            "",
            "# Run this tool if you have added the Root CA to your Linux WSL instance",
            "",
            "echo 'Import system and user certificates into venv'",
            "",
            "if ! dpkg -s ca-certificates >/dev/null 2>&1; then"
            f"{tab}echo 'Trust system and user certificates'",
            f"{tab}sudo apt update",
            f"{tab}sudo apt install ca-certificates",
            f"{tab}sudo update-ca-certificates",
            f"fi",
            ""
        ]

        print("- Add lines to backup old cacert.pem and then create new one in its place")
        for cacert_pem_path in cacert_pem_paths:
            cacert_pem_path_bak = f"{cacert_pem_path}.bak"
            lines.append("echo ''")
            lines.append(f"echo 'Backup file just in case {cacert_pem_path}'")
            lines.append(f"mv {cacert_pem_path} {cacert_pem_path_bak}")
            lines.append("")
            lines.append("echo 'create symbolic link to ca-certificates.crt and rename it as cacert.pem'")
            lines.append(f"ln -s /etc/ssl/certs/ca-certificates.crt {cacert_pem_path}")

        lines.append("")

        path_cert_setup = os.path.join(self.output_dir, "cert-setup.sh")
        with open(path_cert_setup, "w") as writer:
            script = os.linesep.join(lines)
            writer.write(script)

        print(f"- Saved cert setup script to {path_cert_setup}")
        print("")
        print("Run the following command:")
        print("- 'bash venv-scripts/cert-setup.sh'")
       

    def _create_init_script(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

        lines = [
            "#!/bin/bash",
            "echo ''",
            "echo 'Create virtual-environment directory'",
            "python3 -m venv venv",
            "echo ''",
            "echo 'Activate the virtual-environment'",
            "source venv/bin/activate",
            "echo ''",
            "echo 'Install requests'",
            "pip install requests",
            ""
        ]

        path_output = os.path.join(self.output_dir, "init-venv.sh")
        with open(path_output, "w") as writer:
            script = os.linesep.join(lines)
            writer.write(script)

        print(f"- Saved init-script to {path_output}")
        print("")
        print("Run the following command:")
        print("- 'bash venv-scripts/init-venv.sh'")
       

    def _find_cacert_pem_files(self) -> list:
        file_matches = []
        find = "cacert.pem"
        path_start = "venv"
        print(f"- Find {find} in {path_start}...")

        if not os.path.exists(path_start):
            return []
        
        for root, _, files in os.walk(path_start):
            if find in files:
                file_matches.append(os.path.join(root, find))

            if len(file_matches) == 2:
                break

        return file_matches


    def _setup_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "-a", "--action", 
            required=True, 
            type=str, 
            choices=["init-venv", "cert-setup"], 
            help="The action to take. Use 'init-venv' to initialize the venv. Use 'cert-setup' to allow venv to trust user and system certificates."
        )
       


if __name__ == "__main__":
    VenvHelper().run()
