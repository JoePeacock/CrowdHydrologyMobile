# CrowdHydrology Mobile App
A mobile app for collecting data from the CrowdHydrology markings around the Northeast United States.

#### Initial Requirements
PIP (Python Package Index) for installing required python packages with ease:

```
$ curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python2.7
```

Once pip is installed we need to install a package called virtualenv to setup our local environment for the app. This allows us to keep all of the extra dependencies out of the main python index on the system, and some package version control. 

This should be installed to the system python dependenices, hence sudo. 

```
$ sudo pip install virtualenv
```

Now that we have virtualenv installed, the rest of the dependency installations do not require sudo. This is becasue virtualenv will create a local python install when called, and allows us to install all of our dependencies to this maeleable copy.

That being said lets create a new python vritual environment in our current working directory.

```
$ cd /path/to/wd
$ virtualenv venv
```

Where ```venv``` is the name of the folder of which we want to create our environment. ```/path/to/wd/venv```

Now that we have our environment setup we need to actually use it. Beyond this step  we no longer need system access.

```
$ source venv/bin/activate
```

Now we just need to install the app's dependencies to this virtual environment. They are defined in [requirements.txt](https://github.com/JoePeacock/CrowdHydrologyMobile/blob/master/requirements.txt)

```
(venv)$ pip install -r requirements.txt
```

To check that all of our dependenices were installed properly, just make sure everything in our requirements file prints with:

```
(venv)$ pip freeze
```

which takes a snapshot of all of the currently installed dependencies. (NOTE! If you run pip freeze, and are not sourced into the virtualenv that we created, then you will list all system python dependencies and not ours!)

Great! With everything installed you're all set. Everytime you want to develop in this environment simply navigate to the directory. Source your shell to this virtual environment and continue your work.


#### Running the server

Getting the server running requires some more configuration. To run the actual app simply:

```
python run.py
```

This will start a process on port ```5000``` and listen to incoming requests from there. Based on the current server confirugation this will have to change.









