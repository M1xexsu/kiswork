#Генерация зависимостей пакета
import xml.etree.ElementTree as ET

from requests import request

def generate(packagename, genmax, version = 'latest', generation = 0):
    if generation < genmax:
        return
    pname = packagename.split("/")[1]
    packagename = packagename.replace(".","/")
    pomlink = 'https://repo1.maven.org/maven2/' + packagename + '/' + version + '/' + pname + '-' + version + '.pom'
    pomfile = request("get", pomlink)
    pomfile = pomfile.text
    xpomfile = ET.fromstring(pomfile)

    #TODO: построить вывод для puml
    with open("test.txt", "w") as f:
        for i in xpomfile.findall('dependency'):
            f.write(i.find('artifactId').text + "\n")

    for i in xpomfile.findall('dependency'):
        groupid = i.find('groupId').text
        artifactid = i.find('artifactId').text
        pversion = i.find('version').text
        generate('https://repo1.maven.org/maven2/' + groupid.replace(".","/") + '/' + artifactid + '/' + version + '/' + artifactid + '-' + pversion + '.pom',
                 genmax, version, generation+1)
    # TODO: Добавить подсос зависимостей в нужном формате + рекурсивный вызов