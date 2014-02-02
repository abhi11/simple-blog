#Simple Blog#
> Takes a blog post i.e name of the topic and the article 
and generates a permalink for each individual post.
>It uses google appengine for python.

##Requirements
*    It uses python google appengine.
*    Download the appengine from [here](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python "Appengine")  
*    Unzip the file.Go to the appengine directory.
*    To run the app locally download the repo using:

     	  git clone

*    Then run the following command:     	     	 	 

     	  user@user~/google_appengine$ python dev_appserver.py  path-to-cloned-repo

*    For persistent data use the flag --datastore_path.Like this:

     	  user@user~/google_appengine$ python dev_appserver.py --datastore_path=/path/to/datastore path-to-cloned-repo
 
*    For more options use:

     	 python dev_appserver.py --help
