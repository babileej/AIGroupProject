# AiGroupProject

## Basic Git Instructions
These instructions are meant to give you a basic overview of git as we will be using it.

For the purposes of this project, we want to avoid pushing changes directly to the master branch. This is so that we protect the master branch in case any accidents occur when pushing code. Also, this helps us to seperate the code into independent functionality, so that someone working on the backtracking algorithm won't suddenly have their code breaking if something is wrong in another branch.

First, you should clone the repository to your local machine. This is done by hitting the "clone or download" button on the code page of the project. This will give you two options to copy:

  1. https - This option is easier to set up. Simply paste the command you copied into your terminal to 
     clone the repository. It will clone into a folder with the name matching this repository name.
     You will need to re-enter your github credentials every time you access the remote repository.
  2. ssh - Using this option means you do not need to re-enter your credentials every time
     you access the remote repository. However, you need to generate a local ssh key and
     attach it to your git account. Instructions can be found [here](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/). Be sure to follow the link for instruction 3 to add the key to your account.
     
Once you have cloned the project, you will want to switch to the branch you will be working on. The branch should already exist on the repository. To find the name of the branch you need, either click the branches button near the top of the repository or type `git branch -r` in your terminal. When you find the name, type `git checkout <branch-name>`. **Note:** Do not type `git checkout origin\<branch-name>`, just use the part after the `\`. This command creates a local branch with the same name as the remote branch and ties it to the remote branch.

After you have made changes to your code, you can "commit" code to your local repository. This creates a history of the code and the changes made for that point and adds it to the commit history. Try to do this often, since it doesn't affect the remote repository. To do this, type `git add .` to stage all files for commit, then `git commit -m "<enter a commit message here about your changes"`. When you are ready to push your changes to your remote branch, type `git push origin <branch-name>`. Try to do this once a day.

When you are ready for your code to be merged to master (your branch is DONE), use github to create a pull request from your branch to master. Add us all as reviewers so we can check your code before mergin it to master. **IMPORTANT**: Do not merge directly to master or push directly to master. We want to make sure everyone agrees the code is ready before merging it. If you need help with creating a pull request, ask for it in slack.
