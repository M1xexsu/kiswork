#Генерация зависимостей пакета
import xml.etree.ElementTree as ET
import requests

from requests import request

def generate(packagename, genmax, version = 'latest', generation = 0, outfile = "test"):
    print(packagename, version)
    pname = packagename.split("/")[-1]
    packagename = packagename.replace(".", "/")

    if generation == 0:
        with open(f"{outfile}.puml", "w") as f:
            f.write('@startuml\n')

    if generation >= genmax:
        return

    pomlink = f'https://repo1.maven.org/maven2/{packagename}/{version}/{pname}-{version}.pom'
    pomfile = requests.get(pomlink)
    pomfile = pomfile.text
    xpomfile = ET.fromstring(pomfile)
    namespace = {'maven': 'http://maven.apache.org/POM/4.0.0'}
    dependencies = xpomfile.findall('.//maven:dependency', namespace)

    with open(f"{outfile}.puml", "a") as f:
        for dep in dependencies:
            artifact_id = dep.find('maven:artifactId', namespace).text
            f.write(f"({pname}) " + ('-' if generation == 0 else '--') + f"> ({artifact_id})\n")

    for dep in dependencies:
        group_id = dep.find('maven:groupId', namespace).text
        artifact_id = dep.find('maven:artifactId', namespace).text
        try:
            dep_version = dep.find('maven:version', namespace).text
            if dep_version.startswith("$"):
                pkgxml = requests.get(f'https://repo1.maven.org/maven2/{group_id.replace(".","/")}/{artifact_id.replace(".","/")}/maven-metadata.xml').text
                dep_version = ET.fromstring(pkgxml).find('versioning/release').text
        except Exception:
            print("no version, fetching latest")
            pkgxml = requests.get(
                f'https://repo1.maven.org/maven2/{group_id.replace(".", "/")}/{artifact_id.replace(".", "/")}/maven-metadata.xml').text
            dep_version = ET.fromstring(pkgxml).find('versioning/release').text
        finally:
            generate(f"{group_id}/{artifact_id}", genmax, dep_version, generation + 1, outfile)
