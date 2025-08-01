import os
from dotenv import load_dotenv
load_dotenv()

base_directory  = os.getenv("PARENT_DIRECTORY")
package         = os.getenv("PACKAGE_NAME")

teddy_bears = {
    f"{base_directory}/colin/include"       : "koala",
    f"{base_directory}/tarquin/scripts"    : "panda",
    f"{base_directory}/peachy/experts"   : "bear",
    f"{base_directory}/files"              : "dog"
}

for name, animal in list(teddy_bears.items()):
    
    if name.endswith("files"):

        cwd = name

    else:
    
        cwd = os.path.join(name, package)

    print(cwd)
    #print(f">>{os.getenv('PARENT_DIRECTORY')}<<")
