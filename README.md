Utility to automatically remove any files you want to remain hidden when zipping your chrome extension for publication.

This is useful because if you use git as a version control, you don't want to zip up your git repo with the chrome app you publish to the play store. Furthermore, the script provides a utility to update your manfiest.json file's version number. This is useful because chrome requires you to update your version number before you update your extension.

Takes 6 arguments

Argument 1: Name of folder where app is located
Argument 2: folder you want to ignore (could be incomplete features) 
Argument 3: finalName of zipped up app (.zip will be added automatically, no need to specify zip)
Argument 4: path to a json file you might want to update (relative to where the python file is)
            (This is useful because in order to publish a new version of your extension, chrome extension store requires you to update your version in your manifest.json file)
Argument 5: property you want to change
Argument 6: value to update to


Example:

```
  py selective-zip.py exampleAppDev folderToIgnore exampleAppFinalName PathToManifestFile propertyToChange valueToUpdateTo 
  
  ## Functional Example
  
  py selective-zip.py exampleAppDev folderToIgnore exampleApp exampleAppDev/manifest.json version 0.1.2 
```
