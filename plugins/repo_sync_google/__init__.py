#!/usr/local/bin/python3

import urllib.request
import xml.etree.ElementTree as ET

import pandas as pd
from rich import inspect
from rich.console import Console
from rich.progress import Progress
from collections import namedtuple

console = Console()

# TODO:
#   multi-thread

REPOS: tuple = [
  ("google", "https://dl.google.com/dl/android/maven2/"),
  # ("google2", "https://dl.google.com/dl/android/maven2/")
]

RepoPair = namedtuple("RepoPair", ["repo", "groupList"])


class Group():
  repo = None
  groupName = None
  artifacts = []

  def __init__(self, repo, groupName: str):
    console.log("Creating new group:" + groupName)
    self.repo = repo
    self.groupName = groupName

  def printInfo(self):
    print("")


class Artifact():
  group = None
  artifactName = None
  versions = []
  latestVersion = None

  def __init__(self, group: Group, name: str, versions: str):
    if group == None or name == None or versions == None:
      raise Exception("Artifact error, None value")

    self.group = group
    self.artifactName = name
    self.versions = versions.split(',')
    self.latestVersion = self.versions[len(self.versions) - 1]
    console.log("Artifact - " + group.groupName + ":" + name + ":" + self.latestVersion + " #: " + str(len(self.latestVersion)))

  def printInfo(self):
    pass


def parseGroup(repo, groupUrl: str):
  console.log("parsing groupUrl:" + groupUrl)

  groupData = urllib.request.urlopen(groupUrl).read().decode('utf-8')
  # console.log("key:" + key + "\n response:")
  # print(keyData)

  groupRoot = ET.XML(groupData)
  groupName = groupRoot.tag
  group = Group(repo, groupName)

  for i in groupRoot.iter():
    if i is not groupRoot:
      artifactName = i.tag
      artifactVersions = i.get("versions")
      artifact = Artifact(group, artifactName, artifactVersions)
      group.artifacts.append(artifact)

  return group


def parseRepo(repo: tuple):
  repoName = repo[0]
  baseUrl = repo[1]
  repoIndexUrl = str(baseUrl + "master-index.xml")

  console.log(repoName + ":" + repoIndexUrl)

  repoMasterIndexResponse = urllib.request.urlopen(repoIndexUrl)
  repoMasterIndexData = repoMasterIndexResponse.read().decode('utf-8')  # a `bytes` object

  root = ET.XML(repoMasterIndexData)
  groupNameList = []
  groupList = []

  for id in root.iter():
    if id is not root:
      groupNameList.append(id.tag)

  GROUP_SIZE = str(len(groupNameList))

  # progress = Progress()

  for i, key in enumerate(groupNameList):
    groupUrl = baseUrl + key.replace('.', '/') + '/group-index.xml'
    group = parseGroup(repo, groupUrl)

    if group.groupName == None:
      raise Exception("no groupName for key:" + key)

    groupList.append(group)

    # task_download = progress.add_task("[orange]Sync...", total=int(GROUP_SIZE))

    # progress.update(task_download, advance=1)

    console.log(str(i) + "/" + GROUP_SIZE + " : " + groupUrl + " group: " + group.groupName)

  return groupList


def main():
  repoList = []

  for repo in REPOS:
    groupList = parseRepo(repo)
    pair = RepoPair(repo, groupList)

    for implementation in pair.groupList:
      for artifact in implementation.artifacts:
        repoList.append({
          'g': artifact.group.groupName,
          'pkg': artifact.artifactName,
          'version': artifact.latestVersion
        })

  return pd.DataFrame(repoList).drop_duplicates().to_dict('records')
