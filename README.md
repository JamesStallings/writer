***writer*** is a simple service in python3, flask, and markdown2. It provides an entrypoint to more or less instant blogging. It can be run just for local, private use, or it's markdown/image file collection can be shipped off to **GitHub Pages** for processing through to html5 by *Jekyll*.

Like many such similar bits of code, it runs in a virtualenv psuedo-environment, where all dependencies can be met without disturbing the local system python nor the local system administrator (it can be run on an unpriviledged port entirely in userspace). It listens only on localhost, so does not expose the user or content beyond the degree permitted by local system policy.

The software is developed under a BSD license. This means that you can use it how and when you see fit, modify it to your needs, and otherwise use it to secure your satisfaction. Just don't plagiarize it. If you are uncertain of what that means, just *don't claim writer as your own original work*. In that vein, my hat is off and my acknowledgement is extended to the authors of flask, markdown2, and of course, python :) Cheers!

To set up for use, follow this basic workflow:

1. Create a folder from which it might operate: *mkdir writer*

2. Change to that folder and clone the repository: *git clone git@github.com:JamesStallings/writer.git*

3. Create a virtual environment there: *virtualenv -p /usr/bin/python3 ./env*

4. Create a site directory for your markdown and media files: *mkdir site*

   **note** it is possible to edit writer.py and set up a more organized folder structure for your markdown collection. However, doing so will cause all manner of complications with **GitHub Pages**.

5. Activate the virtual environment: *source ./env/bin/activate*

6. Execute the python code: *python writer.py*

7. Browse to the service with a good browser: *https://localhost:7000/writer/*

Note that if you are starting from scratch, you'll get *writer's* **404 NOT FOUND** that will be quite distinct from what the browser typically produces. Embedded in that 404 should be a link to create the requested file; the first one you should see is **index.md**. Edit that, and you're off and running. There should be a markdown language reference embedded in every page.

To create a brand new page, just treat it like a wiki: link to the page, then try to access it: you'll get *writer's* custom 404 NOT FOUND page, complete with a link to create the missing file.

---- 

To host an html5 rendition of your markdown/media collection on github, follow these steps:

5. Change directories to your site folder, and make it a git repository. You'll use git to push changes and updates to the repository that serves as a Jekyll markdown source.

6. If you haven't already, go over to github and insure that you have everything in order to use github pages. This will include having your ssh authentication configured (public key for your user@machine). 

Be certain that you've actually set up the repository on your github account. It should be named ***YourGithubName**.GitHub.io*

7. Unless you already have, configure your upstream: git remote add origin *https://github.com/**user/repo.git***

*You  must replace the bold bits with your unique info.*

You can check the remote for a local repository with: *git remote -v*

8. You should now be able to push your markdown/media files to github, provided you have properly maintained them in the site folder (using git add/git commit) as follows: git push origin *branchname*. You can omit branchname and it will use the default, which is probably what you want. You will, of course, need to repeat the git add/git commit workflow each time you make a change. The best practice is to regularly check the repository status with *git status*.

9. GitHub pages is going to push your markdown collection through an intelligent filter that processes your markdown into html, and complements it with a CSS theme applied by *Jekyll* during the data transform. You can select that theme on the ** * Settings * ** page for your *GitHub Pages* repository at **GitHub**.

It does all of this more or less automatically, though it does take a little while if you have an accumulation of material. 

----

This software is anything but perfect, and might benefit from a few new features. I'm looking at hcard and hentry, for instance. 

It has some code to manually and locally export HTML, but Idk just how good it is ATM. 

Let's just say, pull requests for bug fixes, better documentation, and additional features would be welcome, so long as they are simple and constructive.

I'll be publishing one or more such sites on GitHub Pages, and I hope to be able to take advantage of their *discussions* feature to support users of *writer*. Look for some further cross-pollination between site create tool, site, and author in coming commits :)

Thanks for your time and participation, and I sincerely hope this helps with whatever you need to do.

Cheers!











