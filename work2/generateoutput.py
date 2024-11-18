import subprocess

def generateOutput(richtext, uml):
    subprocess.run(["java", "-jar", uml, richtext + '.puml'])